# ⏰ Work Time Calculator

Calculate when your workday ends: enter your **start time** and (optionally) your **break**, and the tool computes your finish time.

## Rules
- You need **8 hours of actual work**.
- If no break is specified, a **30-minute break** is included.
- If a break is specified, extra break time is added as needed to reach **at least 30 minutes** total (a longer break counts as-is).
- The result can roll over to the **next day** (shown as "Tomorrow" / "+N days").

## Usage
Part of the Portable Toolbox: run `python toolbox.py` at the toolbox root, then open http://localhost:8080 (or directly http://localhost:8080/work_time_calculator) and click the ⏰ card.

The tool is a single static page (`index.html`) — no dependencies, no data leaves the browser. It also works when opened directly as a local file.