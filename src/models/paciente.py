from pydantic import BaseModel

class Sintomas(BaseModel):
    sintomas: list[str]

class Doenca(BaseModel):
    doenca: str
    cid: str

class DoencaPaciente(BaseModel):
    doenca: Doenca
    explicacao: str

class Paciente(BaseModel):
    id: str
    chats: list[str]
    doencas: list[DoencaPaciente]