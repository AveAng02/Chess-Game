
window.addEventListener("DOMContentLoaded", () => {

  const websocket = new WebSocket("ws://localhost:6789/");

  const messages = document.createElement("ul");
  document.body.appendChild(messages);

  // Array of text content for each chessboard cell
  const chessboardCells = document.querySelectorAll('.chessboard > div');

  const cellTexts = [
    "A1", "B1", "C1", "D1", "E1",
    "A2", "B2", "C2", "D2", "E2",
    "A3", "B3", "C3", "D3", "E3",
    "A4", "B4", "C4", "D4", "E4",
    "A5", "B5", "C5", "D5", "E5"
  ];

  const movesTiles = document.querySelectorAll('.moves > div');

  const moveCellText = [
    "TL", "T", "TR",
    "L", "", "R",
    "BL", "B", "BR"
  ];

  // UPDATES: Updating the webpage
  websocket.onmessage = ({ data }) => {
    const event = JSON.parse(data);
    switch (event.type) {
      case "game_history":
        // Updating the +- score
        // document.querySelector(".value").textContent = event.value[0];

        // Updating the game history log
        const message = document.createElement("li");
        const content = document.createTextNode(event.value);
        message.appendChild(content);
        messages.appendChild(message);

        // Updating the chessboard
        const indx = (event.value.charAt(0) - 65) * 5 + parseInt(event.value.charAt(1));

        break;
      case "users": // TODO: make players
        const users = `${event.count} user${event.count == 1 ? "" : "s"}`;
        document.querySelector(".users").textContent = users;
        break;
      default:
        console.error("unsupported event", event);
    }
  };

  // ACTIONS
  // Loop through each cell and assign the corresponding text
  // Get all the div elements inside the chessboard
  chessboardCells.forEach((cell, index) => {
    cell.textContent = cellTexts[index];
  });

  // Add event listeners for each cell to handle clicks
  chessboardCells.forEach((cell, index) => {
    cell.addEventListener('click', () => {
    const row = Math.floor(index / 5) + 1; // Calculate row index (1-based)
    const col = (index % 5) + 1; // Calculate column index (1-based)

      websocket.send(JSON.stringify({
        action: "board_button",
        position: { row: row, col: col }
      }));
    });
  });

  // Get all the div elements inside the moves box
  movesTiles.forEach((cell, index) => {
    cell.textContent = moveCellText[index];
  });

  // Add event listeners for each cell to handle clicks
  movesTiles.forEach((cell, index) => {
    cell.addEventListener('click', () => {
    const row = Math.floor(index / 3) + 1; // Calculate row index (1-based)
    const col = (index % 3) + 1; // Calculate column index (1-based)

      websocket.send(JSON.stringify({
        action: "move_button",
        position: { row: row, col: col }
      }));
    });
  });

  // for pressing plus button
  /*
  document.querySelector(".minus").addEventListener("click", () => {
    websocket.send(JSON.stringify({ action: "minus" }));
  });

  // for pressing minus button
  document.querySelector(".plus").addEventListener("click", () => {
    websocket.send(JSON.stringify({ action: "plus" }));
  });
  */
});
