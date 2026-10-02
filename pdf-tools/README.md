# 📄 PDF Tools

A **static (HTML/JS)** tool of the Portable Toolbox to **merge** and **split** PDF files — 100% in your browser: your files never leave your computer.

## 🚀 Lancement

L'outil fait partie de la **Portable Toolbox** : lance simplement le serveur à la racine de la toolbox :
```bash
python toolbox.py
```

Ouvre ton navigateur et va sur http://localhost:8080 (ou directement http://localhost:8080/pdf-tools/), puis clique sur la carte 📄 **PDF Tools**.

> Le tool fonctionne aussi **sans serveur** : tu peux ouvrir `pdf-tools/index.html` directement dans le navigateur (double-clic), car tout le traitement est côté client.

## 🎯 Fonctionnalités

| Fonctionnalité | Description |
|---|---|
| 🔗 Merge | Ajoute plusieurs PDF (glisser-déposer ou parcours), réordonne-les (↑/↓), supprime-en (✕), fusionne en un seul PDF. |
| ✂️ Extract page ranges | Extrait des pages précises (ex. `1-3, 5, 8-10`) dans un seul PDF de sortie. |
| ✂️ Split every N pages | Découpe le PDF en parts consécutives de N pages (`_part1.pdf`, `_part2.pdf`, …). |
| ✂️ Split every page | Une page = un fichier PDF. |
| ⬇ Download all | Chaque fichier de sortie a son bouton **Download** ; un bouton télécharge tout (autorise les téléchargements multiples si le navigateur le demande). |
| ℹ️ Aperçu | Nombre de pages et taille affichés pour chaque fichier ajouté. |

## 📂 Structure des fichiers

```
pdf-tools/
│── index.html       # Page de l'outil (HTML + CSS + JS)
│── pdf-lib.min.js   # pdf-lib v1.17.1 (MIT) — moteur PDF, embarqué pour un usage 100% hors-ligne
│── README.md
```

## ⚠️ Notes

- **Vie privée** : aucun fichier n'est envoyé sur un réseau — la fusion et la découpe se font dans le navigateur via [pdf-lib](https://pdf-lib.js.org).
- **PDF protégés par mot de passe** : non supportés (les fichiers illisibles ou corrompus sont rejetés avec un message d'erreur).
- Les pages sont numérotées à partir de 1.
- Navigateurs supportés : Opera, Chrome, Firefox, Edge.

## 📜 Licence

Projet personnel – libre d'utilisation. pdf-lib est distribué sous licence MIT (voir https://github.com/Hopding/pdf-lib).