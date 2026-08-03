from textual.app import App, ComposeResult
from textual.containers import Grid, Horizontal, Vertical, VerticalScroll
from textual.widgets import Checkbox, Footer, Header, Label, Static, Switch, TabbedContent, TabPane, TextArea


class VoidApp(App):


    CSS = """
        .section_title{
            text-style: bold;
        }

        #void_note_container{
            padding: 1;
            grid-size: 2 1;
            grid-gutter: 1;
        }

        #void_note_activities,
        #void_note_notes{
            padding: 0 1;
        }

        #void_note_notes{
            border-left: white solid;
        }

        #void_note_date{
            height: auto;
            padding-top: 1;
            padding-left: 2;
            text-style: bold
        }

        .activity_group{
            height: auto;
            padding: 1;
            border-bottom: solid white;
        }

        .activity_group_grid{
            grid-size: 2 2;
            height: auto;
        }

        .activity_group Label{
            margin-bottom: 1;
            text-style: bold;
        }

        .activity_group Checkbox{
            width: 100%;
            height: auto;
        }

        .void_note_group{
            margin-top: 1;
            height: auto;
        }
        .void_note_group Label{
            margin-bottom: 1;
            text-style: bold;
        }

        .void_note_group TextArea{
            height: 5;
        }
    """


    BINDINGS = [
        ("ctrl+1", "show_tab('void_note')", "Void Note"),
        ("ctrl+2", "show_tab('void_collection')", "Void Collection"),
        ("ctrl+q", "quit", "Quit the app")
    ]

    def compose(self) -> ComposeResult:
        yield Header(icon="🧠")

        with TabbedContent(initial="void_note"):
            with TabPane("VOID NOTE", id="void_note"):
                with Horizontal(id="void_note_date"):
                    yield Label("DATE: ")
                    yield Label("2026-08-03")
                with Grid(id="void_note_container"):
                    with VerticalScroll(id="void_note_activities"):
                        yield Label("ACTIVITIES", classes="section_title")

                        with Vertical(classes="activity_group"):
                            yield Label("Exercise")
                            with Grid(classes="activity_group_grid"):
                                    yield Checkbox(label="Full Body") 
                                    yield Checkbox(label="Push")
                                    yield Checkbox(label="Pull")
                                    yield Checkbox(label="Leg")

                        with Vertical(classes="activity_group"):
                            yield Label("Exercise")
                            with Grid(classes="activity_group_grid"):
                                yield Checkbox(label="Full Body")
                                yield Checkbox(label="Push")
                                yield Checkbox(label="Pull")
                                yield Checkbox(label="Leg")

                    with VerticalScroll(id="void_note_notes"):
                        yield Label("NOTES", classes="section_title")

                        with Vertical(classes="void_note_group"):
                            yield Label("Excercise | Full Body")
                            yield TextArea()
                        with Vertical(classes="void_note_group"):
                            yield Label("Excercise | Full Body")
                            yield TextArea()



            with TabPane("VOID COLLECTION", id="void_collection"):
                yield Label("VOID COLLECTION")
        yield Footer()

    def on_mount(self) -> None:
        self.title = "VOID"
        self.sub_title = "Vital Offline Information Diary"
        

if __name__ == "__main__":
    app = VoidApp()
    app.run()
