#!/bin/bash

# Verifica se o banco de dados já existe
python /app/src/utils/start.py
echo "Subindo a API com Uvicorn..."
uvicorn api.main:app --host 0.0.0.0 --reload
