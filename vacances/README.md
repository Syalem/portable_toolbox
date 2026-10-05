# 📅 Calendrier des Vacances (Baden-Württemberg)

Un outil **statique (HTML/JS)** de la Portable Toolbox pour visualiser et planifier tes jours de vacances.
Affiche un calendrier annuel avec :
- Les **weekends** et **jours fériés du Baden-Württemberg** en gris.
- La possibilité de **sélectionner des jours** (en vert).
- Un suivi du **nombre de jours restants** (année précédente, totale, et à planifier).
- Sauvegarde des données dans un fichier **`vacances.json`**.

---

## 🚀 Lancement

L'outil fait partie de la **Portable Toolbox** : lance simplement le serveur à la racine de la toolbox :
```bash
python toolbox.py
```

Ouvre ton navigateur (Opera, Chrome, Firefox, Edge) et va sur :
http://localhost:8080

Clique sur la carte 📅 **Vacances** (ou va directement sur http://localhost:8080/vacances/).

> Aucune dépendance n'est nécessaire : le frontend est statique (`index.html`) et la sauvegarde (POST `/sauvegarder`) est gérée par `toolbox.py`, qui fusionne les données par année dans `vacances.json`.

## 📂 Structure des fichiers

vacances/
│── index.html           # Page de l'outil (HTML + CSS + JS)
│── jours_feries.json    # Jours fériés du Baden-Württemberg (2026-2028)
│── vacances.json        # Données des vacances (créé automatiquement)




## 🎯 Fonctionnalités

  
    
      Fonctionnalité
      Description
    
  
  
    
      Sélection de l'année
      Menu déroulant pour choisir entre l'année en cours ou l'année suivante.
    
    
      Calendrier interactif
      Clique sur un jour pour le sélectionner/désélectionner (vert = sélectionné).
    
    
      Jours grisés
      Weekends et jours fériés du Baden-Württemberg sont désactivés.
    
    
      Champs personnalisables
      Saisis le nombre de jours restants de l'année précédente et le total pour l'année.
    
    
      Sauvegarde
      Automatique après chaque modification, ou bouton 💾 pour enregistrer immédiatement dans vacances.json.
    
    
      Réinitialisation
      Bouton pour effacer toutes les sélections (avec confirmation).
    
    
      Suivi automatique
      Affiche le nombre de jours restants à planifier.
    
  





## 📝 Fichiers JSON
jours_feries.json
Contient les jours fériés pour le Baden-Württemberg (2026, 2027 et 2028) : les 12 jours fériés officiels du Land.
Exemple :
```json
{
  "2026": ["2026-01-01", "2026-01-06", ...],
  "2027": ["2027-01-01", "2027-01-06", ...]
}
```


vacances.json
Stocke tes données personnelles par année (créé automatiquement si absent, et les autres années sont toujours conservées).
Exemple :

```json
{
  "2026": {
    "jours_restants_annee_precedente": 5,
    "jours_total_annee": 30,
    "jours_restants_a_planifier": 25,
    "jours_selectionnes": ["2026-08-15", "2026-08-16"]
  },
  "2027": {
    "jours_restants_annee_precedente": 0,
    "jours_total_annee": 30,
    "jours_restants_a_planifier": 30,
    "jours_selectionnes": []
  }
}
```



## 🔧 Personnalisation

Modifier les jours fériés : Édite jours_feries.json.
Changer le style : Modifie le CSS dans index.html (section <style>).
Ajouter des années : Ajoute les dates dans jours_feries.json ; le menu déroulant se recentre automatiquement sur l'année en cours (±1).

## ⚠️ Notes

Navigateurs supportés : Opera, Chrome, Firefox, Edge.
Données persistantes : Les modifications sont enregistrées automatiquement dans vacances.json (après un court délai) ou immédiatement via le bouton 💾. Le nombre de jours restants à planifier est toujours recalculé (total − jours sélectionnés).
Pas de base de données : Ce projet utilise uniquement des fichiers JSON locaux.

## 🤝 Contribuer
Cet outil est intégré à la Portable Toolbox et non destiné à évoluer. Cependant, tu peux :

Adapter le code pour d'autres régions (en modifiant jours_feries.json).
Améliorer le design en éditant le CSS.

## 📜 Licence
Projet personnel – libre d'utilisation.
