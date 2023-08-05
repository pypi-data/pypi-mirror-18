import re
import subprocess

from setuptools import setup

__version__ = "0.3"

def _get_git_description():
    try:
        return subprocess.check_output(["git", "describe"]).decode("utf-8").strip()
    except subprocess.CalledProcessError:
        return None


def get_version():
    description = _get_git_description()

    match = re.match(r'(?P<tag>[\d\.]+)-(?P<offset>[\d]+)-(?P<sha>\w{8})', description)

    if match:
        version = "{tag}.post{offset}".format(**match.groupdict())
    else:
        version = description

    return version


def main():
    setup(
        name="open-jenkins",
        url="https://github.com/DoWhileGeek/open-jenkins",
        description="A command line utility for opening a repositories corresponding jenkins build homepage.",
        author="Joeseph Rodrigues",
        author_email="dowhilegeek@gmail.com",
        version=__version__,
        scripts=["open-jenkins"]
    )


if __name__ == "__main__":
    main()
