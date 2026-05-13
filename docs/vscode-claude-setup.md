# VS Code + Claude Code Setup

How to develop this repo from VS Code with [Claude Code](https://claude.com/claude-code) running against your WSL clone. Optional — the CLI itself works from any terminal — but it's the smoothest workflow on Windows + WSL2, and it's what unlocks the repo's [Claude skills](../.claude/docs/commands.md) (e.g. [`/playlist-match`](../.claude/skills/playlist-match/SKILL.md), [`/playlist-triage`](../.claude/skills/playlist-triage/SKILL.md)).

> **Already on Linux/macOS with VS Code?** Skip to [3. Install the Claude Code extension](#3-install-the-claude-code-extension).

## 1. Install WSL2 (Windows only)

Open PowerShell as Administrator:

```powershell
wsl --install -d Ubuntu
```

Restart when prompted. After reboot, Ubuntu asks you to create a Linux username and password.

## 2. Install VS Code

Download from [code.visualstudio.com](https://code.visualstudio.com/) and run the installer **on Windows** (not inside WSL). Cursor users: Cursor is a VS Code fork — the steps below work, but it uses `.cursor/` instead of `.claude/` for its own config.

## 3. Install the Claude Code extension

Open VS Code and install these two extensions (`Ctrl+Shift+X`):

| Extension     | ID                            | Purpose                                                  |
| ------------- | ----------------------------- | -------------------------------------------------------- |
| Claude Code   | `anthropic.claude-code`       | The AI assistant — core to this setup                    |
| WSL           | `ms-vscode-remote.remote-wsl` | Lets VS Code on Windows connect to your WSL filesystem   |

Or from the command line:

```bash
code --install-extension anthropic.claude-code
code --install-extension ms-vscode-remote.remote-wsl
```

> `ms-vscode-remote.remote-wsl` must be installed on the **Windows side** of VS Code, not inside WSL.

## 4. Connect VS Code to WSL

1. Open VS Code on Windows
2. `Ctrl+Shift+P` → **"WSL: Connect to WSL"**
3. Choose your Ubuntu distro
4. Once connected, `File → Open Folder` → navigate to `~/spotify-playlist-manager`

VS Code will install its server component inside WSL automatically. From here, every terminal you open in VS Code runs inside WSL.

## 5. Authenticate Claude Code

After installing the extension:

- Open the **Claude Code** panel from the sidebar
- Sign in with your Anthropic account

Or from the WSL terminal:

```bash
claude auth login
```

You only do this once per machine.

## 6. Use the repo's Claude skills

This repo ships five slash commands:

- **`/playlist-match`** — paste a Spotify URL or *"Artist - Title"* in the Claude chat and Claude classifies the genres, suggests playlists from your `playlists.json`, and can run `add` / `smart-add` for you.
- **`/playlist-triage`** — sort a whole source playlist into many target playlists, via `review-playlist` (per-track y/N) or `bulk-playlist` (single y/N).
- **`/playlist-scan`** — mine a source playlist for tracks that fit one chosen target, via `scan-for`.
- **`/playlist-log-import`** — seed the local duplicate-guard log (`.adds_log.json`) for a playlist from an Exportify CSV, via `log-import`.
- **`/playlist-config`** — bootstrap or extend `playlists.json` from your Spotify account, via `list-playlists --all`.

Full reference (triggers, guardrails, source links): [.claude/docs/commands.md](../.claude/docs/commands.md). Contributor docs (authoring new skills, writing-doc conventions) live in [.claude/docs/README.md](../.claude/docs/README.md).

## Next

Continue with [setup.md → Local Python environment](setup.md#local-python-environment) to install the Python venv inside WSL, then run any command from the VS Code terminal.
