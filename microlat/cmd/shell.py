import click

from microlat.cmd.options import config_option
from microlat.cmd.options import debug_option
from microlat.cmd.options import workspace_option
from microlat.cmd import pass_state_context
from microlat.log import setup_log
from microlat.runner import Runner


@click.command
@pass_state_context
@config_option
@workspace_option
@debug_option
def cli(state, config, workspace, debug):
    Runner(state).run()

def main():
    cli(prog_name="microlat")

