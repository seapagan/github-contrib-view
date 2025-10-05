"""Module to read the contributions directly from GitHub using GraphGL."""

from __future__ import annotations

import requests
import typer
from rich import print as rprint

from github_contrib_view.constants import (
    HTTP_OK,
    QUERY,
    REQUEST_TIMEOUT,
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

    rprint(f"Error: {response.status_code}")
    return None
