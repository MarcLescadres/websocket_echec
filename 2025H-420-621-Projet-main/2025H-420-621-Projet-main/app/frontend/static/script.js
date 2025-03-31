console.log("Script chargé.");

// S'assurer que le script est exécuté après le chargement complet de la page
window.onload = function() {
    console.log("Initialisation du jeu...");

    // Récupérer l'élément canvas et le contexte 2D pour dessiner dessus
    const canvas = document.getElementById('chessboard');
    if (!canvas) {
        console.error("Le canvas n'a pas pu être trouvé !");
        return;
    }
    const ctx = canvas.getContext('2d');
    if (!ctx) {
        console.error("Le contexte du canvas n'a pas pu être récupéré !");
        return;
    }

    // Appeler la fonction pour dessiner le plateau
    drawBoard(ctx);
};

// Fonction pour dessiner le plateau d'échecs
function drawBoard(ctx) {
    const squareSize = 60;  // Taille de chaque case (60px x 60px)

    // Dessiner chaque case du plateau
    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
            // Déterminer si la case est sombre ou claire
            const isDarkSquare = (row + col) % 2 === 0;
            
            // Définir la couleur de la case
            ctx.fillStyle = isDarkSquare ? '#D18B47' : '#FFCE9E';  // Couleurs alternées
            // Dessiner la case (colonne x ligne)
            ctx.fillRect(col * squareSize, row * squareSize, squareSize, squareSize);
        }
    }

    // Dessiner les pièces (par exemple les pions) sur le plateau
    drawPieces(ctx);
}

// Fonction pour dessiner des pièces avec des images
function drawPieces(ctx) {
    const squareSize = 60;

    // Dessiner les pions blancs sur la ligne 6 (de bas en haut)
    for (let col = 0; col < 8; col++) {
        drawPiece(ctx, col, 6, 'white', 'pawn'); // Pions blancs sur la ligne 6
    }

    // Dessiner les pions noirs sur la ligne 1 (de bas en haut)
    for (let col = 0; col < 8; col++) {
        drawPiece(ctx, col, 1, 'black', 'pawn'); // Pions noirs sur la ligne 1
    }

    // Dessiner les tours
    drawPiece(ctx, 0, 0, 'black', 'rook');
    drawPiece(ctx, 7, 0, 'black', 'rook');
    drawPiece(ctx, 0, 7, 'white', 'rook');
    drawPiece(ctx, 7, 7, 'white', 'rook');

    // Cavaliers
    drawPiece(ctx, 1, 0, 'black', 'knight');
    drawPiece(ctx, 6, 0, 'black', 'knight');
    drawPiece(ctx, 1, 7, 'white', 'knight');
    drawPiece(ctx, 6, 7, 'white', 'knight');

    // Fous
    drawPiece(ctx, 2, 0, 'black', 'bishop');
    drawPiece(ctx, 5, 0, 'black', 'bishop');
    drawPiece(ctx, 2, 7, 'white', 'bishop');
    drawPiece(ctx, 5, 7, 'white', 'bishop');

    // Reines
    drawPiece(ctx, 3, 0, 'black', 'queen');
    drawPiece(ctx, 3, 7, 'white', 'queen');

    // Rois
    drawPiece(ctx, 4, 0, 'black', 'king');
    drawPiece(ctx, 4, 7, 'white', 'king');
}

// Fonction pour dessiner une pièce avec une image
function drawPiece(ctx, col, row, color, type) {
    const squareSize = 60;
    const image = new Image();  // Créer un nouvel objet Image

    // Utiliser le chemin relatif vers l'image dans le dossier static/assets
    image.src = `/static/assets/${color} ${type}.png`;  // Utiliser /static/ comme base pour les fichiers statiques
    
    // Une fois l'image chargée, dessiner la pièce sur le canvas
    image.onload = function() {
        ctx.drawImage(image, col * squareSize, row * squareSize, squareSize, squareSize);
    };
}
