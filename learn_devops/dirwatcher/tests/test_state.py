import json
import os

from dirwatcher.state import StateStore


def test_load_missing_file_starts_empty(tmp_path):
    store = StateStore(str(tmp_path / "state.json"))
    store.load()
    assert store.get_watch_state("some-watch") == {}


def test_save_and_reload_roundtrip(tmp_path):
    state_path = tmp_path / "state.json"
    store = StateStore(str(state_path))
    store.load()

    store.update_file_state("watch-a", "/tmp/incoming/file.csv", {"size": 100, "stable_count": 2, "processed": True})
    store.save()

    assert state_path.exists()

    reloaded = StateStore(str(state_path))
    reloaded.load()
    watch_state = reloaded.get_watch_state("watch-a")

    assert watch_state["/tmp/incoming/file.csv"]["processed"] is True


def test_remove_file_state(tmp_path):
    store = StateStore(str(tmp_path / "state.json"))
    store.load()

    store.update_file_state("watch-a", "/tmp/incoming/gone.csv", {"size": 5, "stable_count": 1, "processed": False})
    store.remove_file_state("watch-a", "/tmp/incoming/gone.csv")

    assert "/tmp/incoming/gone.csv" not in store.get_watch_state("watch-a")
