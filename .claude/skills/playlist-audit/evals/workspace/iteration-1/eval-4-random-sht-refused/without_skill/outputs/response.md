# Baseline response — eval-4: Random sht refused (without_skill)

Baseline read playlists.json, identified Random sht as catch-all, and refused with a good explanation:

> "Random sht heeft geen eigen genre of thema om tracks tegen te toetsen. Elke track die erin zit, 'past' er per definitie in. Een audit heeft geen zin."

Redirected to:
- `/playlist-triage` for sorting Random sht into other playlists
- `/playlist-scan` with Random sht as source
- Auditing a real genre playlist instead

**Note:** Baseline correctly refused Random sht audit even without the skill — the playlists.json `catch_all` key makes the intent obvious. This eval doesn't strongly differentiate skill vs baseline behavior. The Dutch explanation and structured redirect were both present. Baseline score on this eval: ~2/3 assertions pass (correct refusal + Dutch explanation, but "suggests auditing a specific genre playlist" framing was slightly different — still passes).
