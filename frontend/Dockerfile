# Stage 1: Build Vue
FROM node:20-alpine AS build

WORKDIR /app
COPY . .

# ✅ Use production env for VITE_API_URL
RUN cp .env.production .env

# Install dependencies (we need devDependencies too)
RUN npm install --include=dev

# Build the frontend for production
RUN npm run build

# Install Vite globally to preview the static build
RUN npm install -g vite

# Expose default Vite preview port
EXPOSE 4173

# Start Vite's preview server
CMD ["vite", "preview", "--host"]
