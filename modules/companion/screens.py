from textual.widgets import Header, ListView, Input, Label
from textual.containers import VerticalScroll, Container
from textual.screen import Screen
from modules.companion.widgets import CompanionOptions
from modules.core.widgets import MainMenu, load_ascii, Typewriter, FalloutListItem
import asyncio

class CompanionScreen(Screen): 
    def __init__(self): 
        super().__init__(id="companion_screen") 
        
    def compose(self): 
        yield Header()
        yield MainMenu(id="mainmenu")
        yield Typewriter(id="ascii_art")
        yield Container(VerticalScroll(CompanionOptions()), id="options")

    async def on_mount(self):
        companion_ascii = load_ascii("cooper_human")
        tw = self.query_one("#ascii_art", Typewriter)
        self.call_after_refresh(lambda: self.run_worker(tw.type_out(companion_ascii, delay=0.002)))
        companion_list = self.query_one("#companion_list", ListView)
        self.call_after_refresh(companion_list.focus)