FROM python:3.10

# Definindo as variáveis de ambiente
ENV PYTHONUNBUFFERED=1
ENV PATH="/root/.local/bin:$PATH"
ENV PYTHONPATH="/"

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y curl gcc python3-dev libpq-dev && apt-get clean

# Instalar Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - --yes

# Adicionar Poetry ao PATH
ENV PATH="/root/.local/bin:$PATH"

# Verificar se Poetry está instalado corretamente
RUN poetry --version

# Configurar Poetry para não criar ambientes virtuais
RUN poetry config virtualenvs.create false

# Copiar arquivos do Poetry
COPY pyproject.toml poetry.lock /

# Instalar dependências
RUN poetry install --no-root --no-dev

# Removendo pacotes desnecessários
RUN apt-get remove -y curl && apt-get autoremove -y && apt-get clean

# Criar diretório de migrações e ajustar permissões para todos os usuários
RUN mkdir -p /app/migrations/versions && chmod -R 777 /app/migrations/versions

# Copiar código do aplicativo
COPY . .

# Definir diretório de trabalho
WORKDIR /app

# Expor a porta 8000
EXPOSE 8000

# Comando para iniciar o aplicativo
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]