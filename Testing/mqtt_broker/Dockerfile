# # # Use the iegomez/mosquitto-go-auth image
# # FROM iegomez/mosquitto-go-auth

# # # Copy your custom mosquitto configuration file
# # COPY mosquitto.conf /mosquitto/config/mosquitto.conf

# # RUN git clone https://github.com/iegomez/mosquitto-go-auth

# # RUN cd mosquitto-go-auth
# # RUN export CGO_CFLAGS=”-I/usr/local/include -fPIC”
# # RUN export CGO_LDFLAGS=”-shared”
# # RUN make

# # # Expose default mosquitto ports
# # EXPOSE 1883 8883

# # # Set the entrypoint to run Mosquitto
# # ENTRYPOINT ["/usr/sbin/mosquitto"]
# # CMD ["-c", "/mosquitto/config/mosquitto.conf"]

# FROM ubuntu

# RUN  apt-get update \
#   && apt-get install -y wget \
#   && rm -rf /var/lib/apt/lists/*
  
# RUN wget https://mosquitto.org/files/source/mosquitto-2.0.18.tar.gz
# RUN tar xzvf mosquitto-2.0.18.tar.gz


# # RUN apt-get install -y libwebsockets8 libwebsockets-dev libc-ares2 libc-ares-dev openssl uuid uuid-dev libssl-dev libcjson1 libcjson-dev git

# RUN set -ex; \
#     apt update; \
#     apt install -y libc-ares2 openssl uuid tini wget libssl-dev libcjson-dev
# # RUN make install

# RUN cd mosquitto-2.0.18
# RUN ls
# # RUN make
# RUN make install
# # Now we need to setup the ownership for the build
# RUN groupadd mosquitto
# RUN useradd -s /sbin/nologin mosquitto -g mosquitto -d /var/lib/mosquitto
# RUN mkdir -p /var/log/mosquitto/ /var/lib/mosquitto/
# RUN chown -R mosquitto:mosquitto /var/log/mosquitto/
# RUN chown -R mosquitto:mosquitto /var/lib/mosquitto/

# # Create the .service file for mosquitto using the following steps
# RUN touch /etc/systemd/system/mosquitto.service

# # Since the plugin is on golang we will now install go
# RUN add-apt-repository ppa:longsleep/golang-backports
# RUN apt update
# RUN apt install golang-go

# RUN git clone https://github.com/iegomez/mosquitto-go-auth

# RUN cd mosquitto-go-auth
# RUN export CGO_CFLAGS=”-I/usr/local/include -fPIC”
# RUN export CGO_LDFLAGS=”-shared”
# RUN make

# COPY mosquitto.conf /mosquitto/config/mosquitto.conf


# # Base image with both Mosquitto and Python
# # FROM python:3.8-slim

# # # Install Mosquitto in the same container
# # RUN apt-get update && apt-get install -y mosquitto mosquitto-clients

# # # Copy the Mosquitto config and the auth plugin
# # COPY mosquitto.conf /mosquitto/config/mosquitto.conf
# # # COPY auth-plug.so /mosquitto/plugins/auth-plug.so
# # COPY --from=builder /mosquitto-auth-plug/auth-plug.so /usr/lib/auth-plug.so

# # # Copy the Python script
# # COPY auth_server.py /app/auth_server.py

# # # Install Python dependencies
# # RUN pip install Flask PyJWT
# # RUN pip install python-keycloak

# # # Expose Mosquitto port
# # EXPOSE 1883

# # # Start both Mosquitto and the Python server
# # CMD python /app/auth_server.py & mosquitto -c /mosquitto/config/mosquitto.conf

# Use an Ubuntu base image
FROM ubuntu:20.04

# Install dependencies
RUN apt-get update \
  && apt-get install -y wget build-essential git golang-go libc-ares2 libssl-dev uuid-dev libcjson-dev \
  && rm -rf /var/lib/apt/lists/*

# Download and extract Mosquitto source code
RUN wget https://mosquitto.org/files/source/mosquitto-2.0.18.tar.gz \
  && tar xzvf mosquitto-2.0.18.tar.gz \
  && rm mosquitto-2.0.18.tar.gz

# Build and install Mosquitto
WORKDIR /mosquitto-2.0.18
RUN make \
  && make install

# Setup Mosquitto user and directories
RUN groupadd mosquitto \
  && useradd -s /sbin/nologin mosquitto -g mosquitto -d /var/lib/mosquitto \
  && mkdir -p /var/log/mosquitto/ /var/lib/mosquitto/ \
  && chown -R mosquitto:mosquitto /var/log/mosquitto/ /var/lib/mosquitto/

# Clone and build mosquitto-go-auth plugin
WORKDIR /opt
RUN git clone https://github.com/iegomez/mosquitto-go-auth.git \
  && cd mosquitto-go-auth \
  && make

# Copy the Mosquitto configuration file
COPY mosquitto.conf /mosquitto/config/mosquitto.conf

# Expose Mosquitto ports
EXPOSE 1883 8883

# Set the entrypoint to run Mosquitto
ENTRYPOINT ["/usr/local/sbin/mosquitto", "-c", "/mosquitto/config/mosquitto.conf"]
