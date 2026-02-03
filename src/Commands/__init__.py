from telegram.ext import CommandHandler

from ._start import start_command
from ._help import help_command

# Export names so `Commands.start_command` works
__all__ = [
    "start_command",
    "help_command",
    "list",
]

# A list of handlers (nice for app.add_handlers(...) or a loop)
list = [
    CommandHandler("start", start_command),
    CommandHandler("help", help_command),
]
