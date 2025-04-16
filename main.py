import json
import os
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from apscheduler.schedulers.background import BackgroundScheduler
from pathlib import Path
from importlib import import_module

app = FastAPI()

# Configuration logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("WebSocketServer")

# Gestion des salles
rooms = {"room1": [], "room2": []}  # Exemple de salles simulées

# Mémoire des connexions WebSocket
connections = {}

# Fonction pour charger dynamiquement les modules
def load_module(action):
    module_path = f"modules.{action}"
    if Path(f"modules/{action}.py").exists():
        return import_module(module_path)
    return None

@app.websocket("/ws/{room_name}")
async def websocket_endpoint(websocket: WebSocket, room_name: str):
    if room_name not in rooms:
        await websocket.close()
        return
    await websocket.accept()
    connections[websocket] = room_name
    rooms[room_name].append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"Received: {data}")
            message = json.loads(data)
            action = message["msg"]["header"]["act"]
            module = load_module(action)
            if not module:
                await websocket.send_json({"error": f"Action '{action}' not found"})
                continue
            result = module.handle(message)
            await websocket.send_json(result)
    except WebSocketDisconnect:
        rooms[room_name].remove(websocket)
        del connections[websocket]
        logger.info(f"Client disconnected from {room_name}")

# Interface admin pour logs
@app.get("/")
async def get_logs():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <body>
        <h1>Logs</h1>
        <div id="logs"></div>
        <script>
            const ws = new WebSocket("ws://localhost:8000/ws/admin");
            ws.onmessage = (event) => {
                const logs = document.getElementById("logs");
                logs.innerHTML += `<p>${event.data}</p>`;
            };
        </script>
    </body>
    </html>
    """)

@app.websocket("/ws/admin")
async def admin_logs(websocket: WebSocket):
    await websocket.accept()
    while True:
        await websocket.send_text("Log updated...")
