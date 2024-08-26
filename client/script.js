
window.addEventListener("DOMContentLoaded", () => {

  const messages = document.createElement("ul");
  document.body.appendChild(messages);

  const websocket = new WebSocket("ws://localhost:6789/");

  // for pressing plus button
  document.querySelector(".minus").addEventListener("click", () => {
    websocket.send(JSON.stringify({ action: "minus" }));
  });

  // for pressing minus button
  document.querySelector(".plus").addEventListener("click", () => {
    websocket.send(JSON.stringify({ action: "plus" }));
  });

  document.querySelectorAll(".chessboard > div").forEach(cell => {
    cell.addEventListener("click", () => {
      websocket.send(JSON.stringify({ action: "button" }));
    });
  });

  websocket.onmessage = ({ data }) => {
    const event = JSON.parse(data);
    switch (event.type) {
      case "value":
        document.querySelector(".value").textContent = event.value[0];
        const message = document.createElement("li");
        const content = document.createTextNode(event.value[1]);
        message.appendChild(content);
        messages.appendChild(message);
        break;
      case "users":
        const users = `${event.count} user${event.count == 1 ? "" : "s"}`;
        document.querySelector(".users").textContent = users;
        break;
      default:
        console.error("unsupported event", event);
    }
  };
});
