FROM node:20-alpine
WORKDIR /app
COPY package.json package-lock.json* /app/
RUN npm ci --only=production || npm ci --omit=dev
COPY server.js /app/server.js
EXPOSE 5173
CMD ["node", "server.js"]