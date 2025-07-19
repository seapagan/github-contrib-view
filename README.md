# GitHub Contributions Viewer

A Python package to view your GitHub yearly contributions in the terminal,
duplicating the 'grass' map from your GitHub profile pages.

Right now this app has minimal functionality and configuration, it will become
much more useful very quickly!

## Installation

You can install the package as a standalone tool using
[`uv`](https://docs.astral.sh/uv/):

```console
uv tool install github-contrib-view
```

or `pipx`:

```console
pipx  install github-contrib-view
```

Or simply use `pip` to install to your current virtualenv or global python:

```console
pip install github-contrib-view
```

If you prefer to install it manually, you can clone the repository and run the
following command:

```console
uv sync
source .venv/bin/activate # or .venv/Scripts/activate on Windows
```

In the above case, you will need to have `uv` installed.

## Setup

You will need to have a GitHub Personal Access Token to use this, get one from
[GitHub](https://github.com/settings/tokens).

Once you have one, you will need to set 2 env variables:

```ini
USERNAME=seapagan # YOUR GitHub username
GITHUB_PAT=ghp_xxxxxxxxxxxxxxxxxxxxxxxxx # the PAT you generated.
```

Instead of this, you can specify either or both from the command line. These
will take preference over any environment variables:

```console
ghcview --username seapagan --token ghp_xxxxxxxxxxxxxxxxxxxxxxxxx
```

You can use either or both.

## Usage

Run the viewer as:

```console
ghcview
```

Currently there are 3 CLI options in addition to the `--username` and `--token`
mentioned above:

- `--ascii` / `--no-ascii` : Use ASCII characters instead of the default emojis
  for the coloured boxes. Default is `--no-ascii`.
- `--summary` / `--no-summary` : Display a summary of the past year's
  contribuitions under the chart. Default is `--summary`.
- `--help` : Display brief help for the program.
