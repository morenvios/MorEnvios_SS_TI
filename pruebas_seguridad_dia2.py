"""Pruebas de seguridad del Día 2 - More Envíos API.

Uso:
    pip install httpx
    # 1) base de PRUEBAS recién migrada (bash migrar.sh reset) y API corriendo
    # 2) python pruebas_seguridad_dia2.py  [http://127.0.0.1:8000]

OJO: los PATCH modifican datos. Antes de repetir las pruebas, restaura la
semilla con:  bash migrar.sh reset   (nunca contra una base real).
"""
import sys
import httpx

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000"
# sin keep-alive: tras un error 500 el servidor cierra la conexión y httpx fallaría al reutilizarla
c = httpx.Client(base_url=BASE, timeout=10, limits=httpx.Limits(max_keepalive_connections=0))
resultados = []


def prueba(id_, area, descripcion, esperado, real, hallazgo_si):
    estado = "HALLAZGO" if hallazgo_si else "OK"
    resultados.append(estado)
    print(f"{id_:<4} [{estado:<8}] {area:<9} {descripcion}\n"
          f"      esperado: {esperado} | obtenido: {real}")


G10, G11, G3 = "MEV-2026-000010", "MEV-2026-000011", "MEV-2026-000003"
PATCH = lambda g, **b: c.patch(f"/envios/{g}/estado", json=b)

# ---- ACCESO ----
r = c.get("/clientes/sin-fallidos")
prueba("P1", "Acceso", "Clientes y correos sin credenciales", "401/403", r.status_code, r.status_code == 200)
r = c.get(f"/envios/MEV-2026-000001/historial")
prueba("P2", "Acceso", "Historial con usuario_cambio sin credenciales", "401/403", r.status_code, r.status_code == 200)
r = c.get("/docs")
prueba("P3", "Config", "Documentación interactiva /docs pública", "401/403/404", r.status_code, r.status_code == 200)
r = c.get("/openapi.json")
prueba("P4", "Config", "Esquema /openapi.json público", "401/403/404", r.status_code, r.status_code == 200)

# ---- ENTRADAS: lo que debe resistir ----
r = c.get("/envios", params={"estado": "' OR 1=1 --"})
prueba("P5", "Entradas", "Inyección SQL en filtro estado", "0 resultados", r.json().get("total"), r.json().get("total") != 0)
r = c.get("/envios/x' OR '1'='1/ruta")
prueba("P6", "Entradas", "Inyección SQL en num_guia", "404", r.status_code, r.status_code != 404)
r = c.get("/envios", params={"size": 1000})
prueba("P7", "Entradas", "size=1000 (máximo 50)", "422", r.status_code, r.status_code != 422)
r = c.get("/envios", params={"id_cliente": "abc"})
prueba("P8", "Entradas", "id_cliente con texto", "422", r.status_code, r.status_code != 422)
r = c.patch(f"/envios/{G10}/estado", content='{"estado":', headers={"content-type": "application/json"})
prueba("P9", "Entradas", "JSON roto en PATCH", "422", r.status_code, r.status_code != 422)
r = PATCH(G10, estado="recolectado", usuario="A" * 51)
prueba("P10", "Entradas", "usuario de 51 caracteres", "422", r.status_code, r.status_code != 422)
r = PATCH(G10, estado="hackeado", usuario="x")
prueba("P11", "Entradas", "estado inexistente", "409/422", r.status_code, r.status_code not in (409, 422))
r = PATCH(G11, estado="en_transito", usuario="x", id_repartidor=99999)
prueba("P12", "Entradas", "id_repartidor inexistente (rollback)", "409", r.status_code, r.status_code != 409)

# ---- ENTRADAS: casos límite ----
r = c.get("/envios", params={"page": 9223372036854775807})
prueba("P13", "Entradas", "page en el límite de bigint", "422 o 200 vacío", r.status_code, r.status_code >= 500)
r = c.get("/envios/MEV%00X/historial")
prueba("P14", "Entradas", "num_guia con byte nulo (%00)", "404/422", r.status_code, r.status_code >= 500)
r = c.get("/envios/" + "A" * 5000 + "/ruta")
eco = "A" * 100 in r.text
prueba("P15", "Entradas", "num_guia de 5000 caracteres", "422 sin eco", f"{r.status_code}, eco={eco}", eco)

# ---- ACCESO + ENTRADAS: abuso del cambio de estado ----
r = PATCH(G10, estado="recolectado", usuario="Director General", id_repartidor=1)
prueba("P16", "Acceso", "PATCH sin credenciales con usuario inventado", "401/403", r.status_code, r.status_code == 200)
r = PATCH(G10, estado="en_transito", usuario="<script>alert(1)</script>")
guardado = "<script>" in c.get(f"/envios/{G10}/historial").text
prueba("P17", "Entradas", "HTML en usuario se guarda tal cual", "rechazado", f"{r.status_code}, guardado={guardado}", guardado)
r = PATCH(G3, estado="entregado", usuario="repartidor:99")
prueba("P18", "Acceso", "Repartidor inexistente marca 'entregado'", "401/403", r.status_code, r.status_code == 200)

# ---- DISPONIBILIDAD / CONFIG ----
codigos = [c.get("/envios").status_code for _ in range(100)]
prueba("P19", "Config", "100 peticiones seguidas", "algún 429", f"{codigos.count(200)} x 200, {codigos.count(429)} x 429", 429 not in codigos)
r = c.get("/clientes/sin-fallidos", headers={"Origin": "http://sitio-malo.com"})
cors = "access-control-allow-origin" in r.headers
prueba("P20", "Config", "Cabecera CORS con Origin ajeno", "sin cabecera", f"cabecera={cors}", cors)
r = c.get("/envios", params={"page": 9223372036854775807})
prueba("P21", "Config", "El 500 no muestra traza al cliente", "mensaje genérico", repr(r.text[:30]), "Traceback" in r.text)

print(f"\nTotal: {len(resultados)} pruebas | OK: {resultados.count('OK')} | HALLAZGO: {resultados.count('HALLAZGO')}")
