from typing import override

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import Label, SelectionList, Static
from textual.widgets.selection_list import Selection

from void.controllers.note import NoteController


class NoteView(Static):

    DEFAULT_CSS = """
        .module_title{
            text-style: bold;
        }

        #activities_section{
            padding:0 1;
        }

       #activities_container{
        padding: 1 0
       }

        .activity_name{
            text-style: bold;
            margin-bottom: 1;
        }

        .activity_list{
            margin-bottom: 1;
        }
    """

    @override
    def __init__(self) -> None:
       super().__init__()
       self.ctrl = NoteController()
       self.activities_by_category_data = self.ctrl.get_activities_by_category()

    @override
    def compose(self) -> ComposeResult:
        with Horizontal():
            with Vertical(id="activities_section"):
                yield Label("ACTIVITIES", classes="module_title")
                with VerticalScroll(id="activities_container"):
                    for _, category, activities in self.activities_by_category_data:
                        yield Label(category, classes="activity_name")
                        yield SelectionList[int](
                            *(Selection(name, id) for id, name in activities),
                            classes="activity_list"
                        )
            with Vertical(id="void_form"):
                yield Label("NOTES",classes="module_title")
