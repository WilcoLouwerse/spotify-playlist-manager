"""Unit tests for pure functions in playlist_manager."""

import argparse

import pytest

import playlist_manager as pm


@pytest.fixture(autouse=True)
def _reset_module_state():
    pm._config_cache = None
    pm._WARNED_ABOUT_STRIPPED_DATA = False
    yield
    pm._config_cache = None
    pm._WARNED_ABOUT_STRIPPED_DATA = False


@pytest.fixture
def config():
    cfg = {
        "playlists": {
            "House": "0BEX4bI5xtkEVA4BfYTKg2",
            "Techno": "7lRL294p8uvOOXTxNPIBhn",
            "Random sht": "1PMqc20PYGO1nqOeqY0zRe",
        },
        "aliases": {"techno": "Techno", "house": "House"},
        "categories": {"genre": ["House", "Techno"]},
        "special_rules": {},
        "catch_all": {"playlist": "Random sht", "threshold": 85},
    }
    pm._config_cache = cfg
    return cfg


VALID_ID = "1234567890abcdefghijKL"


class TestExtractTrackId:
    def test_open_url(self):
        assert pm.extract_track_id(f"https://open.spotify.com/track/{VALID_ID}") == VALID_ID

    def test_open_url_with_query(self):
        assert pm.extract_track_id(f"https://open.spotify.com/track/{VALID_ID}?si=xyz") == VALID_ID

    def test_open_url_with_trailing_path(self):
        assert pm.extract_track_id(f"https://open.spotify.com/track/{VALID_ID}/extra") == VALID_ID

    def test_uri(self):
        assert pm.extract_track_id(f"spotify:track:{VALID_ID}") == VALID_ID

    def test_bare_id(self):
        assert pm.extract_track_id(VALID_ID) == VALID_ID


class TestExtractPlaylistId:
    def test_open_url(self):
        assert pm.extract_playlist_id(f"https://open.spotify.com/playlist/{VALID_ID}") == VALID_ID

    def test_open_url_with_query(self):
        assert pm.extract_playlist_id(f"https://open.spotify.com/playlist/{VALID_ID}?si=xyz") == VALID_ID

    def test_open_url_with_trailing_path(self):
        assert pm.extract_playlist_id(f"https://open.spotify.com/playlist/{VALID_ID}/extra") == VALID_ID

    def test_uri(self):
        assert pm.extract_playlist_id(f"spotify:playlist:{VALID_ID}") == VALID_ID

    def test_bare_id(self):
        assert pm.extract_playlist_id(VALID_ID) == VALID_ID


class TestPromptReviewAction:
    @pytest.mark.parametrize("answer,expected", [
        ("y", "yes"),
        ("Y", "yes"),
        ("yes", "yes"),
        ("ja", "yes"),
        ("j", "yes"),
        ("n", "no"),
        ("no", "no"),
        ("nee", "no"),  # falls through to default "no"
        ("", "no"),
        ("s", "skip"),
        ("skip", "skip"),
        ("q", "quit"),
        ("quit", "quit"),
        ("exit", "quit"),
    ])
    def test_answers(self, monkeypatch, answer, expected):
        monkeypatch.setattr("builtins.input", lambda _: answer)
        assert pm._prompt_review_action("prompt: ") == expected

    def test_eof_treated_as_quit(self, monkeypatch):
        def _raise(_):
            raise EOFError
        monkeypatch.setattr("builtins.input", _raise)
        assert pm._prompt_review_action("prompt: ") == "quit"


