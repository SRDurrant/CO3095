import builtins
import types

import app.main as main_mod


def test_main_explicit_exit_calls_save_once(monkeypatch, tmp_path):
    calls = {"save": 0, "load": 0}

    # Force file path into tmp
    monkeypatch.setattr(main_mod, "DEFAULT_SYSTEM_DATA_PATH", str(tmp_path / "system.json"))

    monkeypatch.setattr(main_mod, "load_system_data", lambda *a, **k: calls.__setitem__("load", calls["load"] + 1) or True)
    monkeypatch.setattr(main_mod, "save_system_data", lambda *a, **k: calls.__setitem__("save", calls["save"] + 1) or True)

    # Avoid seeding, noise
    monkeypatch.setattr(main_mod, "example_users", lambda: None)
    monkeypatch.setattr(main_mod, "show_main_menu", lambda: None)

    # Input: immediately exit
    inputs = iter(["0"])
    monkeypatch.setattr(builtins, "input", lambda _="": next(inputs))

    main_mod.main()

    assert calls["load"] == 1
    # explicit exit should save exactly once (did_explicit_exit_save=True prevents finally-save)
    assert calls["save"] == 1
