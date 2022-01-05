# Stage 1
# Download the Mongo Exporter from the Git Repository
FROM alpine/git as git
WORKDIR /app
RUN git clone https://github.com/JamesOsgood/mongodb-grafana.git

COPY . .

RUN npm i

EXPOSE 3000

RUN npm build

CMD [ "npm", "run", "serve" ]
