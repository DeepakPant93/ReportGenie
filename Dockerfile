# Use an official Python image as a base
FROM python:3.12-slim

RUN useradd -m -u 1000 user
# USER user

# Set the working directory inside the container
WORKDIR /app

# Copy the pyproject.toml and any other build-related files
COPY pyproject.toml .

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    gcc \
    libssl-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install Rust (required for orjson and other Rust-based Python packages)
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y \
    && export PATH="$HOME/.cargo/bin:$PATH" \
    && rustc --version

# Ensure Rust is added to PATH for all subsequent RUN commands
ENV PATH="/root/.cargo/bin:$PATH"

RUN pip install --upgrade pip \
    && pip install uv \
    && pip install crewai \
    && crewai install

# Copy the application code into the container
COPY . .

EXPOSE 10000 

# Define the command to run your application
CMD ["uv", "run", "report_genie"]