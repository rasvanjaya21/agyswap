"""Round-trip with a fake keyring: add two accounts, switch, refreshed token survives."""

import base64
import json

from agyswap import cli


def make_token(email, refresh):
    claims = base64.urlsafe_b64encode(json.dumps({"email": email}).encode()).decode().rstrip("=")
    return json.dumps({"token": {"refresh_token": refresh}, "id_token": f"h.{claims}.s"})


def refresh_of(token):
    return json.loads(token)["token"]["refresh_token"]


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
