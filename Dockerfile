# ---- Build the PostgreSQL Base ----
FROM postgres:latest AS postgres-base

ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=password
ENV POSTGRES_DB=postgresDB

FROM python:3.11-bookworm

RUN apt-get update && apt-get install -y supervisor

WORKDIR /workspace

COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements.txt


COPY --from=postgres-base /usr/local/bin /usr/local/bin
COPY --from=postgres-base /usr/lib/postgresql /usr/lib/postgresql
COPY --from=postgres-base /usr/share/postgresql /usr/share/postgresql
COPY --from=postgres-base /var/lib/postgresql /var/lib/postgresql

# Add supervisord config
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 8080 5455

CMD ["/usr/bin/supervisord"]
