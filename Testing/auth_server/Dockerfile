# Base image with both Mosquitto and Python
FROM python:3.8-slim

# Copy the Python script
COPY auth_server.py /app/auth_server.py

# Install Python dependencies
RUN pip install Flask PyJWT
RUN pip install python-keycloak

# Expose Mosquitto port
EXPOSE 5000

# Start the Python server
CMD python /app/auth_server.py