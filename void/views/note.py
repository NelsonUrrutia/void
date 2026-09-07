from datetime import date
from typing import override

from textual.app import ComposeResult
from textual.containers import Grid, Horizontal, Vertical, VerticalScroll
from textual.widgets import Button, Checkbox, Label, Static, TextArea

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
        .activity_card{
            height: auto;
            padding: 1 1;
        }
        .activity_card TextArea{
            height: 6;
        }
    """

    @override
    def __init__(self) -> None:
       super().__init__()
       self.ctrl = NoteController()
       self.activities_by_category_data = self.ctrl.get_activities_by_category()

       self.today = date.today()
       self.date_str = self.today.strftime("%B %d, %Y").upper()

    @override
    def compose(self) -> ComposeResult:
        with Vertical(classes="header"):
                yield Label(self.date_str, classes="module_title")
                yield Button("SAVE VOID NOTE", id="save_note_btn", variant="success", flat=True)
        with VerticalScroll(classes="main_container"):
            for _, category, activities in self.activities_by_category_data:
                yield Label(category, classes="module_title")
                with Grid(classes="activity_grid"):
                    for id, name in activities:
                        with Vertical(classes="activity_card"):
                            yield Checkbox(label=name)
                            yield TextArea()
