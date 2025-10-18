FROM node:20

WORKDIR /app

# lock 유무 관계없이 동작
COPY package*.json ./
RUN if [ -f package-lock.json ]; then npm ci; else npm install || true; fi

COPY . .

EXPOSE 5173