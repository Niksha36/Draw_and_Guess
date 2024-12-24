# frontend/Dockerfile
FROM node:18-alpine

# Set work directory
WORKDIR /app

# Install dependencies
COPY package.json ./
COPY package-lock.json ./
RUN npm install

# Copy project
COPY . .

# Build the application
RUN npm run build

# Expose port
EXPOSE 3000

# Serve the application
CMD ["npx", "serve", "-s", "build"]