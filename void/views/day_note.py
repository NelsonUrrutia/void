from datetime import date
from itertools import groupby
from typing import override

from textual.app import ComposeResult
from textual.containers import Vertical, VerticalScroll
from textual.widgets import Label, Static

from void.controllers.note import NoteController


class DayNote(Static):

    DEFAULT_CSS = """
        .day_category_title{
            text-style: bold;
            color: $text-muted;
        }
        .note_card{
            margin: 0 0 1 0;
        }
        .note_card_title{
            text-style: bold;
            color: $accent;
        }
        .note_card_note{
            color: $text-muted;
        }
        .note_card_empty{
            color: $text-muted;
            text-style: italic;
        }
    """

    @override
    def __init__(self) -> None:
        super().__init__()
        self.ctrl = NoteController()

        self.today = date.today()  # noqa: DTZ011
        self.date_str = self.today.strftime("%B %d, %Y").upper()

    @override
    def compose(self) -> ComposeResult:
        day_note_data = self.ctrl.get_day_note(self.today.isoformat())
        with Vertical(classes="header"):
            yield Label(self.date_str, classes="module_title")
            yield Label(self.counter_text(len(day_note_data)), id="counter")
        with VerticalScroll(classes="main_container"):
            if not day_note_data:
                yield Label("No VOID NOTE saved for today yet.", classes="empty_state")
            for category, rows in groupby(day_note_data, key=lambda row: row["category"]):
                yield Label(f"── {category.upper()} ", classes="day_category_title")
                for row in rows:
                    with Vertical(classes="note_card"):
                        yield Label(row["activity"], classes="note_card_title")
                        if row["notes"]:
                            yield Label(row["notes"], classes="note_card_note")
                        else:
                            yield Label("No notes written.", classes="note_card_empty")

    def counter_text(self, logged: int) -> str:
        return f"{logged} of {self.ctrl.get_activity_total()} activities logged"
