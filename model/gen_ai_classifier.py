from openai import OpenAI
from service.data_models import Sintomas, Doenca, Doencas
import os
from dotenv import load_dotenv
import json
import re

caminho_env = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
load_dotenv(caminho_env)

api_key = os.getenv("API_KEY")
model = os.getenv("MODEL")

if not api_key or not model:
    raise ValueError("API_KEY ou MODEL não foi encontrado no .env")

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def extrair_sintomas(chat_texto):
    prompt = f"""
    Você é um médico especializado em análise de sintomas. Abaixo está um histórico de conversa entre um paciente e um atendente.

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

        # Verifica se há escolhas e mensagens antes de acessar os atributos
        if response.choices and response.choices[0].message:
            sintomas_str = response.choices[0].message.content.strip()  # Correção aqui
        else:
            sintomas_str = ""

        sintomas_lista = sintomas_str.split(", ") if sintomas_str else []  # Converte para lista

        return Sintomas(sintomas=sintomas_lista)

    except Exception as e:
        print(f"Erro ao processar o chat: {e}")
        return Sintomas(sintomas=[])



def extrair_doencas(sintomas: Sintomas, doencas_criterios: str):
    sintomas_str = ", ".join(sintomas.sintomas) if sintomas.sintomas else "Nenhum sintoma fornecido"

    prompt = f"""
    Você é um médico especialista. O paciente apresenta os seguintes sintomas:
    {sintomas_str}

    Aqui estão as doenças possíveis, marcadas como D, o CID, marcado como CID, seus critérios de inclusão, marcados como CI, e exclusão, marcados como CE:
    {doencas_criterios}

    Baseado nos sintomas fornecidos e considerando os critérios de inclusão e exclusão, forneça as doenças compatíveis.

    **Formato da resposta (JSON válido obrigatório):**
    {{
        "doencas": [
            {{
                "doenca": "Nome da Doença",
                "cid": "Código CID",
                "explicacao": "Explicação breve da relação entre a doença e os sintomas"
            }}
        ]
    }}
    """

    try:
        response = client.chat.completions.create(
            model="gemini-2.0-flash",
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
            return Doencas(doencas=[])

        try:
            parsed_response = json.loads(json_text)
            doencas_lista = parsed_response.get("doencas", [])
        except json.JSONDecodeError:
            print("Erro: A resposta da IA não está em formato JSON válido.")
            return Doencas(doencas=[])

        doencas_formatadas = [Doenca(**doenca) for doenca in doencas_lista]

        return Doencas(doencas=doencas_formatadas)

    except Exception as e:
        print(f"Erro ao processar o chat: {e}")
        return Doencas(doencas=[])