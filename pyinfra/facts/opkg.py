from pyinfra.api import FactBase
from pyinfra import logger
from .util.packaging import parse_packages

OPKG_PACKAGE_NAME_REGEX = r"[a-zA-Z0-9\+\-\.]+"
OPKG_PACKAGE_VERSION_REGEX = r"[a-zA-Z0-9:~\.\-\+]+"


class OpkgInstalled(FactBase):
    """
    Returns a boolean indicating whether a package is installed
    """

    def command(self, name):
        self.name = name
        cmd = "opkg list-installed | grep {} || true".format(name)
        logger.debug(cmd)
        return cmd

    def process(self, output):
        logger.debug(output)
        for l in output:
            if not l.strip():
                continue
            pkg, version = l.strip().split(" - ")
            if pkg == self.name:
                return True
        return False


class OpkgPackages(FactBase):
    """
    Returns a dict of installed opkg packages:

    .. code:: python

        {
            "package_name": ["version"],
        }
    """

    command = "opkg list-installed"
    requires_command = "opkg"

    default = dict

    # regex = r"^[i|h]i\s+({0}):?[a-zA-Z0-9]*\s+({1}).+$".format(
    regex = r"^({0}) - ({1})$".format(
        OPKG_PACKAGE_NAME_REGEX,
        OPKG_PACKAGE_VERSION_REGEX,
    )

    def process(self, output):
        return parse_packages(self.regex, output)


class CPUArch(FactBase):
    """
    Returns a string indicating the CPU architecture
    """

    command = "opkg print-architecture | grep mips | awk '{print $2}'"

    def process(self, output):
        arch = output[0]
        logger.debug(arch)
        return arch
