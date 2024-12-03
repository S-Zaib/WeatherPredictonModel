# Build frontend
FROM node:14 AS frontend-build
WORKDIR /app/frontend

# install dependencies
COPY web_app/frontend/package*.json ./
RUN npm install

# Copy project files
COPY web_app/frontend ./

# build
RUN npm run build

# Build backend
FROM python:3.9-slim
WORKDIR /app

# install dependencies
COPY web_app/backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app

# Copy built frontend from previous stage
COPY --from=frontend-build /app/frontend/build /app/web_app/frontend/build

# Expose port
EXPOSE 5000

# Run the application
CMD ["flask", "run", "--host=0.0.0.0"]