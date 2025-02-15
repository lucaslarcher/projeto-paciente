import re
import string
import pandas as pd

# Lista ampliada de expressões desnecessárias para remoção
remover_frases = [
    r'\b(bom dia|boa tarde|boa noite|olá|oi|tudo bem|como vai)\b',  # Saudações
    r'\b(como posso ajudar\?|em que posso te ajudar\?|posso te ajudar com mais alguma coisa\?)\b',  # Perguntas padrão
    r'\b(aguarde um momento|vou verificar|estou analisando|um instante por favor)\b',  # Respostas automáticas
    r'\b(entendi|ok|certo|beleza|tá bom|ah tá|valeu)\b',  # Confirmações vazias
    r'\b(obrigado|obrigada|valeu|grato|de nada|por nada)\b',  # Agradecimentos
    r'\b(já verifico para você|estamos aqui para te ajudar|fico à disposição)\b',  # Frases repetitivas
    r'\b(só um minuto|só um momento|peraí|calma aí|espera um pouco)\b'  # Expressões irrelevantes
]

def limpar_texto(texto):
    if not isinstance(texto, str):
        return ""

    texto = texto.lower()  # Converter para minúsculas
    for padrao in remover_frases:
        texto = re.sub(padrao, '', texto, flags=re.IGNORECASE)  # Remover frases
    texto = texto.translate(str.maketrans('', '', string.punctuation))  # Remover pontuação
    return texto.strip()  # Remover espaços extras

def carregar_doencas():
    doencas_df = pd.read_csv('../data/seed_ciap_raw.csv')

    doencas_df = doencas_df[
        ['titulo original', 'CID10 mais frequente', 'definição', 'critérios de inclusão', 'critérios de exclusão']]

    doencas_df['informações'] = doencas_df.apply(
        lambda row: ' '.join([
            f"D:{row['titulo original']}" if pd.notna(row['titulo original']) else "",
            f"CID:{row['CID10 mais frequente']}" if pd.notna(row['CID10 mais frequente']) else "",
            f"CI:{row['critérios de inclusão']}" if pd.notna(row['critérios de inclusão']) else "",
            f"CE:{row['critérios de exclusão']}" if pd.notna(row['critérios de exclusão']) else ""
        ]).strip(),
        axis=1
    )

    return "\n".join(doencas_df['informações'].tolist())

carregar_doencas()
