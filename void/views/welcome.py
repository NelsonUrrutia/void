from typing import override

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.events import Key
from textual.screen import Screen
from textual.widgets import Label, Rule

LOGO = """\
 █████   █████    ███████    █████ ██████████  
░░███   ░░███   ███░░░░░███ ░░███ ░░███░░░░███ 
 ░███    ░███  ███     ░░███ ░███  ░███   ░░███
 ░███    ░███ ░███      ░███ ░███  ░███    ░███
 ░░███   ███  ░███      ░███ ░███  ░███    ░███
  ░░░█████░   ░░███     ███  ░███  ░███    ███ 
    ░░███      ░░░███████░   █████ ██████████  
     ░░░         ░░░░░░░    ░░░░░ ░░░░░░░░░░\
"""


AUTO_DISMISS = 1.75


class WelcomeScreen(Screen[None]):

    DEFAULT_CSS = """
    .welcome_card{
        width: 59;
        max-width: 100%;
        height: auto;
        padding: 2 4;
        border: round $primary;
    }
    .welcome_card Label{
        width: 100%;
        text-align: center;
    }
    .welcome_logo{
        color: $primary;
        text-style: bold;
    }
    .welcome_card Rule{
        color: $primary;
    }
    .welcome_tagline{
        padding: 0 0 1 0;
        color: $text-muted;
    }
    .welcome_hint{
        color: $accent;
        text-style: italic;
    }
    """

    @override
    def compose(self) -> ComposeResult:
        with Vertical(classes="state_screen"), Vertical(classes="welcome_card"):
            yield Label(LOGO, classes="welcome_logo")
            yield Rule(line_style="heavy")
            yield Label("VITAL OFFLINE INFORMATION DIARY", classes="welcome_tagline")
            yield Label("press any key to skip", classes="welcome_hint")

    def on_mount(self) -> None:
        self.set_timer(AUTO_DISMISS, self.close)

    def on_key(self, _: Key) -> None:
        self.close()

    def close(self) -> None:
        # returns None on purpose: awaiting dismiss() from a handler is an error
        if self.app.screen is self:
            self.dismiss()
