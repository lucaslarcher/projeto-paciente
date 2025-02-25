# Imagem base
FROM python:3.10-alpine

# Setando o diretório de trabalho
WORKDIR /app

# Copiando os arquivos do projeto
COPY . .

# Instalando dependências
RUN pip install --no-cache-dir -r requirements.txt

# Rodando o script de inicialização dos dados
#RUN python src/utils/start.py

# Tornando o script init.sh executável
#RUN chmod +x init.sh

# Expondo a porta da aplicação
EXPOSE 8000

# Comando que será executado ao iniciar o container
CMD ["sh", "-c", "uvicorn api.main:app --host 0.0.0.0 --reload"]
