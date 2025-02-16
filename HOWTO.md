# Ajustar a api-key do modelo
https://ai.google.dev/gemini-api/docs/api-key?hl=pt-br
config/openai_api.yaml

# Instalar o docker engine
https://docs.docker.com/engine/install/ubuntu/

# Remover a necessidade do sudo no docker
https://docs.docker.com/engine/install/linux-postinstall/

# Primeira execução
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