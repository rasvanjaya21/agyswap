"""Round-trip with a fake keyring: add two accounts, switch, refreshed token survives."""

import base64
import json

from agyswap import cli


def make_token(email, refresh):
    claims = base64.urlsafe_b64encode(json.dumps({"email": email}).encode()).decode().rstrip("=")
    return json.dumps({"token": {"refresh_token": refresh}, "id_token": f"h.{claims}.s"})


def refresh_of(token):
    return json.loads(token)["token"]["refresh_token"]


def test_existing_store_dir_is_tightened_and_must_be_ours(tmp_path, monkeypatch):
    import os

    import pytest

    home = tmp_path / "home"
    home.mkdir(mode=0o755)
    home.chmod(0o755)
    monkeypatch.setenv("AGYSWAP_HOME", str(home))
    cli.save_store({"accounts": {}})
    assert home.stat().st_mode & 0o777 == 0o700
    home.chmod(0o750)  # group access alone is enough to tighten
    with cli.locked_store():
        pass
    assert home.stat().st_mode & 0o777 == 0o700
    monkeypatch.setattr(os, "getuid", lambda: home.stat().st_uid + 1)
    with pytest.raises(cli.SwapError, match="not owned by you"):
        cli.save_store({"accounts": {}})


def setup(tmp_path, monkeypatch, running=False):
    keyring = {}
    monkeypatch.setenv("AGYSWAP_HOME", str(tmp_path))
    monkeypatch.setattr(cli, "read_token", lambda: keyring.get("t"))
    monkeypatch.setattr(cli, "write_token", lambda t: keyring.__setitem__("t", t))
    monkeypatch.setattr(cli, "agy_running", lambda: running)
    return keyring


def test_switch_roundtrip(tmp_path, monkeypatch):
    kr = setup(tmp_path, monkeypatch)
    assert cli.main(["add"]) == 1  # not signed in

    kr["t"] = make_token("a@x.com", "r-a")
    assert cli.main(["add"]) == 0
    kr["t"] = make_token("b@x.com", "r-b")
    assert cli.main(["add"]) == 0

    kr["t"] = make_token("b@x.com", "r-b2")  # agy refreshed b's token
    assert cli.main(["switch"]) == 0  # rotate b -> a
    assert refresh_of(kr["t"]) == "r-a"
    assert cli.main(["switch", "B@x.com"]) == 0
    assert refresh_of(kr["t"]) == "r-b2"

    assert cli.main(["switch", "nope"]) == 1
    assert cli.main(["remove", "1", "--yes"]) == 0  # pytest has no TTY: scripts must pass --yes
    assert list(cli.load_store()["accounts"]) == ["2"]
    assert (cli.store_path().stat().st_mode & 0o777) == 0o600


def test_switch_refuses_while_running(tmp_path, monkeypatch):
    kr = setup(tmp_path, monkeypatch, running=True)
    kr["t"] = make_token("a@x.com", "r-a")
    cli.main(["add"])
    assert cli.main(["switch", "1"]) == 1


def test_email_of_garbage():
    assert cli.email_of(None) is None
    assert cli.email_of("not json") is None


def test_fetch_pools_reads_5h_and_weekly_windows(monkeypatch):
    from agyswap import usage

    # Shape of retrieveUserQuotaSummary as observed (architecture/OBSERVE.md).
    summary = {
        "groups": [
            {
                "displayName": "Gemini Models",
                "buckets": [
                    {
                        "bucketId": "gemini-weekly",
                        "window": "weekly",
                        "remainingFraction": 0.56,
                        "resetTime": "2026-10-07T11:50:41Z",
                        "description": "You have used some of your weekly limit",
                    },
                    {
                        "bucketId": "gemini-5h",
                        "window": "5h",
                        "remainingFraction": 1,
                        "resetTime": "2026-10-06T16:07:42Z",
                    },
                ],
            },
            {
                "displayName": "Claude and GPT models",
                "buckets": [
                    {
                        "bucketId": "3p-weekly",
                        "window": "weekly",
                        "remainingFraction": 0.42,
                        "resetTime": "2026-10-11T06:25:12Z",
                    },
                    {"bucketId": "3p-5h", "window": "5h", "resetTime": "2026-10-06T16:14:56Z"},
                ],
            },
        ]
    }
    calls = []

    def fake_post(url, data, headers=None):
        calls.append(url)
        return summary

    monkeypatch.setattr(usage, "_post", fake_post)
    pools = usage.fetch_pools(json.dumps({"token": {"access_token": "x"}}))
    assert calls == ["https://daily-cloudcode-pa.googleapis.com/v1internal:retrieveUserQuotaSummary"]
    assert [(p.group, p.window, round(p.used, 2)) for p in pools] == [
        ("Gemini", "5h", 0),
        ("Gemini", "weekly", 0.44),
        ("Claude/GPT", "5h", 1.0),  # missing remainingFraction counts as exhausted
        ("Claude/GPT", "weekly", 0.58),
    ]
    assert pools[0].reset is None  # full bucket: its reset keeps sliding, so it is not shown
    assert pools[1].reset.isoformat() == "2026-10-07T11:50:41+00:00"


def test_fetch_pools_maps_http_errors(monkeypatch):
    import urllib.error

    import pytest

    from agyswap import usage

    def boom(*a, **k):
        raise urllib.error.HTTPError("u", 403, "forbidden", None, None)

    monkeypatch.setattr(usage, "_post", boom)
    with pytest.raises(usage.UsageError, match="HTTP 403"):
        usage.fetch_pools(json.dumps({"token": {"access_token": "x"}}))


def test_switch_saves_unstored_live_login_first(tmp_path, monkeypatch):
    kr = setup(tmp_path, monkeypatch)
    kr["t"] = make_token("a@x.com", "r-a")
    cli.main(["add"])
    kr["t"] = make_token("c@x.com", "r-c")  # signed in, never added
    assert cli.main(["switch"]) == 0
    accounts = cli.load_store()["accounts"]
    assert accounts["2"]["email"] == "c@x.com" and refresh_of(accounts["2"]["token"]) == "r-c"
    assert refresh_of(kr["t"]) == "r-a"


def test_add_slot_never_overwrites_other_account(tmp_path, monkeypatch):
    kr = setup(tmp_path, monkeypatch)
    kr["t"] = make_token("a@x.com", "r-a")
    cli.main(["add"])
    kr["t"] = make_token("b@x.com", "r-b")
    assert cli.main(["add", "--slot", "1"]) == 1
    assert cli.load_store()["accounts"]["1"]["email"] == "a@x.com"
    assert cli.main(["add"]) == 0
    assert cli.main(["add", "--slot", "5"]) == 0  # moves b from 2 to 5
    assert sorted(cli.load_store()["accounts"]) == ["1", "5"]


def test_usage_refresh_does_not_undo_concurrent_remove(tmp_path, monkeypatch):
    kr = setup(tmp_path, monkeypatch)
    for email in ("a@x.com", "b@x.com"):
        kr["t"] = make_token(email, "r-" + email)
        cli.main(["add"])

    def slow_usage(token):
        if cli.email_of(token) == "a@x.com":
            cli.cmd_remove("2")  # user removes b while the fetch is in flight
        tok = json.loads(token)
        tok["token"]["expiry"] = "2099-01-01T00:00:00+00:00"
        return [], json.dumps(tok)

    monkeypatch.setattr(cli, "account_usage", slow_usage)
    import concurrent.futures

    monkeypatch.setattr(cli, "ThreadPoolExecutor", lambda **k: concurrent.futures.ThreadPoolExecutor(max_workers=1))
    cli.collect_usage()
    accounts = cli.load_store()["accounts"]
    assert list(accounts) == ["1"]
    assert "2099" in json.loads(accounts["1"]["token"])["token"]["expiry"]  # refreshed token merged


def test_account_text_groups_5h_and_weekly():
    from datetime import UTC, datetime, timedelta

    from agyswap.usage import Pool

    now = datetime.now(UTC)
    row = {
        "slot": "1",
        "email": "a@x.com",
        "active": True,
        "error": None,
        "pools": [
            Pool("Gemini", "5h", 0.0, None),
            Pool("Gemini", "weekly", 0.44, now + timedelta(days=1, hours=2, minutes=30)),
            Pool("Claude/GPT", "5h", 0.91, now + timedelta(hours=1, minutes=5, seconds=30)),
            Pool("Claude/GPT", "weekly", 0.58, now + timedelta(days=4, hours=19, minutes=30)),
        ],
    }
    lines = [line.rstrip() for line in cli.account_text(row).plain.splitlines()]
    assert lines[0] == " 1  a@x.com  ● active"
    assert lines[1].split() == ["Gemini", "5h", "━" * cli.BAR, "0%"]  # full bucket: no countdown
    assert lines[2].split()[:1] == ["weekly"] and lines[2].endswith("44%  resets 1d 2h")
    assert lines[3].split()[:2] == ["Claude/GPT", "5h"] and lines[3].endswith("91%  resets 1h 5m")
    assert lines[4].endswith("58%  resets 4d 19h")
    # group name only on its first row, and the window column lines up across groups
    assert lines[2].index("weekly") == lines[1].index("5h") == lines[3].index("5h")


