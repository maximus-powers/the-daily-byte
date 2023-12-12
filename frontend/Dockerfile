# Use an official node runtime based on Alpine Linux as a parent image
FROM node:20.9.0-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the package.json and package-lock.json (if available)
COPY package.json package-lock.json* ./

# Install any needed packages specified in package.json
RUN npm install --frozen-lockfile

# Copy the current directory contents into the container at /app
COPY . .

# Build the app for production to the build folder
RUN npm run build

# Install serve to serve the build directory on a web server
RUN npm install -g serve

# Make port 3000 available to the world outside this container
EXPOSE 3000

# Serve the build directory
CMD ["serve", "-s", "build", "-l", "3000"]
