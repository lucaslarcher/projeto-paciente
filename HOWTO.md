# Ajustar a api-key do modelo
https://ai.google.dev/gemini-api/docs/api-key?hl=pt-br
https://aistudio.google.com/app/apikey?hl=pt-br&_gl=1*ln2eqf*_ga*MjA1Nzg4OTYxLjE3Mzk0MDU1NzE.*_ga_P1DBVKWT6V*MTczOTg0MDg2Ni43LjEuMTczOTg0MDg4Mi40NC4wLjE3NDI0OTE3ODQ.
config/openai_api.yaml

# Usando Docker
    # Buildar o container
docker build -t projeto-paciente -f Dockerfile .
    # Executar o docker
docker run -p 8000:8000 projeto-paciente

# Instalar o docker engine
https://docs.docker.com/engine/install/ubuntu/

# Remover a necessidade do sudo no docker
https://docs.docker.com/engine/install/linux-postinstall/

# Com o docker compose
docker compose up --build
    # Próximas execuções
docker compose up

# Para iniciar o fastAPI server
    # na raiz do projeto fazer um:
uvicorn api.main:app --reload

# Para recuperar cliente/paciente
curl -X 'GET' 'http://127.0.0.1:8000/recuperar_paciente/123'

# Para adicionar um chat novo
curl -X 'POST'   'http://127.0.0.1:8000/processar_chat/'   -H 'Content-Type: application/json'   -d '{"chat": "dor de cabeça, febre, espirro", "id_chat": "123", "id_cliente": "456"}'

# Para teste
    # Na raiz
PYTHONPATH=$(pwd) pytest tests/