def test_account_text_full_bucket_row_has_no_trailing_space():
    from agyswap.usage import Pool

    row = {"slot": "1", "email": "a@x.com", "active": False, "error": None, "pools": [Pool("Gemini", "5h", 0.0, None)]}
    line = cli.account_text(row).plain.splitlines()[1]
    assert not line.endswith(" ")


def test_account_text_widens_group_column_for_long_names():
    from agyswap.usage import Pool

    long_name = "Some Very Long Group"  # 20 characters, longer than the default column
    row = {
        "slot": "1",
        "email": "a@x.com",
        "active": False,
        "error": None,
        "pools": [
            Pool(long_name, "5h", 0.1, None),
            Pool(long_name, "weekly", 0.2, None),
            Pool("Gemini", "5h", 0.3, None),
        ],
    }
    lines = cli.account_text(row).plain.splitlines()[1:]
    assert long_name + "  " in lines[0]  # never glued to the window column
    assert lines[0].index("5h") == lines[1].index("weekly") == lines[2].index("5h")


def _tty(monkeypatch, is_tty):
    monkeypatch.setattr(cli.sys.stdin, "isatty", lambda: is_tty)


def test_remove_asks_and_cancels_on_no(tmp_path, monkeypatch, capsys):
    kr = setup(tmp_path, monkeypatch)
    kr["t"] = make_token("a@x.com", "r-a")
    cli.main(["add"])
    _tty(monkeypatch, True)
    prompts = []
    monkeypatch.setattr("builtins.input", lambda q: prompts.append(q) or "n")
    assert cli.main(["remove", "1"]) == 0
    assert "Cancelled" in capsys.readouterr().out
    assert prompts == ["Remove account 1 (a@x.com)? [y/N] "]
    assert list(cli.load_store()["accounts"]) == ["1"]


def test_remove_warns_for_active_account_and_removes_on_yes(tmp_path, monkeypatch, capsys):
    kr = setup(tmp_path, monkeypatch)
    kr["t"] = make_token("a@x.com", "r-a")
    cli.main(["add"])
    _tty(monkeypatch, True)
    monkeypatch.setattr("builtins.input", lambda q: "y")
    assert cli.main(["remove", "1"]) == 0
    out = capsys.readouterr()
    assert "currently active" in out.err
    assert cli.load_store()["accounts"] == {}


def test_remove_without_tty_needs_yes(tmp_path, monkeypatch):
    kr = setup(tmp_path, monkeypatch)
    kr["t"] = make_token("a@x.com", "r-a")
    cli.main(["add"])
    _tty(monkeypatch, False)
    monkeypatch.setattr("builtins.input", lambda q: (_ for _ in ()).throw(AssertionError("must not prompt")))
    assert cli.main(["remove", "1"]) == 1
    assert list(cli.load_store()["accounts"]) == ["1"]
    assert cli.main(["remove", "1", "--yes"]) == 0
    assert cli.load_store()["accounts"] == {}


def test_bare_agyswap_without_tty_exits_2(monkeypatch, capsys):
    import pytest

    _tty(monkeypatch, False)
    with pytest.raises(SystemExit) as exc:
        cli.main([])
    assert exc.value.code == 2
    assert "no command given" in capsys.readouterr().err


def test_ignore_running_overrides_running_agy_but_force_does_not(tmp_path, monkeypatch):
    kr = setup(tmp_path, monkeypatch, running=True)
    for email in ("a@x.com", "b@x.com"):
        kr["t"] = make_token(email, "r-" + email)
        cli.main(["add"])
    assert cli.main(["switch", "1"]) == 1
    assert cli.main(["switch", "1", "--force"]) == 1
    assert cli.main(["switch", "1", "--ignore-running"]) == 0
    assert cli.email_of(kr["t"]) == "a@x.com"


def test_force_skips_syncing_the_live_token(tmp_path, monkeypatch):
    kr = setup(tmp_path, monkeypatch)
    for email, refresh in (("a@x.com", "r-a"), ("b@x.com", "r-b")):
        kr["t"] = make_token(email, refresh)
        cli.main(["add"])
    kr["t"] = make_token("b@x.com", "r-b2")  # agy refreshed b; the live copy is newer
    assert cli.main(["switch", "1", "--force"]) == 0
    accounts = cli.load_store()["accounts"]
    assert refresh_of(accounts["2"]["token"]) == "r-b"  # not synced
    assert sorted(accounts) == ["1", "2"]  # and not saved again as a duplicate slot


def test_force_still_saves_an_unstored_login(tmp_path, monkeypatch):
    kr = setup(tmp_path, monkeypatch)
    kr["t"] = make_token("a@x.com", "r-a")
    cli.main(["add"])
    kr["t"] = make_token("c@x.com", "r-c")  # live login never added
    assert cli.main(["switch", "1", "--force"]) == 0
    accounts = cli.load_store()["accounts"]
    assert accounts["2"]["email"] == "c@x.com" and refresh_of(accounts["2"]["token"]) == "r-c"


def test_remove_enter_defaults_to_no(tmp_path, monkeypatch, capsys):
    kr = setup(tmp_path, monkeypatch)
    kr["t"] = make_token("a@x.com", "r-a")
    cli.main(["add"])
    _tty(monkeypatch, True)
    monkeypatch.setattr("builtins.input", lambda q: "")
    assert cli.main(["remove", "1"]) == 0
    assert "Cancelled" in capsys.readouterr().out
    assert list(cli.load_store()["accounts"]) == ["1"]


def test_remove_ctrl_d_or_ctrl_c_cancels(tmp_path, monkeypatch, capsys):
    kr = setup(tmp_path, monkeypatch)
    kr["t"] = make_token("a@x.com", "r-a")
    cli.main(["add"])
    _tty(monkeypatch, True)
    for exc in (EOFError, KeyboardInterrupt):

        def raise_(q, exc=exc):
            raise exc

        monkeypatch.setattr("builtins.input", raise_)
        assert cli.main(["remove", "1"]) == 0
        assert "Cancelled" in capsys.readouterr().out
    assert list(cli.load_store()["accounts"]) == ["1"]


def test_dropped_connection_becomes_a_row_error(tmp_path, monkeypatch):
    import http.client

    from agyswap import usage

    kr = setup(tmp_path, monkeypatch)
    kr["t"] = make_token("a@x.com", "r-a")
    cli.cmd_add()
    monkeypatch.setattr(usage, "_agy_client_secrets", lambda: ("S",))
    for exc in (
        TimeoutError("read timed out"),
        ConnectionResetError(),
        http.client.RemoteDisconnected(),
        http.client.IncompleteRead(b""),
    ):

        def boom(*a, exc=exc, **k):
            raise exc

        monkeypatch.setattr(usage._opener, "open", boom)
        [row] = cli.collect_usage()
        assert row["error"] == f"network error: {type(exc).__name__}"


def _run_tui(monkeypatch, collect):
    import asyncio

    from agyswap import tui

    monkeypatch.setattr(cli, "collect_usage", collect)

    async def go():
        app = tui.AgySwapApp()
        async with app.run_test() as pilot:
            for _ in range(2):  # the second refresh re-adds the empty-state item
                await app.workers.wait_for_complete()
                await pilot.pause()
                app.action_refresh()
            await app.workers.wait_for_complete()
            await pilot.pause()
            return app.is_running, str(app.query_one("#status").render())

    return asyncio.run(go())


def test_tui_survives_refresh_on_empty_store(monkeypatch):
    running, _ = _run_tui(monkeypatch, lambda: [])
    assert running


def test_tui_row_keys_do_nothing_on_an_empty_store(monkeypatch):
    import asyncio

    import pytest

    from agyswap import tui

    monkeypatch.setattr(cli, "collect_usage", lambda: [])
    for name in ("cmd_switch", "cmd_remove", "cmd_disable", "cmd_enable", "cmd_alias"):
        monkeypatch.setattr(cli, name, lambda *a: pytest.fail("no row to act on"))

    async def go():
        app = tui.AgySwapApp()
        async with app.run_test() as pilot:
            await app.workers.wait_for_complete()
            for key in ("s", "enter", "d", "x", "n"):
                await pilot.press(key)
            await app.workers.wait_for_complete()
            await pilot.pause()
            return app.is_running, type(app.screen).__name__

    assert asyncio.run(go()) == (True, "Screen")  # no crash, no modal


def test_tui_shows_refresh_error_instead_of_exiting(monkeypatch):
    def fail():
        raise cli.SwapError("secret-tool not found, run `agyswap list`", tui="secret-tool not found, press [b]r[/b]")

    running, status = _run_tui(monkeypatch, fail)
    assert running
    assert "secret-tool not found, press [b]r[/b]" in status  # the TUI wording, shown verbatim


def test_tui_first_load_failure_replaces_the_loading_text(monkeypatch):
    import asyncio

    from agyswap import tui

    def fail():
        raise cli.SwapError("boom")

    monkeypatch.setattr(cli, "collect_usage", fail)

    async def go():
        app = tui.AgySwapApp()
        async with app.run_test() as pilot:
            await app.workers.wait_for_complete()
            await pilot.pause()
            return str(app.query_one("#loading").render()), app.query_one(tui.ListView).display

    assert asyncio.run(go()) == ("Could not load accounts.", False)


def test_post_keeps_http_errors_for_callers(monkeypatch):
    import urllib.error
    import urllib.request

    import pytest

    from agyswap import usage

    def boom(*a, **k):
        raise urllib.error.HTTPError("u", 403, "forbidden", None, None)

    monkeypatch.setattr(usage._opener, "open", boom)
    with pytest.raises(usage.UsageError, match="HTTP 403"):
        usage.fetch_pools(json.dumps({"token": {"access_token": "x"}}))


