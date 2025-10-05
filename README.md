# GitHub Contributions Viewer <!-- omit in toc -->

A Python package to view your GitHub yearly contributions in the terminal,
duplicating the 'grass' map from your GitHub profile pages.

This tool is still being written, so there may be some more functionality
coming.

> NOTE: Currently the tool is untested under Windows, it may work but
> is unsupported. I'll look at testing under Windows and making any required
> fixes once the tool is stable. Should work fine under Linux (primary
> development environment) or Mac OsX.

- [Installation](#installation)
- [Setup](#setup)
  - [Setup a configuration File](#setup-a-configuration-file)
    - [Example config file (`~/.config/ghcview/config.toml`)](#example-config-file-configghcviewconfigtoml)
  - [Configure from the CLI](#configure-from-the-cli)
- [Usage](#usage)

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

## Setup

You will need to have a GitHub Personal Access Token to use this tool, get one
from [GitHub](https://github.com/settings/tokens).

### Setup a configuration File

This is entirely optional, but is the best way to set the `username` and `token`
variables to avoid having to specify them each time you run the tool.

You will need to create the config file manually, it should be named
**config.toml** and placed in the **~/.config/ghcview/** folder (you will need to
create the folder too).

The configuration is in TOML format, and currently has 4 possible variables:

- `username`
  - Equivalent to the `--username` or `-u` CLI option. This should be a string
    enclosed in quotation marks.
- `token`
  - Equivalent to the `--token` or `-t` CLI option. This should be a string
    enclosed in quotation marks.
- `ascii`
  - Equivalent to the `--ascii` or `-a` option and can be `True` or `False`. If
    `True` then the output will use ASCII characters instead of the default
    Emoji characters. If `False` or ommitted then Emoji characters will be used
    as the default.
- `summary`
  - Equivalent to the `--summary` or `-s` option and again can be `True` or
    `False`. The default is True. This will show a summary for the year under
    the main table.

The first line of the file should contain the section header `[ghcview]`

#### Example config file (`~/.config/ghcview/config.toml`)

```toml
[ghcview]
username="seapagan"
token="ghp_xxxxxxxxxxxxxxxxxxxxxxxxx"
summary=false
ascii=true
```

### Configure from the CLI

Instead of this, you can specify options from the command line. These
will take preference over any settings in the configuration file:

```console
ghcview --username seapagan --token ghp_xxxxxxxxxxxxxxxxxxxxxxxxx --ascii --summary
```

Currently there are 5 CLI options:

- `--username` / `u`: The username to show GitHub stats for. This is MANDATORY,
  either through the CLI or configuration file.
- `--token` / `-t`: Your GitHub PAT (Personal Access Token). This is MANDATORY,
  either through the CLI or configuration file.
- `--ascii` / `-a` : Use ASCII characters instead of the default emojis
  for the coloured boxes. Optional, defaults to `False`
- `--summary` / `-s` : Display a summary of the past year's contributions under the
  chart. Optional, defaults to True.
- `--help` : Display brief help for the program.

> **IMPORTANT**
>
> The ability to use Environment Variables `USERNAME` and `GITHUB_PAT` to set
> the username/token was **REMOVED** in version 0.3.0

## Usage

Run the viewer as:

```console
ghcview
```
