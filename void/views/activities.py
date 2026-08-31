from typing import override

from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, DataTable, Input, Label, Select, Static

from void.controllers.activity import ActivityController
from void.controllers.category import CategoryController


class ActivitiesView(Static):

    @override
    def compose(self) -> ComposeResult:
        with Horizontal():
            with Vertical():
                yield Label("CATEGORIES")
                yield Label("New Category")
                yield Input(placeholder="Add a new category", id="new_category")
                yield Button(label="ADD",  flat=True, id="add_category")
                yield DataTable(id="categories_table")
            with Vertical():
                yield Label("ACTIVITIES")
                yield Label("Activity")
                yield Input(placeholder="Add a new activity", id="new_activity")
                yield Label("Select a category")
                yield Select([], type_to_search=True, id="category_select")
                yield Button(label="ADD",  flat=True, id="add_activity")
                yield DataTable(id="activities_table")

    def on_mount(self) -> None:
        self.ctrl = ActivityController()
        self.categoriesCtrl = CategoryController()
        self.init_table()
        self.init_categories()
        self.init_categories_table()

    def init_table(self):
        activities = self.ctrl.get_activities()
        table = self.query_one("#activities_table", DataTable)
        table.add_columns("ACTIVITY", "CATEGORY")
        table.add_rows(activities)

    def init_categories(self):
        select = self.query_one("#category_select", Select)
        select.clear()
        select.set_options(self.categoriesCtrl.get_categories_for_activities())

    def init_categories_table(self):
        categories = self.categoriesCtrl.get_categories()
        table = self.query_one("#categories_table", DataTable)
        table.add_columns("CATEGORY")
        table.add_rows(categories)

    def update_activities(self):
        activities = self.ctrl.get_activities()
        table = self.query_one("#activities_table", DataTable)
        table.clear()
        table.add_rows(activities)

    def update_categories(self):
        categories = self.categoriesCtrl.get_categories()
        table = self.query_one("#categories_table", DataTable)
        table.clear()
        table.add_rows(categories)
        self.init_categories()

    @on(Button.Pressed, "#add_activity")
    def on_add_activity(self) -> None:
        activity_input = self.query_one("#new_activity", Input)
        activity = activity_input.value
        category_id = self.query_one("#category_select", Select).value
        if not activity:
            self.notify("Activity must be set", severity="error")
            return
        if not category_id:
            self.notify("Category must be set", severity="error")
            return

        self.ctrl.create_activity(activity, category_id)
        activity_input.value = ""
        self.update_activities()

    @on(Button.Pressed, "#add_category")
    def on_add_category(self) -> None:
        category_input = self.query_one("#new_category", Input)
        category = category_input.value
        if not category:
            self.notify("Category must be set", severity="error")
            return

        self.categoriesCtrl.create_category(category)
        category_input.value = ""
        self.update_categories()