def test_tui_unexpected_refresh_error_shows_only_its_type(monkeypatch):
    def fail():
        raise ValueError("doc with r-secret")

    running, status = _run_tui(monkeypatch, fail)
    assert running
    assert "ValueError" in status
    assert "r-secret" not in status


def test_secret_tool_timeout_is_a_swap_error(monkeypatch):
    import subprocess

    import pytest

    def slow(*a, **k):
        raise subprocess.TimeoutExpired("secret-tool", 30)

    monkeypatch.setattr(cli.subprocess, "run", slow)
    with pytest.raises(cli.SwapError, match="keyring did not answer"):
        cli.read_token()


def test_tui_action_error_does_not_close_the_app(tmp_path, monkeypatch):
    import asyncio

    from agyswap import tui

    setup(tmp_path, monkeypatch)
    row = {"slot": "1", "email": "a@x.com", "active": False, "pools": [], "error": None}
    monkeypatch.setattr(cli, "collect_usage", lambda: [row])

    def boom(*a):
        raise OSError("r-secret")

    monkeypatch.setattr(cli, "cmd_switch", boom)

    async def go():
        app = tui.AgySwapApp()
        async with app.run_test() as pilot:
            await app.workers.wait_for_complete()
            await pilot.pause()
            await pilot.press("s")
            await app.workers.wait_for_complete()
            await pilot.pause()
            return app.is_running, [n.message for n in app._notifications]

    running, notes = asyncio.run(go())
    assert running
    assert any("OSError" in n for n in notes)
    assert not any("r-secret" in n for n in notes)


def test_unexpected_usage_error_stays_on_its_row(tmp_path, monkeypatch):
    kr = setup(tmp_path, monkeypatch)
    kr["t"] = make_token("a@x.com", "r-a")
    cli.cmd_add()

    def odd(token):
        raise TypeError("r-secret")

    monkeypatch.setattr(cli, "account_usage", odd)
    [row] = cli.collect_usage()
    assert row["error"] == "unexpected error: TypeError"


def _expiring(token, expiry):
    tok = json.loads(token)
    tok["token"]["expiry"] = expiry
    return json.dumps(tok)


def test_list_exits_1_when_every_account_fails(tmp_path, monkeypatch):
    kr = setup(tmp_path, monkeypatch)
    kr["t"] = make_token("a@x.com", "r-a")
    cli.cmd_add()

    def fail(token):
        raise cli.UsageError("HTTP 500")

    monkeypatch.setattr(cli, "account_usage", fail)
    assert cli.main(["list"]) == 1
    monkeypatch.setattr(cli, "account_usage", lambda t: ([], t))
    assert cli.main(["list"]) == 0


def test_corrupt_store_is_a_swap_error(tmp_path, monkeypatch, capsys):
    setup(tmp_path, monkeypatch)
    cli.store_path().write_text("{not json")
    assert cli.main(["status"]) == 0  # signed out: never reads the store
    assert cli.main(["list"]) == 1
    assert "not valid JSON" in capsys.readouterr().err


def test_keyring_read_failure_is_not_signed_out(monkeypatch):
    import subprocess

    import pytest

    monkeypatch.setattr(
        cli.subprocess, "run", lambda *a, **k: subprocess.CompletedProcess(a, 1, "", "Cannot autolaunch D-Bus")
    )
    with pytest.raises(cli.SwapError, match="D-Bus"):
        cli.read_token()
    monkeypatch.setattr(cli.subprocess, "run", lambda *a, **k: subprocess.CompletedProcess(a, 1, "", ""))
    assert cli.read_token() is None  # missing item: exit 1, silent


def test_save_store_leaves_no_temp_file(tmp_path, monkeypatch):
    setup(tmp_path, monkeypatch)
    cli.save_store({"accounts": {}})
    assert sorted(p.name for p in tmp_path.iterdir()) == ["accounts.json"]
    assert (cli.store_path().stat().st_mode & 0o777) == 0o600


def test_locked_store_is_exclusive(tmp_path, monkeypatch):
    import threading

    setup(tmp_path, monkeypatch)
    order = []

    def other():
        with cli.locked_store():
            order.append("other")

    with cli.locked_store():
        t = threading.Thread(target=other)
        t.start()
        t.join(0.2)
        order.append("first")
    t.join()
    assert order == ["first", "other"]


def test_add_slot_zero_is_rejected(tmp_path, monkeypatch):
    kr = setup(tmp_path, monkeypatch)
    kr["t"] = make_token("a@x.com", "r-a")
    assert cli.main(["add", "--slot", "0"]) == 1
    assert cli.load_store()["accounts"] == {}


def test_usage_uses_live_token_for_active_account(tmp_path, monkeypatch):
    kr = setup(tmp_path, monkeypatch)
    kr["t"] = make_token("a@x.com", "r-a")
    cli.cmd_add()
    kr["t"] = make_token("a@x.com", "r-live")  # agy refreshed it after add
    seen = []
    monkeypatch.setattr(cli, "account_usage", lambda t: (seen.append(refresh_of(t)), ([], t))[1])
    [row] = cli.collect_usage()
    assert row["active"] and seen == ["r-live"]


def test_usage_merge_skips_older_or_foreign_tokens(tmp_path, monkeypatch):
    kr = setup(tmp_path, monkeypatch)
    for email in ("a@x.com", "b@x.com"):
        kr["t"] = _expiring(make_token(email, "r-" + email), "2090-01-01T00:00:00+00:00")
        cli.cmd_add()
    kr["t"] = None
    returned = {
        "a@x.com": _expiring(make_token("a@x.com", "old"), "2080-01-01T00:00:00+00:00"),  # older
        "b@x.com": _expiring(make_token("z@x.com", "foreign"), "2099-01-01T00:00:00+00:00"),  # other account
    }
    monkeypatch.setattr(cli, "account_usage", lambda t: ([], returned[cli.email_of(t)]))
    mtime = cli.store_path().stat().st_mtime_ns
    cli.collect_usage()
    accounts = cli.load_store()["accounts"]
    assert [refresh_of(a["token"]) for a in accounts.values()] == ["r-a@x.com", "r-b@x.com"]
    assert cli.store_path().stat().st_mtime_ns == mtime  # nothing changed: no rewrite


def test_usage_catches_malformed_token_errors(tmp_path, monkeypatch):
    kr = setup(tmp_path, monkeypatch)
    kr["t"] = make_token("a@x.com", "r-a")
    cli.cmd_add()
    for exc in (KeyError("token"), ValueError("bad")):

        def boom(t, exc=exc):
            raise exc

        monkeypatch.setattr(cli, "account_usage", boom)
        [row] = cli.collect_usage()
        assert row["error"] and not row["error"].startswith("unexpected")


def test_invalid_grant_says_token_revoked(monkeypatch):
    import io
    import urllib.error

    import pytest

    from agyswap import usage

    monkeypatch.setattr(usage, "_agy_client_secrets", lambda: ("S",))

    def boom(*a, **k):
        raise urllib.error.HTTPError("u", 400, "bad", None, io.BytesIO(b'{"error": "invalid_grant"}'))

    monkeypatch.setattr(usage, "_post", boom)
    with pytest.raises(usage.UsageError, match="token revoked"):
        usage.fresh_token(make_token("a@x.com", "r-a"))


def test_quota_429_is_named(monkeypatch):
    import urllib.error

    import pytest

    from agyswap import usage

    def boom(*a, **k):
        raise urllib.error.HTTPError("u", 429, "slow down", None, None)

    monkeypatch.setattr(usage, "_post", boom)
    with pytest.raises(usage.UsageError, match="rate limited"):
        usage.fetch_pools(json.dumps({"token": {"access_token": "x"}}))


def test_requests_never_follow_redirects():
    import urllib.request

    from agyswap import usage

    req = urllib.request.Request("https://a.example/", headers={"Authorization": "Bearer x"})
    handler = next(h for h in usage._opener.handlers if isinstance(h, urllib.request.HTTPRedirectHandler))
    assert handler.redirect_request(req, None, 302, "Found", {}, "https://b.example/") is None


def test_tui_targets_accounts_by_email_and_escapes_markup(tmp_path, monkeypatch):
    import asyncio

    from agyswap import tui

    setup(tmp_path, monkeypatch)
    row = {"slot": "1", "email": "a@x.com", "active": False, "pools": [], "error": None}
    monkeypatch.setattr(cli, "collect_usage", lambda: [row])
    calls = []

    def fake_switch(target, force):
        calls.append(target)
        raise cli.SwapError("Run `agyswap list` [bold unclosed", tui="Failed to write keyring: [bold unclosed")

    monkeypatch.setattr(cli, "cmd_switch", fake_switch)

    async def go():
        app = tui.AgySwapApp()
        async with app.run_test() as pilot:
            await app.workers.wait_for_complete()
            await pilot.pause()
            await pilot.press("s")
            await app.workers.wait_for_complete()
            await pilot.pause()
            return app.is_running, [(n.message, n.markup) for n in app._notifications]

    running, notes = asyncio.run(go())
    assert running and calls == ["a@x.com"]
    assert ("Failed to write keyring: [bold unclosed", False) in notes  # shown verbatim, never parsed


