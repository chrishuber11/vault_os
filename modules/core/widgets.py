from textual.widgets import Static, ListItem
from rich.text import Text
from textual.message import Message
import asyncio

class MenuFinished(Message):
    namespace = "menu_finished"

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
            await tw.type_out(self.MENU_TEXT, delay=0.03)
            self.app.main_menu_animated = True
            self.app.post_message(MenuFinished())

        self.call_after_refresh(lambda: self.run_worker(animate()))

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