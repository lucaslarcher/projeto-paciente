from openai import OpenAI
from src.models.paciente import Sintomas, Doenca, DoencaPaciente
import json
import re
import yaml
import os

# Recupera o caminho desse arquivo em específico
script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, '../../config/openai_api.yaml')
with open(config_path, "r") as arquivo:
    config = yaml.safe_load(arquivo)

api_key = config["generative_ai"]["api_key"]
model = config["generative_ai"]["model"]

if not api_key or not model:
    raise ValueError("API_KEY ou MODEL não foi encontrado no arquivo de configuração.")

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def extrair_sintomas(chat_texto: str) -> Sintomas:
    prompt = f"""
    Você é um médico especializado em análise de sintomas. Abaixo está um histórico de conversa entre um paciente, marcado como p, e um atendente, marcad com o a.

    Extraia e retorne apenas os principais sintomas mencionados pelo paciente na conversa.

    Responda com uma lista de sintomas separados por vírgula.

    Conversa:
    {chat_texto}

    Responda apenas com a lista de sintomas, sem explicações extras.
    """

    try:
        response = client.chat.completions.create(
            model=model,
            n=1,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        if response.choices and response.choices[0].message:
            sintomas_str = response.choices[0].message.content.strip()
        else:
            sintomas_str = ""

        sintomas_lista = sintomas_str.split(", ") if sintomas_str else []  # Converte para lista

        return Sintomas(sintomas=sintomas_lista)

    except Exception as e:
        print(f"Erro ao processar o chat: {e}")
        return Sintomas(sintomas=[])


def extrair_doencas(sintomas: Sintomas, doencas_criterios: str) -> list[DoencaPaciente]:
    sintomas_str = ", ".join(sintomas.sintomas) if sintomas.sintomas else "Nenhum sintoma fornecido"

    prompt = f"""
    Você é um médico especialista. O paciente apresenta os seguintes sintomas:
    {sintomas_str}

    Aqui estão as doenças possíveis, marcadas como D, o CID, marcado como CID, seus critérios de inclusão, marcados como CI, e exclusão, marcados como CE:
    {doencas_criterios}

    Baseado nos sintomas fornecidos e considerando os critérios de inclusão e exclusão, forneça uma doença compatível.

    **Formato da resposta (JSON válido obrigatório):**
    {{
        "doencas": [
            {{
                "doenca": "Nome da Doença",
                "cid": "Código CID",
                "explicacao": "Explicação breve da relação entre a doença e os sintomas"
            }},
            ...
        ]
    }}
    """

    try:
        response = client.chat.completions.create(
            model=model,
            n=1,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        if response.choices and response.choices[0].message:
            response_text = response.choices[0].message.content.strip()
        else:
            response_text = ""

        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            json_text = json_match.group(0)  # Pega apenas o JSON encontrado
        else:
            print("Erro: Nenhum JSON válido encontrado na resposta da IA.")
            return []

        try:
            parsed_response = json.loads(json_text)
            doencas_lista = parsed_response.get("doencas", [])
        except json.JSONDecodeError:
            print("Erro: A resposta da IA não está em formato JSON válido.")
            return []

        # Cria instâncias de Doenca e DoencaPaciente para todas as doenças retornadas
        doencas_formatadas = [
            Doenca(doenca=doenca["doenca"], cid=doenca["cid"]) for doenca in doencas_lista
        ]

        doenca_pacientes = [
            DoencaPaciente(
                doenca=doenca,
                explicacao=doenca["explicacao"] if "explicacao" in doenca else "Explicação não fornecida"  # Verifica a existência de "explicacao"
            )
            for doenca in doencas_lista
        ]

        return doenca_pacientes

    except Exception as e:
        print(f"Erro ao processar os sintomas: {e}")
        return []
