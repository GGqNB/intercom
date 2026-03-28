FROM node:20.14

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .
EXPOSE 3030
CMD ["npm", "run", "start"]