def test_tui_cursor_starts_on_active_and_stays_visible_on_its_email(monkeypatch):
    import asyncio

    from agyswap import tui

    rows = [{"slot": str(i), "email": f"{i}@x.com", "active": i == 2, "pools": [], "error": None} for i in (1, 2, 3)]
    monkeypatch.setattr(cli, "collect_usage", lambda: list(rows))

    async def go():
        app = tui.AgySwapApp()
        async with app.run_test() as pilot:

            async def refresh():
                await app.workers.wait_for_complete()
                await pilot.pause()
                lv = app.query_one(tui.ListView)
                return app._selected()["email"], [c.highlighted for c in lv.children]

            seen = [await refresh()]
            await pilot.press("j")
            rows.reverse()  # another terminal reordered the slots
            app.action_refresh()
            seen.append(await refresh())
            rows.pop(0)  # and removed the highlighted account
            app.action_refresh()
            seen.append(await refresh())
            return seen

    assert asyncio.run(go()) == [
        ("2@x.com", [False, True, False]),
        ("3@x.com", [True, False, False]),
        ("2@x.com", [True, False]),  # gone: back to the active account
    ]


def test_tui_alias_best_auto_export_import_reach_their_commands(monkeypatch):
    import asyncio
    from pathlib import Path

    from agyswap import tui

    row = {"slot": "1", "email": "[b]a@x.com", "alias": "old", "active": True, "pools": [], "error": None}
    monkeypatch.setattr(cli, "collect_usage", lambda: [row])
    calls = []
    monkeypatch.setattr(cli, "cmd_alias", lambda t, n: calls.append(("alias", t, n)) or "ok")
    monkeypatch.setattr(tui, "_switch_best", lambda: calls.append(("best",)) or "ok")
    monkeypatch.setattr(tui, "_auto", lambda: calls.append(("auto",)) or "ok")
    monkeypatch.setattr(cli, "cmd_export", lambda path: calls.append(("export", path)) or "ok")
    monkeypatch.setattr(cli, "cmd_import", lambda path: calls.append(("import", path)) or "ok")
    monkeypatch.setenv("HOME", "/home/u")

    async def go():
        app = tui.AgySwapApp()
        async with app.run_test() as pilot:

            async def keys(*ks):
                for k in ks:
                    await pilot.press(k)
                await app.workers.wait_for_complete()
                await pilot.pause()

            await keys()
            await keys("n")
            prompt = (app.screen.query_one(tui.Input).value, str(app.screen.query_one(tui.Label).render()))
            await keys("ctrl+u", *"  work  ", "enter")  # rename, trimmed
            await keys("n", "ctrl+u", *"   ", "enter")  # blank clears
            await keys("n", "escape")  # cancel does nothing
            await keys("b", "u")
            for close in ("escape", "m"):
                await keys("m", close)  # closing More runs nothing
                assert not isinstance(app.screen, tui.More)
            await keys("m", "b", "m", "u")  # More forwards its keys
            opened = []
            for key in ("e", "i"):  # ...and opens the right prompts
                await keys("m", key)
                opened.append(str(app.screen.query_one(tui.Label).render()))
                await keys("escape")
            await keys("e", "enter")  # default name
            await keys("e", "ctrl+u", *"~/x.json", "enter")
            await keys("e", "ctrl+u", "enter", "i", "enter")  # an empty path runs nothing
            await keys("i", *"y.json", "enter")
            await keys("i", *"~/z.json", "enter")
            return prompt, opened, sorted(k for k, b in app.active_bindings.items() if b.binding.show)

    prompt, opened, footer = asyncio.run(go())
    assert [q.split()[0] for q in opened] == ["Export", "Import"]
    assert prompt == ("old", "Alias for account 1: [b]a@x.com")  # prefilled; the email shown verbatim
    assert footer == ["a", "d", "m", "n", "q", "r", "s", "x"]  # b/u/e/i live behind More
    assert calls == [
        ("alias", "[b]a@x.com", "work"),
        ("alias", "[b]a@x.com", None),
        ("best",),
        ("auto",),
        ("best",),
        ("auto",),
        ("export", "/home/u/agyswap-export.agyswap"),
        ("export", "/home/u/x.json"),
        ("import", str(Path("y.json").resolve())),
        ("import", "/home/u/z.json"),
    ]


def test_tui_best_and_auto_use_the_cli_defaults_and_messages(monkeypatch):
    from agyswap import tui

    r = {"switched": True, "saved_slot": None, "slot": "2", "email": "b@x.com", "max_used": 0.95}
    seen = []
    monkeypatch.setattr(cli, "cmd_switch_strategy", lambda strategy, threshold: seen.append((strategy, threshold)) or r)
    monkeypatch.setattr(cli, "cmd_auto", lambda: seen.append("auto") or r)
    assert tui._switch_best() == "Switched to account 2: b@x.com"
    assert tui._auto() == "Switched to account 2: b@x.com (max 95% used)"
    monkeypatch.setattr(cli, "cmd_export", lambda path: f"Exported 2 accounts to {path}")
    assert tui._export("/x") == "Exported 2 accounts to /x. It holds refresh tokens; keep it private."
    assert seen == [("best", 90), "auto"]


def test_tui_overlapping_refreshes_never_duplicate_cards(monkeypatch):
    import asyncio

    from agyswap import tui

    rows = [{"slot": str(i), "email": f"{i}@x.com", "active": i == 1, "pools": [], "error": None} for i in (1, 2, 3)]
    monkeypatch.setattr(cli, "collect_usage", lambda: rows)

    async def go():
        app = tui.AgySwapApp()
        async with app.run_test() as pilot:
            await app.workers.wait_for_complete()
            await asyncio.gather(app._show(rows), app._show(rows))  # two refreshes finishing together
            await pilot.pause()
            return len(app.query_one(tui.ListView).children)

    assert asyncio.run(go()) == 3


def test_tui_shows_loading_in_the_middle_until_the_first_refresh(monkeypatch):
    import asyncio
    import threading

    from agyswap import tui

    gate = threading.Event()
    row = {"slot": "1", "email": "a@x.com", "active": True, "pools": [], "error": None}
    monkeypatch.setattr(cli, "collect_usage", lambda: gate.wait(5) and [row])

    async def go():
        app = tui.AgySwapApp()
        async with app.run_test() as pilot:
            await pilot.pause()
            loading, lv = app.query_one("#loading"), app.query_one(tui.ListView)
            before = (str(loading.render()), loading.display, lv.display)
            gate.set()
            await app.workers.wait_for_complete()
            await pilot.pause()
            return before, (loading.display, lv.display, app.focused is lv)

    assert asyncio.run(go()) == (("Loading accounts…", True, False), (False, True, True))


def _add(kr, *emails):
    for email in emails:
        kr["t"] = make_token(email, "r-" + email)
        cli.cmd_add()


def test_alias_set_clear_and_target(tmp_path, monkeypatch):
    kr = setup(tmp_path, monkeypatch)
    _add(kr, "a@x.com", "b@x.com")
    assert cli.main(["alias", "1", "Work"]) == 0
    assert cli.load_store()["accounts"]["1"]["alias"] == "Work"
    assert cli.main(["switch", "work"]) == 0
    assert cli.email_of(kr["t"]) == "a@x.com"
    for bad in ("WORK", "42", "me@home"):
        assert cli.main(["alias", "2", bad]) == 1
    assert cli.main(["alias", "1"]) == 0
    assert "alias" not in cli.load_store()["accounts"]["1"]
    assert cli.main(["alias", "2", "work"]) == 0  # free again
    assert cli.main(["remove", "work", "--yes"]) == 0
    assert list(cli.load_store()["accounts"]) == ["1"]


def test_account_text_shows_alias():
    row = {"slot": "1", "email": "a@x.com", "alias": "work", "active": False, "pools": [], "error": None}
    assert cli.account_text(row).plain.splitlines()[0] == " 1  a@x.com (work)"


def test_errors_give_cli_and_tui_their_own_instructions(tmp_path, monkeypatch):
    import pytest

    kr = setup(tmp_path, monkeypatch)
    _add(kr, "a@x.com", "b@x.com")
    cli.cmd_disable("1")
    with pytest.raises(cli.SwapError) as e:
        cli.switch_account("1")
    assert str(e.value) == "Account 1 is disabled (manual). Run `agyswap enable 1` first."
    assert e.value.tui == "Account 1 is disabled (manual). Press x on it first."
    monkeypatch.setattr(cli, "agy_running", lambda: True)
    for call in (lambda: cli.switch_account("2"), lambda: cli.cmd_switch_strategy("best", 90), cli.cmd_auto):
        with pytest.raises(cli.SwapError) as e:
            call()
        assert "--ignore-running" in str(e.value) and "--" not in e.value.tui


def test_every_cli_instruction_reachable_from_the_tui_has_a_tui_wording():
    import ast
    import inspect

    cli_only = {
        "--slot must be 1 or higher.",
        "Refusing to remove without confirmation. Pass --yes to remove from a script.",
    }

    def text(node):
        if isinstance(node, ast.Constant):
            return str(node.value)
        if isinstance(node, ast.JoinedStr):
            return "".join(text(v) if isinstance(v, ast.Constant) else "{}" for v in node.values)
        if isinstance(node, ast.Name):
            return str(getattr(cli, node.id))
        return ""

    for call in ast.walk(ast.parse(inspect.getsource(cli))):
        if not (isinstance(call, ast.Call) and getattr(call.func, "id", None) == "SwapError" and call.args):
            continue
        msg = text(call.args[0])
        tui = next((text(k.value) for k in call.keywords if k.arg == "tui"), None)
        if msg in cli_only:
            continue
        if "`agyswap " in msg or " --" in msg or "(--" in msg:
            assert tui is not None, msg
        if tui is not None:
            assert "`agyswap" not in tui and "--" not in tui, tui


