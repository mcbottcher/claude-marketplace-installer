# claude-marketplace-installer

A CLI tool that reads your project's `.claude/settings.json` and installs all Claude Code plugin marketplaces listed there.

## Why?

Claude Code supports [plugin marketplaces](https://docs.anthropic.com/en/docs/claude-code/plugins) — sources that distribute skills, slash commands, hooks, and other Claude Code extensions. This tool lets teams version-control which marketplaces a project uses by declaring them in `.claude/settings.json`, then running a single install command to set them all up.

This is useful when you want to:
- Keep skills, slash commands, and hooks in a shared repo and distribute them as a marketplace
- Ensure everyone on a team is running the same Claude Code plugins
- Onboard new contributors by running one command instead of manually adding each marketplace

## Installation

```bash
pip install claude-marketplace-installer
```

Or with `uv`:

```bash
uv tool install claude-marketplace-installer
```

## Usage

Add your marketplaces to `.claude/settings.json` in your project:

```json
{
  "extraKnownMarketplaces": {
    "my-team-plugins": {
      "source": {
        "source": "github",
        "repo": "my-org/claude-plugins"
      }
    }
  }
}
```

Then, from the project root, run:

```bash
claude-install-marketplaces
```

This will install each marketplace listed under `extraKnownMarketplaces` using `claude plugin marketplace add`.

## Settings format

Each entry under `extraKnownMarketplaces` must have a `source` object with:

| Field | Value |
|-------|-------|
| `source` | `"github"` (only supported source type currently) |
| `repo` | GitHub repo in `owner/repo` format |

## Requirements

- Python 3.9+
- [Claude Code CLI](https://claude.ai/code) (`claude` must be available on your `PATH`)
