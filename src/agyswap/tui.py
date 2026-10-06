"""Interactive dashboard: every account's quota, keyboard-driven switching."""

from __future__ import annotations

from datetime import datetime

from rich.markup import escape
from textual import work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.theme import Theme
from textual.widgets import Footer, Label, ListItem, ListView, Static

from agyswap import cli

REFRESH_SECS = 120

PITCH_BLACK = Theme(
    name="pitch-black",
    primary="#0178d4",
    secondary="#8a8a8a",
    accent="#ffa62b",
    foreground="#e5e5e5",
    background="#000000",
    surface="#000000",
    panel="#0a0a0a",
    success="#22c55e",
    warning="#eab308",
    error="#ef4444",
    dark=True,
    variables={
        "block-cursor-foreground": "#e5e5e5",
        "block-cursor-background": "#000000",
        "block-cursor-text-style": "none",
        "block-cursor-blurred-foreground": "#e5e5e5",
        "block-cursor-blurred-background": "#000000",
        "block-cursor-blurred-text-style": "none",
        "block-hover-background": "#000000",
        "footer-background": "#141414",
        "footer-item-background": "#141414",
        "footer-key-background": "#ffa62b",
        "footer-key-foreground": "#000000",
        "footer-description-foreground": "#d4d4d4",
        "scrollbar": "#262626",
        "scrollbar-background": "#000000",
    },
)


class Confirm(ModalScreen[bool]):
    BINDINGS = [Binding("y", "answer(True)", "Yes"), Binding("n,escape", "answer(False)", "No")]
    DEFAULT_CSS = """
    Confirm { align: center middle; background: #000000 70%; }
    Confirm > Vertical { width: 64; height: auto; border: round $error; padding: 1 2; background: #000000; }
    Confirm .hint { color: $text-muted; margin-top: 1; }
    """

    def __init__(self, question: str) -> None:
        super().__init__()
        self.question = question

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label(self.question)
            yield Label("[b $error]y[/] remove   [b]n[/] cancel", classes="hint")

    def action_answer(self, value: bool) -> None:
        self.dismiss(value)


class AgySwapApp(App):
    TITLE = "agyswap - Antigravity CLI Accounts Swap"
    ENABLE_COMMAND_PALETTE = False
    CSS = """
    Screen { background: #000000; }
    #title { width: 1fr; height: 3; padding: 1 2; background: #000000; text-align: center; }
    Footer { background: #141414; padding: 0 2; }
    FooterKey .footer-key--key, FooterKey.-compact .footer-key--key { padding: 0 1; text-style: bold; }
    FooterKey .footer-key--description, FooterKey.-compact .footer-key--description { padding: 0 2 0 1; }
    ListView { height: 1fr; padding: 0 1; background: #000000; }
    ListView:focus { background-tint: #000000 0%; }
    ListView > ListItem { height: auto; padding: 1 2; background: #000000; }
    ListView > ListItem.-highlight, ListView:focus > ListItem.-highlight {
        background: $primary;
        color: #ffffff;
    }
    #status { height: 1; padding: 0 2; color: $text-muted; background: #000000; }
    """
    BINDINGS = [
        Binding("s", "switch", "Switch"),
        Binding("a", "add", "Add current"),
        Binding("d", "remove", "Remove"),
        Binding("r", "refresh", "Refresh"),
        Binding("j", "cursor_down", show=False),
        Binding("k", "cursor_up", show=False),
        Binding("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Static("[b $accent]agyswap[/] [dim]- Antigravity CLI Accounts Swap[/]", id="title")
        yield ListView()
        yield Static("Loading…", id="status")
        yield Footer()

    def on_mount(self) -> None:
        self.register_theme(PITCH_BLACK)
        self.theme = "pitch-black"
        self.rows: list[dict] = []
        self.action_refresh()
        self.set_interval(REFRESH_SECS, self.action_refresh)

    # --- data -------------------------------------------------------------

    @work(thread=True, exclusive=True)
    def action_refresh(self) -> None:
        self.call_from_thread(self._status, "[dim]⟳ refreshing usage…[/]")
        # Textual's crash report prints locals, and these hold tokens; show the type only. The UI
        # calls stay outside the except blocks so a failing call never chains the original error.
        try:
            rows, err = cli.collect_usage(), None
        except cli.SwapError as e:
            rows, err = [], escape(str(e))
        except Exception as e:
            rows, err = [], f"refresh failed: {type(e).__name__}"
        if err is not None:
            self.call_from_thread(self._status, f"[$error]{err}[/]")
            return
        self.call_from_thread(self._show, rows)

    def _show(self, rows: list[dict]) -> None:
        lv = self.query_one(ListView)
        keep = lv.index or 0
        self.rows = rows
        lv.clear()
        for row in rows:
            lv.append(ListItem(Static(cli.account_text(row))))
        if rows:
            lv.index = min(keep, len(rows) - 1)
            n = len(rows)
            self._status(
                f"{n} account{'s' if n != 1 else ''}  ·  updated {datetime.now():%H:%M}"
                f"  ·  refreshes every {REFRESH_SECS // 60} min"
            )
        else:
            lv.append(ListItem(Static("No accounts yet.\nIn agy: /logout, sign in, exit. Then press [b]a[/b].")))
            self._status("")

    def _status(self, msg: str) -> None:
        self.query_one("#status", Static).update(msg)

    def _selected(self) -> dict | None:
        idx = self.query_one(ListView).index
        return self.rows[idx] if self.rows and idx is not None and idx < len(self.rows) else None

    def _run(self, fn, *args) -> bool:
        try:
            msg, err = fn(*args), None
        except cli.SwapError as e:
            msg, err = None, str(e)
        except Exception as e:
            msg, err = None, f"failed: {type(e).__name__}"
        if err is not None:
            self.notify(err, severity="error", timeout=8)
            return False
        self.notify(msg)
        return True

    # --- actions ----------------------------------------------------------

    def action_switch(self) -> None:
        row = self._selected()
        if row and self._run(cli.cmd_switch, row["slot"], False):
            self.action_refresh()

    def on_list_view_selected(self) -> None:
        self.action_switch()

    def action_add(self) -> None:
        if self._run(cli.cmd_add, None):
            self.action_refresh()

    def action_remove(self) -> None:
        row = self._selected()
        if not row:
            return

        def done(ok: bool | None) -> None:
            if ok and self._run(cli.cmd_remove, row["slot"]):
                self.action_refresh()

        self.push_screen(Confirm(f"Remove account {row['slot']}: [b]{row['email']}[/b]?"), done)

    def action_cursor_down(self) -> None:
        self.query_one(ListView).action_cursor_down()

    def action_cursor_up(self) -> None:
        self.query_one(ListView).action_cursor_up()
