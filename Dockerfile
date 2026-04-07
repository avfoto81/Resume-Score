FROM python:3.11-slim

# Instala as dependências do sistema necessárias para o PDF
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copia os arquivos de requisitos e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

# Expõe a porta 7860 (padrão do Hugging Face)
EXPOSE 7860

# Comando para rodar o servidor
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "main:app"]