import json
import pytest
import requests

BASE_URL = "http://127.0.0.1:8000"

@pytest.fixture
def paciente_id():
    return "3"

@pytest.fixture
def chat_data():
    return {
        "chat": "paciente: dor de cabeça, febre, espirro",
        "id_chat": "12345",
        "id_cliente": "3"
    }

def test_recuperando_paciente_id_api(paciente_id):
    url = f"{BASE_URL}/recuperar_paciente/{paciente_id}"
    response = requests.get(url)

    assert response.status_code == 200, f"Erro ao recuperar paciente. Status: {response.status_code}"

    try:
        response_json = response.json()
    except json.JSONDecodeError:
        pytest.fail("A resposta da API não é um JSON válido")

    assert "id" in response_json, "Resposta da API não contém a chave 'id'"

    print(f"Esperado: {paciente_id} ({type(paciente_id)}), Obtido: {response_json['id']} ({type(response_json['id'])})")

    assert str(response_json["id"]) == str(paciente_id), f"ID do paciente esperado era {paciente_id}, mas foi {response_json['id']}"


def test_processar_chat_api(chat_data):
    url = f"{BASE_URL}/processar_chat/"
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, data=json.dumps(chat_data), headers=headers)

    assert response.status_code == 200, f"Erro {response.status_code}: {response.text}"

    try:
        response_json = response.json()
    except json.JSONDecodeError:
        pytest.fail("A resposta da API não é um JSON válido")

    assert isinstance(response_json, dict), "A resposta da API deve ser um dicionário"
    assert "status" in response_json, "A resposta da API deve conter a chave 'status'"
    assert response_json["status"] in [True, False], "O valor de 'status' deve ser True ou False"