from textual.app import App, ComposeResult
from textual.widgets import Static, Footer, Header, ListView, ListItem, Label
from textual.widget import Widget
from textual.containers import VerticalScroll, Vertical, Container
from textual import events
from textual.screen import Screen
from rich.text import Text
from textual.message import Message

from modules.games import launch_rogue
from modules.terminal import launch_terminal
import time
import asyncio

class FalloutListItem(ListItem):
    def render(self):
        # Width of THIS item, not the ListView
        width = self.region.width

        label = self.query_one(Label)
        renderable = label.render()

        if isinstance(renderable, Text):
            text = renderable.plain
        else:
            text = str(renderable)

        # Pad text to full width
        padded = text.ljust(width)

        is_highlighted = self.parent.highlighted_child is self

        if is_highlighted:
            return Text(padded, style="black on green")
        else:
            return Text(padded, style="green on black")



class Status(Static):
    pass

# class BootFinished(Message):
#     pass

class MainMenu(Static):
    #Main Menu Widget
    # CSS_PATH = "assets/themes/green.tcss"

    MENU_TEXT = """
ROBCO INDUSTRIES UNIFIED OPERATING SYSTEM
COPYRIGHT 2075-2077 ROBCO INDUSTRIES
"""

    def compose(self) -> ComposeResult:
        yield Static(self.MENU_TEXT)

#     LINES = [
#         "INITIALIZING VAULT-TEC SYSTEMS...",
#         "LOADING KERNEL MODULES...",
#         "CHECKING MEMORY...",
#         "SYSTEM READY."
#     ]

class Options(ListView):
    #Main Menu Widget
    # CSS_PATH = "assets/themes/green.tcss"

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        item_id = event.item.id

        if item_id == "games":
            self.app.action_games()
        elif item_id == "terminal":
            self.app.action_terminal()

    def compose(self):
        yield FalloutListItem(Label("Chatbot"), id="chatbot")
        yield FalloutListItem(Label("Notes"), id="notes")
        yield FalloutListItem(Label("Games"), id="games")
        yield FalloutListItem(Label("Terminal"), id="terminal")


class GamesScreen(Screen): 
    def compose(self): 
        yield Static("Games coming soon...")

class VaultOS(App):
    CSS_PATH = "assets/themes/green.tcss"

    BINDINGS = [
        ("9", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        # yield BootSeq(id="bootseq")
        yield MainMenu(id="mainmenu")
        yield Container(VerticalScroll(Options()), id="options")
        yield Status(id="status")
        
    def action_games(self):
        self.push_screen(GamesScreen())

    def action_terminal(self):
        self.exit()
        launch_terminal()

    async def action_quit(self):
        status = self.query_one("#status", Static)
        status.update("VAULT OS shutting down...")
        await asyncio.sleep(2)
        self.exit()

    # async def run_boot_sequence(self):
    #     options = self.query_one(Options)
    #     options.focus()

    def on_mount(self):
        options = self.query_one(Options)
        self.call_after_refresh(options.focus)




if __name__ == "__main__":
    VaultOS().run()

