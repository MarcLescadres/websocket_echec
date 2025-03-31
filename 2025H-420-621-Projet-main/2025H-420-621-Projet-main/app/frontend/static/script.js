console.log("Script chargé.")

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
    
    // Dessiner les pièces (par exemple les pions) sur le plateau (si nécessaire)
    drawPieces(ctx);
}

// Fonction pour dessiner des pièces (pour l'exemple, nous plaçons des pions sur les deux premières lignes)
function drawPieces(ctx) {
    const squareSize = 60;
    
    // Dessiner les pions blancs sur la ligne 2
    for (let col = 0; col < 8; col++) {
        drawPiece(ctx, col, 1, 'white'); // Pions blancs sur la ligne 2
    }
    
    // Dessiner les pions noirs sur la ligne 7
    for (let col = 0; col < 8; col++) {
        drawPiece(ctx, col, 6, 'black'); // Pions noirs sur la ligne 7
    }
}

// Fonction pour dessiner une pièce (ici, un simple cercle pour simuler une pièce)
function drawPiece(ctx, col, row, color) {
    const squareSize = 60;
    const radius = squareSize / 4;  // Taille de la pièce
    
    ctx.beginPath();
    ctx.arc((col * squareSize) + squareSize / 2, (row * squareSize) + squareSize / 2, radius, 0, 2 * Math.PI);
    ctx.fillStyle = color === 'white' ? '#FFFFFF' : '#000000';  // Blanc ou noir
    ctx.fill();
    ctx.stroke();  // Ajouter un contour pour la pièce
}
