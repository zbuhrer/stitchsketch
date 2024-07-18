# ./stsk-3d-app/Dockerfile
# Use Node.js as base image
FROM node:14-alpine as builder

# Install git
RUN apk add --no-cache git

# Clone Potree repository
RUN git clone https://github.com/potree/potree.git /potree

# Set working directory
WORKDIR /potree

# Install dependencies and build
RUN npm install && npm run build

# Use Nginx as the final base image
FROM nginx:alpine

# Copy the built Potree files from the builder stage
COPY --from=builder /potree/build /usr/share/nginx/html/build
COPY --from=builder /potree/examples /usr/share/nginx/html/examples
COPY --from=builder /potree/libs /usr/share/nginx/html/libs

# Copy a custom nginx configuration file
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]