#!/usr/bin/env python3
"""Genera, a partir de correos.txt, el comunicado.json y el JSON de PATCH de cada correo DeiWorld.

Salida en ../envios/deiworld-NN.comunicado.json y ../envios/deiworld-NN.json
"""
import copy, json, os, re, subprocess, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
ENVIOS = os.path.join(AQUI, "..", "envios")
PLANTILLA = os.path.join(AQUI, "..", "plantilla.py")
BASE = json.load(open(os.path.join(ENVIOS, "501405127901.json"), encoding="utf-8"))
REG = "https://app.vidiv.net/event/novedades-deiworld-2026"
TOKEN = '{{ contact.firstname | default("cliente") }}'
TOTAL = 20


def negritas(t):
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)


def html_gen(cmd, path):
    return subprocess.check_output([sys.executable, PLANTILLA, cmd, path], text=True).rstrip("\n")


def parse():
    for bloque in open(os.path.join(AQUI, "correos.txt"), encoding="utf-8").read().split("=== ")[1:]:
        cab, *lineas = bloque.strip().split("\n")
        n, nombre, texto_boton, url = [x.strip() for x in cab.split("|")]
        yield int(n), nombre, texto_boton, url, [l for l in lineas if l.strip()]


for n, nombre, texto_boton, url, lineas in parse():
    asunto = prev = None
    bloques = [{"tipo": "p", "html": f"Hola, {TOKEN}."}]
    items = []
    for l in lineas + ["Z: "]:
        if not l.startswith("- ") and items:
            bloques.append({"tipo": "ul", "items": items})
            items = []
        if l.startswith("S: "):
            asunto = l[3:]
        elif l.startswith("V: "):
            prev = l[3:]
        elif l.startswith("H: "):
            bloques.append({"tipo": "h3", "texto": l[3:]})
        elif l.startswith("- "):
            items.append(negritas(l[2:]))
        elif l.startswith("Z: "):
            pass
        else:
            bloques.append({"tipo": "p", "html": negritas(l)})
    titular = asunto.replace("[Nombre], ", "")
    titular = titular[0].upper() + titular[1:]
    com = {"titular": titular, "bloques": bloques}
    if url == "REG":
        com["boton"] = {"texto": texto_boton, "url": REG}
    cpath = os.path.join(ENVIOS, f"deiworld-{n:02d}.comunicado.json")
    json.dump(com, open(cpath, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    d = copy.deepcopy(BASE)
    w = d["content"]["widgets"]
    w["module-1-0-1"]["body"]["html"] = html_gen("titular", cpath)
    w["module-1-0-2"]["body"]["html"] = html_gen("cuerpo", cpath)
    if url == "REG":
        w["module-1-0-3"]["body"]["text"] = texto_boton
        w["module-1-0-3"]["body"]["destination"] = REG
        w["module-1-0-3"]["body"].pop("link", None)
    else:
        del w["module-1-0-3"]  # sin URL no hay botón
    w["preview_text"]["body"]["value"] = prev
    d["previewText"] = prev
    d["subject"] = asunto.replace("[Nombre]", TOKEN)
    d["name"] = f"2026-10 novedades DeiWorld {n}/{TOTAL}"
    json.dump(d, open(os.path.join(ENVIOS, f"deiworld-{n:02d}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(n, d["name"], "|", d["subject"], "|", "boton" if url == "REG" else "sin boton")
