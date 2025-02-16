from fastapi import FastAPI, HTTPException
from starlette.responses import JSONResponse

from src.models.paciente import Paciente
from src.utils.pipeline import pipeline_entrada_chat
from src.utils.database import buscar_paciente_por_id
app = FastAPI()

@app.get("/")
def home():
    return {"message": "API está rodando!"}

@app.get("/recuperar_paciente/{id}", response_model=Paciente)
def recuperar_paciente(id: str):
    paciente = buscar_paciente_por_id(id)  # Replace this with the actual function to retrieve the patient
    if paciente is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return paciente

from pydantic import BaseModel

class ChatRequest(BaseModel):
    chat: str
    id_chat: str
    id_cliente: str

@app.post("/processar_chat/")
def processar_chat(data: ChatRequest):
    print(data.chat)
    resultado = pipeline_entrada_chat(data.chat, data.id_chat, data.id_cliente)
    if resultado:
        return {"message": "Chat processado com sucesso!", "status": True}
    else:
        return {"message": "Falha ao processar o chat.", "status": False}

