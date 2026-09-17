FROM node:22-alpine AS build

WORKDIR /app

COPY package.json package-lock.json ./
# The checked-in lint tooling has a peer-version mismatch. It is not part of
# the browser bundle, but Vite is a development dependency required to build
# that bundle, so install the locked tree with npm's legacy peer resolution.
RUN npm ci --legacy-peer-deps

COPY . ./
RUN npm run build

FROM nginx:1.27-alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
