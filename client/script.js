
window.addEventListener("DOMContentLoaded", () => {

  const websocket = new WebSocket("ws://localhost:6789/");

  const messages = document.createElement("ul");
  document.body.appendChild(messages);

  // Array of text content for each chessboard cell
  const chessboardCells = document.querySelectorAll('.chessboard > div');

  var cellTexts = [
    "A1", "B1", "C1", "D1", "E1",
    "A2", "B2", "C2", "D2", "E2",
    "A3", "B3", "C3", "D3", "E3",
    "A4", "B4", "C4", "D4", "E4",
    "A5", "B5", "C5", "D5", "E5"
  ];

  const movesTiles = document.querySelectorAll('.moves > div');

  const moveCellText = [
    "FL", "F", "FR",
    "L", "", "R",
    "BL", "B", "BR"
  ];

  // UPDATES: Updating the webpage
  websocket.onmessage = ({ data }) => {
    const event = JSON.parse(data);
    switch (event.type) {
      case "game_history":
        // Updating the game history log
        const message = document.createElement("li");
        const content = document.createTextNode(event.value);
        message.appendChild(content);
        messages.appendChild(message);
        break;

      case "board_update":
        // a string with each word seperated by space 
        // and only the empty cells maked as None
        const str = event.value;
        var arr = str.split(/\s+/).filter(Boolean);

        for (var i = 0; i < data.length; i++){
          if (arr[i] != "None")
            cellTexts[i] = arr[i];
          else
            cellTexts[i] = " ";
        }
        chessboardCells.forEach((cell, index) => {
          cell.textContent = cellTexts[index];
        });
        break;
      
      case "users": // TODO: make players
        const users = `${event.count} sessions${event.count == 1 ? "" : "s"}`;
        document.querySelector(".users").textContent = users;
        break;
      default:
        console.error("unsupported event", event);
    }
  };

  // ACTIONS
  // Loop through each cell and assign the corresponding text
  // Get all the div elements inside the chessboard
  // Function to wait for a chessboard click and return the position
  function waitForChessboardClick() {
    return new Promise((resolve) => {
      chessboardCells.forEach((cell, index) => {
        const row = Math.floor(index / 5) + 1;
        const col = (index % 5) + 1;

        const clickHandler = () => {
          resolve({ row, col });

          // Remove all chessboard event listeners after the first click
          chessboardCells.forEach((c) => c.removeEventListener('click', clickHandler));
        };

        cell.addEventListener('click', clickHandler);
      });
    });
  }

  // Function to wait for a move tile click and return the position
  function waitForMoveClick() {
    return new Promise((resolve) => {
      movesTiles.forEach((cell, index) => {
        const row = Math.floor(index / 3) + 1;
        const col = (index % 3) + 1;

        const clickHandler = () => {
          resolve({ row, col });

          // Remove all move tile event listeners after the first click
          movesTiles.forEach((c) => c.removeEventListener('click', clickHandler));
        };

        cell.addEventListener('click', clickHandler);
      });
    });
  }

  // Main function to handle the click sequence
  async function handleClicks() {
    while (true) {  // Loop indefinitely to handle multiple click sequences
      const boardPosition = await waitForChessboardClick();
      const movePosition = await waitForMoveClick();

      websocket.send(JSON.stringify({
        event_type: "game_life_event",
        boardPosition: boardPosition,
        movePosition: movePosition
      }));
    }
  }

  // Initialize the board and moves with their text content
  chessboardCells.forEach((cell, index) => {
    cell.textContent = cellTexts[index];
  });

  movesTiles.forEach((cell, index) => {
    cell.textContent = moveCellText[index];
  });

  // Start handling clicks
  handleClicks();

  document.querySelector(".start_game_button").addEventListener("click", () => {
    websocket.send(JSON.stringify({ event_type: "session_life_event",
                                    action: "start_game_button_pressed" }));
  });
});
