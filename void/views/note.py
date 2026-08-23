
from textual.app import ComposeResult
from textual.widgets import Static, Label

from typing import override

class NoteView(Static):
    @override
    def compose(self) -> ComposeResult:
        yield Label("VOID NOTE")
