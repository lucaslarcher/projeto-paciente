import pytest
from src.models.paciente import Paciente, Doenca, DoencaPaciente
from src.utils.database import inserir_paciente, buscar_paciente_por_id, remover_paciente


@pytest.fixture
def paciente_exemplo():
    return Paciente(
        id="3",
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


def test_inserir_paciente(paciente_exemplo):
    inserir_paciente(paciente_exemplo)
    paciente_recuperado = buscar_paciente_por_id(paciente_exemplo.id)

    assert paciente_recuperado is not None, "Paciente não foi inserido corretamente"
    assert paciente_recuperado.id == paciente_exemplo.id, "ID do paciente recuperado não corresponde"
    assert len(paciente_recuperado.doencas) == len(paciente_exemplo.doencas), "Número de doenças não corresponde"


def test_recuperar_paciente(paciente_exemplo):
    inserir_paciente(paciente_exemplo)
    paciente_recuperado = buscar_paciente_por_id(paciente_exemplo.id)

    assert paciente_recuperado is not None, "Paciente não encontrado"
    assert paciente_recuperado.id == "3", "ID do paciente incorreto"


def test_remover_paciente(paciente_exemplo):
    inserir_paciente(paciente_exemplo)
    remover_paciente(paciente_exemplo.id)
    paciente_removido = buscar_paciente_por_id(paciente_exemplo.id)

    assert paciente_removido is None, "Paciente não foi removido corretamente"