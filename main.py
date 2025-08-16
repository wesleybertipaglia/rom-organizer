from cliengine.runner import run_cli
from cli.types import CommandType
from cliengine.loader import load_commands_from

load_commands_from("tools")

run_cli(
    app_name="Rom Organizer",
    description="A command-line utility powered by CLI Engine for organizing your ROMs on the go.",
    types=list(CommandType)
)