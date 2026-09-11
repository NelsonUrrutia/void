from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, TabbedContent, TabPane

from void.views.activity import ActivitiesView
from void.views.collection import CollectionView
from void.views.day_note import DayNote
from void.views.note import NoteView
from void.views.note_form import NoteForm


class VoidApp(App):

    def compose(self) -> ComposeResult:
        yield Header(icon="🧠")

        with TabbedContent(initial="void_note"):

            with TabPane("VOID NOTE", id="void_note"):
                yield NoteView()

            with TabPane("VOID DAY NOTE", id="void_day_note"):
                yield DayNote()

            with TabPane("VOID COLLECTION", id="void_collection"):
                yield CollectionView()

            with TabPane("VOID ACTIVITIES", id="void_activities"):
                yield ActivitiesView()


        yield Footer()

    @on(NoteForm.Saved)
    async def on_note_saved(self) -> None:
        await self.query_one(DayNote).recompose()
        self.query_one(TabbedContent).active = "void_day_note"

    @on(ActivitiesView.Changed)
    async def on_activities_changed(self) -> None:
        await self.query_one(NoteView).recompose()

    def on_mount(self) -> None:
        self.title = "VOID"
        self.sub_title = "Vital Offline Information Diary"

def run() -> None:
    VoidApp().run()

if __name__ == "__main__":
    run()
