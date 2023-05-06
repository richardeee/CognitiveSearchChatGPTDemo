FROM node:19-alpine as builder

# Create app directory
WORKDIR /app

COPY frontend/package*.json ./frontend/
RUN npm install

COPY frontend/ ./frontend
COPY backend/ ./backend

RUN npm run build

# Production image
FROM python:3.10-alpine

WORKDIR /app

COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY --from=builder /app/backend ./

EXPOSE 5000

CMD [ "python", "app.py" ]
