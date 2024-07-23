from typing import TYPE_CHECKING, Optional

from pyinfra import logger
from pyinfra.api.connectors import BaseConnectorMeta
from pyinfra.api.exceptions import InventoryError
from pyinfra.api.util import memoize

from .local import run_shell_command as run_local_shell_command

if TYPE_CHECKING:
    from pyinfra.api.host import Host
    from pyinfra.api.state import State


class Meta(BaseConnectorMeta):
    handles_execution = True


@memoize
def show_warning():
    logger.warning("The @dummy connector is in beta!")


def make_names_data(directory: Optional[str] = None):
    if not directory:
        raise InventoryError("No directory provided!")

    show_warning()

    yield "@dummy/{0}".format(directory), {
        "dummy_directory": "/{0}".format(directory.lstrip("/")),
    }, ["@dummy"]


def connect(state: "State", host: "Host"):
    return True


def run_shell_command(
    state: "State",
    host: "Host",
    command,
    get_pty: bool = False,
    timeout=None,
    stdin=None,
    success_exit_codes=None,
    print_output: bool = False,
    print_input: bool = False,
    return_combined_output: bool = False,
    **command_kwargs,
):

    return run_local_shell_command(
        state,
        host,
        "true",
        timeout=timeout,
        stdin=stdin,
        success_exit_codes=success_exit_codes,
        print_output=print_output,
        print_input=print_input,
        return_combined_output=return_combined_output,
    )


def put_file(
    state: "State",
    host: "Host",
    filename_or_io,
    remote_filename,
    remote_temp_filename=None,  # ignored
    print_output: bool = False,
    print_input: bool = False,
    **kwargs,  # ignored (sudo/etc)
):
    return True


def get_file(
    state: "State",
    host: "Host",
    remote_filename,
    filename_or_io,
    remote_temp_filename=None,  # ignored
    print_output: bool = False,
    print_input: bool = False,
    **kwargs,  # ignored (sudo/etc)
):
    return True
