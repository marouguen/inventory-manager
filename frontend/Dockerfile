# Stage 1: Build with Node
FROM node:20-alpine AS build

WORKDIR /app
COPY . .

# Install dependencies
RUN npm install

# Optional: Specify environment explicitly for Vite to pick correct .env file
ENV NODE_ENV=production

# Build the project (Vite will use .env.production)
RUN npm run build

# Stage 2: Serve with NGINX
FROM nginx:stable-alpine

# Remove default nginx static assets
RUN rm -rf /usr/share/nginx/html/*

# Copy built app from Stage 1
COPY --from=build /app/dist /usr/share/nginx/html

# Optional: Custom nginx config (we'll generate it if needed)
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port (default is 80)
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
