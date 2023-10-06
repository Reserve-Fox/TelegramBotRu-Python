def change_separators(old_sep: str, path: str) -> str:
    from os.path import sep as os_sep
    return path.replace(old_sep, os_sep)