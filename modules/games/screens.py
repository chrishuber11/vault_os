from textual.widgets import Header, ListView
from textual.containers import VerticalScroll, Container
from textual.screen import Screen
from textual.widgets import ListView
from modules.core.widgets import MainMenu
from modules.games.widgets import GameOptions

class GamesScreen(Screen): 
    def compose(self): 
        yield Header()
        yield MainMenu(id="mainmenu")
        yield Container(VerticalScroll(GameOptions()), id="options")
        # yield InputWidget(id="command_input", placeholder="▌")

    def on_mount(self):
        game_option_list = self.query_one("#game_option_list", ListView)
        self.call_after_refresh(game_option_list.focus)