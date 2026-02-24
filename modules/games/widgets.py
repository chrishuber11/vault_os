from textual.widgets import Static, ListView, Label
from textual.containers import Horizontal, Vertical
from textual.widgets import Input
from textual.widgets import ListView
from modules.games.logic import launch_rogue
from modules.core.widgets import FalloutListItem

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