class TestExtractUriFromLine:
    def test_full_uri_in_line(self):
        assert pm._extract_uri_from_line(f"spotify:track:{VALID_ID}") == f"spotify:track:{VALID_ID}"

    def test_open_url_in_line(self):
        line = f"https://open.spotify.com/track/{VALID_ID}?si=foo"
        assert pm._extract_uri_from_line(line) == f"spotify:track:{VALID_ID}"

    def test_bare_id(self):
        assert pm._extract_uri_from_line(VALID_ID) == f"spotify:track:{VALID_ID}"

    def test_csv_first_field(self):
        line = f"{VALID_ID},Some Artist,Some Track"
        assert pm._extract_uri_from_line(line) == f"spotify:track:{VALID_ID}"

    def test_tsv_first_field(self):
        line = f"{VALID_ID}\tSome Artist\tSome Track"
        assert pm._extract_uri_from_line(line) == f"spotify:track:{VALID_ID}"

    def test_empty_line(self):
        assert pm._extract_uri_from_line("") is None
        assert pm._extract_uri_from_line("   \n") is None

    def test_garbage_line(self):
        assert pm._extract_uri_from_line("this is not a track id") is None

    def test_short_id_rejected(self):
        assert pm._extract_uri_from_line("1234567890abcdefghijk") is None  # 21 chars


class TestRangedInt:
    def test_within_range(self):
        parser = pm._ranged_int(1, 5)
        assert parser("1") == 1
        assert parser("3") == 3
        assert parser("5") == 5

    def test_below_range(self):
        parser = pm._ranged_int(1, 5)
        with pytest.raises(argparse.ArgumentTypeError):
            parser("0")

    def test_above_range(self):
        parser = pm._ranged_int(1, 5)
        with pytest.raises(argparse.ArgumentTypeError):
            parser("6")

    def test_non_integer(self):
        parser = pm._ranged_int(1, 5)
        with pytest.raises(argparse.ArgumentTypeError):
            parser("not-a-number")


class TestApplyCatchAll:
    def test_no_catch_all_returns_unchanged(self):
        matches = [{"playlist": "House", "confidence": 50}]
        assert pm._apply_catch_all(matches, None) == matches

    def test_below_threshold_appends_fallback(self):
        catch_all = {"playlist": "Random sht", "threshold": 85}
        matches = [{"playlist": "House", "confidence": 50}]
        result = pm._apply_catch_all(matches, catch_all)
        assert len(result) == 2
        assert result[-1]["playlist"] == "Random sht"
        assert result[-1]["confidence"] == 100

    def test_above_threshold_no_fallback(self):
        catch_all = {"playlist": "Random sht", "threshold": 85}
        matches = [{"playlist": "House", "confidence": 90}]
        assert pm._apply_catch_all(matches, catch_all) == matches

    def test_at_threshold_no_fallback(self):
        catch_all = {"playlist": "Random sht", "threshold": 85}
        matches = [{"playlist": "House", "confidence": 85}]
        assert pm._apply_catch_all(matches, catch_all) == matches

    def test_catch_all_already_present_no_duplicate(self):
        catch_all = {"playlist": "Random sht", "threshold": 85}
        matches = [{"playlist": "Random sht", "confidence": 30}]
        assert pm._apply_catch_all(matches, catch_all) == matches

    def test_empty_matches_appends_fallback(self):
        catch_all = {"playlist": "Random sht", "threshold": 85}
        result = pm._apply_catch_all([], catch_all)
        assert len(result) == 1
        assert result[0]["playlist"] == "Random sht"


