# Copilot instructions — Selene 2.0

Short, practical guide for AI coding agents working on this repo.

## Purpose
- Help contributors and AI agents quickly understand the app structure, run it locally, and make safe, focused edits.

## How to run (local)
- Entry point: run `python main.py` from the project root.
- This opens a Tkinter GUI (`ui/main_window.py`) that drives most flows.

## High-level architecture
- GUI layer: `ui/main_window.py`, `ui/tooltip.py` — builds the Tkinter app and updates `Text` widgets and `StringVar` states.
- Data layer: `data/loader.py`, `data/analysis.py`, `data/validators.py` — CSV loading (returns dict of DataFrames) and processing helpers. Example: `load_csv_files(paths)` → `{stem: DataFrame}`.
- Automation: `automation/login.py`, `automation/driver.py`, `automation/upload.py` — Selenium integration. `login.start_login()` launches `webdriver.Firefox()` and is invoked in a background `threading.Thread` from the UI to avoid blocking.
- Config: `config/settings.py` (currently empty; treat as central place for runtime settings).
- Orchestration: `main.py` constructs `MainWindow()` and runs the Tk loop.

## Project-specific patterns and conventions
- Language: identifiers and UI text are Spanish. Preserve Spanish names (e.g., `generar_lista_desaprobados`) when editing to keep consistency.
- CSV conventions: grade columns appear as patterns like `NE1`, `R1E1`, `R2E1` or `EVAL 1`, `R1E1`, `R2E1`. UI populates comboboxes with these names — search `for i in range(1, 9)` loops in `ui/main_window.py` for examples.
- UI background tasks: use `threading.Thread(target=..., daemon=True).start()` for long-running automation (see login button handlers).
- Dataflow example (concrete): UI calls `load_csv_files(self.csv_paths)` → iterates `for nombre_archivo, df in dataframes.items()` → verifies `columna in df.columns` → calls `generar_lista_desaprobados(df, columna, n_estudiantes)` and writes to `self.output_text`.
- Error handling: surface errors to the GUI via `self.output_text.insert(...)` — follow existing UX pattern rather than raising raw exceptions to the user.

## Integration points & runtime dependencies
- Python packages used: `pandas`, `selenium`, `tkinter` (stdlib). Ensure these are available in the runtime environment.
- Selenium: `automation/login.py` uses `webdriver.Firefox()` — requires Firefox and geckodriver on PATH. Agents modifying automation should document driver assumptions and platform notes.

## Files to inspect for changes (quick links)
- `main.py` — app entry
- `ui/main_window.py` — primary UI + user flows (loading CSVs, calling analysis)
- `data/loader.py` — CSV reading helper (returns dict of DataFrames)
- `data/analysis.py` — data processing helpers (contains Spanish-named functions)
- `automation/login.py` — Selenium login flow
- `config/settings.py` — central settings placeholder

## Editing guidance for AI agents
- Preserve Spanish naming and visible UI text unless user requests translation.
- When changing data processing functions, update `ui/main_window.py` call sites and the UX messages shown in `self.output_text` to keep behavior consistent.
- For automation changes, add platform checks and document required external binaries (e.g., geckodriver). Prefer adding configuration knobs in `config/settings.py` rather than hardcoding paths.
- Keep UI responsiveness: offload blocking I/O (Selenium, file reads on large datasets) to background threads and use thread-safe UI update patterns (queue back to main thread or use `after` if needed).

## Examples extracted from the codebase
- Start GUI: `python main.py` → constructs `MainWindow()` which uses `load_csv_files(...)` and `generar_lista_desaprobados(...)`.
- Background login call: `threading.Thread(target=login.start_login, daemon=True).start()` (see `ui/main_window.py`).
- CSV loader returns dict keyed by `Path(path).stem` (see `data/loader.py`).

## What this file does NOT include
- It does not prescribe new architectural changes. Only document observable behaviors and concrete patterns found in the repository.

If any section is unclear or you want more examples (call sites, exact column names, integration tests), tell me which area to expand. I'll iterate.
