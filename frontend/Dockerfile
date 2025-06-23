# Stage 1: Build Vue
FROM node:20-alpine AS build

WORKDIR /app
COPY . .

# ✅ Do NOT set NODE_ENV=production here — we need devDependencies for Vite build
RUN npm install --include=dev

# RUN npm run build

# # Stage 2: Nginx to serve frontend + reverse proxy
# FROM nginx:stable-alpine

# # ❌ Remove default Nginx config
# RUN rm /etc/nginx/conf.d/default.conf

# # ✅ Add your custom config and built frontend
# COPY --from=build /app/dist /usr/share/nginx/html
# COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf

# EXPOSE 80
# CMD ["nginx", "-g", "daemon off;"]

# ✅ Expose the Vite dev server port
EXPOSE 5173

# ✅ Start Vite dev server (used in development, not in production builds)
CMD ["npm", "run", "dev"]