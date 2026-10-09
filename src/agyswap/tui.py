"""Interactive dashboard: every account's quota, keyboard-driven switching."""

from __future__ import annotations

import asyncio
from datetime import datetime
from pathlib import Path

from rich.markup import escape
from textual import work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.theme import Theme
from textual.widgets import Footer, Input, Label, ListItem, ListView, Static

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


class Prompt(ModalScreen[str | None]):
    """One line of text; Enter submits (possibly empty), Escape cancels with None."""

    BINDINGS = [Binding("escape", "cancel", "Cancel")]
    DEFAULT_CSS = """
    Prompt { align: center middle; background: #000000 70%; }
    Prompt > Vertical { width: 64; height: auto; border: round $primary; padding: 1 2; background: #000000; }
    Prompt Input { margin-top: 1; }
    Prompt .hint { color: $text-muted; margin-top: 1; }
    """

    def __init__(self, question: str, value: str = "", hint: str = "") -> None:
        super().__init__()
        self.question, self.value, self.hint = question, value, hint

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label(self.question)
            yield Input(self.value)
            yield Label(f"{self.hint}[b]enter[/] ok   [b]esc[/] cancel", classes="hint")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.dismiss(event.value.strip())

    def action_cancel(self) -> None:
        self.dismiss(None)


class More(ModalScreen[str | None]):
    """Keys kept out of the footer; pressing one closes this and runs it."""

    MORE = [
        ("b", "best", "Switch to the account with the most quota left"),
        ("u", "auto", "Switch away only if the active account is at 90% or more"),
        ("e", "export", "Export all accounts, refresh tokens included, to a file"),
        ("i", "import", "Import accounts from an export file"),
    ]
    BINDINGS = [Binding(key, f"pick('{action}')", show=False) for key, action, _ in MORE] + [
        Binding("m,escape", "pick(None)", show=False)
    ]
    DEFAULT_CSS = """
    More { align: center middle; background: #000000 70%; }
    More > Vertical { width: 72; height: auto; border: round $primary; padding: 1 2; background: #000000; }
    More .hint { color: $text-muted; margin-top: 1; }
    """

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label("[b]More shortcuts[/b]")
            for key, _, desc in self.MORE:
                yield Label(f"[b $accent]{key}[/]  {desc}")
            yield Label("[b]esc[/] close", classes="hint")

    def action_pick(self, action: str | None) -> None:
        self.dismiss(action)


def _switch_best() -> str:
    return cli.switch_message(cli.cmd_switch_strategy("best", 90))


def _auto() -> str:
    return cli.auto_message(cli.cmd_auto())


def _export(path: str) -> str:
    # The CLI warns on stderr, which the TUI swallows.
    return cli.cmd_export(path) + ". It holds refresh tokens; keep it private."


def _abspath(path: str) -> str:
    """Absolute path, so the toast says where the file really is."""
    return str(Path(path).expanduser().resolve())


