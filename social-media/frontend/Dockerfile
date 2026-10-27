# Stage 1: Build React/Vite
FROM node:20-alpine AS builder
LABEL authors="silence-suzuka"

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# Stage 2: Serve via Nginx
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html/main