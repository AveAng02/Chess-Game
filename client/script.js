const ws = new WebSocket("ws://localhost:8080"); // Replace with your server address and port

const messageInput = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");

const buttons = document.querySelectorAll(".btn-secondary"); // Select all secondary buttons

// Function to send the button ID
function sendButtonId(buttonId) {
  if (ws.readyState === WebSocket.OPEN) {
    ws.send(buttonId);
  } else {
    console.error("WebSocket connection not open!");
  }
}

// Add click event listener to all secondary buttons
buttons.forEach((button) => {
  button.addEventListener("click", () => {
    const buttonId = button.id; // Get the button ID
    sendButtonId(buttonId); // Send the button ID to the server
  });
});

// Handle WebSocket events (optional)
ws.onopen = () => {
  console.log("WebSocket connection opened!");
};

ws.onmessage = (event) => {
  console.log("Received message: ", event.data);
};

ws.onerror = (error) => {
  console.error("WebSocket error: ", error);
};

ws.onclose = () => {
  console.log("WebSocket connection closed!");
};