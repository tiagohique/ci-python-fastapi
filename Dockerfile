# Usando a imagem oficial do Python 3.12 slim
FROM python:3.12-slim

# Definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos requirements.txt e instalar as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o resto do código da aplicação
COPY . .

# Expor a porta usada pela FastAPI
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]