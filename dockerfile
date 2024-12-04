# Multi-stage build for frontend and backend
FROM node:14 AS frontend-build
WORKDIR /app/frontend
COPY web_app/frontend/package*.json ./
RUN npm install
COPY web_app/frontend ./
RUN npm run build

FROM python:3.10-slim
WORKDIR /app

# Install system dependencies and clean up
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install dependencies
COPY web_app/backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . /app

# Copy built frontend from previous stage
COPY --from=frontend-build /app/frontend/build /app/web_app/frontend/build

# Install serve to run frontend
RUN npm install -g serve

# Expose ports for backend and frontend
EXPOSE 5000 3000

# Create a startup script
RUN echo '#!/bin/bash\n\
flask run --host=0.0.0.0 --port=5000 & \n\
serve -s /app/web_app/frontend/build -l 3000\n\
wait' > /app/start.sh && chmod +x /app/start.sh

# Set environment variables for production
ENV FLASK_ENV=production
ENV FLASK_APP=web_app/backend/app.py
ENV REACT_APP_API_URL=http://localhost:5000

# Run the startup script
CMD ["/app/start.sh"]