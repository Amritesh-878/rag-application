import asyncio
import json
import os
import sys
import websockets
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import webbrowser

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from core.rag_system import RAGSystem
    from utils.ingest import DocumentProcessor
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)


class WebHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=Path(__file__).parent.parent, **kwargs)

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.path = "/index.html"
        return super().do_GET()


class DocumentChatServer:
    def __init__(self, host="localhost", http_port=8000, ws_port=8765):
        self.host = host
        self.http_port = http_port
        self.ws_port = ws_port
        self.rag_system = RAGSystem()
        self.document_processor = DocumentProcessor()
        self.clients = set()

    async def handle_client(self, websocket):
        print(f"New client connected: {websocket.remote_address}")
        self.clients.add(websocket)
        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                    print(f"Received message: {data.get('type', 'unknown')}")
                    await self.process_message(websocket, data)
                except json.JSONDecodeError:
                    print("JSON decode error")
                    await websocket.send(
                        json.dumps({"type": "error", "message": "Invalid JSON format"})
                    )
                except Exception as e:
                    print(f"Error processing message: {e}")
                    await websocket.send(
                        json.dumps(
                            {"type": "error", "message": f"Server error: {str(e)}"}
                        )
                    )
        except Exception as e:
            print(f"Client connection error: {e}")
        finally:
            print(f"Client disconnected: {websocket.remote_address}")
            self.clients.remove(websocket)

    async def process_message(self, websocket, data):
        if data["type"] == "user_message":
            message = data["message"]

            await websocket.send(json.dumps({"type": "start"}))

            try:
                result = self.rag_system.query(message)

                if isinstance(result, dict):
                    response = result.get("answer", str(result))
                else:
                    response = str(result)

                for chunk in self.chunk_text(response, 10):
                    await websocket.send(json.dumps({"type": "stream", "delta": chunk}))
                    await asyncio.sleep(0.05)

                await websocket.send(json.dumps({"type": "done"}))

            except Exception as e:
                error_msg = f"Error processing your question: {str(e)}"
                await websocket.send(json.dumps({"type": "stream", "delta": error_msg}))
                await websocket.send(json.dumps({"type": "done"}))

    def chunk_text(self, text, chunk_size):
        for i in range(0, len(text), chunk_size):
            yield text[i : i + chunk_size]

    def start_http_server(self):
        def run_server():
            server = HTTPServer((self.host, self.http_port), WebHandler)
            print(f"HTTP server running on http://{self.host}:{self.http_port}")
            server.serve_forever()

        thread = threading.Thread(target=run_server, daemon=True)
        thread.start()

    async def start_websocket_server(self):
        print(f"WebSocket server starting on ws://{self.host}:{self.ws_port}")
        server = await websockets.serve(self.handle_client, self.host, self.ws_port)
        print("WebSocket server started successfully")
        return server

    def run(self, open_browser=True):
        self.start_http_server()

        if open_browser:
            threading.Timer(
                1.0, lambda: webbrowser.open(f"http://{self.host}:{self.http_port}")
            ).start()

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.start_websocket_server())
        loop.run_forever()


if __name__ == "__main__":
    server = DocumentChatServer()
    try:
        print("Starting Document Chat Server...")
        print("Features available:")
        print("- Document Q&A using RAG system")
        print("- Real-time chat interface")
        print("- Multi-conversation support")
        print("- Theme customization")
        server.run()
    except KeyboardInterrupt:
        print("\nShutting down server...")
