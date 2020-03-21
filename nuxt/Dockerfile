ARG NODE_VERSION
# Defining the base image
FROM node:$NODE_VERSION

# Set the working directory
WORKDIR /usr/src/app

# Copy the app package and package-lock.json file
COPY ./package*.json ./

# Install node packages
RUN npm install

# Copy or project directory (locally) in the current directory of our docker image (/app)
COPY ./ ./usr/src/app

# Build the app
RUN npm run build
