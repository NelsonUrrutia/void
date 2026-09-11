from datetime import date
from typing import override

from textual.app import ComposeResult
from textual.containers import Vertical, VerticalScroll
from textual.widgets import Label, Static

from void.controllers.note import NoteController


class DayNote(Static):

    DEFAULT_CSS = """
        .header{
            padding: 0 1;
            height: auto;
        }
        .main_container{
            padding: 1 1;
        }
        .module_title{
            text-style: bold;
        }
        .note_card{
            height: auto;
            padding: 0 0 1 0;
        }
    """

    @override
    def __init__(self) -> None:
        super().__init__()
        self.ctrl = NoteController()

        self.today = date.today()  # noqa: DTZ011
        self.date_str = self.today.strftime("%B %d, %Y").upper()
        self.day_note_data = self.ctrl.get_day_note(self.today.isoformat())

    @override
    def compose(self) -> ComposeResult:
        with Vertical(classes="header"):
            yield Label(self.date_str, classes="module_title")
        with VerticalScroll(classes="main_container"):
            for row in self.day_note_data:
                with Vertical(classes="note_card"):
                    yield Label(row["activity"], classes="module_title")
                    yield Label(row["notes"] or "")
