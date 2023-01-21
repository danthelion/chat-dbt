FROM ubuntu:latest

# System dependencies & python3
RUN apt update && \
    apt upgrade &&\
    apt install -y \
    build-essential \
    curl \
    git \
    python3 \
    python3-dev \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    python3-venv \
    && rm -rf /var/lib/apt/lists/* \
    && pip3 install --upgrade pip \
    && pip3 install --upgrade setuptools

# Rust compiler for tiktoken
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y
# add to env
ENV PATH="/root/.cargo/bin:${PATH}"

# Check if rustc is installed
RUN rustc --version

# Install dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy source code
COPY . .

# Run the app
ENTRYPOINT ["./entrypoint.sh"]
