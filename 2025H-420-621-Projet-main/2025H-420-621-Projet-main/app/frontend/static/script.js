let canvas = null;
let boardState = null;
let boardFlipped = false;

window.onload = function () {
    canvas = document.getElementById('chessboard');
    const ctx = canvas.getContext('2d');
    const squareSize = 60;
    const socket = io();

    const btnMulti = document.getElementById("btn-multiplayer");
    const btnAI = document.getElementById("btn-ai");
    const form = document.getElementById("player-form");
    const nameInput = document.getElementById("player-name");
    const submitBtn = document.getElementById("submit-name");
    const info = document.getElementById("info");
    const abandonBtn = document.createElement("button");
    abandonBtn.innerText = "Abandonner la partie";
    abandonBtn.style.display = "none";
    abandonBtn.style.marginTop = "10px";
    document.body.appendChild(abandonBtn);

    let playerName = "";
    let myColor = null;
    let canPlay = false;
    let multiplayerRequested = false;
    let currentTurn = "white";

    btnMulti.onclick = () => {
        multiplayerRequested = true;
        btnMulti.style.display = "none";
        btnAI.style.display = "none";
        form.style.display = "block";
    };

    submitBtn.onclick = () => {
        playerName = nameInput.value.trim();
        if (playerName !== "" && multiplayerRequested) {
            socket.emit("register_name", { name: playerName });
            form.style.display = "none";
            canvas.style.display = "block";
            abandonBtn.style.display = "inline-block";
            fetch('/initial/board')
                .then(response => response.json())
                .then(board => {
                    boardState = board;
                    drawBoard(ctx, board);
                    drawPieces(ctx, board);
                })
                .catch(error => console.error("Erreur lors du chargement du plateau:", error));
        }
    };

    abandonBtn.onclick = () => {
        socket.emit("player_abandon");
        alert("Vous avez abandonné la partie.");
        location.reload();
    };

    socket.on("player_list", (players) => {
        if (!multiplayerRequested) return;
        const me = players[socket.id];
        if (me) {
            myColor = me.color;
            boardFlipped = (myColor === "black");

            const opponents = Object.values(players).filter(p => p.color !== me.color && p.color !== "spectator").map(p => p.name);
            const opponent = opponents.length > 0 ? opponents[0] : null;

            if (myColor === "spectator") {
                canPlay = false;
                info.innerText = "Mode spectateur";
            } else {
                canPlay = true;
                info.innerText = `Vous êtes ${playerName} (${myColor}). Adversaire: ${opponent || "En attente..."}`;
            }
        }
    });

    socket.on('opponent_abandoned', () => {
        alert("Votre adversaire a abandonné la partie. Vous avez gagné !");
        location.reload();
    });

    socket.on("victory_checkmate", () => {
        alert("Vous avez gagné par échec et mat !");
        location.reload();
    });

    socket.on("defeat_checkmate", () => {
        alert("Vous avez perdu par échec et mat.");
        location.reload();
    });

    socket.on('board_update', (data) => {
        const updatedBoard = data.board;
        boardState = updatedBoard;

        const fromX = data.from_x;
        const fromY = data.from_y;
        const toX = data.to_x;
        const toY = data.to_y;

        if (data.reason === "prise en passant") {
            const direction = (fromX < toX) ? -1 : 1;
            const capturedX = toX + direction;
            const capturedY = toY;
            drawSquare(ctx, capturedX, capturedY);
            drawPieceAt(ctx, capturedX, capturedY, updatedBoard[capturedX][capturedY]);
        }

        drawSquare(ctx, fromX, fromY);
        drawPieceAt(ctx, fromX, fromY, updatedBoard[fromX][fromY]);
        drawSquare(ctx, toX, toY);
        drawPieceAt(ctx, toX, toY, updatedBoard[toX][toY]);

        if (Math.abs(fromY - toY) === 2) {
            if (toY < fromY) {
                drawSquare(ctx, toX, 0);
                drawPieceAt(ctx, toX, 0, updatedBoard[toX][0]);
                drawSquare(ctx, toX, toY + 1);
                drawPieceAt(ctx, toX, toY + 1, updatedBoard[toX][toY + 1]);
            } else {
                drawSquare(ctx, toX, 7);
                drawPieceAt(ctx, toX, 7, updatedBoard[toX][7]);
                drawSquare(ctx, toX, toY - 1);
                drawPieceAt(ctx, toX, toY - 1, updatedBoard[toX][toY - 1]);
            }
        }
    });

    socket.on('move_error', (data) => {
        console.error('Erreur de mouvement:', data.error);
        alert("Erreur : " + data.error);
    });

    let selectedPiece = null;

    canvas.addEventListener('click', function (event) {
        if (!canPlay) return;

        const rect = canvas.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;

        let col = Math.floor(x / squareSize);
        let row = Math.floor(y / squareSize);

        const realRow = boardFlipped ? 7 - row : row;
        const realCol = boardFlipped ? 7 - col : col;

        if (selectedPiece) {
            const piece = boardState?.[selectedPiece.row]?.[selectedPiece.col];
            if (piece && !piece.startsWith(myColor)) {
                alert("Vous ne pouvez déplacer que vos propres pièces.");
                selectedPiece = null;
                return;
            }

            const moveData = {
                from_x: selectedPiece.row,
                from_y: selectedPiece.col,
                to_x: realRow,
                to_y: realCol
            };
            socket.emit('move_piece', moveData);
            selectedPiece = null;
        } else {
            selectedPiece = { row: realRow, col: realCol };
        }
    });
};

function drawBoard(ctx, board) {
    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
            drawSquare(ctx, row, col);
        }
    }
}

function drawSquare(ctx, row, col) {
    const squareSize = 60;
    let drawRow = boardFlipped ? 7 - row : row;
    let drawCol = boardFlipped ? 7 - col : col;
    const isDark = (drawRow + drawCol) % 2 === 1;
    ctx.fillStyle = isDark ? '#D18B47' : '#FFCE9E';
    ctx.fillRect(drawCol * squareSize, drawRow * squareSize, squareSize, squareSize);
}

function drawPieces(ctx, board) {
    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
            drawPieceAt(ctx, row, col, board[row][col]);
        }
    }
}

function drawPieceAt(ctx, row, col, piece) {
    const squareSize = 60;
    if (piece && piece !== " ") {
        const drawRow = boardFlipped ? 7 - row : row;
        const drawCol = boardFlipped ? 7 - col : col;
        const image = new Image();
        image.src = `/static/assets/${piece}.png`;
        image.onload = function () {
            ctx.drawImage(image, drawCol * squareSize, drawRow * squareSize, squareSize, squareSize);
        };
    }
}