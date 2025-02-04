FROM node:14

WORKDIR /app

COPY package.json package.json
# Use npm ci for faster, deterministic installs when a package-lock.json is available.
RUN npm install

COPY . .

CMD ["npm", "start"]