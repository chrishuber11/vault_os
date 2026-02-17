from textual.app import App, ComposeResult
from textual.widgets import Static, Footer, Header, ListView, ListItem, Label
from textual.widget import Widget
from textual.containers import VerticalScroll, Vertical, Container
from textual import events
from textual.screen import Screen
from rich.text import Text
from textual.message import Message
from modules.notes import init_db, load_notes, get_note_by_id, create_note, update_note, delete_note

from modules.games import launch_rogue
from modules.terminal import launch_terminal
import time
import asyncio
import sqlite3
import os

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


class MainMenu(Static):
    MENU_TEXT = """
ROBCO INDUSTRIES UNIFIED OPERATING SYSTEM
COPYRIGHT 2075-2077 ROBCO INDUSTRIES

Welcome to ROBCO Industries (TM) Termlink
"""

    def compose(self):
        yield Typewriter(id="menu_text")

    def on_mount(self):
        tw = self.query_one("#menu_text", Typewriter)

        async def start():
            # Wait until boot screen is gone
            while self.app.screen_stack and isinstance(self.app.screen_stack[-1], BootUp):
                await asyncio.sleep(0.1)

            if self.app.main_menu_animated:
                tw.update(self.MENU_TEXT)
                return

            await tw.type_out(self.MENU_TEXT, delay=0.025)
            self.app.main_menu_animated = True

        self.run_worker(start())


class BootUp(Screen):
    BOOT_TEXT = """
ROBCO INDUSTRIES UNIFIED OPERATING SYSTEM
COPYRIGHT 2075-2077 ROBCO INDUSTRIES

Welcome to ROBCO Industries (TM) Termlink
INITIALIZING VAULT-TEC SYSTEMS...
LOADING KERNEL MODULES...
CHECKING MEMORY...
SYSTEM READY.
"""

    def compose(self):
        yield Header()
        yield Typewriter(id="bootuptext")

    def on_mount(self):
        tw = self.query_one("#bootuptext", Typewriter)

        async def start():
            await tw.type_out(self.BOOT_TEXT, delay=0.02)
            await asyncio.sleep(1)
            self.app.pop_screen()

        self.run_worker(start())

class Options(ListView):
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
        yield FalloutListItem(Typewriter("", id="chatbot_tw"), id="chatbot")
        yield FalloutListItem(Typewriter("", id="notes_tw"), id="notes")
        yield FalloutListItem(Typewriter("", id="games_tw"), id="games")
        yield FalloutListItem(Typewriter("", id="terminal_tw"), id="terminal")
        yield FalloutListItem(Typewriter("", id="settings_tw"), id="settings")
        yield FalloutListItem(Typewriter("", id="quit_tw"), id="quit")
    
    async def on_mount(self):
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

        self.focus()



class GameOptions(ListView):
    #Game Options Menu

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        item_id = event.item.id

        if item_id == "home":
            self.app.return_home()
        elif item_id == "rogue":
            launch_rogue()

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

class NotesOptions(ListView):
    #Note Options Menu

    def __init__(self, notes, **kwargs): 
        super().__init__(**kwargs) 
        self.notes = notes

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        item_id = event.item.id

        if item_id == "create":
            new_id = create_note("Note 1","Hello, World!")
            self.app.open_note(new_id)
        elif item_id == "home":
            self.app.return_home()
        else:
            #user selected an active note
            self.app.open_note(item_id)

    def compose(self):
        yield FalloutListItem(Label("Create New Note"), id="create")
        for note_id, title in self.notes.items():
            yield FalloutListItem(Label(title), id=note_id)
        yield FalloutListItem(Label("Home"), id="home")

class NotesScreen(Screen): 
    def __init__(self, notes): 
        super().__init__() 
        self.notes = notes

    def compose(self): 
        yield Header()
        yield MainMenu(id="mainmenu")
        yield Container(VerticalScroll(NotesOptions(self.notes)), id="options")

    def on_mount(self):
        options = self.query_one(NotesOptions)
        self.call_after_refresh(options.focus)

class NoteViewerOptions(ListView):
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
        yield FalloutListItem(Label("Edit Note"), id="edit")
        yield FalloutListItem(Label("Delete Note"), id="delete")
        yield FalloutListItem(Label("Home"), id="home")

class NoteViewerScreen(Screen): 
    def __init__(self, title, body): 
        super().__init__() 
        self.title = title
        self.body = body

    def compose(self): 
        yield Header()
        yield MainMenu(id="mainmenu")
        yield Typewriter(self.title)
        yield Typewriter(self.body)
        yield Container(VerticalScroll(NoteViewerOptions()), id="options")

    def on_mount(self):
        options = self.query_one(NoteViewerOptions)
        self.call_after_refresh(options.focus)


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
        yield Container(VerticalScroll(Options()), id="options")
        
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
        self.push_screen(BootUp())
        options = self.query_one(Options)
        self.call_after_refresh(options.focus)


if __name__ == "__main__":
    VaultOS().run()
