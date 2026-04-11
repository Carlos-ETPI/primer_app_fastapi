from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from openpyxl import Workbook
import time

app = FastAPI()

@app.get("/")
async def get():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Barra de Progreso</title>
    </head>
    <body>
        <h1>Generar Excel con Progreso</h1>
        <button onclick="startProgress()">Generar Excel</button>
        <div id="progress"></div>
        <script>
            const progressDiv = document.getElementById("progress");

            async function startProgress() {
                const socket = new WebSocket("ws://localhost:8000/ws");

                socket.onmessage = (event) => {
                    progressDiv.innerHTML = event.data;
                };

                socket.onclose = () => {
                    progressDiv.innerHTML += "<br>Archivo generado con éxito.";
                };
            }
        </script>
    </body>
    </html>
    """)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    # Crear el archivo Excel
    nombre_archivo = "archivo_generado_websocket.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.title = "Datos"

    # Escribir encabezados
    ws.append(["ID", "Nombre", "Edad"])

    total = 100  # Número de filas

    # Escribir datos y enviar progreso
    for i in range(1, total + 1):
        ws.append([i, f"Nombre_{i}", 20 + (i % 10)])
        porcentaje = (i / total) * 100
        barra = '█' * int(porcentaje // 2) + '-' * (50 - int(porcentaje // 2))
        await websocket.send_text(f"[{barra}] {porcentaje:.2f}%")
        time.sleep(0.1)  # Simula un proceso que tarda tiempo

    # Guardar el archivo
    wb.save(nombre_archivo)
    await websocket.close()