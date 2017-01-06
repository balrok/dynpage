from .dependencies import init_dependencies, find_dependencies
from .modelparser import get_stats_for_models


def get_stats_for_file(filename: str, folder: str=None) -> str:
    init_dependencies()
    files = find_dependencies(filename, folder)
    return get_stats_for_models(files)
