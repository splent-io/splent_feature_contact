"""
CLI commands contributed by splent_feature_contact.

These commands are auto-discovered by the framework and exposed in the
SPLENT CLI under the ``feature:contact`` group.

Usage::

    splent feature:contact hello
"""

import click


@click.command("hello")
def hello():
    """Example command — replace with your own."""
    click.echo("  Hello from splent_feature_contact!")


cli_commands = [hello]