class TestValidateConfig:
    def test_minimal_valid(self):
        pm._validate_config({"playlists": {"X": VALID_ID}})

    def test_root_not_object(self):
        with pytest.raises(ValueError):
            pm._validate_config([])

    def test_missing_playlists(self):
        with pytest.raises(ValueError):
            pm._validate_config({})

    def test_empty_playlists(self):
        with pytest.raises(ValueError):
            pm._validate_config({"playlists": {}})

    def test_invalid_playlist_id(self):
        with pytest.raises(ValueError):
            pm._validate_config({"playlists": {"X": "too-short"}})

    def test_alias_targets_unknown_playlist(self):
        with pytest.raises(ValueError):
            pm._validate_config({
                "playlists": {"X": VALID_ID},
                "aliases": {"y": "Z"},
            })

    def test_category_references_unknown_playlist(self):
        with pytest.raises(ValueError):
            pm._validate_config({
                "playlists": {"X": VALID_ID},
                "categories": {"cat": ["Z"]},
            })

    def test_category_must_be_list(self):
        with pytest.raises(ValueError):
            pm._validate_config({
                "playlists": {"X": VALID_ID},
                "categories": {"cat": "not-a-list"},
            })

    def test_special_rules_unknown_playlist(self):
        with pytest.raises(ValueError):
            pm._validate_config({
                "playlists": {"X": VALID_ID},
                "special_rules": {"Other": "rule"},
            })

    def test_catch_all_unknown_playlist(self):
        with pytest.raises(ValueError):
            pm._validate_config({
                "playlists": {"X": VALID_ID},
                "catch_all": {"playlist": "Other"},
            })

    def test_catch_all_threshold_out_of_range(self):
        with pytest.raises(ValueError):
            pm._validate_config({
                "playlists": {"X": VALID_ID},
                "catch_all": {"playlist": "X", "threshold": 200},
            })


class TestNormalizePlaylistName:
    def test_exact_match(self, config):
        assert pm.normalize_playlist_name("House") == "House"

    def test_case_insensitive_match(self, config):
        assert pm.normalize_playlist_name("HOUSE") == "House"

    def test_alias_lookup(self, config):
        assert pm.normalize_playlist_name("techno") == "Techno"

    def test_alias_is_lowercased(self, config):
        assert pm.normalize_playlist_name("  Techno  ") == "Techno"

    def test_unknown_raises(self, config):
        with pytest.raises(ValueError):
            pm.normalize_playlist_name("Nonexistent")


class TestValidateClassification:
    def test_valid(self, config):
        pm.validate_classification({
            "playlist_matches": [{"playlist": "House", "confidence": 80}]
        })

    def test_not_an_object(self, config):
        with pytest.raises(ValueError):
            pm.validate_classification([])

    def test_missing_matches(self, config):
        with pytest.raises(ValueError):
            pm.validate_classification({})

    def test_empty_matches(self, config):
        with pytest.raises(ValueError):
            pm.validate_classification({"playlist_matches": []})

    def test_unknown_playlist(self, config):
        with pytest.raises(ValueError):
            pm.validate_classification({
                "playlist_matches": [{"playlist": "Nope", "confidence": 50}]
            })

    def test_confidence_out_of_range(self, config):
        with pytest.raises(ValueError):
            pm.validate_classification({
                "playlist_matches": [{"playlist": "House", "confidence": 150}]
            })

    def test_confidence_not_int(self, config):
        with pytest.raises(ValueError):
            pm.validate_classification({
                "playlist_matches": [{"playlist": "House", "confidence": "high"}]
            })


class TestAddsLog:
    def test_load_missing_file_returns_empty(self, monkeypatch, tmp_path):
        monkeypatch.setattr(pm, "ADDS_LOG_PATH", str(tmp_path / "missing.json"))
        assert pm._load_adds_log() == {}

    def test_load_corrupt_file_returns_empty(self, monkeypatch, tmp_path):
        path = tmp_path / "log.json"
        path.write_text("not valid json {")
        monkeypatch.setattr(pm, "ADDS_LOG_PATH", str(path))
        assert pm._load_adds_log() == {}

    def test_save_then_load_roundtrip(self, monkeypatch, tmp_path):
        monkeypatch.setattr(pm, "ADDS_LOG_PATH", str(tmp_path / "log.json"))
        pm._save_adds_log({"pid1": ["spotify:track:a", "spotify:track:b"]})
        assert pm._load_adds_log() == {"pid1": ["spotify:track:a", "spotify:track:b"]}

    def test_log_successful_add_appends(self, monkeypatch, tmp_path):
        monkeypatch.setattr(pm, "ADDS_LOG_PATH", str(tmp_path / "log.json"))
        pm.log_successful_add("pid1", "spotify:track:a")
        pm.log_successful_add("pid1", "spotify:track:b")
        assert pm._load_adds_log() == {"pid1": ["spotify:track:a", "spotify:track:b"]}

    def test_log_successful_add_dedups(self, monkeypatch, tmp_path):
        monkeypatch.setattr(pm, "ADDS_LOG_PATH", str(tmp_path / "log.json"))
        pm.log_successful_add("pid1", "spotify:track:a")
        pm.log_successful_add("pid1", "spotify:track:a")
        assert pm._load_adds_log() == {"pid1": ["spotify:track:a"]}

    def test_log_successful_add_separate_playlists(self, monkeypatch, tmp_path):
        monkeypatch.setattr(pm, "ADDS_LOG_PATH", str(tmp_path / "log.json"))
        pm.log_successful_add("pid1", "spotify:track:a")
        pm.log_successful_add("pid2", "spotify:track:b")
        log = pm._load_adds_log()
        assert log == {"pid1": ["spotify:track:a"], "pid2": ["spotify:track:b"]}


