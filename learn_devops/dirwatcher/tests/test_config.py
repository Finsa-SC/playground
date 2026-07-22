import os
import textwrap

import pytest

from dirwatcher.config import load_settings


@pytest.fixture
def watch_config_file(tmp_path):
    content = textwrap.dedent(
        """
        watches:
          - name: test-watch
            path: /tmp/incoming
            pattern: "*.csv"
            action: move
            destination: /tmp/processed
        """
    )
    config_path = tmp_path / "watch_config.yaml"
    config_path.write_text(content)
    return str(config_path)


def test_load_settings_reads_watch_targets(watch_config_file, monkeypatch):
    monkeypatch.setenv("WATCH_CONFIG_PATH", watch_config_file)
    monkeypatch.setenv("POLL_INTERVAL_SECONDS", "10")

    settings = load_settings()

    assert settings.poll_interval_seconds == 10
    assert len(settings.watches) == 1
    assert settings.watches[0].name == "test-watch"
    assert settings.watches[0].action == "move"


def test_load_settings_requires_watch_config_path(monkeypatch):
    monkeypatch.delenv("WATCH_CONFIG_PATH", raising=False)

    with pytest.raises(KeyError):
        load_settings()
