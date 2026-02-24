from textual.app import App, ComposeResult
from textual.widgets import Static, Header, ListView, ListItem, Label
from textual.containers import VerticalScroll, Container, Horizontal, Vertical
from textual.screen import Screen
from rich.text import Text
from textual.message import Message
from textual.widgets import Input
from textual.widgets import ListView
from modules.notes import init_db, load_notes, get_note_by_id, create_note, update_note, delete_note

from modules.games import launch_rogue
from modules.terminal import launch_terminal
import asyncio

class Typewriter(Static):
    async def type_out(self, text: str, delay: float = 0.02):
        buffer = ""
        for char in text:
            buffer += char
            self.update(buffer + "▌")
            await asyncio.sleep(delay)
        self.update(buffer)

class FalloutListItem(ListItem):
    def render(self):
        width = self.region.width

        # Get the first child (Label OR Typewriter)
        child = self.children[0]

        renderable = child.render()

        if isinstance(renderable, Text):
            text = renderable.plain
        else:
            text = str(renderable)

        padded = text.ljust(width)

        is_highlighted = self.parent.highlighted_child is self

        if is_highlighted:
            return Text(padded, style="black on green")
        else:
            return Text(padded, style="green on black")

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


class GameOptions(Static):
    #Game Options Menu

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        item_id = event.item.id

        if item_id == "home":
            self.app.return_home()
        elif item_id == "rogue":
            launch_rogue()

    def compose(self):
        yield Vertical(
            ListView(
                FalloutListItem(Label("Rogue"), id="rogue"),
                FalloutListItem(Label("Back to Home"), id="home"),
                id="game_option_list"
            ),
            Horizontal(
                Label("> ", id="prompt_symbol"),
                Input(id="command_input"),
                id="prompt_line"
            )
        )

class GamesScreen(Screen): 
    def compose(self): 
        yield Header()
        yield MainMenu(id="mainmenu")
        yield Container(VerticalScroll(GameOptions()), id="options")
        # yield InputWidget(id="command_input", placeholder="▌")

    def on_mount(self):
        game_option_list = self.query_one("#game_option_list", ListView)
        self.call_after_refresh(game_option_list.focus)

class NotesOptions(Static):
    #Note Options Menu

    def __init__(self, notes, **kwargs): 
        super().__init__(**kwargs) 
        self.notes = notes
        self.pending_action = None

    def on_list_view_selected(self, event: ListView.Selected):
        item_id = event.item.id

        if item_id == "create":
            self.pending_action = "create_note"
            input_box = self.query_one("#command_input")
            # input_box.placeholder = "Enter note name"
            input_box.focus()
        elif item_id == "home":
            self.app.return_home()
        else:
            #user selected an active note
            self.app.open_note(item_id)

    def on_input_submitted(self, event: Input.Submitted):
        text = event.value

        if self.pending_action == "create_note":
            new_id = create_note(text, "")
            notes_list = self.query_one("#notes_list", ListView)
            notes_list.focus()
            self.app.open_note(new_id)

        # clear the mode
        self.pending_action = None
        event.input.value = ""

    def compose(self):
        yield Vertical(
            ListView(
                FalloutListItem(Label("Create New Note"), id="create"),
                *[
                    FalloutListItem(Label(title), id=note_id)
                    for note_id, title in self.notes.items()
                ],
                FalloutListItem(Label("Home"), id="home"),
                id="notes_list"
            ),
            Horizontal(
                Label("> ", id="prompt_symbol"),
                Input(id="command_input"),
                id="prompt_line"
            )
        )


class NotesScreen(Screen): 
    def __init__(self, notes): 
        super().__init__() 
        self.notes = notes

    def compose(self): 
        yield Header()
        yield MainMenu(id="mainmenu")
        yield Container(VerticalScroll(NotesOptions(self.notes)), id="options")

    def on_mount(self):
        notes_list = self.query_one("#notes_list", ListView)
        self.call_after_refresh(notes_list.focus)

class NoteViewerOptions(Static):
    #Note Viewer Options Menu

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        item_id = event.item.id

        if item_id == "edit":
            self.app.return_home()
        elif item_id == "delete":
            self.app.return_home()
        elif item_id == "home":
            self.app.return_home()

    def compose(self):
        yield Vertical(
            ListView(
                FalloutListItem(Label("Edit Note"), id="edit"),
                FalloutListItem(Label("Delete Note"), id="delete"),
                FalloutListItem(Label("Home"), id="home"),
                id="note_viewer_list"
            ),
            Horizontal(
                Label("> ", id="prompt_symbol"),
                Input(id="command_input"),
                id="prompt_line"
            )
        )

class NoteViewerScreen(Screen): 
    def __init__(self, title, body): 
        super().__init__() 
        self.title = title
        self.body = body

    def compose(self): 
        yield Header()
        yield MainMenu(id="mainmenu")
        yield Typewriter("", id="notetitle")
        yield Typewriter("", id="notebody")
        yield Container(VerticalScroll(NoteViewerOptions()), id="options")

    async def on_mount(self):
        note_viewer_list = self.query_one("#note_viewer_list", ListView)
        self.call_after_refresh(note_viewer_list.focus)
        self.call_after_refresh(self.run_typewriter)

    async def run_typewriter(self):
        title_tw = self.query_one("#notetitle", Typewriter)
        body_tw = self.query_one("#notebody", Typewriter)

        await title_tw.type_out(self.title, delay=0.01)
        # await asyncio.sleep(0.3)
        await body_tw.type_out(self.body, delay=0.005)

class MenuFinished(Message):
    namespace = "menu_finished"

class MainMenu(Static):
    MENU_TEXT = """
ROBCO INDUSTRIES UNIFIED OPERATING SYSTEM
COPYRIGHT 2075-2077 ROBCO INDUSTRIES

Welcome to ROBCO Industries (TM) Termlink"""

    def compose(self):
        yield Typewriter(id="menu_text")

    async def on_mount(self):
        tw = self.query_one("#menu_text", Typewriter)

        async def animate():
            # If it has already animated once, show instantly
            if self.app.main_menu_animated:
                tw.update(self.MENU_TEXT)
                return

            # Otherwise animate it
            await tw.type_out(self.MENU_TEXT, delay=0.025)
            self.app.main_menu_animated = True
            self.app.post_message(MenuFinished())

        self.call_after_refresh(lambda: self.run_worker(animate()))

class BootFinished(Message):
    namespace = "boot_finished"

class BootUp(Static):
    BOOT_TEXT = """
INITIALIZING VAULT-TEC SYSTEMS...
LOADING KERNEL MODULES...
CHECKING MEMORY...
SYSTEM READY."""

    def compose(self):
        yield Typewriter(id="boot_text")

    async def run_boot(self):
        tw = self.query_one("#boot_text", Typewriter)

        async def animate():
            await tw.type_out(self.BOOT_TEXT, delay=0.03)
            await asyncio.sleep(1)
            self.display = False
            self.app.post_message(BootFinished())

        self.call_after_refresh(lambda: self.run_worker(animate()))



class Options(Static):
    #Main Options Menu

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        item_id = event.item.id

        if item_id == "games":
            self.app.games_menu()
        elif item_id == "notes":
            self.app.notes_menu()
        elif item_id == "quit":
            self.app.call_later(self.app.action_quit)

    def compose(self):
        yield Vertical(
            ListView(
                FalloutListItem(Typewriter("", id="chatbot_tw"), id="chatbot"),
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
            ("chatbot_tw", "Chatbot"),
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

    def open_note(self, note_id):
        title, body = get_note_by_id(note_id)
        self.push_screen(NoteViewerScreen(title, body))

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
