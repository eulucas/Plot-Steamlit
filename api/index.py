from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import os

app = FastAPI()

# Adicione o middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    # Execute o script Streamlit e capture a saída
    process = subprocess.Popen(
        ["streamlit", "run", "stock_visualizer.py", "--server.port=8501", "--server.headless=true"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Aguarde um pouco para o servidor Streamlit iniciar
    await asyncio.sleep(5)
    
    # Faça uma solicitação para o servidor Streamlit local
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8501")
    
    # Encerre o processo Streamlit
    process.terminate()
    
    # Retorne o conteúdo HTML do aplicativo Streamlit
    return HTMLResponse(content=response.text, status_code=200)
