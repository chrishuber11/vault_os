from textual.widgets import Header, ListView
from textual.containers import VerticalScroll, Container
from textual.screen import Screen
from textual.widgets import ListView
from modules.notes.widgets import NotesOptions, NoteViewerOptions
from modules.core.widgets import MainMenu, Typewriter

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
