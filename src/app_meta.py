"""
Application metadata shared across the project.
"""

APP_NAME = "CPA-Codex-Manager"
__version__ = "1.1.1"
APP_VERSION = __version__
APP_DESCRIPTION = "CPA-Codex-Manager"


def display_name() -> str:
    return f"{APP_NAME} v{APP_VERSION}"