def test_rotation_skips_disabled_accounts(tmp_path, monkeypatch):
    kr = setup(tmp_path, monkeypatch)
    _add(kr, "a@x.com", "b@x.com", "c@x.com")  # c is live
    assert cli.main(["disable", "a@x.com"]) == 0
    assert cli.load_store()["accounts"]["1"]["disabled_reason"] == "manual"
    assert cli.main(["switch"]) == 0  # c -> (skip a) -> b
    assert cli.email_of(kr["t"]) == "b@x.com"
    assert cli.main(["switch", "1"]) == 1  # explicit switch to a disabled account
    assert cli.email_of(kr["t"]) == "b@x.com"
    assert cli.main(["disable", "3"]) == 0
    assert cli.main(["switch"]) == 1  # nothing else enabled
    assert cli.email_of(kr["t"]) == "b@x.com"
    assert cli.main(["enable", "1"]) == 0
    assert "disabled" not in cli.load_store()["accounts"]["1"]
    assert cli.main(["switch"]) == 0
    assert cli.email_of(kr["t"]) == "a@x.com"


def test_usage_skips_disabled_accounts(tmp_path, monkeypatch):
    kr = setup(tmp_path, monkeypatch)
    _add(kr, "a@x.com", "b@x.com")
    cli.cmd_disable("1")
    fetched = []
    monkeypatch.setattr(cli, "account_usage", lambda t: (fetched.append(cli.email_of(t)), ([], t))[1])
    rows = cli.collect_usage()
    assert fetched == ["b@x.com"]
    assert rows[0]["disabled"] and rows[0]["disabled_reason"] == "manual"
    text = cli.account_text(rows[0]).plain
    assert "disabled: manual" in text and "━" not in text


def test_tui_x_toggles_disable_by_email(tmp_path, monkeypatch):
    import asyncio

    from agyswap import tui

    setup(tmp_path, monkeypatch)
    rows = [
        {"slot": "1", "email": "a@x.com", "active": False, "disabled": False, "pools": [], "error": None},
        {"slot": "2", "email": "b@x.com", "active": False, "disabled": True, "pools": [], "error": None},
    ]
    monkeypatch.setattr(cli, "collect_usage", lambda: rows)
    calls = []
    monkeypatch.setattr(cli, "cmd_disable", lambda t: calls.append(("disable", t)) or "ok")
    monkeypatch.setattr(cli, "cmd_enable", lambda t: calls.append(("enable", t)) or "ok")

    async def go():
        app = tui.AgySwapApp()
        async with app.run_test() as pilot:
            for key in ("x", "j", "x"):
                await app.workers.wait_for_complete()
                await pilot.pause()
                await pilot.press(key)
            await app.workers.wait_for_complete()
            await pilot.pause()

    asyncio.run(go())
    assert calls == [("disable", "a@x.com"), ("enable", "b@x.com")]


def _revoked_post(*a, **k):
    import io
    import urllib.error

    raise urllib.error.HTTPError("u", 400, "bad", None, io.BytesIO(b'{"error": "invalid_grant"}'))


def test_revoked_token_quarantines_account(tmp_path, monkeypatch):
    from agyswap import usage

    kr = setup(tmp_path, monkeypatch)
    _add(kr, "a@x.com")
    kr["t"] = None
    monkeypatch.setattr(usage, "_agy_client_secrets", lambda: ("S",))
    monkeypatch.setattr(usage, "_post", _revoked_post)
    [row] = cli.collect_usage()
    assert "token revoked" in row["error"]
    acc = cli.load_store()["accounts"]["1"]
    assert acc["disabled"] and acc["disabled_reason"] == "token revoked"


def test_quarantine_skips_token_replaced_during_fetch(tmp_path, monkeypatch):
    from agyswap import usage

    kr = setup(tmp_path, monkeypatch)
    _add(kr, "a@x.com")

    def revoked_then_readd(token):
        kr["t"] = make_token("a@x.com", "r-new")
        cli.cmd_add()  # user signs in again while the fetch runs
        raise usage.TokenRevoked("token revoked")

    kr["t"] = None
    monkeypatch.setattr(cli, "account_usage", revoked_then_readd)
    cli.collect_usage()
    acc = cli.load_store()["accounts"]["1"]
    assert "disabled" not in acc and refresh_of(acc["token"]) == "r-new"


def test_add_clears_revoked_mark_but_keeps_alias_and_manual(tmp_path, monkeypatch):
    kr = setup(tmp_path, monkeypatch)
    _add(kr, "a@x.com", "b@x.com")
    cli.cmd_alias("1", "work")
    cli.cmd_disable("1", reason="token revoked")
    cli.cmd_disable("2")
    _add(kr, "a@x.com", "b@x.com")
    accounts = cli.load_store()["accounts"]
    assert accounts["1"]["alias"] == "work" and "disabled" not in accounts["1"]
    assert accounts["2"]["disabled_reason"] == "manual"


def _pools(used):
    from agyswap.usage import Pool

    return [Pool("Gemini", "5h", used, None), Pool("Gemini", "weekly", used, None)]


def test_usage_cache_fills_failed_fetch(tmp_path, monkeypatch):
    kr = setup(tmp_path, monkeypatch)
    _add(kr, "a@x.com", "b@x.com")
    monkeypatch.setattr(cli, "account_usage", lambda t: (_pools(0.4), t))
    cli.collect_usage()
    path = tmp_path / "usage.json"
    assert (path.stat().st_mode & 0o777) == 0o600
    assert "r-a@x.com" not in path.read_text() and "id_token" not in path.read_text()

    def fail(t):
        raise cli.UsageError("network error: TimeoutError")

    monkeypatch.setattr(cli, "account_usage", fail)
    rows = cli.collect_usage()
    assert [p.used for p in rows[0]["pools"]] == [0.4, 0.4]
    assert rows[0]["stale"] is not None and rows[0]["error"].startswith("network error")
    assert "stale, " in cli.account_text(rows[0]).plain

    cli.cmd_remove("2")
    monkeypatch.setattr(cli, "account_usage", lambda t: (_pools(0.5), t))
    [row] = cli.collect_usage()
    assert row["stale"] is None
    assert list(json.loads(path.read_text())) == ["a@x.com"]  # removed accounts are pruned


def test_corrupt_usage_cache_is_ignored(tmp_path, monkeypatch):
    kr = setup(tmp_path, monkeypatch)
    _add(kr, "a@x.com")
    (tmp_path / "usage.json").write_text("{nope")
    monkeypatch.setattr(cli, "account_usage", lambda t: (_pools(0.1), t))
    [row] = cli.collect_usage()
    assert row["error"] is None


def test_rate_limited_reads_retry_after(monkeypatch):
    import email.utils
    import time
    import urllib.error
    from email.message import Message

    import pytest

    from agyswap import usage

    for header, expected in (("120", 120), (None, 300), ("soon", 300)):
        headers = Message()
        if header:
            headers["Retry-After"] = header

        def boom(*a, headers=headers, **k):
            raise urllib.error.HTTPError("u", 429, "slow", headers, None)

        monkeypatch.setattr(usage, "_post", boom)
        with pytest.raises(usage.RateLimited) as exc:
            usage.fetch_pools(json.dumps({"token": {"access_token": "x"}}))
        assert exc.value.retry_after == expected
    headers = Message()
    headers["Retry-After"] = email.utils.formatdate(time.time() + 600, usegmt=True)
    monkeypatch.setattr(
        usage, "_post", lambda *a, **k: (_ for _ in ()).throw(urllib.error.HTTPError("u", 429, "", headers, None))
    )
    with pytest.raises(usage.RateLimited) as exc:
        usage.fetch_pools(json.dumps({"token": {"access_token": "x"}}))
    assert 590 <= exc.value.retry_after <= 600


def test_rate_limited_account_is_not_fetched_until_retry_at(tmp_path, monkeypatch):
    from datetime import UTC, datetime, timedelta

    from agyswap import usage

    kr = setup(tmp_path, monkeypatch)
    _add(kr, "a@x.com")
    monkeypatch.setattr(cli, "account_usage", lambda t: (_pools(0.3), t))
    cli.collect_usage()
    calls = []

    def limited(t):
        calls.append(1)
        raise usage.RateLimited("rate limited (HTTP 429), try again later", 600)

    monkeypatch.setattr(cli, "account_usage", limited)
    cli.collect_usage()
    [row] = cli.collect_usage()  # inside the backoff window: no request
    assert calls == [1]
    assert row["error"].startswith("rate limited, retry in") and row["pools"]
    cache = json.loads((tmp_path / "usage.json").read_text())
    cache["a@x.com"]["retry_at"] = (datetime.now(UTC) - timedelta(seconds=1)).isoformat()
    (tmp_path / "usage.json").write_text(json.dumps(cache))
    cli.collect_usage()
    assert calls == [1, 1]


