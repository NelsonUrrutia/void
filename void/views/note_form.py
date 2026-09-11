from datetime import date
from typing import override

from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Grid, Horizontal, Vertical, VerticalScroll
from textual.message import Message
from textual.widgets import Button, Checkbox, Input, Label, Static, TextArea

from void.controllers.note import NoteController


class NoteForm(Static):

    class Saved(Message):
        """Posted once the day's note is stored, so NoteView can swap to DayNote."""

    BINDINGS = [Binding("ctrl+s", "save", "SAVE VOID NOTE", priority=True)]

    DEFAULT_CSS = """
        NoteForm{
            layout: vertical;
        }
        .header{
            dock: top;
            height: auto;
            padding: 1 2 0 2;
            border-bottom: solid $panel;
        }
        .actions{
            dock: bottom;
            height: auto;
            padding: 0 2 1 2;
            align-horizontal: right;
        }
        .main_container{
            padding: 1 2;
        }
        .module_title{
            text-style: bold;
        }
        #date_str{
            display: none;
        }
        #counter{
            color: $text-muted;
        }

        .category_block{
            height: auto;
            padding: 0 0 1 0;
        }
        .category_title{
            text-style: bold;
            color: $accent;
            padding: 0 0 1 0;
        }
        .activity_grid{
            grid-size: 2;
            grid-columns: 1fr;
            grid-gutter: 1 2;
            height: auto;
        }
        .activity_card{
            height: auto;
            padding: 1 1;
        }
        .activity_card Checkbox{
            width: 100%;
        }
        .activity_card TextArea{
            height: 6;
        }
        .activity_handle{
            display: none;
        }
    """

    @override
    def __init__(self) -> None:
       super().__init__()
       self.ctrl = NoteController()
       self.activities_by_category_data = self.ctrl.get_activities_by_category()
       self.activity_total = sum(len(activities) for _, _, activities in self.activities_by_category_data)

       self.today = date.today()  # noqa: DTZ011
       self.date_str = self.today.strftime("%B %d, %Y").upper()
       self.date_iso = self.today.isoformat()

       day_note_data = self.ctrl.get_day_note(self.today.isoformat())

       self.disable_add_note_btn = False
       if day_note_data:
           self.disable_add_note_btn = True



    @override
    def compose(self) -> ComposeResult:
        with Vertical(classes="header"):
            yield Label(self.date_str, classes="module_title")
            yield Label(self.counter_text(0), id="counter")
            yield Input(value=self.date_iso, id="date_str")
        with Horizontal(classes="actions"):
            yield Button("SAVE VOID NOTE", id="save_note_btn", variant="success", flat=True, disabled=self.disable_add_note_btn)
        with VerticalScroll(classes="main_container"):
            for _, category, activities in self.activities_by_category_data:
                if activities:
                    with Vertical(classes="category_block"):
                        yield Label(f"── {category} ", classes="category_title")
                        with Grid(classes="activity_grid"):
                            for id, name in activities:
                                handle = f"{id}::{self.handleize(name)}"
                                with Vertical(classes="activity_card"):
                                    yield Checkbox(label=name)
                                    yield Input(value=handle, classes="activity_handle")
                                    yield TextArea()

    @on(Checkbox.Changed)
    def on_activity_toggled(self) -> None:
        self.query_one("#counter", Label).update(self.counter_text(self.count_check_elements()))

    def counter_text(self, checked: int) -> str:
        return f"{checked} of {self.activity_total} activities logged"

    def action_save(self) -> None:
        if not self.disable_add_note_btn:
            self.on_save_note()

    @on(Button.Pressed, "#save_note_btn")
    def on_save_note(self) -> None:
        if self.count_check_elements() == 0:
            self.notify("Please check at least one activity to save", severity="warning")
            return

        checked_activities = []
        for checkbox in self.query(Checkbox):
            if checkbox.value:
                parent_container = checkbox.query_ancestor(Vertical)
                handle = parent_container.query_one(Input).value
                note = parent_container.query_one(TextArea).text
                checked_activities.append((handle, note))

        self.save_note(checked_activities)

    def save_note(self, activities):
        date_str = self.query_one("#date_str", Input).value.strip()
        self.ctrl.save_note(date_str, activities)
        self.notify("VOID NOTE successfully saved", severity="information")
        self.post_message(self.Saved())

    def count_check_elements(self) -> int:
        counter = 0
        for checkbox in self.query(Checkbox):
            if checkbox.value:
               counter += 1
        return counter

    def handleize(self, string_to_handle):
        return string_to_handle.lower().replace("'","").replace(" ", "-")
