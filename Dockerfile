# Dockerfile
FROM python:3

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Export configurations from .env file
ENV $(cat .env | xargs)

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python bot.py file to the container
COPY . /app

ARG BUILD
ENV BUILD_VERSION=$BUILD

# Start the Python bot
CMD ["python", "bot.py"]
