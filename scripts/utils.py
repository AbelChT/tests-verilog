import pathlib


def get_project_root_path() -> pathlib.Path:
    return pathlib.Path(__file__).parent.parent.absolute()
