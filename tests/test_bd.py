from service.data_models import Paciente, Doenca, Doencas
from service.banco_de_dados import salvar_paciente_json, carregar_paciente_json


def test_salvar_paciente():
    paciente = Paciente(
        id="123",
        chats=["chat1", "chat2"],
        doencas=Doencas(doencas=[
            Doenca(doenca="Hipertensão", cid="I10", explicacao="Pressão alta"),
            Doenca(doenca="Diabetes", cid="E11", explicacao="Nível alto de açúcar no sangue")
        ])
    )
    salvar_paciente_json(paciente)

def test_carregar_paciente():
    print(carregar_paciente_json("123"))

test_salvar_paciente()
test_carregar_paciente()