class TestLogImport:
    @pytest.fixture
    def log_path(self, monkeypatch, tmp_path):
        path = tmp_path / "log.json"
        monkeypatch.setattr(pm, "ADDS_LOG_PATH", str(path))
        return path

    def test_imports_new_uris(self, config, log_path, tmp_path, capsys):
        src = tmp_path / "tracks.txt"
        src.write_text(
            f"spotify:track:{VALID_ID}\n"
            f"https://open.spotify.com/track/{'a' * 22}?si=x\n"
        )
        pm.log_import("House", str(src))

        house_id = config["playlists"]["House"]
        assert pm._load_adds_log() == {
            house_id: [f"spotify:track:{VALID_ID}", f"spotify:track:{'a' * 22}"]
        }
        out = capsys.readouterr().out
        assert "Imported new URIs: 2" in out
        assert "Total URIs logged: 2" in out

    def test_counters_cover_all_branches(self, config, log_path, tmp_path, capsys):
        house_id = config["playlists"]["House"]
        pm._save_adds_log({house_id: [f"spotify:track:{VALID_ID}"]})

        new_id = "b" * 22
        src = tmp_path / "tracks.txt"
        src.write_text(
            f"spotify:track:{VALID_ID}\n"     # already in log
            f"spotify:track:{new_id}\n"        # new
            f"spotify:track:{new_id}\n"        # duplicate within file
            "this is not a track id\n"         # invalid (non-empty, unparseable)
            "\n"                               # blank line — ignored, not counted as invalid
        )
        pm.log_import("House", str(src))

        assert pm._load_adds_log() == {
            house_id: [f"spotify:track:{VALID_ID}", f"spotify:track:{new_id}"]
        }
        out = capsys.readouterr().out
        assert "Imported new URIs: 1" in out
        assert "Already in log:    1" in out
        assert "Duplicate in file: 1" in out
        assert "Unparseable lines: 1" in out
        assert "Total URIs logged: 2" in out

    def test_resolves_alias_to_canonical_playlist(self, config, log_path, tmp_path):
        src = tmp_path / "tracks.txt"
        src.write_text(f"spotify:track:{VALID_ID}\n")
        pm.log_import("techno", str(src))

        techno_id = config["playlists"]["Techno"]
        assert pm._load_adds_log() == {techno_id: [f"spotify:track:{VALID_ID}"]}

    def test_missing_file_is_graceful(self, config, log_path, tmp_path, capsys):
        pm.log_import("House", str(tmp_path / "nope.txt"))
        assert pm._load_adds_log() == {}
        assert "File not found" in capsys.readouterr().out

    def test_unknown_playlist_raises(self, config, log_path, tmp_path):
        src = tmp_path / "tracks.txt"
        src.write_text(f"spotify:track:{VALID_ID}\n")
        with pytest.raises(ValueError):
            pm.log_import("Nonexistent", str(src))


