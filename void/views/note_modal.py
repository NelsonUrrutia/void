from itertools import groupby
from typing import override

from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Center, Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Button, Label


class NoteModal(ModalScreen[None]):

    BINDINGS = [Binding("escape", "close", "Close")]

    DEFAULT_CSS = """
        NoteModal{
            align: center middle;
        }
        .modal_card{
            width: 90%;
            height: 90%;
            padding: 1 4;
            border: round $primary;
            border-title-color: $accent;
            border-title-style: bold;
            background: $background;
        }
        .modal_card .section_title{
            padding: 1 0 1 0;
        }
        .modal_card .entry_card{
            padding: 1 0 1 2;
        }
        .modal_body{
            height: 1fr;
        }
        .modal_footer{
            height: auto;
            padding: 1 0 0 0;
        }
    """

    @override
    def __init__(self, title: str, rows: list) -> None:
        super().__init__()
        self.note_title = title
        self.rows = sorted(rows, key=lambda row: (row["category"], row["activity"]))

    @override
    def compose(self) -> ComposeResult:
        with Vertical(classes="modal_card") as card:
            card.border_title = self.note_title
            with VerticalScroll(classes="modal_body"):
                for category, group in groupby(self.rows, key=lambda row: row["category"]):
                    entries = list(group)
                    yield Label(f"── {category.upper()} · {len(entries)} ", classes="section_title")
                    for row in entries:
                        with Vertical(classes="entry_card"):
                            yield Label(row["activity"], classes="entry_title")
                            if row["notes"]:
                                yield Label(row["notes"], classes="entry_note")
                            else:
                                yield Label("No notes written.", classes="entry_empty")
            with Center(classes="modal_footer"):
                yield Button("CLOSE", id="close_note_modal", variant="primary", flat=True)

    @on(Button.Pressed, "#close_note_modal")
    def on_close_pressed(self) -> None:
        self.action_close()

    def action_close(self) -> None:
        self.dismiss()