class AgySwapApp(App):
    TITLE = "agyswap - Antigravity CLI Accounts Swap"
    ENABLE_COMMAND_PALETTE = False
    CSS = """
    Screen { background: #000000; }
    #title { width: 1fr; height: 3; padding: 1 2; background: #000000; text-align: center; }
    Footer { background: #141414; padding: 0 2; }
    FooterKey .footer-key--key, FooterKey.-compact .footer-key--key { padding: 0 1; text-style: bold; }
    FooterKey .footer-key--description, FooterKey.-compact .footer-key--description { padding: 0 2 0 1; }
    ListView { height: 1fr; padding: 0 1; background: #000000; display: none; scrollbar-size: 0 0; }
    ListView:focus { background-tint: #000000 0%; }
    ListView > ListItem { height: auto; padding: 1 2; background: #000000; }
    ListView > ListItem.-highlight, ListView:focus > ListItem.-highlight {
        background: $primary;
        color: #ffffff;
    }
    #loading { height: 1fr; content-align: center middle; color: $text-muted; background: #000000; }
    ToastRack { margin-bottom: 3; }
    #status { height: 1; padding: 0 2; color: $text-muted; background: #000000; }
    """
    BINDINGS = [
        Binding("s", "switch", "Switch"),
        Binding("a", "add", "Add"),
        Binding("d", "remove", "Remove"),
        Binding("x", "toggle", "Toggle"),
        Binding("n", "alias", "Alias"),
        Binding("b", "best", show=False),
        Binding("u", "auto", show=False),
        Binding("e", "export", show=False),
        Binding("i", "import", show=False),
        Binding("r", "refresh", "Refresh"),
        Binding("j", "cursor_down", show=False),
        Binding("k", "cursor_up", show=False),
        Binding("q", "quit", "Quit"),
        Binding("m", "more", "More"),
    ]

    def compose(self) -> ComposeResult:
        yield Static("[b $accent]agyswap[/] [dim]- Antigravity CLI Accounts Swap[/]", id="title")
        yield Static("Loading accounts…", id="loading")
        yield ListView()
        yield Static("", id="status")
        yield Footer()

    def on_mount(self) -> None:
        self.register_theme(PITCH_BLACK)
        self.theme = "pitch-black"
        self.rows: list[dict] = []
        self._show_lock = asyncio.Lock()
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
            rows, err = [], escape(e.tui)
        except Exception as e:
            rows, err = [], f"refresh failed: {type(e).__name__}"
        if err is not None:
            self.call_from_thread(self._fail, err)
            return
        self.call_from_thread(self._show, rows)

    def _fail(self, err: str) -> None:
        self.query_one("#loading", Static).update("Could not load accounts.")
        self._status(f"[$error]{err}[/]")

    async def _show(self, rows: list[dict]) -> None:
        # Refreshes can finish together; interleaved clear/extend would duplicate the cards.
        async with self._show_lock:
            lv = self.query_one(ListView)
            self.query_one("#loading").display, lv.display = False, True
            lv.focus()  # hidden until now, so nothing focused it on mount
            keep = (self._selected() or {}).get("email")
            self.rows = rows
            # Await both: until the old items are gone, setting the index highlights a dying item.
            await lv.clear()
            await lv.extend(ListItem(Static(cli.account_text(row))) for row in rows)
            if rows:
                # Keep the cursor on the same account; on first load (or if it is gone) start on the active one.
                emails = [r["email"] for r in rows]
                active = next((i for i, r in enumerate(rows) if r["active"]), 0)
                lv.index = emails.index(keep) if keep in emails else active
                n = len(rows)
                self._status(
                    f"{n} account{'s' if n != 1 else ''}  ·  updated {datetime.now():%H:%M}"
                    f"  ·  refreshes every {REFRESH_SECS // 60} min"
                )
            else:
                await lv.append(
                    ListItem(Static("No accounts yet.\nIn agy: /logout, sign in, exit. Then press [b]a[/b]."))
                )
                self._status("")

    def _status(self, msg: str) -> None:
        self.query_one("#status", Static).update(msg)

    def _selected(self) -> dict | None:
        idx = self.query_one(ListView).index
        return self.rows[idx] if self.rows and idx is not None and idx < len(self.rows) else None

    @work(thread=True, group="action")
    def _run(self, fn, *args) -> None:
        # Off the UI thread: a locked keyring may take up to 30s to answer.
        try:
            msg, err = fn(*args), None
        except cli.SwapError as e:
            msg, err = None, e.tui
        except Exception as e:
            msg, err = None, f"failed: {type(e).__name__}"
        if err is not None:
            self.call_from_thread(self.notify, err, severity="error", timeout=8, markup=False)
            return
        self.call_from_thread(self.notify, msg, markup=False)
        self.call_from_thread(self.action_refresh)

    # --- actions ----------------------------------------------------------
    # Rows can be stale (another terminal may reuse a slot); target accounts by email.

    def action_switch(self) -> None:
        row = self._selected()
        if row:
            self._run(cli.cmd_switch, row["email"], False)

    def on_list_view_selected(self) -> None:
        self.action_switch()

    def action_add(self) -> None:
        self._run(cli.cmd_add, None)

    def action_toggle(self) -> None:
        row = self._selected()
        if row:
            self._run(cli.cmd_enable if row.get("disabled") else cli.cmd_disable, row["email"])

    def action_remove(self) -> None:
        row = self._selected()
        if not row:
            return

        def done(ok: bool | None) -> None:
            if ok:
                self._run(cli.cmd_remove, row["email"])

        self.push_screen(Confirm(f"Remove account {row['slot']}: [b]{escape(row['email'])}[/b]?"), done)

    def action_alias(self) -> None:
        row = self._selected()
        if not row:
            return

        def done(name: str | None) -> None:
            if name is not None:
                self._run(cli.cmd_alias, row["email"], name or None)

        question = f"Alias for account {row['slot']}: [b]{escape(row['email'])}[/b]"
        self.push_screen(Prompt(question, row.get("alias") or "", "empty clears it   "), done)

    def action_more(self) -> None:
        def done(action: str | None) -> None:
            if action:
                getattr(self, f"action_{action}")()

        self.push_screen(More(), done)

    def action_best(self) -> None:
        self._run(_switch_best)

    def action_auto(self) -> None:
        self._run(_auto)

    def action_export(self) -> None:
        def done(path: str | None) -> None:
            if path:
                self._run(_export, _abspath(path))

        # Home, not the cwd: a TUI started inside a git checkout must not drop tokens into it.
        self.push_screen(
            Prompt("Export all accounts [b]with refresh tokens[/b] to file:", "~/agyswap-export.agyswap"), done
        )

    def action_import(self) -> None:
        def done(path: str | None) -> None:
            if path:
                self._run(cli.cmd_import, _abspath(path))

        self.push_screen(Prompt("Import accounts from an export file:"), done)

    def action_cursor_down(self) -> None:
        self.query_one(ListView).action_cursor_down()

    def action_cursor_up(self) -> None:
        self.query_one(ListView).action_cursor_up()