EXPORTIFY_HEADER = (
    "Track URI,Track Name,Album Name,Artist Name(s),Release Date,Duration (ms),"
    "Popularity,Explicit,Added By,Added At\n"
)


class TestNormalizeForCsvMatch:
    @pytest.mark.parametrize("inp,expected", [
        ("House", "house"),
        ("Drum & Bass", "drum_&_bass"),
        ("Drum_&_Bass", "drum_&_bass"),
        ("Pop / Mainstream", "pop_mainstream"),
        ("Pop_Mainstream", "pop_mainstream"),
        ("Rustig / 'anders'", "rustig_'anders'"),
        ("Random sht", "random_sht"),
        ("Random_sht", "random_sht"),
        ("", ""),
        ("   ", ""),
    ])
    def test_normalization(self, inp, expected):
        assert pm._normalize_for_csv_match(inp) == expected


class TestCsvPathForName:
    @pytest.fixture
    def exportify_dir(self, monkeypatch, tmp_path):
        d = tmp_path / "exportify-exports"
        d.mkdir()
        for fname in ("House.csv", "Drum_&_Bass.csv", "Pop_Mainstream.csv", "notes.txt"):
            (d / fname).write_text("")
        monkeypatch.setattr(pm, "EXPORTIFY_DIR", str(d))
        return d

    def test_exact_match(self, exportify_dir):
        assert pm._csv_path_for_name("House") == str(exportify_dir / "House.csv")

    def test_case_insensitive(self, exportify_dir):
        assert pm._csv_path_for_name("house") == str(exportify_dir / "House.csv")

    def test_spaces_match_underscores(self, exportify_dir):
        assert pm._csv_path_for_name("Drum & Bass") == str(exportify_dir / "Drum_&_Bass.csv")

    def test_slash_separator_stripped(self, exportify_dir):
        # "Pop / Mainstream" should map to Pop_Mainstream.csv (exportify strips '/')
        assert pm._csv_path_for_name("Pop / Mainstream") == str(exportify_dir / "Pop_Mainstream.csv")

    def test_no_match(self, exportify_dir):
        assert pm._csv_path_for_name("Nonexistent") is None

    def test_empty_name(self, exportify_dir):
        assert pm._csv_path_for_name("") is None

    def test_missing_dir(self, monkeypatch, tmp_path):
        monkeypatch.setattr(pm, "EXPORTIFY_DIR", str(tmp_path / "does-not-exist"))
        assert pm._csv_path_for_name("House") is None


class TestResolveCsvPath:
    @pytest.fixture
    def exportify_dir(self, monkeypatch, tmp_path):
        d = tmp_path / "exportify-exports"
        d.mkdir()
        (d / "House.csv").write_text("")
        monkeypatch.setattr(pm, "EXPORTIFY_DIR", str(d))
        return d

    def test_existing_csv_path(self, exportify_dir, tmp_path):
        csv_file = tmp_path / "elsewhere.csv"
        csv_file.write_text("")
        assert pm._resolve_csv_path(str(csv_file)) == str(csv_file)

    def test_csv_extension_but_missing(self, tmp_path):
        assert pm._resolve_csv_path(str(tmp_path / "missing.csv")) is None

    def test_bare_name_match(self, exportify_dir):
        assert pm._resolve_csv_path("House") == str(exportify_dir / "House.csv")

    def test_url_rejected(self, exportify_dir):
        assert pm._resolve_csv_path("https://open.spotify.com/playlist/abc") is None

    def test_uri_rejected(self, exportify_dir):
        assert pm._resolve_csv_path("spotify:playlist:abc") is None

    def test_bare_22_char_id_rejected(self, exportify_dir):
        assert pm._resolve_csv_path(VALID_ID) is None

    def test_unknown_bare_name_returns_none(self, exportify_dir):
        assert pm._resolve_csv_path("Nonexistent") is None

    def test_empty_returns_none(self):
        assert pm._resolve_csv_path("") is None