def _row(slot, used, active=False, disabled=False, error=None, stale=None):
    return {
        "slot": slot,
        "email": f"{slot}@x.com",
        "active": active,
        "disabled": disabled,
        "error": error,
        "stale": stale,
        "pools": _pools(used) if used is not None else [],
    }


def test_pick_account_strategies():
    rows = [
        _row("1", 0.2, active=True),
        _row("2", 0.95),  # over the threshold
        _row("3", 0.5),
        _row("4", 0.1, disabled=True),
        _row("5", 0.3, error="network error", stale=60),  # recent cache counts
        _row("6", 0.0, error="network error", stale=3600),  # too old
        _row("7", None, error="HTTP 500"),
        _row("8", 0.3),
    ]
    assert cli.pick_account(rows, "best", 90)["slot"] == "5"  # 0.3 ties with 8: lowest slot wins
    assert cli.pick_account(rows, "next-available", 90)["slot"] == "3"
    assert cli.pick_account(rows, "best", 25) is None
    rows[0]["active"], rows[7]["active"] = False, True
    assert cli.pick_account(rows, "next-available", 90)["slot"] == "1"  # wraps around after the active slot


def test_switch_strategy_switches_to_picked_account(tmp_path, monkeypatch):
    kr = setup(tmp_path, monkeypatch)
    _add(kr, "a@x.com", "b@x.com", "c@x.com")
    usage = {"a@x.com": 0.5, "b@x.com": 0.2, "c@x.com": 0.99}
    monkeypatch.setattr(cli, "account_usage", lambda t: (_pools(usage[cli.email_of(t)]), t))
    assert cli.main(["switch", "--strategy", "best"]) == 0
    assert cli.email_of(kr["t"]) == "b@x.com"
    assert cli.main(["switch", "--strategy", "next-available"]) == 0  # after b comes c (99%), then a
    assert cli.email_of(kr["t"]) == "a@x.com"
    assert cli.main(["switch", "--strategy", "best", "--threshold", "10"]) == 1
    assert cli.email_of(kr["t"]) == "a@x.com"


def test_switch_strategy_rejects_target(capsys):
    import pytest

    with pytest.raises(SystemExit) as exc:
        cli.main(["switch", "2", "--strategy", "best"])
    assert exc.value.code == 2


def _auto_setup(tmp_path, monkeypatch, usage, running=False):
    kr = setup(tmp_path, monkeypatch, running=running)
    _add(kr, *usage)

    def fake(t):
        u = usage[cli.email_of(t)]
        if isinstance(u, Exception):
            raise u
        return _pools(u), t

    monkeypatch.setattr(cli, "account_usage", fake)
    return kr


def test_auto_stays_below_threshold(tmp_path, monkeypatch, capsys):
    kr = _auto_setup(tmp_path, monkeypatch, {"a@x.com": 0.1, "b@x.com": 0.5})
    before = kr["t"]
    assert cli.main(["auto"]) == 0
    assert kr["t"] is before
    assert "is fine (max 50% used)" in capsys.readouterr().out


def test_auto_switches_when_active_is_over_threshold(tmp_path, monkeypatch, capsys):
    kr = _auto_setup(tmp_path, monkeypatch, {"a@x.com": 0.6, "b@x.com": 0.95, "c@x.com": 0.2})
    kr["t"] = make_token("b@x.com", "r-b@x.com")
    assert cli.main(["auto"]) == 0
    assert cli.email_of(kr["t"]) == "c@x.com"
    assert "Switched to account 3: c@x.com (max 20% used)" in capsys.readouterr().out
    kr["t"] = make_token("b@x.com", "r-b@x.com")
    assert cli.main(["auto", "--strategy", "next-available"]) == 0  # after b: c, then a
    assert cli.email_of(kr["t"]) == "c@x.com"


def test_auto_without_candidate_or_quota_stays(tmp_path, monkeypatch, capsys):
    kr = _auto_setup(tmp_path, monkeypatch, {"a@x.com": 0.92, "b@x.com": 0.95})
    assert cli.main(["auto"]) == 1
    assert cli.email_of(kr["t"]) == "b@x.com"
    assert "No account below 90% usage; staying on account 2" in capsys.readouterr().err

    kr = _auto_setup(tmp_path, monkeypatch, {"a@x.com": 0.1, "b@x.com": cli.UsageError("HTTP 500")})
    (tmp_path / "usage.json").unlink()
    assert cli.main(["auto"]) == 1
    assert cli.email_of(kr["t"]) == "b@x.com"


def test_auto_refuses_while_agy_runs(tmp_path, monkeypatch):
    kr = _auto_setup(tmp_path, monkeypatch, {"a@x.com": 0.1, "b@x.com": 0.99}, running=True)
    assert cli.main(["auto"]) == 1
    assert cli.email_of(kr["t"]) == "b@x.com"
    assert cli.main(["auto", "--ignore-running"]) == 0
    assert cli.email_of(kr["t"]) == "a@x.com"


def test_auto_saves_unstored_live_login_first(tmp_path, monkeypatch):
    usage = {"a@x.com": 0.1, "c@x.com": 0.99}
    kr = setup(tmp_path, monkeypatch)
    _add(kr, "a@x.com")
    monkeypatch.setattr(cli, "account_usage", lambda t: (_pools(usage[cli.email_of(t)]), t))
    kr["t"] = make_token("c@x.com", "r-c")  # signed in, never added
    assert sorted(cli.load_store()["accounts"]) == ["1"]
    assert cli.main(["auto"]) == 0
    accounts = cli.load_store()["accounts"]
    assert accounts["2"]["email"] == "c@x.com" and refresh_of(accounts["2"]["token"]) == "r-c"
    assert cli.email_of(kr["t"]) == "a@x.com"


def test_json_output_for_list_status_switch_auto(tmp_path, monkeypatch, capsys):
    kr = _auto_setup(tmp_path, monkeypatch, {"a@x.com": 0.1, "b@x.com": 0.95})
    cli.cmd_alias("1", "work")

    def run(*argv):
        code = cli.main([*argv, "--json"])
        out = capsys.readouterr().out
        assert "r-a@x.com" not in out and "r-b@x.com" not in out and "id_token" not in out
        return code, json.loads(out)

    code, data = run("list")
    assert code == 0 and data["version"] == 1
    a = data["accounts"][0]
    assert {k: a[k] for k in ("slot", "email", "alias", "active", "disabled", "stale", "error")} == {
        "slot": "1",
        "email": "a@x.com",
        "alias": "work",
        "active": False,
        "disabled": False,
        "stale": False,
        "error": None,
    }
    assert a["pools"][0] == {"group": "Gemini", "window": "5h", "used": 0.1, "reset": None}
    assert run("status") == (0, {"version": 1, "email": "b@x.com", "slot": "2"})
    code, data = run("auto")
    assert code == 0
    assert data == {
        "version": 1,
        "switched": True,
        "slot": "1",
        "email": "a@x.com",
        "saved_slot": None,
        "max_used": 0.1,
    }
    assert run("switch", "2") == (
        0,
        {"version": 1, "switched": True, "slot": "2", "email": "b@x.com", "saved_slot": None},
    )
    assert run("switch", "nope") == (1, {"version": 1, "error": "No account matches 'nope'. Run `agyswap list`."})
    kr["t"] = None
    assert run("status") == (0, {"version": 1, "email": None, "slot": None})


def test_export_import_roundtrip(tmp_path, monkeypatch, capsys):
    import os

    kr = setup(tmp_path / "home", monkeypatch)
    _add(kr, "a@x.com", "b@x.com")
    cli.cmd_alias("1", "work")
    cli.cmd_disable("2")
    kr["t"] = make_token("b@x.com", "r-b-live")  # agy refreshed b; export takes the keyring copy
    store_before = cli.store_path().read_text()
    out = tmp_path / "backup.agyswap"
    assert cli.main(["export", str(out)]) == 0
    captured = capsys.readouterr()
    assert "refresh tokens" in captured.err
    assert "r-a@x.com" not in captured.out + captured.err
    assert (os.stat(out).st_mode & 0o777) == 0o600
    assert cli.store_path().read_text() == store_before and refresh_of(kr["t"]) == "r-b-live"
    data = json.loads(out.read_text())
    assert data["format"] == "agyswap-export" and data["version"] == 1
    assert [refresh_of(a["token"]) for a in data["accounts"]] == ["r-a@x.com", "r-b-live"]
    assert cli.main(["export", str(out)]) == 1  # never overwrites by accident
    assert cli.main(["export", str(out), "--force"]) == 0

    kr2 = setup(tmp_path / "other", monkeypatch)
    _add(kr2, "b@x.com")  # already here: skipped unless --force
    assert cli.main(["import", str(out)]) == 0
    assert "Imported 1, skipped 1" in capsys.readouterr().out
    accounts = cli.load_store()["accounts"]
    assert accounts["2"]["email"] == "a@x.com" and accounts["2"]["alias"] == "work"
    assert "disabled" not in accounts["1"]
    assert cli.main(["import", str(out), "--force"]) == 0
    accounts = cli.load_store()["accounts"]
    assert accounts["1"]["disabled"] and refresh_of(accounts["1"]["token"]) == "r-b-live"
    assert sorted(accounts) == ["1", "2"]


