from pydantic import BaseModel

class Sintomas(BaseModel):
    sintomas: list[str]

class Doenca(BaseModel):
    doenca: str
    cid: str
    explicacao: str

class Doencas(BaseModel):
    doencas: list[Doenca]

class Paciente(BaseModel):
    id : str
    chats: list[str]
    doencas: Doencas