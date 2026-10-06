from datetime import date
from itertools import groupby
from typing import override

from textual import on
from textual.app import ComposeResult
from textual.containers import Grid, Right, Vertical, VerticalScroll
from textual.widgets import Button, Label, Static

from void.controllers.note import NoteController
from void.views.note_modal import NoteModal


class CollectionView(Static):

    DEFAULT_CSS = """
        .note_grid{
            grid-size: 3;
            grid-gutter: 1;
        }
        .note_card_actions{
            height: auto;
            margin: 0 0 1 0;
        }
    """

    @override
    def __init__(self) -> None:
        super().__init__()
        self.ctrl = NoteController()
        self.notes_by_date: dict[str, list] = {}

    @override
    def compose(self) -> ComposeResult:
        notes = self.ctrl.get_notes()
        self.notes_by_date = {
            note_date: list(rows) for note_date, rows in groupby(notes, key=lambda row: row["note_date"])
        }
        with Vertical(classes="header"):
            yield Label("VOID COLLECTION", classes="module_title")
        with VerticalScroll(classes="main_container"):
            if not notes:
                yield Label("No VOID NOTE saved yet.")
                return
            with Grid(classes="card_grid note_grid"):
                for note_date, rows in self.notes_by_date.items():
                    with Vertical(classes="note_card") as card:
                        card.border_title = self.format_date(note_date)
                        for row in rows:
                            with Vertical(classes="entry_card"):
                                yield Label(row["activity"], classes="entry_title")
                                if row["notes"]:
                                    yield Label(row["notes"], classes="entry_note")
                                else:
                                    yield Label("No notes written.", classes="entry_empty")
                        with Right(classes="note_card_actions"):
                            yield Button("EXPAND", name=note_date, classes="open_note", flat=True)

    def format_date(self, date_str):
        return date.fromisoformat(date_str).strftime("%B %d, %Y").upper()

    @on(Button.Pressed, ".open_note")
    def on_open_note(self, event: Button.Pressed) -> None:
        note_date = event.button.name
        if note_date in self.notes_by_date:
            self.app.push_screen(NoteModal(self.format_date(note_date), self.notes_by_date[note_date]))
