from collections import Counter
from datetime import date
from itertools import groupby
from typing import override

from textual import on
from textual.app import ComposeResult
from textual.containers import Center, Horizontal, Vertical, VerticalScroll
from textual.widgets import Button, Label, Static, TabbedContent

from void.controllers.note import NoteController


class DayNote(Static):

    DEFAULT_CSS = """
        .day_section_title{
            text-style: bold;
            color: $text-muted;
        }
        .day_card{
            height: auto;
            margin: 0 0 1 0;
            padding: 0 0 0 2;
            border-left: thick $accent;
        }
        .day_card Label{
            width: 100%;
        }
        .day_card_title{
            text-style: bold;
        }
        .day_card_note{
            color: $text-muted;
        }
        .day_card_empty{
            color: $text-muted;
            text-style: italic;
        }
        .day_logged{
            width: 2fr;
        }
        .day_pending{
            width: 1fr;
            padding: 0 0 0 2;
        }
        .day_pending Label{
            width: 100%;
        }
        .pending_category{
            color: $text-muted;
            padding: 1 0 0 3;
        }
        .pending_item{
            color: $text-disabled;
            padding: 0 0 0 2;
            border-left: thick $panel;
        }
        .empty_day{
            height: 1fr;
            align: center middle;
        }
        .empty_card{
            width: 60;
            max-width: 100%;
            height: auto;
            padding: 1 2;
            border: round $panel;
        }
        .empty_card Label{
            width: 100%;
            text-align: center;
        }
        .empty_title{
            text-style: bold;
        }
        .empty_hint{
            color: $text-muted;
            padding: 0 0 1 0;
        }
    """

    @override
    def __init__(self) -> None:
        super().__init__()
        self.ctrl = NoteController()

        self.today = date.today()  # noqa: DTZ011
        self.date_str = self.today.strftime("%B %d, %Y").upper()

    @override
    def compose(self) -> ComposeResult:
        day_note_data = self.ctrl.get_day_note(self.today.isoformat())
        activities = self.ctrl.get_activities()
        per_category = Counter(category for _, _, category in activities)

        logged_ids = {row["activity_id"] for row in day_note_data}
        pending = sorted(
            (category, name)
            for activity_id, name, category in activities
            if activity_id not in logged_ids
        )

        with Vertical(classes="header"):
            yield Label(self.date_str, classes="module_title")
            yield Label(self.counter_text(len(day_note_data), len(activities)), id="counter")

        if not day_note_data:
            with Vertical(classes="empty_day"), Vertical(classes="empty_card"):
                yield Label("NOTHING LOGGED TODAY", classes="empty_title")
                yield Label("Write today's VOID NOTE to fill the void.", classes="empty_hint")
                with Center():
                    yield Button("WRITE VOID NOTE", id="go_to_note", variant="primary", flat=True)
            return

        with Horizontal(classes="main_container"):
            with VerticalScroll(classes="day_logged"):
                for category, group in groupby(day_note_data, key=lambda row: row["category"]):
                    rows = list(group)
                    yield Label(
                        f"── {category.upper()} · {len(rows)} of {per_category[category]} ",
                        classes="day_section_title",
                    )
                    for row in rows:
                        with Vertical(classes="day_card"):
                            yield Label(row["activity"], classes="day_card_title")
                            if row["notes"]:
                                yield Label(row["notes"], classes="day_card_note")
                            else:
                                yield Label("No notes written.", classes="day_card_empty")

            if pending:
                with VerticalScroll(classes="day_pending"):
                    yield Label(f"── NOT LOGGED · {len(pending)} ", classes="day_section_title")
                    for category, group in groupby(pending, key=lambda item: item[0]):
                        yield Label(category.upper(), classes="pending_category")
                        for _, name in group:
                            yield Label(name, classes="pending_item")

    def counter_text(self, logged: int, total: int) -> str:
        activities = "activity" if total == 1 else "activities"
        return f"{logged} of {total} {activities} logged"

    @on(Button.Pressed, "#go_to_note")
    def on_go_to_note(self) -> None:
        self.app.query_one(TabbedContent).active = "void_note"
