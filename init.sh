#!/bin/bash

echo "Subindo a API com Uvicorn..."
uvicorn api.main:app --host 0.0.0.0 --reload
