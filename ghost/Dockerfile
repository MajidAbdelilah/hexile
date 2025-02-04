FROM ghost:alpine

COPY config.production.json /var/lib/ghost/config.production.json

# Add a healthcheck to verify Ghost startup faster
HEALTHCHECK CMD curl -f http://localhost:2368/ || exit 1