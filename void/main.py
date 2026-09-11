from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, TabbedContent, TabPane

from void.views.activity import ActivitiesView
from void.views.collection import CollectionView
from void.views.day_note import DayNote
from void.views.note import NoteView
from void.views.note_form import NoteForm


class VoidApp(App):

    CSS = """
        .header{
            dock: top;
            height: auto;
            padding: 1 2 0 2;
            border-bottom: solid $panel;
        }
        .main_container{
            padding: 1 2;
        }
        .module_title{
            text-style: bold;
        }
        #counter{
            color: $text-muted;
        }
        .empty_state{
            color: $text-muted;
            padding: 1 0;
        }
        .note_card{
            height: auto;
            padding: 0 2;
            border: round $primary;
        }
        .note_card Label{
            width: 100%;
        }
    """

    def compose(self) -> ComposeResult:
        yield Header(icon="🧠")

        with TabbedContent(initial="void_note"):

            with TabPane("VOID NOTE", id="void_note"):
                yield NoteView()

            with TabPane("VOID DAY", id="void_day_note"):
                yield DayNote()

            with TabPane("VOID COLLECTION", id="void_collection"):
                yield CollectionView()

            with TabPane("VOID ACTIVITIES", id="void_activities"):
                yield ActivitiesView()


        yield Footer()

    @on(NoteForm.Saved)
    async def on_note_saved(self) -> None:
        await self.query_one(DayNote).recompose()
        await self.query_one(CollectionView).recompose()
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
