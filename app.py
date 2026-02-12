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

class ShutdownScreen(Screen):

    MENU_TEXT = """
ROBCO INDUSTRIES UNIFIED OPERATING SYSTEM
COPYRIGHT 2075-2077 ROBCO INDUSTRIES
"""

    def compose(self):
        yield Header()
        yield Static(self.MENU_TEXT, id="shutdownmenu")
        yield Static("VAULT OS shutting down...", id="shutdown")

class MainMenu(Static):
    #Main Menu Widget

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
    #Main Options Menu

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        item_id = event.item.id

        if item_id == "games":
            self.app.games_menu()
        elif item_id == "quit":
            self.app.call_later(self.app.action_quit)

    def compose(self):
        yield FalloutListItem(Label("Chatbot"), id="chatbot")
        yield FalloutListItem(Label("Notes"), id="notes")
        yield FalloutListItem(Label("Games"), id="games")
        yield FalloutListItem(Label("Terminal"), id="terminal")
        yield FalloutListItem(Label("Settings"), id="settings")
        yield FalloutListItem(Label("Shutdown"), id="quit")

class GameOptions(ListView):
    #Game Options Menu

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        item_id = event.item.id

        if item_id == "home":
            self.app.return_home()

    def compose(self):
        yield FalloutListItem(Label("Rogue"), id="rogue")
        yield FalloutListItem(Label("Back to Home"), id="home")

class GamesScreen(Screen): 
    def compose(self): 
        yield Header()
        yield MainMenu(id="mainmenu")
        yield Container(VerticalScroll(GameOptions()), id="options")

    def on_mount(self):
        options = self.query_one(GameOptions)
        self.call_after_refresh(options.focus)

class VaultOS(App):
    CSS_PATH = "assets/themes/green.tcss"

    BINDINGS = [
        ("9", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield MainMenu(id="mainmenu")
        yield Container(VerticalScroll(Options()), id="options")
        
    def games_menu(self):
        self.push_screen(GamesScreen())

    def return_home(self):
        self.pop_screen()

    def action_terminal(self):
        self.exit()
        launch_terminal()

    async def action_quit(self):
        await self.push_screen(ShutdownScreen())
        await asyncio.sleep(2)
        self.exit()

    def on_mount(self):
        options = self.query_one(Options)
        self.call_after_refresh(options.focus)


if __name__ == "__main__":
    VaultOS().run()

