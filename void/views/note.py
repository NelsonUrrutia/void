from datetime import date
from typing import override

from textual import on
from textual.app import ComposeResult
from textual.widgets import Label, Static

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
           yield Label("VOID NOTE already saved for today. See the VOID DAY NOTE tab.")
       else:
           yield NoteForm()

   @on(NoteForm.Saved)
   async def on_note_saved(self) -> None:
       await self.recompose()
