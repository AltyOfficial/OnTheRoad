# Stage 1: Сборка
FROM node:20-alpine AS builder

WORKDIR /app

# Копируем только package файлы
COPY package*.json ./

# Чистая установка + фикс optional dependencies
RUN npm ci --force

# Копируем остальной код
COPY . .

# Сборка
RUN npm run build

# Stage 2: Продакшен
FROM nginx:stable-alpine AS production

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]