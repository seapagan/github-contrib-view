"""Main module for the project."""

# ruff: noqa: T201
from __future__ import annotations

import contextlib
import locale
import sys
from bisect import bisect_left
from datetime import datetime, timedelta, timezone
from typing import NoReturn, Optional, TypedDict

import requests
import typer
from dotenv import dotenv_values
from rich import print as rprint

from github_contrib_view.config import settings
from github_contrib_view.constants import (
    DAYS_PER_WEEK,
    HTTP_OK,
    QUERY,
    REQUEST_TIMEOUT,
)


# Define a TypedDict for options
class ContribOptions(TypedDict):
    """TypedDict for contribution display options."""

    ascii: bool
    summary: bool
    username: str
    token: str


config = dotenv_values(".env")

# Set locale for date formatting (falls back to system default)
with contextlib.suppress(locale.Error):
    locale.setlocale(locale.LC_TIME, "")


app = typer.Typer(
    pretty_exceptions_show_locals=False,
    add_completion=False,
    rich_markup_mode="rich",
)


def get_github_contributions(
    username: str, token: str
) -> dict[str, int] | None:
    """Get GitHub contributions using GraphQL API.

    You need a GitHub Personal Access Token
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        "https://api.github.com/graphql",
        json={"query": QUERY, "variables": {"username": username}},
        headers=headers,
        timeout=REQUEST_TIMEOUT,
    )

    data = response.json()

    if data["data"]["user"] is None:
        rprint(
            f"[red]Error[/red] : User '{username}' cannot be found on GitHub, "
            "[red]Exiting[/red]"
        )
        raise typer.Exit(code=1)

    if response.status_code == HTTP_OK:
        weeks = data["data"]["user"]["contributionsCollection"][
            "contributionCalendar"
        ]["weeks"]

        contributions = {}
        for week in weeks:
            for day in week["contributionDays"]:
                date = day["date"]
                count = day["contributionCount"]
                contributions[date] = count

        return contributions

    print(f"Error: {response.status_code}")
    return None


def get_symbol(count: int, *, use_ascii: bool = False) -> str:
    """Return the relevant emoji symbol.

    This depends on the contribution count passed.
    """
    thresholds = [1, 4, 7, 10]
    if use_ascii:
        symbols = [
            "\u25a0 ",
            "[green3]\u25a0 [/green3]",
            "[yellow3]\u25a0 [/yellow3]",
            "[orange3]\u25a0 [/orange3]",
            "[red3]\u25a0 [/red3]",
        ]
    else:
        # use colored emoji blocks ...
        symbols = [
            "\u2b1c",
            "\U0001f7e9",
            "\U0001f7e8",
            "\U0001f7e7",
            "\U0001f7e5",
        ]

    return symbols[bisect_left(thresholds, count + 1)]


def print_legend() -> None:
    """Print the contribution legend."""
    # Use the actual threshold values that get_symbol expects
    legend_data = [
        (0, "0"),
        (2, "1-3"),
        (5, "4-6"),
        (8, "7-9"),
        (12, "10+"),
    ]

    legend_items = [
        f"{get_symbol(count)} {label}" for count, label in legend_data
    ]
    rprint("Legend: " + "   ".join(legend_items))


def print_header(
    start_date: datetime, end_date: datetime, options: ContribOptions
) -> None:
    """Print out the header and legend."""
    rprint(
        f"\n🎨 [bold]{options['username'].capitalize()}'s[/bold] "
        "GitHub Contributions for the last year "
        f"({start_date.strftime('%x')} to {end_date.strftime('%x')})\n"
    )
    print_legend()
    print()


def print_month_header(start_date: datetime, end_date: datetime) -> None:
    """Print the month header at the start of the chart."""
    # Create month headers - each emoji block takes 2 character widths
    month_line = "    "  # Space for day labels (4 chars: "Mon ")
    current_week_start = start_date
    last_month = ""
    skipped_space = True  # used to adjust the month header

    for week in range(53):  # 53 weeks to cover full year
        week_date = current_week_start + timedelta(weeks=week)

        if week_date > end_date:
            break

        month_abbr = week_date.strftime("%b")

        # Show month name only at the start of each month
        if week_date.day <= DAYS_PER_WEEK and month_abbr != last_month:
            month_line += month_abbr[:3]  # Get 3-letter Month name
            last_month = month_abbr
            skipped_space = False
        elif skipped_space:
            month_line += "  "  # 2 spaces to match emoji width
        else:
            month_line += (
                " "  # 1 space to compensate for the month names being 3 chars
            )
            skipped_space = True

    print(month_line)


def print_grid(
    start_date: datetime,
    end_date: datetime,
    contributions: dict[str, int],
    *,
    use_ascii: bool,
) -> None:
    """Generate and print out the actual contributions grid."""
    day_names = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

    for day_of_week in range(7):
        day_label = day_names[day_of_week]

        row = f"{day_label} "  # 4 characters total

        # Go through each week of the year
        for week in range(53):
            current_day = start_date + timedelta(weeks=week, days=day_of_week)

            if current_day > end_date:
                break

            date_str = current_day.strftime("%Y-%m-%d")
            count = contributions.get(date_str, 0)
            row += get_symbol(count, use_ascii=use_ascii)

        rprint(row)


def print_github_style_grid_full_year(
    contributions: dict[str, int], options: ContribOptions
) -> None:
    """Print a full year GitHub-style contribution grid."""
    if not contributions:
        return

    # Get the date range - full last year
    all_dates = sorted(contributions.keys())
    if not all_dates:
        return

    # Use the last date as reference and go back 52 weeks
    end_date = datetime.strptime(all_dates[-1], "%Y-%m-%d").replace(
        tzinfo=timezone.utc
    )
    start_date = end_date - timedelta(weeks=52)

    # Adjust to start on Sunday (GitHub convention)
    days_since_sunday = (start_date.weekday() + 1) % 7
    start_date = start_date - timedelta(days=days_since_sunday)

    print_header(start_date, end_date, options=options)
    print_month_header(start_date, end_date)
    print_grid(start_date, end_date, contributions, use_ascii=options["ascii"])

    print()

    # Statistics
    year_contributions = {
        k: v
        for k, v in contributions.items()
        if start_date.strftime("%Y-%m-%d") <= k <= end_date.strftime("%Y-%m-%d")
    }

    total = sum(year_contributions.values())
    active_days = sum(1 for count in year_contributions.values() if count > 0)
    max_day = (
        max(year_contributions.items(), key=lambda x: x[1])
        if year_contributions
        else ("", 0)
    )

    if options["summary"]:
        print("📊 Year Summary:")
        print(f"   Total contributions: {total}")
        print(f"   Active days: {active_days}/{len(year_contributions)}")
        best_day_formatted = (
            datetime.strptime(max_day[0], "%Y-%m-%d")
            .replace(tzinfo=timezone.utc)
            .strftime("%x")
            if max_day[0]
            else ""
        )
        print(f"   Best day: {best_day_formatted} ({max_day[1]} contributions)")
        if year_contributions:
            daily_average = total / len(year_contributions)
            activity_rate = active_days / len(year_contributions) * 100
            print(f"   Average per day: {daily_average:.1f}")
            print(f"   Activity rate: {activity_rate:.1f}%")


def print_contribution_list(contributions: dict[str, int]) -> None:
    """Print a list of all contributions by date.

    This is really a debug function and will probably not be available from the
    CLI.
    """
    for date, count in contributions.items():
        status = "✅ Contributed" if count > 0 else "❌ No contribution"
        print(f"{date}: {count} contributions - {status}")


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
