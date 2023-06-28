FROM node:20
WORKDIR /usr/src/app
COPY package*.json ./
RUN npm install -g @angular/cli
RUN npm install
COPY . ./
RUN npm run build --force
EXPOSE 8080
CMD [ "node", "index.js" ]