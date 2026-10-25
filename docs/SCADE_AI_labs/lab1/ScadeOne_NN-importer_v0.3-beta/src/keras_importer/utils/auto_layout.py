import os
import re
import string
from ctypes import windll
from pathlib import Path
from subprocess import run
from typing import Generator, Optional, Union

PathStr = Union[Path, str]


def get_drives():
    """Get the list of available drives"""
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1

    return drives


def _get_potential_s1_install(
    root: PathStr, max_depth: int = 3, depth: int = 0, exclude: Optional[PathStr] = None
) -> Generator[Path, None, None]:
    """Get directories that may contain Scade One Install"""
    dir_to_skip = (
        "Windows",
        "Users",
        "temp",
        "Program Files (x86)",
        "Documents and Settings",
    )
    patt_s1_install = re.compile(
        r"Scade[_ ]?One|S[_ ]One|[\W_]S1[\W_]|^S1$", flags=re.IGNORECASE
    )
    if exclude and Path(root) == Path(exclude):
        return

    with os.scandir(root) as scanner:
        for entry in scanner:
            # We will search among directories for keywords (like "Ansys", "Scade")
            # As some directories (like Windows, Users) are big, we skip them
            if (
                not entry.is_dir()
                or entry.name.startswith((".", "$"))
                or depth > max_depth
                or (depth == 0 and entry.name in dir_to_skip)
            ):
                continue

            path = Path(entry.path)
            if patt_s1_install.search(path.name):
                # print(f"... ROOT={path}")
                yield path
            else:
                try:
                    yield from _get_potential_s1_install(
                        path, max_depth=max_depth, depth=depth + 1, exclude=exclude
                    )
                except PermissionError:
                    pass


def get_s1_exe(exe_name: str) -> Generator[Path, None, None]:
    """List all the Scade One executables with a given name"""
    # Note: we use os.scandir because it allows a better speed
    # ... and more control over the depth of parsing
    # (compared to os.walk or pathlib.glob)

    def iter_exe(root: Path, max_depth=6, depth=0) -> Generator[Path, None, None]:
        """Find the selected exe from a given root"""
        if not root.is_dir():
            return
        if depth > max_depth:
            return

        with os.scandir(root) as scanner:
            for entry in scanner:
                path = Path(entry.path)
                if entry.name == exe_name:
                    yield path
                elif entry.is_dir():
                    yield from iter_exe(path, max_depth=max_depth, depth=depth + 1)

    for drive in get_drives():
        drive_root = Path(f"{drive}://")
        ansys_program_files = drive_root / "Program Files" / "ANSYS Inc"
        try:
            # for dir_ in _get_potential_s1_install(drive_root):  # TODO: Refine by adding C:\no-backup or C:\AnsysDev
            for dir_ in _get_potential_s1_install(ansys_program_files):
                yield from iter_exe(dir_)
        except OSError:
            pass


# AutoLayout sorted by modification dates, from older to most recent
AUTO_LAYOUT_EXE_SORTED_DATE: list[Path] = []


def scan_for_auto_layout(force: bool = False) -> Optional[Path]:
    """Scan for auto-layout exe if needed and return most recent exe (if any)

    Args:
        force: Scan from scratch if set to True.
            Otherwise, no new scan is performed if any exe has been found before

    Returns:
        * Latest auto-layout exe (by modification date) if any found
        * None, if no exe found
    """
    if force:
        AUTO_LAYOUT_EXE_SORTED_DATE.clear()
    if not AUTO_LAYOUT_EXE_SORTED_DATE:
        exe_paths = get_s1_exe("swan_auto_layout.exe")
        AUTO_LAYOUT_EXE_SORTED_DATE.extend(
            sorted((p for p in exe_paths), key=lambda p: p.stat().st_mtime)
        )
    return AUTO_LAYOUT_EXE_SORTED_DATE[-1] if AUTO_LAYOUT_EXE_SORTED_DATE else None


def check_windows_path(path: Path, name: str, suffix: str) -> None:
    """Check path existence and extension"""
    suffix = "." + suffix.lstrip(".")
    if not path.is_file():
        raise FileNotFoundError(f"{name} does not exist or is not a file: {path}")
    if path.suffix != suffix:
        raise AttributeError(f"{name} shall be a {suffix} file but is: {path}")


def run_auto_layout(
    project: PathStr, *args, auto_layout_exe: Optional[PathStr] = None, **kwargs
):
    """Run auto-layout on a Scade One Project (file .sproj)

    Note: *args and **kwargs are passed to the `subprocess.run` function
    """
    if auto_layout_exe is None:
        scan_for_auto_layout()
        if AUTO_LAYOUT_EXE_SORTED_DATE:
            auto_layout_exe = AUTO_LAYOUT_EXE_SORTED_DATE[-1]
        else:
            raise AttributeError(
                "Path of AutoLayout not provided and no exe found on drive"
            )

    check_windows_path(Path(project), "Project", ".sproj")
    check_windows_path(Path(auto_layout_exe), "Auto-layout executable", ".exe")

    run([str(auto_layout_exe), "--project", str(project)], check=True, *args, **kwargs)


if __name__ == "__main__":
    from datetime import datetime

    print(f"DRIVES = {get_drives()}")
    print("-" * 25)
    print("--- Auto Layout Found ---")
    print("-" * 25)
    scan_for_auto_layout()
    for p in AUTO_LAYOUT_EXE_SORTED_DATE:
        print(f"{p} => {datetime.fromtimestamp(p.stat().st_mtime).isoformat()}")
