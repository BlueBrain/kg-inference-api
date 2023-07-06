FROM nginx:1.21.3

ARG GENERATED_DOCS_PATH

# Copy generated files to nginx default html directory
COPY $GENERATED_DOCS_PATH /usr/share/nginx/html
# Copy nginx custom configuration to default directory
COPY nginx.conf /etc/nginx/nginx.conf
# Expose port
EXPOSE 8080
# Run nginx server
CMD ["nginx", "-g", "daemon off;"]