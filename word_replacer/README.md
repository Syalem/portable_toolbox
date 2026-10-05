# 🔁 Word Replacer

A **static (HTML/JS) tool** of the Portable Toolbox: write a string and get it back with a few given words replaced.

- **Default pairs**: `maelys → m`, `flohimont → f`, `optonic → o`.
- The replacement runs **live while you type**, with a count of the replacements made.
- Pairs are **editable**: add new ones, edit or delete them, or **reset to the defaults** at any time.
- Options:
  - **Ignore case** (on by default): `Maelys`, `MAELYS` and `maelys` are all matched.
  - **Whole words only** (off by default): by default the word is replaced even inside longer words (`maelysflohimont` → `mf`); enable this option to match whole words only.
- One-click **⧉ Copy** of the result (also `Ctrl+Enter`).
- Custom pairs are stored in the browser (`localStorage`), so they survive a page reload.

## 🚀 Usage

1. Start the toolbox:

   ```
   python toolbox.py
   ```

2. Click the 🔁 **Word Replacer** card (or go directly to http://localhost:8080/word_replacer/).
3. Type or paste your text: the result updates live below. Tweak the pairs if needed, then copy the result.

## 📂 File structure

```
word_replacer/
│── index.html    # Page de l'outil (HTML + CSS + JS)
│── README.md
```

## 📝 Notes

- No server endpoint, no data file: everything happens **in the browser** (like `work_time_calculator`), so the page also works when opened directly as a local file.
- Matching is literal text matching — regular expression special characters in a word are escaped automatically — and the longest words are replaced first, so a word contained in another one is handled correctly.
- Rows with an empty "Word to replace" field are ignored (shown dimmed) until filled in.
- The custom pairs are saved in `localStorage` under the key `word_replacer_pairs`; **↺ Reset to defaults** restores `maelys → m`, `flohimont → f`, `optonic → o`.