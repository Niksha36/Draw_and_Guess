FROM node:18-alpine

COPY . /app

# Set work directory
WORKDIR /app/frontend

# Install dependencies
RUN npm install
RUN npm install string-similarity

# Expose the port the server will run on
EXPOSE 3000

# Command to run the server
CMD ["node", "/app/frontend/src/js/server.js"]