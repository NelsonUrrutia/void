from typing import override

from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal, HorizontalScroll, Vertical, VerticalScroll
from textual.widgets import Button, DataTable, Input, Label, Select, Static

from void.controllers.activity import ActivityController
from void.controllers.category import CategoryController


class ActivitiesView(Static):
    DEFAULT_CSS = """
        .module_title{
           text-style: bold;
        }

        #category_module{
            height: auto;
            padding: 1 1;
            width: 35%
        }

        #activity_module{
            padding: 1 1;
            height: 100%;
            width: 60%;
        }

        #activity_form{
            height: auto;
        }

        #activity_form Horizontal{
            height: auto;
        }

        #activities_table{
            height: 1fr;
        }

        #activity_id{
            display: none;
        }

    """

    @override
    def compose(self) -> ComposeResult:
        with Horizontal():
            with Vertical(id="category_module"):
                yield Label("CATEGORIES", classes="module_title")
                yield Label("New Category")
                yield Input(placeholder="Add a new category", id="new_category")
                yield Button(label="ADD",  flat=True, id="add_category")
                yield DataTable(id="categories_table")
            with Vertical(id="activity_module"):
                with Vertical(id="activity_form"):
                    yield Label("ACTIVITIES", classes="module_title")
                    yield Label("Activity")
                    yield Input(placeholder="Add a new activity", id="new_activity")
                    yield Label("Select a category")
                    yield Select([], type_to_search=True, id="category_select")
                    yield Input(id="activity_id", compact=True)
                    with Horizontal():
                        yield Button(label="ADD",  flat=True, id="add_activity", variant="success")
                        yield Button(label="UPDATE", flat=True, id="update_activity",variant="warning", disabled=True)
                        yield Button(label="SUSPEND", flat=True, id="suspend_activity", variant="error", disabled=True)
                        yield Button(label="CLEAR", flat=True, id="clear_activity_form", variant="default")
                yield DataTable(id="activities_table", cursor_type="row")

    def on_mount(self) -> None:
        # Controller
        self.ctrl = ActivityController()
        self.categoriesCtrl = CategoryController()

        # Category inputs
        self.add_category_input = self.query_one("#new_category", Input)
        self.add_category_btn = self.query_one("#add_category", Button)
        self.categories_table = self.query_one("#categories_table", DataTable)

        # Activity inputs
        self.add_activity_input = self.query_one("#new_activity", Input)
        self.category_selector = self.query_one("#category_select", Select)
        self.activity_id = self.query_one("#activity_id", Input)
        self.add_activity_btn = self.query_one("#add_activity", Button)
        self.update_activity_btn = self.query_one("#update_activity", Button)
        self.suspend_activity_btn = self.query_one("#suspend_activity", Button)
        self.clear_activity_form_btn = self.query_one("#clear_activity_form", Button)
        self.activities_table = self.query_one("#activities_table", DataTable)

        self.init_activities_table()
        self.init_categories_selector()
        self.init_categories_table()

    def init_activities_table(self):
        activities = self.ctrl.get_activities()
        self.activities_table.add_columns("ID","ACTIVITY", "CATEGORY")
        self.activities_table.add_rows(activities)

    def init_categories_selector(self):
        self.category_selector.clear()
        self.category_selector.set_options(self.categoriesCtrl.get_categories_for_activities())

    def init_categories_table(self):
        categories = self.categoriesCtrl.get_categories()
        self.categories_table.add_columns("CATEGORY")
        self.categories_table.add_rows(categories)

    def update_activities(self):
        activities = self.ctrl.get_activities()
        self.activities_table.clear()
        self.activities_table.add_rows(activities)

    def update_categories(self):
        categories = self.categoriesCtrl.get_categories()
        self.categories_table.clear()
        self.categories_table.add_rows(categories)
        self.init_categories_selector()


    @on(Button.Pressed, "#clear_activity_form")
    def on_clear_activity_form(self) -> None:
        self.clear_activity_form()

    @on(Button.Pressed, "#add_activity")
    def on_add_activity(self) -> None:
        activity = self.add_activity_input.value
        category_id = self.category_selector.value

        if not activity:
            self.notify("Activity must be set", severity="error")
            return
        if not category_id:
            self.notify("Category must be set", severity="error")
            return

        self.ctrl.create_activity(activity, category_id)
        self.add_activity_input.value = ""
        self.category_selector.clear()
        self.update_activities()

    @on(Button.Pressed, "#update_activity")
    def on_update_activity(self) -> None:
        activity = self.add_activity_input.value
        activity_id = self.activity_id.value
        category_id = self.category_selector.value

        if not activity:
            self.notify("Activity must be set", severity="error")
            return
        if not category_id:
            self.notify("Category must be set", severity="error")
            return

        self.ctrl.update_activity(activity_id, activity, category_id)
        self.update_activities()
        self.clear_activity_form()

    @on(Button.Pressed, "#suspend_activity")
    def on_suspend_activity(self) -> None:
        activity_id = self.activity_id.value
        self.ctrl.suspend_activity(activity_id)
        self.clear_activity_form()
        self.update_activities()



    @on(Button.Pressed, "#add_category")
    def on_add_category(self) -> None:
        category = self.add_category_input.value
        if not category:
            self.notify("Category must be set", severity="error")
            return

        self.categoriesCtrl.create_category(category)
        self.add_category_input.value = ""
        self.update_categories()

    @on(DataTable.RowSelected, "#activities_table")
    def on_activity_row_selected(self, event: DataTable.RowSelected) -> None:
        row = event.data_table.get_row(event.row_key)
        ac_id = row[0]
        ac_name = row[1]
        ac_category = row[2]

        self.add_activity_input.value = ac_name
        self.activity_id.value = str(ac_id)

        categories = self.categoriesCtrl.get_categories_for_activities()
        category_id = next((cid for name, cid in categories if name == ac_category), Select.BLANK)
        self.category_selector.value = category_id

        self.update_activity_btn.disabled = False
        self.add_activity_btn.disabled = True
        self.suspend_activity_btn.disabled = False

    def clear_activity_form(self):
        self.add_activity_input.value = ""
        self.activity_id.value = ""
        self.category_selector.clear()
        self.update_activity_btn.disabled = True
        self.add_activity_btn.disabled = False
        self.suspend_activity_btn.disabled = True
