FROM python:3.12-slim

LABEL io.modelcontextprotocol.server.name="io.github.yannabadie/eu-us-opendata-mcp"
LABEL org.opencontainers.image.source="https://github.com/yannabadie/eu-us-opendata-mcp"
LABEL org.opencontainers.image.licenses="MIT"

WORKDIR /app
COPY pyproject.toml README.md LICENSE ./
COPY src ./src

RUN pip install --no-cache-dir .

ENTRYPOINT ["eu-us-opendata-mcp"]
