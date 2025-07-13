# GitHub Contributions Viewer

A Python package to view your GitHub yearly contributions in the terminal,
duplicating the 'grass' map from your GitHub profile pages.

Right now this app has minimal functionality and configuration, I have just
packaged it to save the name. It will become much more useful very quickly!

## Installation

You can install the package using uv:

```bash
uv install github-contrib-view
```

If you prefer to install it manually, you can clone the repository and run the
following command:

```bash
uv sync
source .venv/bin/activate # or .venv/Scripts/activate on Windows
```

In either case, you will need to have `uv` installed.

## Setup

You will need to have a GitHub Personal Access Token to use this, get one from
[GitHub](https://github.com/settings/tokens).

Once you have one, you will need to set 2 env variables:

```ini
USERNAME=seapagan # YOUR GitHub username
GITHUB_PAT=ghp_xxxxxxxxxxxxxxxxxxxxxxxxx # the PAT you generated.
```

Very shortly this will be set from a config file and the command line.

## Usage

Right now there are no options nor settings. Run the viewer as:

```console
ghcview
```

The output uses emojie's for the colored boxes, ASCII-only mode is coming.
