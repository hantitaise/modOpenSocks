const ws = new WebSocket("ws://localhost:8000/ws/room1");

ws.onopen = () => console.log("Connected");
ws.onclose = () => setTimeout(() => location.reload(), 5000); // Auto-reconnect
ws.onmessage = (event) => console.log("Message received:", event.data);
