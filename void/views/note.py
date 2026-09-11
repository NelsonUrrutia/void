from datetime import date
from typing import override

from textual import on
from textual.app import ComposeResult
from textual.containers import Center, Vertical
from textual.widgets import Button, Label, Static, TabbedContent

from void.controllers.note import NoteController
from void.views.note_form import NoteForm


class NoteView(Static):


   @override
   def __init__(self) -> None:
      super().__init__()
      self.ctrl = NoteController()
      self.today = date.today()  # noqa: DTZ011
      self.date_str = self.today.strftime("%B %d, %Y").upper()


   @override
   def compose(self) -> ComposeResult:
       created_note_of_the_day = self.ctrl.get_day_note(self.today.isoformat())
       if created_note_of_the_day:
           with Vertical(classes="state_screen"), Vertical(classes="state_card state_card_success"):
               yield Label(self.date_str, classes="state_muted")
               yield Label("VOID NOTE SAVED", classes="state_title state_success")
               yield Label(self.hint_text(len(created_note_of_the_day)), classes="state_hint")
               with Center():
                   yield Button("SEE VOID DAY", id="go_to_day_note", variant="success", flat=True)
       else:
           yield NoteForm()

   def hint_text(self, logged: int) -> str:
       activities = "activity" if logged == 1 else "activities"
       return f"{logged} {activities} logged today"

   @on(Button.Pressed, "#go_to_day_note")
   def on_go_to_day_note(self) -> None:
       self.app.query_one(TabbedContent).active = "void_day_note"

   @on(NoteForm.Saved)
   async def on_note_saved(self) -> None:
       await self.recompose()
