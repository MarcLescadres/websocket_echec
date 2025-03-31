# Projet d'échecs - Semaine 1

## Objectifs de la semaine
Cette semaine, vous commencerez à implémenter les premières fonctionnalités de votre jeu d’échecs. Vous allez :
- Afficher un plateau de jeu d'échecs 8x8 avec les pièces aux bonnes positions de départ.
- Mettre en place la communication entre le frontend et le backend en utilisant des WebSockets.
- Gérer les clics de souris et afficher un message dans la console indiquant la case cliquée.
---
## Structure du projet et démarrage de l'application

Voir la structure du projet dans le fichier **README.md**. Cette structure contient déjà les fichiers nécessaires et les répertoires pour les templates, les fichiers statiques et les scripts Python.

Le **README.md** contiendra également les instructions pour démarrer l'application.

Votre code sera évalué en fonction de sa propreté et de la logique utilisée pour organiser votre projet.

---

## Détails des objectifs de cette semaine
### Afficher un plateau de jeu d'échecs 8x8 avec les pièces aux bonnes positions de départ
Créer un **plateau de jeu interactif** où chaque case peut être cliquée pour déplacer une pièce d'échecs.

### Détails :
- Le plateau doit être composé de **64 cases** (8x8) avec des couleurs alternées (noir/blanc ou autre).
- Chaque case doit avoir une taille de **60x60 pixels**.
- Implémentez l'affichage des **pièces d’échecs** sur le plateau. Les pièces doivent être représentées par des images, que vous pouvez télécharger ou dessiner. (ex.: https://greenchess.net/info.php?item=downloads )

#### Pièces à implémenter :
- **Pion (Pawn)** : Noir et Blanc
- **Tour (Rook)** : Noir et Blanc
- **Cavalier (Knight)** : Noir et Blanc
- **Fou (Bishop)** : Noir et Blanc
- **Reine (Queen)** : Noir et Blanc
- **Roi (King)** : Noir et Blanc

Vous pouvez placer les images des pièces dans le dossier `frontend/static/assets/` (par exemple : `black_pawn.png`, `white_pawn.png`, etc.).

### Mettre en place la communication entre le frontend et le backend en utilisant des WebSockets

- Utilisez **WebSockets** pour permettre la communication entre le backend (serveur Flask ou autre) et le frontend (HTML/CSS/Javascript)
- Pour ce premier travail, la communication sera limitée (principalement reliée à l'initialisation du plateau de jeu). Cependant, il est important de mettre la logique en place pour les prochaines semaines.

### Conseils :
- Dans `websockets.py` se trouvera la logique de connexion et d'envoi/recevoir de messages via WebSockets pour le côté backend.
- Dans `script.js` se trouvera la logique de connexion et d'envoi/recevoir de messages via WebSockets pour le côté frontend.
- Dans `app.py`, vous pouvez initialiser le serveur Flask et ajouter le serveur WebSocket pour gérer les connexions.


### Gérer les clics de souris et afficher un message dans la console indiquant la case cliquée
Du côté frontend, implémentez une gestion de base des clics de souris. Vous devrez faire les calculs pour savoir dans quelle case le clic a été fait. Voici quelques étapes pour vous aider:

1. Ajoutez un écouteur d'événements click sur le plateau d'échecs dans `script.js`.
2. Récupérez les coordonnées du clic en utilisant `event.clientX` et `event.clientY`.
3. Convertissez ces coordonnées en indices de la grille (ligne et colonne).
4. Affichez ces indices dans la console avec `console.log("Case cliquée : ", ligne, colonne);`.

Exemple de code (fichier `script.js`):
``` javascript
const board = document.getElementById("chessboard");
board.addEventListener("click", function(event) {
    const rect = board.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    const col = Math.floor(x / 60); // Case de 60px
    const row = Math.floor(y / 60);
    console.log("Case cliquée :", row, col);
});
```

---
## **Restrictions**
- **Obligatoire** :
  - Utiliser WebSockets pour la communication entre le backend et le frontend.
- **Libre à vous** :
  - Vous pouvez modifier le gabarit de solution fourni ou créer votre propre structure.
  - Vous pouvez utiliser Pygame, Canvas, ou HTML/CSS pour l'affichage du plateau.

**Note sur l'utilisation de l'IA:**
L'utilisation de l'IA est autorisée et même encouragée pour vous aider dans votre travail. Cependant, lors de l'évaluation finale, vous devrez être en mesure d'expliquer votre code, justifier vos choix de conception et répondre à des questions sur son fonctionnement. Assurez-vous donc de bien comprendre ce que vous utilisez, comme dans un contexte professionnel réel.  

---

## **Étapes suggérées**

1. **Affichage du plateau**
   - Complétez `frontend/static/script.js` et `frontend/templates/index.html` pour utiliser un `canvas` qui affichera une grille 8x8.
   - Ajustez le CSS si nécessaire pour styliser le plateau (`frontend/static/style.css`).
  
2. **Logique de jeu**
   - Ajoutez la logique nécessaire aux classes Game et Board pour l'initialisation du plateau et des pièces.
   - Ajoutez l'initialisation des objets aux bons endroits
  
3. **Mise en place des WebSockets**
   - Dans `app.py`, faites l'initialisation de SocketIO et lancez l'application avec socketio.
   - Dans `script.js`, utilisez `socket.emit("get_board");` pour demander l’état du jeu.
   - Dans `websockets.py`, ajoutez un événement `@socketio.on("get_board")` pour envoyer le plateau au frontend, soit envoyer un `socket.emit("update_board")`
   - Ajoutez `socket.on("update_board", function(data) {...});` pour recevoir et afficher les mises à jour du plateau.
     En premier, ne faites que l'affichage de message dans ces fonctions pour vous assurer qu'elles sont bien appelées. Ensuite, rajoutez la logique et l'envoi d'informations.

3. **Ajout des pièces sur le plateau**
   - Complétez `script.js` pour afficher les images des pièces.
   - Vérifiez que les pièces sont bien placées au chargement.

4. **Gestion des événements de clic**
   - Dans `script.js`, écoutez les clics sur le plateau.
   - Affichez dans la console les coordonnées de la case cliquée.


---
## **Conseils et bonnes pratiques**

- **Utiliser `console.log` + Inspecteur de navigateur** :
  - Ouvrir la console avec `F12` (ou `Ctrl + Shift + I` sur Chrome/Firefox) pour voir les erreurs et les logs.
  - `console.log(variable);` est votre ami.

- **WebSockets** :
  - Un `socket.on("event", function(data) {...})` doit être accompagné d’un `socket.emit("event", data);` dans un autre fichier.

- **Représenter le jeu en interne** :
  - Utiliser un tableau 2D (`board[8][8]`) pour stocker l’état du jeu.

---

## **Livrable pour cette semaine**

- Un **journal de bord** décrivant :
  - Quels fichiers ont été remplis.
  - Quelles fonctionnalités ont été implémentées.
  - Quelles difficultés ont été rencontrées.

Le journal de bord doit être déposé dans Léa au plus tard le dimanche 6 avril à minuit.
