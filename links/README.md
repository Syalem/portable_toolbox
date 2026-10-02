# 🔗 Links

A **static (HTML/JS) tool** of the Portable Toolbox to store **online links** and **local paths**, each with a **title** describing what it points to (plus an optional category and note).

- Entries are listed with a 🌐 (online) or 📁 (local path) badge, auto-detected from the value.
- A **search box** filters by title, link/path, category or note.
- Actions per entry: **Open** (new tab), **Copy** (copies the raw value), **Edit**, **Delete**.
- Data is **auto-saved** after each change into `links.json`.

---

## 🚀 Usage

1. Start the toolbox:

   ```
   python toolbox.py
   ```

2. Click the 🔗 **Links** card (or go directly to http://localhost:8080/links/).
3. Fill in a **Title** and the **link or local path**, optionally a category and a note, then click **➕ Add link**.

## 📂 Structure des fichiers

```
links/
│── index.html    # Page de l'outil (HTML + CSS + JS)
│── README.md
│── links.json    # Données sauvegardées (créé automatiquement)
```

## 📝 Data format (links.json)

```json
{
    "links": [
        {
            "id": "l1abc2345",
            "title": "Python documentation",
            "target": "https://docs.python.org/3/",
            "category": "dev",
            "note": "Official docs",
            "added": "2026-10-02"
        }
    ]
}
```

- `target` holds either an online URL (`https://...`, `http://...`, `www....`) or a local path (`C:\Users\...`, `\\server\share\...`, relative paths).
- The type badge is derived from `target`: anything starting with `http://`, `https://` or `www.` is considered an **online link**, everything else a **local path**.

## 🔌 Server contract

The frontend persists data with `POST /links/sauvegarder`, handled by `toolbox.py`:

- Body: a JSON object `{"links": [ ... ]}` (the whole list is replaced on each save).
- The server validates that `links` is a list and writes `links/links.json` (UTF-8, indented, `ensure_ascii=False`).
- Responses: `{"status": "success"}` or `{"status": "error", "detail": "..."}`.

## ⚠️ Notes

- **Opening local paths**: for security reasons, browsers usually block navigation from an `http://` page to a `file://` target. The **Copy** button always works — paste the path into your file explorer. The **Open** button on local paths is a best effort.
- No database: only a local JSON file, like the other tools of the toolbox.
- The list is saved automatically after every change (no save button needed).
