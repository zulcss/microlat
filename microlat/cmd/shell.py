import click

from . import compose


@click.group(
    help=f"\nOstree image builder"
)
@click.pass_context
def cli(ctx: click.Context):
    ctx.ensure_object(dict)


cli.add_command(compose.compose)


def main():
    cli(prog_name="microlat")


if __name__ == '__main__':
    main()
