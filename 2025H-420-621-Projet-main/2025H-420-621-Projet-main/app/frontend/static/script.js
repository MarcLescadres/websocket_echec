window.onload = function() {
    const canvas = document.getElementById('chessboard');
    const ctx = canvas.getContext('2d');
    const squareSize = 60;

    // Charger le plateau d'échecs depuis l'API
    fetch('/initial/board')
        .then(response => response.json())
        .then(board => {
            drawBoard(ctx, board);
            drawPieces(ctx, board);
        })
        .catch(error => console.error("Erreur lors du chargement du plateau:", error));
};

function drawBoard(ctx, board) {
    const squareSize = 60;
    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
            // Inverser la logique de la couleur des cases pour que la case en bas à gauche soit noire
            const isDarkSquare = (row + col) % 2 === 1; // Inverser la condition
            ctx.fillStyle = isDarkSquare ? '#D18B47' : '#FFCE9E';
            ctx.fillRect(col * squareSize, row * squareSize, squareSize, squareSize);
        }
    }
}

function drawPieces(ctx, board) {
    const squareSize = 60;
    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
            const piece = board[row][col];
            if (piece !== ' ') {
                drawPiece(ctx, col, row, piece);
            }
        }
    }
}

function drawPiece(ctx, col, row, piece) {
    const squareSize = 60;
    const image = new Image();
    image.src = `/static/assets/${piece}.png`;  // Assurez-vous que les images sont dans le bon dossier

    image.onload = function() {
        ctx.drawImage(image, col * squareSize, row * squareSize, squareSize, squareSize);
    };
}