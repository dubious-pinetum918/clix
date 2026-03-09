"""Tweet detail CLI commands."""

from __future__ import annotations

from typing import Annotated, Optional

import typer

from x_cli.cli.helpers import get_client, is_json_mode, output_json
from x_cli.display.formatter import format_thread, format_tweet, console

tweet_app = typer.Typer(no_args_is_help=False, invoke_without_command=True)


@tweet_app.callback(invoke_without_command=True)
def tweet(
    ctx: typer.Context,
    tweet_id: Annotated[str, typer.Argument(help="Tweet ID")],
    thread: Annotated[bool, typer.Option("--thread", help="Show full thread")] = False,
    json_output: Annotated[bool, typer.Option("--json", help="JSON output")] = False,
    account: Annotated[Optional[str], typer.Option(help="Account name")] = None,
):
    """View a tweet and its thread."""
    if ctx.invoked_subcommand is not None:
        return

    from x_cli.core.api import get_tweet_detail

    with get_client(account) as client:
        tweets = get_tweet_detail(client, tweet_id)

    if not tweets:
        from x_cli.display.formatter import print_error

        print_error(f"Tweet {tweet_id} not found")
        raise typer.Exit(1)

    if is_json_mode(json_output):
        output_json([t.to_json_dict() for t in tweets])
    elif thread:
        format_thread(tweets, focal_id=tweet_id)
    else:
        # Show just the focal tweet
        focal = next((t for t in tweets if t.id == tweet_id), tweets[0])
        console.print(format_tweet(focal))
