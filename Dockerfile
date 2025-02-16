# Etapa de construção do Docker
FROM python:3.10-alpine as build

# Setando o diretório de trabalho
WORKDIR /app

# Copiando os arquivos do projeto
COPY . .

# Instalando dependências
RUN pip install --no-cache-dir -r requirements.txt

# Rodando o script de inicialização dos dados
RUN python /app/src/utils/start.py

# Etapa final (onde a aplicação será executada)
FROM python:3.10-slim

# Setando o diretório de trabalho
WORKDIR /app

# Copiando os arquivos do projeto do estágio de construção
COPY --from=build /app /app

# Instalando dependências novamente para garantir que tudo esteja no container final
RUN pip install --no-cache-dir -r requirements.txt

# Copiando o script init.sh
COPY init.sh init.sh

# Tornando o script executável
RUN chmod +x init.sh

# Expõe a porta
EXPOSE 8000

# Comando que será executado quando o container iniciar
CMD ["/bin/bash", "-c", "./init.sh && uvicorn api.main:app --host 0.0.0.0 --reload"]
