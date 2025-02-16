from src.models.paciente import Paciente, Doenca, DoencaPaciente
from src.utils.database import inserir_paciente, buscar_paciente_por_id, remover_paciente


def teste_inserir_paciente():
    paciente_exemplo = Paciente(
        id="123",
        chats=["chat001"],
        doencas=[
            DoencaPaciente(
                doenca=Doenca(doenca="Cólera", cid="A00"),
                explicacao="Paciente apresenta sintomas graves de diarreia e desidratação."
            ),
            DoencaPaciente(
                doenca=Doenca(doenca="Gripe", cid="J10"),
                explicacao="Paciente tem febre e tosse seca há 3 dias."
            ),
        ],
    )

    inserir_paciente(paciente_exemplo)


def teste_recuperar_paciente():
    # Teste de busca
    paciente_recuperado = buscar_paciente_por_id("123")
    print(paciente_recuperado)

def teste_remover_paciente():

    paciente = Paciente(
        id="123",
        chats=["chat1"],
        doencas=[DoencaPaciente(doenca=Doenca(cid="D1", doenca="Diabetes"), explicacao="Explicação diabetes")]
    )
    inserir_paciente(paciente)
    print("Paciente inserido.")

    # Agora, tentar remover o paciente
    remover_paciente("123")

    # Verificar se o paciente foi removido
    paciente_removido = buscar_paciente_por_id("123")
    if paciente_removido:
        print("Paciente ainda encontrado.")
    else:
        print("Paciente removido com sucesso.")

teste_inserir_paciente()
#teste_recuperar_paciente()
#teste_remover_paciente()