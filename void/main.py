from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, TabbedContent, TabPane

from void.views.activity import ActivitiesView
from void.views.collection import CollectionView
from void.views.day_note import DayNote
from void.views.note import NoteView
from void.views.note_form import NoteForm
from void.views.welcome import WelcomeScreen


class VoidApp(App):

    CSS = """
        /* LAYOUT */
        .header{
            dock: top;
            height: auto;
            padding: 1 2 0 2;
            border-bottom: solid $panel;
        }
        .main_container{
            padding: 1 2;
        }
        .card_grid{
            grid-columns: 1fr;
            height: auto;
        }

        /* TITLES */
        .module_title{
            text-style: bold;
        }
        .section_title{
            text-style: bold;
            color: $text-muted;
        }
        #counter{
            color: $text-muted;
        }
        .empty_state{
            color: $text-muted;
            padding: 1 0;
        }

        /* CARDS */
        .note_card{
            height: auto;
            padding: 0 2;
            border: round $primary;
        }
        .note_card Label{
            width: 100%;
        }

        /* LOGGED ACTIVITY ENTRY */
        .entry_card{
            height: auto;
            margin: 0 0 1 0;
            padding: 0 0 0 2;
            border-left: thick $accent;
        }
        .entry_card Label{
            width: 100%;
        }
        .entry_title{
            text-style: bold;
        }
        .entry_note{
            color: $text-muted;
        }
        .entry_empty{
            color: $text-muted;
            text-style: italic;
        }

        /* CENTERED STATE SCREENS */
        .state_screen{
            height: 1fr;
            align: center middle;
        }
        .state_card{
            width: 60;
            max-width: 100%;
            height: auto;
            padding: 1 2;
            border: round $panel;
        }
        .state_card Label{
            width: 100%;
            text-align: center;
        }
        .state_card_success{
            border: round $success;
        }
        .state_title{
            text-style: bold;
        }
        .state_success{
            color: $success;
        }
        .state_muted{
            color: $text-muted;
        }
        .state_hint{
            color: $text-muted;
            padding: 0 0 1 0;
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
        self.push_screen(WelcomeScreen())

def run() -> None:
    VoidApp().run()

if __name__ == "__main__":
    run()
