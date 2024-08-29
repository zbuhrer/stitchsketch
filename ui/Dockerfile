# Use an official lightweight nodejs image as our base
FROM node:14-slim

# Set the working directory to /app
WORKDIR /app

# Copy the package*.json and yarn.lock files from the current directory
COPY package*.json package-lock.json ./

# Install dependencies
RUN npm ci --only=production

# Copy the rest of your application code, including all Dockerfile-ignores (e.g., node_modules)
COPY . .

# Build the application to optimize for production.
RUN npm run build

# Expose the container port
EXPOSE 3000

# Run the command to start the app when the container launches
CMD ["npm", "start"]