class TestLoadTracksFromCsv:
    def test_parses_exportify_csv(self, tmp_path):
        csv_file = tmp_path / "House.csv"
        csv_file.write_text(
            EXPORTIFY_HEADER
            + f'spotify:track:{VALID_ID},"Walk That Walk","The Spirit","Bakermat;Nic Hanson",2021-06-25,164411,27,false,user,2026-05-12T14:52:49Z\n'
            + f'spotify:track:{"a" * 22},"Solo Track","Album","Single Artist",2020-01-01,180000,50,false,user,2026-05-12T14:52:49Z\n'
        )
        items = pm._load_tracks_from_csv(str(csv_file))

        assert len(items) == 2
        first = items[0]
        assert first["uri"] == f"spotify:track:{VALID_ID}"
        assert first["id"] == VALID_ID
        assert first["name"] == "Walk That Walk"
        assert first["artists"] == ["Bakermat", "Nic Hanson"]
        assert first["label"] == "Bakermat - Walk That Walk"

        second = items[1]
        assert second["artists"] == ["Single Artist"]
        assert second["label"] == "Single Artist - Solo Track"

    def test_handles_bom(self, tmp_path):
        # Exportify writes a UTF-8 BOM as the first byte
        csv_file = tmp_path / "House.csv"
        csv_file.write_bytes(
            b"\xef\xbb\xbf"
            + EXPORTIFY_HEADER.encode("utf-8")
            + f'spotify:track:{VALID_ID},"A","B","C",2020-01-01,1,1,false,u,t\n'.encode("utf-8")
        )
        items = pm._load_tracks_from_csv(str(csv_file))
        assert len(items) == 1
        assert items[0]["uri"] == f"spotify:track:{VALID_ID}"

    def test_skips_rows_without_uri(self, tmp_path):
        csv_file = tmp_path / "House.csv"
        csv_file.write_text(
            EXPORTIFY_HEADER
            + ',"No URI Track","Album","Artist",2020-01-01,1,1,false,u,t\n'
            + f'spotify:track:{VALID_ID},"Good Track","A","B",2020-01-01,1,1,false,u,t\n'
        )
        items = pm._load_tracks_from_csv(str(csv_file))
        assert len(items) == 1
        assert items[0]["uri"] == f"spotify:track:{VALID_ID}"

    def test_empty_file(self, tmp_path):
        csv_file = tmp_path / "empty.csv"
        csv_file.write_text(EXPORTIFY_HEADER)
        assert pm._load_tracks_from_csv(str(csv_file)) == []


class _StubSpotify:
    """Minimal stand-in for the spotipy client. Used in _resolve_source tests."""

    def __init__(self, playlist_info=None, raise_on_playlist=None, items=None):
        self._playlist_info = playlist_info or {}
        self._raise = raise_on_playlist
        self._items_pages = [{"items": items or [], "next": None}]

    def playlist(self, pid, fields=None):
        if self._raise:
            raise self._raise
        return self._playlist_info

    def playlist_items(self, pid, fields=None, additional_types=None, limit=None):
        return self._items_pages[0]

    def next(self, results):
        return None


