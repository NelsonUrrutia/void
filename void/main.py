from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, TabbedContent, TabPane

from void.views.activities import ActivitiesView
from void.views.collection import CollectionView
from void.views.note import NoteView


class VoidApp(App):

    BINDINGS = [
        ("ctrl+1", "show_tab('void_note')", "Note"),
        ("ctrl+2", "show_tab('void_collection')", "Collection"),
        ("ctrl+3", "show_tab('void_activities')", "Activities"),
        ("ctrl+q", "quit", "Quit the app")
    ]

    def compose(self) -> ComposeResult:
        yield Header(icon="🧠")

        with TabbedContent(initial="void_note"):
            with TabPane("VOID NOTE", id="void_note"):
                yield NoteView()

            with TabPane("VOID COLLECTION", id="void_collection"):
                yield CollectionView()

            with TabPane("VOID ACTIVITIES", id="void_activities"):
                yield ActivitiesView()


        yield Footer()

    def on_mount(self) -> None:
        self.title = "VOID"
        self.sub_title = "Vital Offline Information Diary"

def run() -> None:
    VoidApp().run()

if __name__ == "__main__":
    run()
