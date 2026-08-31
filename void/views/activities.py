from typing import override

from textual import on
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, DataTable, Input, Label, Select, Static

from void.controllers.activity import ActivityController
from void.controllers.category import CategoryController


class ActivitiesView(Static):

    @override
    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label("ACTIVITIES")
            yield Label("Activity")
            yield Input(placeholder="Add a new activity")
            yield Label("Select a category")
            yield Select([],type_to_search=True )
            yield Button(label="ADD",  flat=True, id="add_activity")
            yield DataTable()

    def on_mount(self) -> None:
        self.ctrl = ActivityController()
        self.categoriesCtrl = CategoryController()
        self.init_table()
        self.init_categories()

    def init_table(self):
        activities = self.ctrl.get_activities()
        table = self.query_one(DataTable)
        table.add_columns("ACTIVITY", "CATEGORY")
        table.add_rows(activities)

    def init_categories(self):
        select = self.query_one(Select)
        select.set_options(self.categoriesCtrl.get_categories_for_activities())

    def update_table(self):
        activities = self.ctrl.get_activities()
        table = self.query_one(DataTable)
        table.clear()
        table.add_rows(activities)

    @on(Button.Pressed, "#add_activity")
    def on_button_pressed(self) -> None:
        activity = self.query_one(Input).value
        category_id = self.query_one(Select).value
        if not activity:
            self.notify("Activity must be set", severity="error")
            return
        if not category_id:
            self.notify("Category must be set", severity="error")
            return

        self.ctrl.create_activity(activity, category_id)
        self.update_table()
