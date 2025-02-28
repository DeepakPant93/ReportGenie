# Use an official Python image as a base
FROM python:3.12-slim

RUN useradd -m -u 1000 user

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

# Set the working directory inside the container
WORKDIR /app

# Copy the pyproject.toml and any other build-related files
COPY --chown=user pyproject.toml .


# Install dependencies
RUN pip install --upgrade pip \
    && pip install uv crewai \
    && crewai install

# Ensure the /app directory is owned by the non-root user
RUN chown -R user:user /app

# Switch to the non-root user
USER user

# Copy the application code into the container
COPY --chown=user . .

# Expose the port on which the application will run it's a default Gradio port.
EXPOSE 7860

# Set the server name as 0.0.0.0 to access it from any host
ENV GRADIO_SERVER_NAME="0.0.0.0"

# Define the command to run your application
CMD ["uv", "run", "report_genie"]
