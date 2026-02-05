from textual.app import App, ComposeResult
from textual.widgets import Static, Footer, Header, ListView, ListItem, Label
from textual.widget import Widget
from textual.containers import VerticalScroll, Vertical, Container
from textual import events
from textual.screen import Screen

from modules.games import launch_rogue
from modules.terminal import launch_terminal
import time
import asyncio

class MainMenu(Static):
    #Main Menu Widget
    CSS_PATH = "assets/themes/green.tcss"

    MENU_TEXT = """
ROBCO INDUSTRIES UNIFIED OPERATING SYSTEM
COPYRIGHT 2075-2077 ROBCO INDUSTRIES
"""

    def compose(self) -> ComposeResult:
        yield Static(self.MENU_TEXT)

class ScanlineOverlay(Widget):
    def render(self):
        width = self.size.width
        height = self.size.height
        lines = []
        for i in range(height):
            if i % 2 == 0:
                lines.append(" " * width)
            else:
                lines.append(" " * width)
        return "\n".join(lines)


class Options(ListView):
    #Main Menu Widget
    CSS_PATH = "assets/themes/green.tcss"

    def compose(self):
        yield ListItem(Label("Chatbot"))
        yield ListItem(Label("Notes"))
        yield ListItem(Label("Games"))
        yield ListItem(Label("Terminal"))

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
        yield MainMenu()
        yield Container(VerticalScroll(Options()), id="options")
        # yield ScanlineOverlay(id="scanlines")
        # yield Footer()
        
    def action_games(self):
        self.push_screen(GamesScreen())

    def action_terminal(self):
        self.exit()
        launch_terminal()

    async def action_quit(self):
        self.screen.update("VAULT OS shutting down...")
        await asyncio.sleep(2)
        await self.shutdown()

    async def on_mount(self):
        self.query_one(MainMenu).display = False
        await self.run_boot_sequence()
        self.query_one(MainMenu).display = True

    async def run_boot_sequence(self):
        boot = Static("INITIALIZING VAULT-TEC SYSTEMS...", id="boot")
        await self.mount(boot)
        # await asyncio.sleep(1.5)
        boot.update("LOADING KERNEL MODULES...")
        # await asyncio.sleep(1.5)
        boot.update("SYSTEM READY.")
        await asyncio.sleep(1.0)
        await boot.remove()



if __name__ == "__main__":
    VaultOS().run()

