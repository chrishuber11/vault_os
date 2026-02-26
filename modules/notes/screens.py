from textual.widgets import Header, ListView, Input, Label
from textual.containers import VerticalScroll, Container
from textual.screen import Screen
from modules.notes.widgets import NotesOptions, NoteViewerOptions
from modules.core.widgets import MainMenu, Typewriter, FalloutListItem
from modules.notes.logic import update_note, delete_note, load_notes
import asyncio

class NotesScreen(Screen): 
    def __init__(self, notes): 
        super().__init__(id="notes_screen") 
        self.notes = notes
        
    def compose(self): 
        yield Header()
        yield MainMenu(id="mainmenu")
        yield Container(VerticalScroll(NotesOptions(self.notes)), id="options")

    def on_mount(self):
        notes_list = self.query_one("#notes_list", ListView)
        self.call_after_refresh(notes_list.focus)


class NoteViewerScreen(Screen): 
    def __init__(self, note_id, title, body): 
        super().__init__() 
        self.id="note_viewer_screen"
        self.title = title
        self.body = body
        self.note_id = note_id
        self.edit_mode = False

    def compose(self): 
        yield Header()
        yield MainMenu(id="mainmenu")

        yield Typewriter(id="notetitle")
        yield Typewriter(id="notebody")

        body_input = Input(value=self.body, id="edit_body")
        body_input.visible = False
        yield body_input

        yield Container(VerticalScroll(NoteViewerOptions()), id="options")

    def enter_edit_mode(self):
        self.edit_mode = True

        # Hide typewriters
        self.query_one("#notetitle").visible = False
        self.query_one("#notebody").visible = False

        # Show inputs
        body_input = self.query_one("#edit_body", Input)
        body_input.visible = True

        # Focus first input
        self.call_after_refresh(body_input.focus)

    def exit_edit_mode(self):
        self.edit_mode = False

        # Hide inputs
        self.query_one("#edit_body").visible = False

        # Update typewriters with new content
        title_tw = self.query_one("#notetitle", Typewriter)
        body_tw = self.query_one("#notebody", Typewriter)
        body_tw.update(self.query_one("#edit_body").value)

        # Show typewriters
        title_tw.visible = True
        body_tw.visible = True
        note_viewer_list = self.query_one("#note_viewer_list", ListView)
        self.call_after_refresh(note_viewer_list.focus)

    def rename_note(self,text):
        update_note(self.note_id,text,self.body)

    def confirm_delete_note(self):
        delete_note(self.note_id)

    async def on_input_submitted(self, event: Input.Submitted):
        if not self.edit_mode:
            return

        # Save the data
        new_body = self.query_one("#edit_body", Input).value
        update_note(self.note_id, self.title, new_body)

        # Switch back to view mode
        self.exit_edit_mode()

    async def on_mount(self):
        note_viewer_list = self.query_one("#note_viewer_list", ListView)
        self.call_after_refresh(note_viewer_list.focus)
        self.call_after_refresh(lambda: self.run_worker(self.run_typewriter()))

    async def run_typewriter(self):
        title_tw = self.query_one("#notetitle", Typewriter)
        body_tw = self.query_one("#notebody", Typewriter)

        await title_tw.type_out(self.title, delay=0.02)
        await asyncio.sleep(0.3)
        await body_tw.type_out(self.body, delay=0.01)
