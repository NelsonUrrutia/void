from datetime import date
from typing import override

from textual import on
from textual.app import ComposeResult
from textual.containers import Grid, Vertical, VerticalScroll
from textual.widgets import Button, Checkbox, Input, Label, Static, TextArea

from void.controllers.note import NoteController


class NoteView(Static):

    DEFAULT_CSS = """
        .header{
            padding: 0 1;
            height: auto;
        }
        .main_container{
            padding: 1 1 ;
        }
        .activity_grid{
            grid-size: 2;
            grid-columns: 1fr;
            height: auto;
            grid-gutter: 1;
        }
        .module_title{
            text-style: bold;
        }

        #date_str{
            display: none;
        }
        .activity_card{
            height: auto;
            padding: 1 1;
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


       self.today = date.today()  # noqa: DTZ011
       self.date_str = self.today.strftime("%B %d, %Y").upper()


    @override
    def compose(self) -> ComposeResult:
        with Vertical(classes="header"):
                yield Label(self.date_str, classes="module_title")
                yield Input(value=self.date_str, id="date_str")
                yield Button("SAVE VOID NOTE", id="save_note_btn", variant="success", flat=True)
        with VerticalScroll(classes="main_container"):
            for _, category, activities in self.activities_by_category_data:
                if activities:
                    yield Label(category, classes="module_title")
                    with Grid(classes="activity_grid"):
                        for id, name in activities:
                            handle = f"{id}::{self.handleize(name)}"
                            with Vertical(classes="activity_card"):
                                yield Checkbox(label=name)
                                yield Input(value=handle, classes="activity_handle")
                                yield TextArea()

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
        self.clear_form()

    def count_check_elements(self) -> int:
        counter = 0
        for checkbox in self.query(Checkbox):
            if checkbox.value:
               counter += 1
        return counter

    def clear_form(self):
        for checkbox in self.query(Checkbox):
            checkbox.value = False

        for textArea in self.query(TextArea):
            textArea.text = ""

    def handleize(self, string_to_handle):
        return string_to_handle.lower().replace("'","").replace(" ", "-")
