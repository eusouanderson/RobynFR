services:
  nginx:
    image: nginx:latest
    container_name: nginx
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
    ports:
      - "80:80"
    depends_on:
      - backend
      - frontend

  backend:
    build: ./backend
    container_name: backend
    scale: 3   # sobe 3 instâncias automaticamente
    environment:
      - PORT=8000
    expose:
      - "8000"

  frontend:
    build: ./robyn
    container_name: frontend
    expose:
      - "3000"
