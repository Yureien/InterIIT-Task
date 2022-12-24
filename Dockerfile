FROM node:16 as build

WORKDIR /src

COPY frontend/package.json frontend/yarn.lock /src/

RUN yarn install

COPY frontend /src

RUN yarn build

FROM nginx:latest

EXPOSE 80

COPY ./docker/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf

COPY --from=build /src/build /usr/share/nginx/html