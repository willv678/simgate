# Fresh install of SimGate, 12 Oct (Griffin)

Following only the README of github.com/willv678/simgate, as a newcomer
without a GPU would.

**Machine:** Windows laptop, PowerShell. No NVIDIA GPU, no WSL.

**Result:** stopped before any test ran. Three walls, each one undocumented
in the README. Total time: FILL IN.

## Steps

| # | What I did | Command | What happened (exact error) | Minutes |
|---|---|---|---|---|
| 1 | Clone | `git clone https://github.com/willv678/simgate.git` | FILL IN (worked?) | |
| 2 | Look for how to run the tests | README | Not in "Run it". The only test command (about line 140) runs one old file from Will's own path (`/home/willvarner/alpasim`). The real steps are only in `.github/workflows/tests.yml`. | |
| 3 | Run the tests | FILL IN (exact command) | `command not found`: FILL IN which command | |
| 4 | Install uv | `curl -LsSf https://astral.sh/uv/install.sh \| sh` | Did not work: FILL IN error. (That command is for bash; on Windows uv's PowerShell installer is `powershell -c "irm https://astral.sh/uv/install.ps1 \| iex"`.) | |
| 5 | Install uv, second try | FILL IN | Worked | |
| 6 | Run the tests | `uv run pytest research/harness` | Import error in `research/harness/conftest.py`: FILL IN the module it named | |

## Why it stopped

`conftest.py` imports `alpasim_grpc` and `alpasim_utils`, which come from
NVIDIA's AlpaSim, not from this repo. Getting them needs (from CI):
AlpaSim cloned at commit `affc2eab`, this repo cloned inside it as
`research/`, `git apply research/patches/alpasim-src.diff`, a Rust toolchain
for `utils_rs`, and a hand-picked package list. The scripts (`research/simgate`)
are bash. None of that works in native Windows PowerShell; the route for a
Windows user would be WSL2 (Ubuntu), not tried (needs admin rights and a
restart).

Not reached: `simgate doctor`, the read-only results site (`site/`).

## What the README should say

1. **Platform:** Linux, or WSL2 on Windows. Native Windows and PowerShell are
   not supported.
2. **How to install uv** (link and one command), and that every Python
   command goes through `uv run` from the AlpaSim folder that contains
   `research/`.
3. **A "Run the tests without a GPU" section** with the CI steps: AlpaSim at
   the pinned commit, this repo as `research/`, the src patch, Rust, the
   package list, `pytest research/harness`. What a pass looks like (337
   passed, 6 skipped on the lab machine).
4. **How to see the results without installing anything** (the `site/`
   snapshot), near the top, for readers who only want to look.
5. Delete the leftover line "Griffin: clone or pull that repo for the week
   plan" (README, about line 136): a note to one person in a public README.

## Other notes


