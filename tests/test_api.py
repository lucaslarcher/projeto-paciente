import json

import requests

def teste_recuperando_paciente_id_api():
    url_get = "http://127.0.0.1:8000/recuperar_paciente/123"
    # Realizando a requisição GET
    response_get = requests.get(url_get)
    # Verificando a resposta
    if response_get.status_code == 200:
        print("Paciente encontrado:", response_get.json())
    else:
        print("Erro ao recuperar paciente. Status:", response_get.status_code)


def teste_processar_chat_api():
    url = "http://127.0.0.1:8000/processar_chat/"
    data = {
        "chat": "paciente: dor de cabeça, febre, espirro",
        "id_chat": "12345",
        "id_cliente": "67890"
    }

    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)

    print(f"Request sent: {json.dumps(data, indent=2)}")
    print(f"Response status code: {response.status_code}")
    if response.status_code == 200:
        print("Resposta da API:", response.json())
    else:
        print(f"Erro {response.status_code}: {response.text}")

#teste_recuperando_paciente_id_api()
teste_processar_chat_api()