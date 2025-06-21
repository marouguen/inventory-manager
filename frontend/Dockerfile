# Stage 1: Build with Node
FROM node:20-alpine AS build

WORKDIR /app
COPY . .

# Install dependencies
RUN npm install

# Specify environment for Vite
ENV NODE_ENV=production

# Build the app
RUN npm run build

# Stage 2: Serve with NGINX
FROM nginx:stable-alpine

# Remove default nginx static assets
RUN rm -rf /usr/share/nginx/html/*

# Copy built app
COPY --from=build /app/dist /usr/share/nginx/html

# ✅ Copy only the server block config
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]
