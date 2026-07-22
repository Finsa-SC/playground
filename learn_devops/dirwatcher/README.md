# dirwatcher

Polling-based directory watcher for drop-folder style ingestion. Watches one
or more directories for files matching a pattern, waits for them to become
"stable" (stops growing across a configurable number of polls), and then
performs a configured action: move, copy, or log-only.

Typical use case: an upstream system (SFTP drop, export job, etc.) writes
files into a folder, and we need to pick them up once they're fully written
and route them somewhere for downstream processing.

## How it works

1. On each poll cycle, every configured watch directory is scanned for files
   matching its glob pattern.
2. For each matching file, its size is compared against the previous poll.
   If the size is unchanged for `STABILITY_CHECKS` consecutive polls, the
   file is considered stable.
3. Once stable, the configured action runs:
   - `move` - moves the file to `destination`
   - `copy` - copies the file to `destination`
   - `log_only` - just logs that the file was observed (no side effects)
4. State (which files have been seen/processed) is persisted to a JSON file
   so a restart doesn't cause re-processing.

## Project layout

```
config/
  watch_config.yaml   # list of directories to watch + actions
src/dirwatcher/
  config.py           # env + yaml config loading
  state.py            # JSON-backed state persistence
  watcher.py           # polling/scanning logic
  handlers.py          # move/copy/log actions
  logging_setup.py     # logging configuration
  main.py              # entry point / run loop
scripts/
  run.sh               # convenience local runner
tests/
  test_config.py
  test_state.py
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
```

Edit `.env` and `config/watch_config.yaml` to point at real directories.

## Running

```bash
./scripts/run.sh
```

or directly:

```bash
python -m dirwatcher.main
```

The process runs in a continuous loop, polling every
`POLL_INTERVAL_SECONDS`. Stop it with Ctrl+C.

## Configuration reference

Environment variables (see `.env.example`):

| Variable                | Description                                         |
|-------------------------|------------------------------------------------------|
| `WATCH_CONFIG_PATH`     | Path to the watch_config.yaml file (required)        |
| `STATE_FILE_PATH`       | Where to persist seen-file state                     |
| `POLL_INTERVAL_SECONDS` | Seconds between scans                                |
| `STABILITY_CHECKS`      | Consecutive unchanged-size polls before processing   |
| `LOG_LEVEL`             | DEBUG / INFO / WARNING / ERROR                       |

`watch_config.yaml` entries:

| Field         | Description                                    |
|---------------|-------------------------------------------------|
| `name`        | Friendly name, used in logs                     |
| `path`        | Directory to scan                                |
| `pattern`     | Glob pattern for files to pick up                |
| `action`      | `move`, `copy`, or `log_only`                    |
| `destination` | Target directory for `move`/`copy`               |

## Tests

```bash
pytest
```

## Notes

This project only covers the watcher process itself. Deployment,
scheduling, and infrastructure are handled by other teams/tooling.
