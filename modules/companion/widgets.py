from textual.widgets import Static, ListView, Label
from textual.containers import Horizontal, Vertical
from textual.widgets import Input
from textual.widgets import ListView
from modules.core.widgets import FalloutListItem

class CompanionOptions(Static):
    #Note Options Menu

    def __init__(self,**kwargs): 
        super().__init__(**kwargs) 

    def on_list_view_selected(self, event: ListView.Selected):
        item_id = event.item.id

        if item_id == "home":
            self.app.return_home()

    def compose(self):
        yield Vertical(
            ListView(
                FalloutListItem(Label("Home"), id="home"),
                id="companion_list"
            ),
            Horizontal(
                Label("> ", id="prompt_symbol"),
                Input(id="command_input"),
                id="prompt_line"
            )
        )