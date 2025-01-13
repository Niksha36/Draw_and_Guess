# FrontendDockerfile
FROM node:18-alpine

COPY . /app
# Set work directory
WORKDIR /app/frontend

RUN npm cache verify

# Install dependencies
RUN npm install

# Build the application
RUN npm run build

# Expose port
EXPOSE 3000

CMD ["npm", "run", "serve"]