def test_import_rejects_whole_file_on_bad_entry(tmp_path, monkeypatch):
    kr = setup(tmp_path, monkeypatch)
    keyring_before = kr.get("t")
    bad = {
        "format": "agyswap-export",
        "version": 1,
        "accounts": [
            {"email": "a@x.com", "token": make_token("a@x.com", "r-a")},
            {"email": "b@x.com", "token": make_token("evil@x.com", "r-e")},  # claim does not match
        ],
    }
    f = tmp_path / "bad.agyswap"
    f.write_text(json.dumps(bad))
    assert cli.main(["import", str(f)]) == 1
    f.write_text("{}")
    assert cli.main(["import", str(f)]) == 1
    assert cli.load_store()["accounts"] == {} and kr.get("t") == keyring_before


def test_import_drops_alias_taken_by_another_account(tmp_path, monkeypatch, capsys):
    kr = setup(tmp_path, monkeypatch)
    _add(kr, "a@x.com")
    cli.cmd_alias("1", "work")
    f = tmp_path / "in.agyswap"
    entry = {"email": "b@x.com", "alias": "WORK", "token": make_token("b@x.com", "r-b")}
    f.write_text(json.dumps({"format": "agyswap-export", "version": 1, "accounts": [entry]}))
    assert cli.main(["import", str(f)]) == 0
    assert "alias" not in cli.load_store()["accounts"]["2"]
    assert "alias 'WORK' dropped" in capsys.readouterr().out


def test_fresh_token_refreshes_and_skips_rejected_client(monkeypatch):
    import io
    import urllib.error

    from agyswap import usage

    monkeypatch.setattr(usage, "_agy_client_secrets", lambda: ("S1", "S2"))
    sent = []

    def fake_post(url, data, headers=None):
        sent.append(dict(__import__("urllib.parse").parse.parse_qsl(data.decode())))
        if sent[-1]["client_secret"] == "S1":
            raise urllib.error.HTTPError(url, 401, "", None, io.BytesIO(b'{"error": "invalid_client"}'))
        return {"access_token": "new-access", "expires_in": 3600, "id_token": "new-id"}

    monkeypatch.setattr(usage, "_post", fake_post)
    old = _expiring(make_token("a@x.com", "r-a"), "2000-01-01T00:00:00Z")
    new = json.loads(usage.fresh_token(old))
    assert [s["client_secret"] for s in sent] == ["S1", "S2"]
    assert sent[1]["refresh_token"] == "r-a" and sent[1]["grant_type"] == "refresh_token"
    assert new["token"]["access_token"] == "new-access" and new["id_token"] == "new-id"
    assert new["token"]["refresh_token"] == "r-a"  # Google does not rotate it
    assert usage.parse_time(new["token"]["expiry"]) > usage.parse_time("2026-01-01T00:00:00Z")
    fresh = _expiring(make_token("a@x.com", "r-a"), "2999-01-01T00:00:00Z")
    sent.clear()
    assert usage.fresh_token(fresh) == fresh and sent == []  # still valid: no request


def test_fresh_token_fails_when_no_client_is_accepted(monkeypatch):
    import io
    import urllib.error

    import pytest

    from agyswap import usage

    monkeypatch.setattr(usage, "_agy_client_secrets", lambda: ("S1",))

    def reject(url, data, headers=None):
        raise urllib.error.HTTPError(url, 401, "", None, io.BytesIO(b'{"error": "invalid_client"}'))

    monkeypatch.setattr(usage, "_post", reject)
    with pytest.raises(usage.UsageError, match="no agy OAuth client secret"):
        usage.fresh_token(_expiring(make_token("a@x.com", "r-a"), "2000-01-01T00:00:00Z"))


def test_switch_strategy_refuses_while_agy_runs(tmp_path, monkeypatch, capsys):
    kr = _auto_setup(tmp_path, monkeypatch, {"a@x.com": 0.1, "b@x.com": 0.5}, running=True)
    fetched = []
    monkeypatch.setattr(cli, "account_usage", lambda t: (fetched.append(t), ([], t))[1])
    assert cli.main(["switch", "--strategy", "best"]) == 1
    assert "agy is running" in capsys.readouterr().err
    assert fetched == [] and cli.email_of(kr["t"]) == "b@x.com"


def test_switch_to_active_account_is_a_no_op(tmp_path, monkeypatch, capsys):
    kr = setup(tmp_path, monkeypatch)
    _add(kr, "a@x.com", "b@x.com")
    writes = []
    monkeypatch.setattr(cli, "write_token", writes.append)
    assert cli.main(["switch", "2"]) == 0
    assert "Already on account 2: b@x.com" in capsys.readouterr().out
    assert writes == []


def test_tui_remove_confirms_and_targets_email(tmp_path, monkeypatch):
    import asyncio

    from agyswap import tui

    setup(tmp_path, monkeypatch)
    rows = [{"slot": "1", "email": "a@x.com", "active": False, "pools": [], "error": None}]
    monkeypatch.setattr(cli, "collect_usage", lambda: rows)
    removed = []
    monkeypatch.setattr(cli, "cmd_remove", lambda t: removed.append(t) or "Removed")

    async def go():
        app = tui.AgySwapApp()
        async with app.run_test() as pilot:
            for key in ("d", "n", "d", "y"):
                await app.workers.wait_for_complete()
                await pilot.pause()
                await pilot.press(key)
            await app.workers.wait_for_complete()
            await pilot.pause()

    asyncio.run(go())
    assert removed == ["a@x.com"]  # "n" cancelled, "y" removed by email


def test_import_rejects_unreadable_or_foreign_files(tmp_path, monkeypatch):
    setup(tmp_path, monkeypatch)
    f = tmp_path / "x.agyswap"
    for content in ("not json", '{"format": "other", "version": 1}', '{"format": "agyswap-export", "version": 1}'):
        f.write_text(content)
        assert cli.main(["import", str(f)]) == 1
    assert cli.main(["import", str(tmp_path / "missing")]) == 1
    assert cli.load_store()["accounts"] == {}


def test_threshold_must_be_a_percentage():
    import pytest

    for bad in ("0", "101", "abc"):
        with pytest.raises(SystemExit):
            cli.build_parser().parse_args(["auto", "--threshold", bad])
    assert cli.build_parser().parse_args(["auto", "--threshold", "75.5"]).threshold == 75.5


def test_list_json_on_empty_store(tmp_path, monkeypatch, capsys):
    setup(tmp_path, monkeypatch)
    assert cli.main(["list", "--json"]) == 0
    assert json.loads(capsys.readouterr().out) == {"version": 1, "accounts": []}


def test_malformed_cache_entry_is_not_shown(tmp_path, monkeypatch):
    kr = setup(tmp_path, monkeypatch)
    _add(kr, "a@x.com")
    (tmp_path / "usage.json").write_text(json.dumps({"a@x.com": {"fetched_at": "2026-01-01T00:00:00Z", "pools": [{}]}}))

    def fail(t):
        raise cli.UsageError("network error: x")

    monkeypatch.setattr(cli, "account_usage", fail)
    [row] = cli.collect_usage()
    assert row["pools"] == [] and row["stale"] is None and row["error"] == "network error: x"


def test_auto_keeps_unstored_live_login_with_quota_left(tmp_path, monkeypatch):
    usage = {"a@x.com": 0.1, "c@x.com": 0.2}
    kr = setup(tmp_path, monkeypatch)
    _add(kr, "a@x.com")
    monkeypatch.setattr(cli, "account_usage", lambda t: (_pools(usage[cli.email_of(t)]), t))
    kr["t"] = make_token("c@x.com", "r-c")  # signed in, never added, 20% used
    assert cli.main(["auto"]) == 0
    assert cli.email_of(kr["t"]) == "c@x.com"  # its quota was read, so it stays
    assert cli.load_store()["accounts"]["2"]["email"] == "c@x.com"


def test_auto_skips_account_revoked_in_the_same_run(tmp_path, monkeypatch):
    from agyswap import usage

    kr = setup(tmp_path, monkeypatch)
    _add(kr, "a@x.com", "b@x.com", "c@x.com")
    monkeypatch.setattr(
        cli, "account_usage", lambda t: (_pools({"a": 0.95, "b": 0.1, "c": 0.5}[cli.email_of(t)[0]]), t)
    )
    kr["t"] = make_token("a@x.com", "r-a@x.com")
    cli.collect_usage()  # b's 10% is now cached

    def revoked_b(t):
        if cli.email_of(t) == "b@x.com":
            raise usage.TokenRevoked("token revoked")
        return _pools({"a": 0.95, "c": 0.5}[cli.email_of(t)[0]]), t

    monkeypatch.setattr(cli, "account_usage", revoked_b)
    assert cli.main(["auto"]) == 0
    assert cli.email_of(kr["t"]) == "c@x.com"


def test_auto_leaves_a_disabled_active_account(tmp_path, monkeypatch):
    kr = _auto_setup(tmp_path, monkeypatch, {"a@x.com": 0.1, "b@x.com": 0.1})
    cli.cmd_disable("2", reason="token revoked")  # the live login was quarantined
    assert cli.main(["auto"]) == 0
    assert cli.email_of(kr["t"]) == "a@x.com"


