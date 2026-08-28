from textual.app import ComposeResult
from textual.widgets import DataTable, Static, Label

from typing import override

from void.controllers.activity import ActivityController

class ActivitiesView(Static):

    @override
    def compose(self) -> ComposeResult:
        yield Label("VOID ACTIVITIES")
        yield DataTable()

    def on_mount(self) -> None:
        self.ctrl = ActivityController()
        self.init_table()
        
    def init_table(self):
        activities = self.ctrl.get_activities()
        table = self.query_one(DataTable)
        table.add_columns("ID", "ACTIVITY", "CATEGORY")
        table.add_rows(activities)




