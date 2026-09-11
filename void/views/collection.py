from datetime import date
from itertools import groupby
from typing import override

from textual.app import ComposeResult
from textual.containers import Grid, Vertical, VerticalScroll
from textual.widgets import Label, Static

from void.controllers.note import NoteController


class CollectionView(Static):

    DEFAULT_CSS = """
        .note_grid{
            grid-size: 3;
            grid-gutter: 1;
        }
        .note_card_date{
            color: $text-muted;
            padding: 0 0 1 0;
        }
    """

    @override
    def __init__(self) -> None:
        super().__init__()
        self.ctrl = NoteController()

    @override
    def compose(self) -> ComposeResult:
        notes = self.ctrl.get_notes()
        with Vertical(classes="header"):
            yield Label("VOID COLLECTION", classes="module_title")
        with VerticalScroll(classes="main_container"):
            if not notes:
                yield Label("No VOID NOTE saved yet.")
                return
            with Grid(classes="card_grid note_grid"):
                for note_date, rows in groupby(notes, key=lambda row: row["note_date"]):
                    with Vertical(classes="note_card"):
                        yield Label(self.format_date(note_date), classes="note_card_date")
                        for row in rows:
                            with Vertical(classes="entry_card"):
                                yield Label(row["activity"], classes="entry_title")
                                if row["notes"]:
                                    yield Label(row["notes"], classes="entry_note")
                                else:
                                    yield Label("No notes written.", classes="entry_empty")

    def format_date(self, date_str):
        return date.fromisoformat(date_str).strftime("%B %d, %Y").upper()
