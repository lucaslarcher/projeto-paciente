from fastapi import FastAPI, HTTPException

from src.models.paciente import Paciente

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API está rodando!"}

# Endpoint para recuperar paciente pelo id
@app.get("/paciente/{id}", response_model=Paciente)
def recuperar_paciente(id: str):
    paciente = recuperar_paciente(id)
    if paciente is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return paciente