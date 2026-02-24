from textual.widgets import Static, ListView, Label
from textual.containers import Horizontal, Vertical
from textual.widgets import Input
from textual.widgets import ListView
from modules.notes.logic import init_db, load_notes, get_note_by_id, create_note, update_note, delete_note
from modules.core.widgets import FalloutListItem

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