# Use an official Node.js image as the base
FROM node:latest

# Set the working directory to /app
WORKDIR /app

# Copy package*.json files & install dependencies 
COPY package*.json ./
RUN npm install

# Copy the rest of the codebase 
COPY . .

# Expose the port & run 
EXPOSE 3000
RUN npm install
RUN npm run build