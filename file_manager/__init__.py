"""This package allows the user to open a file stored in
 a different directory. It works across different platforms."""

from pathlib import Path

def get_absolute_path(path_in_working_dir):
    """
    returns the absolute path of a file
    :var
    str path
        the file path within the working dir
    :returns
    PureWindowsPath or PurePosixPath object
        type depends on the operating system in use
    """
    def get_project_root() -> Path:
        """Returns project root folder."""
        return Path(__file__).parent.parent

    return get_project_root().joinpath(path_in_working_dir)

