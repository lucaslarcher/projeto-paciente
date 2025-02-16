#!/bin/bash

# Verifica se o banco de dados já existe
if [ ! -f /app/src/data/projeto_paciente.db ]; then
  echo "Banco de dados não encontrado. Executando inicialização."
  # Executa a função de inicialização do banco
  python /app/src/utils/start.py
else
  echo "Banco de dados já existe. Pulando a inicialização."
fi

# Agora sobe o uvicorn para rodar a API
echo "Subindo a API com Uvicorn..."
uvicorn api.main:app --host 0.0.0.0 --reload