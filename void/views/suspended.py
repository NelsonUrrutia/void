from typing import override

from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.message import Message
from textual.widgets import Button, DataTable, Label, Static

from void.controllers.activity import ActivityController


class SuspendedView(Static):

    class Restored(Message):
        """Posted when an activity is restored, so the other views can re-render."""

    DEFAULT_CSS = """
        #suspended_module{
            height: 1fr;
        }

        #selected_activity{
            color: $text-muted;
            margin: 1 0 0 0;
        }

        #suspended_cta_container{
            height: auto;
            margin: 1 0;
        }

        #suspended_cta_container Button{
            margin: 0 1 0 0;
        }

        #suspended_table{
            height: 1fr;
        }
    """

    @override
    def __init__(self) -> None:
        super().__init__()
        self.ctrl = ActivityController()
        self.selected_id: int | None = None

    @override
    def compose(self) -> ComposeResult:
        with Vertical(classes="header"):
            yield Label("VOID SUSPENDED", classes="module_title")
            yield Label(self.counter_text(), id="counter")
        with Vertical(classes="main_container", id="suspended_module"):
            yield Label("SUSPENDED ACTIVITIES", classes="module_title")
            yield Label(self.selected_text(), id="selected_activity")
            with Horizontal(id="suspended_cta_container"):
                yield Button(label="RESTORE", flat=True, id="restore_activity", variant="success", disabled=True)
                yield Button(label="CLEAR", flat=True, id="clear_selection", variant="default")
            yield DataTable(id="suspended_table", cursor_type="row")

    def on_mount(self) -> None:
        self.restore_btn = self.query_one("#restore_activity", Button)
        self.suspended_table = self.query_one("#suspended_table", DataTable)
        self.suspended_table.add_columns("ID", "ACTIVITY", "CATEGORY")
        self.suspended_table.add_rows(self.ctrl.get_suspended_activities())

    def counter_text(self) -> str:
        total = len(self.ctrl.get_suspended_activities())
        activities = "activity" if total == 1 else "activities"
        return f"{total} suspended {activities}"

    def selected_text(self, name: str | None = None) -> str:
        if name is None:
            return "Select an activity to restore it."
        return f"Selected: {name}"

    def update_suspended(self) -> None:
        self.suspended_table.clear()
        self.suspended_table.add_rows(self.ctrl.get_suspended_activities())
        self.query_one("#counter", Label).update(self.counter_text())
        self.clear_selection()

    @on(DataTable.RowSelected, "#suspended_table")
    def on_suspended_row_selected(self, event: DataTable.RowSelected) -> None:
        row = event.data_table.get_row(event.row_key)
        self.selected_id = row[0]
        self.query_one("#selected_activity", Label).update(self.selected_text(f"{row[1]} ({row[2]})"))
        self.restore_btn.disabled = False

    @on(Button.Pressed, "#clear_selection")
    def on_clear_selection(self) -> None:
        self.clear_selection()

    @on(Button.Pressed, "#restore_activity")
    def on_restore_activity(self) -> None:
        if self.selected_id is None:
            return

        if not self.ctrl.restore_activity(self.selected_id):
            self.notify("An active activity with that name already exists in its category", severity="error")
            return

        self.notify("Activity restored", severity="information")
        self.update_suspended()
        self.post_message(self.Restored())

    def clear_selection(self) -> None:
        self.selected_id = None
        self.query_one("#selected_activity", Label).update(self.selected_text())
        self.restore_btn.disabled = True
