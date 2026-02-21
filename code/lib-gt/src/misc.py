
from constants import Colors
import sys
from typing import Any


def printerr(*args: Any) -> None:
    """Prints a red message"""
    sys.stderr.write(f"{Colors.RED}")
    sys.stderr.write(*args)
    sys.stderr.write(f'{Colors.END}\n')