def test_retry_after_is_clamped(monkeypatch):
    from agyswap import usage

    assert usage._retry_after("99999999999999999999") == 3600
    assert usage._retry_after("999999999") == 3600
    assert usage._retry_after("Fri, 31 Dec 9999 23:59:59 GMT") == 3600
    assert usage._retry_after("Thu, 01 Jan 1970 00:00:00 GMT") == 0
    assert usage._retry_after("Thu, 01 Jan 2099 00:00:00 -0000") == 3600  # naive date
    assert usage._retry_after("²") == 300


def _export_file(tmp_path, *entries, version=1):
    f = tmp_path / "in.agyswap"
    f.write_text(json.dumps({"format": "agyswap-export", "version": version, "accounts": list(entries)}))
    return str(f)


def test_import_rejects_malformed_entries(tmp_path, monkeypatch):
    setup(tmp_path, monkeypatch)
    no_refresh = json.loads(make_token("a@x.com", "r"))
    del no_refresh["token"]["refresh_token"]
    good = make_token("a@x.com", "r-a")
    bad_entries = [
        {"email": "a@x.com", "token": json.dumps(no_refresh)},  # agy could not use it
        {"email": "a@x.com", "token": good, "disabled": "no"},  # not a bool
        {"email": "a\x1b]0;pwn\x07@x.com", "token": make_token("a\x1b]0;pwn\x07@x.com", "r")},  # terminal escape
        {"email": "a@x.com", "token": good, "disabled": True, "disabled_reason": "\x1b[2Jx"},  # escape via reason
    ]
    for entry in bad_entries:
        assert cli.main(["import", _export_file(tmp_path, entry)]) == 1
    assert cli.main(["import", _export_file(tmp_path, {"email": "a@x.com", "token": good}, version=2)]) == 1
    assert cli.load_store()["accounts"] == {}


def test_import_drops_invalid_alias_and_keeps_own_alias_on_force(tmp_path, monkeypatch, capsys):
    kr = setup(tmp_path, monkeypatch)
    _add(kr, "a@x.com")
    cli.cmd_alias("1", "work")
    own = {"email": "a@x.com", "alias": "work", "token": make_token("a@x.com", "r-new")}
    digits = {"email": "b@x.com", "alias": "42", "token": make_token("b@x.com", "r-b")}
    escape = {"email": "c@x.com", "alias": "w\x1b]0;pwn\x07", "token": make_token("c@x.com", "r-c")}
    assert cli.main(["import", _export_file(tmp_path, own, digits, escape), "--force"]) == 0
    accounts = cli.load_store()["accounts"]
    assert accounts["1"]["alias"] == "work" and refresh_of(accounts["1"]["token"]) == "r-new"
    assert "alias" not in accounts["2"] and "alias" not in accounts["3"]
    assert "\x1b" not in capsys.readouterr().out  # the dropped alias is reported escaped, never raw


def test_list_exit_code_ignores_disabled_accounts(tmp_path, monkeypatch):
    kr = setup(tmp_path, monkeypatch)
    _add(kr, "a@x.com", "b@x.com")
    cli.cmd_disable("1")

    def fail(t):
        raise cli.UsageError("HTTP 500")

    monkeypatch.setattr(cli, "account_usage", fail)
    assert cli.main(["list"]) == 1  # the only enabled account failed


def test_export_file_errors_are_swap_errors(tmp_path, monkeypatch, capsys):
    kr = setup(tmp_path, monkeypatch)
    _add(kr, "a@x.com")
    (tmp_path / "dir").mkdir()
    assert cli.main(["export", str(tmp_path / "dir"), "--force"]) == 1
    assert cli.main(["export", str(tmp_path / "missing" / "x.agyswap")]) == 1
    assert "Cannot write" in capsys.readouterr().err
    assert not (tmp_path / "missing").exists()


def test_switch_rejects_flags_that_would_be_ignored():
    import pytest

    for argv in (["switch", "--strategy", "best", "--force"], ["switch", "2", "--threshold", "50"]):
        with pytest.raises(SystemExit) as exc:
            cli.main(argv)
        assert exc.value.code == 2


def test_old_cache_is_not_used_to_pick(tmp_path, monkeypatch):
    kr = _auto_setup(tmp_path, monkeypatch, {"a@x.com": cli.UsageError("x"), "b@x.com": 0.95})
    old = {
        "fetched_at": "2020-01-01T00:00:00+00:00",
        "pools": [{"group": "G", "window": "5h", "used": 0.1, "reset": None}],
    }
    (tmp_path / "usage.json").write_text(json.dumps({"a@x.com": old}))
    assert cli.main(["auto"]) == 1
    assert cli.email_of(kr["t"]) == "b@x.com"


def test_agy_running_ignores_only_the_bg_updater(monkeypatch):
    import subprocess

    def pgrep(out):
        monkeypatch.setattr(cli.subprocess, "run", lambda *a, **k: subprocess.CompletedProcess(a, 0, out, ""))

    pgrep("12 /x/agy --bg-updater --app_data_dir=antigravity-cli\n")
    assert not cli.agy_running()
    pgrep("12 /x/agy --bg-updater\n13 /x/agy -p hi\n")
    assert cli.agy_running()
    pgrep("")
    assert not cli.agy_running()


def test_add_slot_move_keeps_alias_and_disable(tmp_path, monkeypatch):
    kr = setup(tmp_path, monkeypatch)
    _add(kr, "a@x.com")
    cli.cmd_alias("1", "w")
    cli.cmd_disable("1")
    cli.cmd_add(5)
    accounts = cli.load_store()["accounts"]
    assert list(accounts) == ["5"] and accounts["5"]["alias"] == "w" and accounts["5"]["disabled_reason"] == "manual"


def test_threshold_is_strict(tmp_path, monkeypatch):
    rows = [_row("1", 0.95, active=True), _row("2", 0.9)]
    assert cli.pick_account(rows, "best", 90) is None
    kr = _auto_setup(tmp_path, monkeypatch, {"a@x.com": 0.1, "b@x.com": 0.9})
    assert cli.main(["auto", "--threshold", "90"]) == 0  # exactly 90% used is not "fine"
    assert cli.email_of(kr["t"]) == "a@x.com"


def test_auto_refuses_before_saving_or_fetching_while_agy_runs(tmp_path, monkeypatch):
    kr = setup(tmp_path, monkeypatch, running=True)
    _add(kr, "a@x.com")
    kr["t"] = make_token("c@x.com", "r-c")  # unstored live login
    monkeypatch.setattr(cli, "account_usage", lambda t: _fail("auto fetched while agy runs"))
    assert cli.main(["auto"]) == 1
    assert sorted(cli.load_store()["accounts"]) == ["1"]


def _fail(msg):
    import pytest

    pytest.fail(msg)


def test_auto_json_reports_saved_slot_after_switch(tmp_path, monkeypatch, capsys):
    usage = {"a@x.com": 0.1, "c@x.com": 0.99}
    kr = setup(tmp_path, monkeypatch)
    _add(kr, "a@x.com")
    monkeypatch.setattr(cli, "account_usage", lambda t: (_pools(usage[cli.email_of(t)]), t))
    kr["t"] = make_token("c@x.com", "r-c")
    assert cli.main(["auto", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["switched"] and data["slot"] == "1" and data["saved_slot"] == "2"


def test_list_json_marks_stale_and_disabled_reason(tmp_path, monkeypatch, capsys):
    kr = setup(tmp_path, monkeypatch)
    _add(kr, "a@x.com", "b@x.com")
    monkeypatch.setattr(cli, "account_usage", lambda t: (_pools(0.2), t))
    cli.collect_usage()
    cli.cmd_disable("2")

    def fail(t):
        raise cli.UsageError("network error: x")

    monkeypatch.setattr(cli, "account_usage", fail)
    assert cli.main(["list", "--json"]) == 1
    a, b = json.loads(capsys.readouterr().out)["accounts"]
    assert a["stale"] is True and a["pools"] and b["disabled_reason"] == "manual"


def test_cache_survives_while_account_is_disabled(tmp_path, monkeypatch):
    kr = setup(tmp_path, monkeypatch)
    _add(kr, "a@x.com")
    monkeypatch.setattr(cli, "account_usage", lambda t: (_pools(0.4), t))
    cli.collect_usage()
    cli.cmd_disable("1")
    cli.collect_usage()
    assert json.loads((tmp_path / "usage.json").read_text())["a@x.com"]["pools"]


def test_switch_to_disabled_current_account_is_already_on(tmp_path, monkeypatch, capsys):
    kr = setup(tmp_path, monkeypatch)
    _add(kr, "a@x.com", "b@x.com")
    cli.cmd_disable("2")
    assert cli.main(["switch", "2"]) == 0
    assert "Already on account 2" in capsys.readouterr().out


def test_alias_can_change_case_on_same_account(tmp_path, monkeypatch):
    kr = setup(tmp_path, monkeypatch)
    _add(kr, "a@x.com")
    cli.cmd_alias("1", "work")
    assert cli.main(["alias", "1", "Work"]) == 0
    assert cli.load_store()["accounts"]["1"]["alias"] == "Work"


def test_usage_refresh_never_writes_the_keyring(tmp_path, monkeypatch):
    import pytest

    kr = setup(tmp_path, monkeypatch)
    _add(kr, "a@x.com")
    monkeypatch.setattr(cli, "write_token", lambda t: pytest.fail("keyring written during refresh"))
    monkeypatch.setattr(cli, "account_usage", lambda t: (_pools(0.1), _expiring(t, "2099-01-01T00:00:00+00:00")))
    cli.collect_usage()
