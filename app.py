from textual.app import App, ComposeResult
from textual.widgets import Static, Header, ListView, Label
from textual.containers import VerticalScroll, Container, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Input
from textual.widgets import ListView
import asyncio

from modules.notes.logic import init_db, load_notes, get_note_by_id
from modules.notes.screens import NotesScreen, NoteViewerScreen
from modules.games.screens import GamesScreen
from modules.companion.screens import CompanionScreen
from modules.core.widgets import MainMenu, BootUp, Typewriter, MenuFinished, BootFinished, FalloutListItem

from modules.terminal.terminal import launch_terminal

class ShutdownScreen(Screen):

    def compose(self):
        yield Header()
        yield MainMenu(id="mainmenu")
        yield Typewriter(id="shutdownmenu")
        yield Typewriter(id="shutdown")

    def on_mount(self):
        msg = self.query_one("#shutdown", Typewriter)

        async def sequence():
            await msg.type_out("VAULT OS shutting down...", delay=0.02)

        self.run_worker(sequence())

class Options(Static):
    #Main Options Menu

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        item_id = event.item.id

        if item_id == "games":
            self.app.games_menu()
        elif item_id == "notes":
            self.app.notes_menu()
        elif item_id == "companion":
            self.app.companion_menu()
        elif item_id == "quit":
            self.app.call_later(self.app.action_quit)

    def compose(self):
        yield Vertical(
            ListView(
                FalloutListItem(Typewriter("", id="companion_tw"), id="companion"),
                FalloutListItem(Typewriter("", id="notes_tw"), id="notes"),
                FalloutListItem(Typewriter("", id="games_tw"), id="games"),
                FalloutListItem(Typewriter("", id="terminal_tw"), id="terminal"),
                FalloutListItem(Typewriter("", id="settings_tw"), id="settings"),
                FalloutListItem(Typewriter("", id="quit_tw"), id="quit"),
                id="main_option_list"
            ),
            Horizontal(
                Label("> ", id="prompt_symbol"),
                Input(id="command_input"),
                id="prompt_line"
            )
        )
    
    async def on_mount(self):
        main_list = self.query_one("#main_option_list", ListView)
        self.call_after_refresh(main_list.focus)

        menu_items = [
            ("companion_tw", "Companion"),
            ("notes_tw", "Notes"),
            ("games_tw", "Games"),
            ("terminal_tw", "Terminal"),
            ("settings_tw", "Settings"),
            ("quit_tw", "Shutdown"),
        ]

        for tw_id, text in menu_items:
            tw = self.query_one(f"#{tw_id}", Typewriter)
            await tw.type_out(text, delay=0.01)
            await asyncio.sleep(0.05)

class VaultOS(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_menu_animated = False


    CSS_PATH = "assets/themes/green.tcss"

    BINDINGS = [
        ("9", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield MainMenu(id="mainmenu")
        yield BootUp(id="bootup")
        yield Container(VerticalScroll(Options()), id="options")
        
    async def on_menu_finished(self, message: MenuFinished): 
        boot = self.query_one("#bootup", BootUp) 
        self.run_worker(boot.run_boot()) 
    async def on_boot_finished(self, message: BootFinished): 
        self.query_one("#options").display = True

    def games_menu(self):
        self.push_screen(GamesScreen())

    def notes_menu(self):
        notes = load_notes()
        self.push_screen(NotesScreen(notes))

    def companion_menu(self):
        self.push_screen(CompanionScreen())

    def open_note(self, note_id):
        title, body = get_note_by_id(note_id)
        self.push_screen(NoteViewerScreen(note_id, title, body))

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
        init_db()
        self.query_one("#options").display = False


if __name__ == "__main__":
    VaultOS().run()
