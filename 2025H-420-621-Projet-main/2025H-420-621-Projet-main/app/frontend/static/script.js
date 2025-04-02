window.onload = function () {
    const canvas = document.getElementById('chessboard');
    const ctx = canvas.getContext('2d');
    const squareSize = 60;

    // Connexion WebSocket à l'origine actuelle
    const socket = io();

    // Charger le plateau d'échecs depuis l'API
    fetch('/initial/board')
        .then(response => response.json())
        .then(board => {
            drawBoard(ctx, board);
            drawPieces(ctx, board);
        })
        .catch(error => console.error("Erreur lors du chargement du plateau:", error));

    // Écouter les mises à jour du plateau (après un mouvement)
    socket.on('board_update', (data) => {
        const updatedBoard = data.board;

        const fromX = data.from_x;
        const fromY = data.from_y;
        const toX = data.to_x;
        const toY = data.to_y;

        // Redessiner uniquement les cases impactées (roi)
        drawSquare(ctx, fromX, fromY);
        drawPieceAt(ctx, fromX, fromY, updatedBoard[fromX][fromY]);

        drawSquare(ctx, toX, toY);
        drawPieceAt(ctx, toX, toY, updatedBoard[toX][toY]);

        // 🔄 Mise à jour spéciale pour le roque (roi a bougé de 2 cases horizontalement)
        if (Math.abs(fromY - toY) === 2) {
            // Grand roque
            if (toY < fromY) {
                // Efface l'ancienne tour (coin gauche)
                drawSquare(ctx, toX, 0);
                drawPieceAt(ctx, toX, 0, updatedBoard[toX][0]);

                // Affiche la tour à sa nouvelle position
                drawSquare(ctx, toX, toY + 1);
                drawPieceAt(ctx, toX, toY + 1, updatedBoard[toX][toY + 1]);
            }
            // Petit roque
            else {
                // Efface l'ancienne tour (coin droit)
                drawSquare(ctx, toX, 7);
                drawPieceAt(ctx, toX, 7, updatedBoard[toX][7]);

                // Affiche la tour à sa nouvelle position
                drawSquare(ctx, toX, toY - 1);
                drawPieceAt(ctx, toX, toY - 1, updatedBoard[toX][toY - 1]);
            }
        }
    });

    // Écouter les erreurs de mouvement
    socket.on('move_error', (data) => {
        console.error('Erreur de mouvement:', data.error);
        alert("Erreur : " + data.error);
    });

    let selectedPiece = null;

    // Écouter les clics pour déplacer les pièces
    canvas.addEventListener('click', function (event) {
        const rect = canvas.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;

        const col = Math.floor(x / squareSize);
        const row = Math.floor(y / squareSize);

        if (selectedPiece) {
            console.log(`From (${selectedPiece?.row}, ${selectedPiece?.col}) → (${row}, ${col})`);

            const moveData = {
                from_x: selectedPiece.row,
                from_y: selectedPiece.col,
                to_x: row,
                to_y: col
            };
            socket.emit('move_piece', moveData);
            selectedPiece = null;
        } else {
            selectedPiece = { row: row, col: col };
        }
    });
};

// 🔳 Dessine le plateau complet (si besoin au début)
function drawBoard(ctx, board) {
    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
            drawSquare(ctx, row, col);
        }
    }
}

// 🧱 Dessine une seule case (fond clair ou foncé)
function drawSquare(ctx, row, col) {
    const squareSize = 60;
    const isDark = (row + col) % 2 === 1;
    ctx.fillStyle = isDark ? '#D18B47' : '#FFCE9E';
    ctx.fillRect(col * squareSize, row * squareSize, squareSize, squareSize);
}

// 🧩 Dessine toutes les pièces du plateau (au chargement initial)
function drawPieces(ctx, board) {
    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
            drawPieceAt(ctx, row, col, board[row][col]);
        }
    }
}

// ♟️ Dessine une pièce si présente
function drawPieceAt(ctx, row, col, piece) {
    const squareSize = 60;
    if (piece && piece !== " ") {
        const image = new Image();
        image.src = `/static/assets/${piece}.png`;

        image.onload = function () {
            ctx.drawImage(image, col * squareSize, row * squareSize, squareSize, squareSize);
        };
    }
}
