# Build frontend
FROM node:14 AS frontend-build
WORKDIR /app/frontend
COPY web_app/frontend/package*.json ./
RUN npm install
COPY web_app/frontend ./
RUN npm run build

# Backend setup
FROM python:3.10-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install dependencies
COPY web_app/backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app

# Copy built frontend from previous stage
COPY --from=frontend-build /app/frontend/build /app/web_app/frontend/build

# Expose port
EXPOSE 5000

# Set environment variables for production
ENV FLASK_ENV=production
ENV FLASK_APP=web_app/backend/app.py

# Run the application
CMD ["flask", "run", "--host=0.0.0.0"]