# Práctica 12 — el servidor de Charla

Código de arranque del servidor de la Práctica 12 de TC2007B: **tu** sala de chat,
con FastAPI y WebSocket, en Docker, con un túnel HTTPS para que tus compañeros
entren desde su computadora.

Este repo casi no trae nada, a propósito: el servidor lo construyes tú en la
Parte A de la guía. Lo que ya viene:

| Archivo | Para qué |
| --- | --- |
| `pyproject.toml` y `uv.lock` | Las dependencias, con versiones exactas (FastAPI, uvicorn, pytest) |
| `.env.example` | La plantilla de tu `.env`: ahí va la clave de anfitrión |
| `herramientas/consola.py` | Una persona de mentira para probar la sala desde la terminal |

## Cómo empezar

1. Clona el repositorio. Necesitas Docker Desktop corriendo.
2. `cp .env.example .env` y cambia la clave.
3. Sigue la guía: https://startdroid.com/practicas/charla.html

`.env` nunca se sube al repositorio.

## Cómo trabajar

Haz un commit en cada checkpoint de la guía:

    git add -A ; git commit -m "checkpoint a4"

## Entrega

Ver la rúbrica en la guía. Sube todas las ramas: `git push origin --all`.
