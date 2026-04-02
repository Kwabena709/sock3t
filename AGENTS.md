# AGENTS.md

## Cursor Cloud specific instructions

### Repository overview

This repository contains two distinct layers:

1. **HolyScreen (Node.js/TypeScript)** — A church presentation web application (React + Express + tRPC + Drizzle ORM + MySQL). Only configuration scaffolding (`package.json`, `tsconfig.json`, `vite.config.ts`, `vitest.config.ts`, `drizzle.config.ts`) is committed. The actual source directories (`client/`, `server/`, `shared/`, `drizzle/`) are **not committed**, so `pnpm dev`, `pnpm build`, `pnpm check`, and `pnpm test` will all fail with "file not found" errors. This is expected — the source code was never pushed to the repository.

2. **Python desktop apps** — Several independent Tkinter GUI applications in top-level directories (`Login and Registration System/`, `Inventory management system/`, `Church management system/`, `WelfareApp/`, `Gamex/`, `Search Bar/`, `python test project/`). These are the runnable applications.

### MySQL setup

MySQL 8.0 is installed. To start it with TCP networking enabled:

```
sudo mysqld --user=mysql --datadir=/var/lib/mysql --port=3306 --bind-address=127.0.0.1 &
```

The Python apps hardcode MySQL credentials: `host=localhost, user=root, password=1989`. Use `127.0.0.1` instead of `localhost` if you see connection refused errors (forces TCP instead of socket).

### Running Python apps

All Python GUI apps require a display server (`$DISPLAY` must be set). The VM has Xvfb at `:1`.

Example (welfare management app):
```
cd "/workspace/Login and Registration System" && python3 App.py
```

The `python3-tk` package must be installed for Tkinter to work. Python deps: `pymysql`, `mysql-connector-python`, `bcrypt`, `Pillow`, `customtkinter`, `ttkthemes`, `pandas`, `openpyxl`, `tkcalendar`.

### Node.js tooling

- `pnpm install --no-frozen-lockfile` — installs deps (no lockfile in repo).
- The `patchedDependencies` entry for `wouter@3.7.1` in `package.json` references a missing patch file. This has been removed.
- `pnpm rebuild esbuild` — needed after install since esbuild build scripts are initially blocked by pnpm's build approval.
- `pnpm run format` (Prettier) and `pnpm run check` (tsc) are the lint commands, though `check` fails due to missing source files.

### Known limitations

- The HolyScreen TypeScript source code was never committed. All Node.js dev/build/test scripts expect `client/`, `server/`, and `shared/` directories that don't exist.
- The Python apps expect specific image files in their directories (icons, logos, backgrounds). Missing images will cause import errors on launch.
- The Inventory management system app expects PNG icon files (`icon.png`, `logo.png`, etc.) in its directory.
