FROM node:16 as build-stage
WORKDIR /app
COPY package*.json /app/
RUN npm install
COPY ./ /app/
ARG FRONTEND_ENV
ENV VUE_APP_ENV=${FRONTEND_ENV}
ARG FRONTEND_NAME
ENV VUE_APP_NAME=${FRONTEND_NAME}
RUN npm run build
FROM nginx:1.15
COPY --from=build-stage /app/dist/ /usr/share/nginx/html
COPY ./nginx.conf /etc/nginx/conf.d/default.conf
COPY ./nginx-backend-not-found.conf /etc/nginx/extra-conf.d/backend-not-found.conf
