"""Main module for the project."""

from __future__ import annotations

import contextlib
import locale
from typing import TYPE_CHECKING, NoReturn, Optional

import typer
from rich import print as rprint

from github_contrib_view.config import settings
from github_contrib_view.contrib import get_github_contributions
from github_contrib_view.output import (
    print_github_style_grid_full_year,
)

if TYPE_CHECKING:
    from github_contrib_view.structures import ContribOptions

# Set locale for date formatting (falls back to system default)
with contextlib.suppress(locale.Error):
    locale.setlocale(locale.LC_TIME, "")


app = typer.Typer(
    pretty_exceptions_show_locals=False,
    add_completion=False,
    rich_markup_mode="rich",
)


def bad_env() -> NoReturn:
    """Exit with a message if the .env is not set."""
    err_str = (
        "[red]USERNAME and GITHUB_PAT must be set in the config file or "
        "passed as a CLI option. Exiting."
    )
    rprint(err_str)
    raise typer.Exit(code=2)


@app.command()
def main(
    username: Optional[str] = typer.Option(
        None,
        "--username",
        "-u",
        help="GitHub Username to query",
        show_default=False,
    ),
    token: Optional[str] = typer.Option(
        None,
        "--token",
        "-t",
        help="GitHub Personal Access Token",
        show_default=False,
    ),
    *,
    ascii_mode: Optional[bool] = typer.Option(
        None,
        "--ascii",
        "-a",
        help="Use plain ASCII output",
    ),
    summary: Optional[bool] = typer.Option(
        None,
        "--summary",
        "-s",
        help="Show a summary after the table",
    ),
) -> None:
    """Display your GitHub contributions for the last year to the console."""
    options: ContribOptions = {
        "ascii": ascii_mode or settings.ascii,
        "summary": summary or settings.summary,
        "username": username or settings.username,
        "token": token or settings.token,
    }

    try:
        if options["username"] == "" or options["token"] == "":
            bad_env()
    except KeyError:
        bad_env()

    contributions = get_github_contributions(
        options["username"], options["token"]
    )

    # Print days with and without contributions
    if contributions:
        print_github_style_grid_full_year(contributions, options=options)
