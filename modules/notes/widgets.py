from textual.widgets import Static, ListView, Label
from textual.containers import Horizontal, Vertical
from textual.widgets import Input
from textual.widgets import ListView
from modules.notes.logic import create_note
from modules.core.widgets import FalloutListItem

#NEEDS A PROPER REFRESH AFTER ANY DATABASE CHANGES TO OPTIONS MENU

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
            screen = self.screen
            screen.enter_edit_mode()
        elif item_id == "rename":
            self.pending_action = "rename"
            input_box = self.query_one("#command_input")
            input_box.focus()
        elif item_id == "delete":
            self.pending_action = "delete"
            input_box = self.query_one("#command_input")
            input_box.placeholder = 'Type "CONFIRM" to Delete.'
            input_box.focus()
        elif item_id == "home":
            self.app.return_home()

    def on_input_submitted(self, event: Input.Submitted):
        text = event.value

        if self.pending_action == "rename":
            screen = self.screen
            screen.rename_note(text)
            notes_list = self.query_one("#note_viewer_list", ListView)
            notes_list.focus()
        elif self.pending_action == "delete":
            if text == "CONFIRM":
                screen = self.screen
                screen.confirm_delete_note()
            notes_list = self.query_one("#note_viewer_list", ListView)
            notes_list.focus()
            self.app.return_home()

        # clear the mode
        self.pending_action = None
        event.input.value = ""

    def compose(self):
        yield Vertical(
            ListView(
                FalloutListItem(Label("Edit"), id="edit"),
                FalloutListItem(Label("Rename"), id="rename"),
                FalloutListItem(Label("Delete"), id="delete"),
                FalloutListItem(Label("Back to Notes List"), id="home"),
                id="note_viewer_list"
            ),
            Horizontal(
                Label("> ", id="prompt_symbol"),
                Input(id="command_input"),
                id="prompt_line"
            )
        )