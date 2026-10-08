"""Una persona de mentira para tu sala, desde la terminal. Corre DENTRO del contenedor:

    docker compose exec api uv run --no-sync python herramientas/consola.py anfitrion
    docker compose exec api uv run --no-sync python herramientas/consola.py invitado dani

Como anfitrión: lo que escribas se manda a la sala; `/si` acepta la última
solicitud y `/no` la rechaza. Como invitado: pide entrar, espera a que lo
acepten y después platica. Ctrl+C para salir.

No es parte de la práctica: es para probar el servidor antes de tener la app.
"""
import json
import os
import sys
import threading
import time
import urllib.error
import urllib.request

from websockets.sync.client import connect

SALA = os.environ.get("SALA", "http://localhost:8000")


def http(metodo, ruta, cuerpo=None):
    datos = json.dumps(cuerpo).encode() if cuerpo is not None else None
    peticion = urllib.request.Request(SALA + ruta, data=datos, method=metodo,
                                      headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(peticion) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        sys.exit(f"{metodo} {ruta} -> {e.code}: {e.read().decode()}")


def pedir_entrar(nickname):
    s = http("POST", "/solicitudes", {"nickname": nickname})
    print(f"Pediste entrar como {nickname}. Esperando a que el anfitrión te acepte…")
    while s["estado"] == "pendiente":
        time.sleep(2)
        s = http("GET", f"/solicitudes/{s['id']}")
    if s["estado"] != "aprobada":
        sys.exit("El anfitrión te rechazó.")
    return s["token"]


def platicar(token, es_anfitrion):
    url = SALA.replace("http", "ws", 1) + "/chat"
    pendientes = []
    with connect(url, additional_headers={"Authorization": f"Bearer {token}"}) as ws:
        def escuchar():
            for crudo in ws:
                e = json.loads(crudo)
                if e["tipo"] == "bienvenida":
                    print(f"Entraste como «{e['yo']}». Mensajes anteriores: {len(e['mensajes'])}")
                    for m in e["mensajes"]:
                        print(f"  {m['de']}: {m['texto']}")
                    for s in e["solicitudes"]:
                        pendientes.append(s)
                        print(f"  ¿Dejas entrar a {s['nickname']}? Escribe /si o /no")
                elif e["tipo"] == "mensaje":
                    print(f"{e['de']}: {e['texto']}")
                elif e["tipo"] == "solicitud":
                    pendientes.append(e)
                    print(f"¿Dejas entrar a {e['nickname']}? Escribe /si o /no")

        threading.Thread(target=escuchar, daemon=True).start()
        for linea in sys.stdin:
            linea = linea.strip()
            if es_anfitrion and linea in ("/si", "/no"):
                if not pendientes:
                    print("Nadie está esperando.")
                    continue
                s = pendientes.pop()
                ws.send(json.dumps({"tipo": "aprobar" if linea == "/si" else "rechazar", "id": s["id"]}))
            elif linea:
                ws.send(json.dumps({"tipo": "mensaje", "texto": linea}))


if __name__ == "__main__":
    if sys.argv[1:2] == ["anfitrion"]:
        platicar(os.environ["CLAVE_ANFITRION"], es_anfitrion=True)
    elif sys.argv[1:2] == ["invitado"] and len(sys.argv) == 3:
        platicar(pedir_entrar(sys.argv[2]), es_anfitrion=False)
    else:
        sys.exit(__doc__)