class TestResolveSource:
    @pytest.fixture
    def exportify_dir(self, monkeypatch, tmp_path):
        d = tmp_path / "exportify-exports"
        d.mkdir()
        monkeypatch.setattr(pm, "EXPORTIFY_DIR", str(d))
        return d

    def _write_csv(self, path, n=1):
        rows = "".join(
            f'spotify:track:{chr(ord("a") + i) * 22},"T{i}","A","Artist{i}",2020-01-01,1,1,false,u,t\n'
            for i in range(n)
        )
        path.write_text(EXPORTIFY_HEADER + rows)

    def test_csv_path_input(self, exportify_dir, tmp_path):
        csv_file = tmp_path / "House.csv"
        self._write_csv(csv_file, n=2)
        sp = _StubSpotify()
        name, locator, items = pm._resolve_source(sp, str(csv_file))
        assert name == "House"
        assert locator == str(csv_file)
        assert len(items) == 2

    def test_bare_name_input(self, exportify_dir):
        csv_file = exportify_dir / "House.csv"
        self._write_csv(csv_file, n=1)
        sp = _StubSpotify()
        name, locator, items = pm._resolve_source(sp, "House")
        assert name == "House"
        assert locator == str(csv_file)
        assert len(items) == 1

    def test_empty_csv_returns_none(self, exportify_dir, tmp_path, capsys):
        csv_file = tmp_path / "empty.csv"
        csv_file.write_text(EXPORTIFY_HEADER)
        sp = _StubSpotify()
        name, locator, items = pm._resolve_source(sp, str(csv_file))
        assert (name, locator, items) == (None, None, None)
        assert "No readable tracks" in capsys.readouterr().out

    def test_url_with_tracks(self, exportify_dir):
        sp = _StubSpotify(
            playlist_info={"name": "My Playlist", "id": VALID_ID},
            items=[{
                "track": {
                    "id": "b" * 22,
                    "uri": f"spotify:track:{'b' * 22}",
                    "name": "Song",
                    "artists": [{"name": "Artist"}],
                }
            }],
        )
        name, locator, items = pm._resolve_source(sp, f"https://open.spotify.com/playlist/{VALID_ID}")
        assert name == "My Playlist"
        assert locator == VALID_ID
        assert len(items) == 1

    def test_url_stripped_falls_back_to_csv_with_yes(self, exportify_dir, monkeypatch, capsys):
        csv_file = exportify_dir / "House.csv"
        self._write_csv(csv_file, n=3)
        sp = _StubSpotify(
            playlist_info={"name": "House", "id": VALID_ID},
            items=[],  # Spotify returned nothing (dev-tier stripping)
        )
        prompts = []
        monkeypatch.setattr("builtins.input", lambda p: (prompts.append(p), "y")[1])
        name, locator, items = pm._resolve_source(sp, f"https://open.spotify.com/playlist/{VALID_ID}")
        assert name == "House"
        assert locator == str(csv_file)
        assert len(items) == 3
        assert any("Found local export" in p for p in prompts)
        assert "no readable tracks for 'House'" in capsys.readouterr().out

    def test_url_stripped_user_declines_fallback(self, exportify_dir, monkeypatch, capsys):
        csv_file = exportify_dir / "House.csv"
        self._write_csv(csv_file, n=3)
        sp = _StubSpotify(
            playlist_info={"name": "House", "id": VALID_ID},
            items=[],
        )
        prompts = []
        monkeypatch.setattr("builtins.input", lambda p: (prompts.append(p), "n")[1])
        name, locator, items = pm._resolve_source(sp, f"https://open.spotify.com/playlist/{VALID_ID}")
        assert (name, locator, items) == (None, None, None)
        assert any("Found local export" in p for p in prompts)
        assert "Export the playlist" in capsys.readouterr().out  # the standard pointer message

    def test_url_stripped_no_matching_csv(self, exportify_dir, capsys):
        sp = _StubSpotify(
            playlist_info={"name": "Some Unmatched Name", "id": VALID_ID},
            items=[],
        )
        name, locator, items = pm._resolve_source(sp, f"https://open.spotify.com/playlist/{VALID_ID}")
        assert (name, locator, items) == (None, None, None)
        out = capsys.readouterr().out
        assert "Found local export" not in out
        assert "Export the playlist" in out

    def test_spotify_error(self, exportify_dir, capsys):
        import spotipy
        exc = spotipy.SpotifyException(404, -1, "Not found")
        sp = _StubSpotify(raise_on_playlist=exc)
        name, locator, items = pm._resolve_source(sp, f"https://open.spotify.com/playlist/{VALID_ID}")
        assert (name, locator, items) == (None, None, None)
        assert "Could not load playlist" in capsys.readouterr().out
