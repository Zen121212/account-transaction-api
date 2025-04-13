# 1. Start from a lightweight Python image
FROM python:3.10-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy requirements.txt first (so Docker caches dependencies)
COPY requirements.txt .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install wait-for-it
RUN apt-get update && apt-get install -y wait-for-it

# 5. Expose port (optional but good practice)
EXPOSE 8000

# 6. Set the environment variable to point to the FastAPI app entry
ENV MODULE_NAME=main

# 7. Start FastAPI using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
