#!/usr/bin/env python3
"""Cliente mínimo de la API de Marketing Emails de HubSpot (v3).

Lee el token de la variable de entorno HUBSPOT_TOKEN (app privada con scope `content`).
Nunca imprime el token.

Uso:
  hubspot_api.py check                       Comprueba token y acceso
  hubspot_api.py find <texto>                Busca emails cuyo nombre contenga <texto>
  hubspot_api.py get <emailId> [salida.json] Descarga el email completo (incluye content.widgets)
  hubspot_api.py clone <emailId> <nombre>    Clona un email; imprime el id del nuevo borrador
  hubspot_api.py patch <emailId> <cambios.json>
                                             PATCH con el JSON indicado (subject, name,
                                             previewText, content.widgets…)
"""
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://api.hubapi.com/marketing/v3/emails"


def request(method, url, body=None):
    token = os.environ.get("HUBSPOT_TOKEN")
    if not token:
        sys.exit("ERROR: falta la variable de entorno HUBSPOT_TOKEN")
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        sys.exit(f"ERROR HTTP {e.code}: {e.read().decode(errors='replace')}")


def main(argv):
    if len(argv) < 2:
        sys.exit(__doc__)
    cmd = argv[1]

    if cmd == "check":
        r = request("GET", f"{BASE}?limit=1")
        print(f"OK: acceso a marketing emails ({r.get('total', '?')} emails en el portal)")

    elif cmd == "find":
        text = argv[2].lower()
        after = None
        while True:
            q = {"limit": 100, "archived": "false"}
            if after:
                q["after"] = after
            r = request("GET", f"{BASE}?{urllib.parse.urlencode(q)}")
            for e in r.get("results", []):
                if text in (e.get("name") or "").lower():
                    print(f"{e['id']}\t{e.get('state')}\t{e.get('name')}\t{e.get('subject')}")
            after = r.get("paging", {}).get("next", {}).get("after")
            if not after:
                break

    elif cmd == "get":
        r = request("GET", f"{BASE}/{argv[2]}")
        out = json.dumps(r, ensure_ascii=False, indent=2)
        if len(argv) > 3:
            with open(argv[3], "w") as f:
                f.write(out)
            print(f"Guardado en {argv[3]}")
        else:
            print(out)

    elif cmd == "clone":
        r = request("POST", f"{BASE}/clone", {"id": argv[2], "cloneName": argv[3]})
        print(r["id"])

    elif cmd == "patch":
        with open(argv[3]) as f:
            body = json.load(f)
        r = request("PATCH", f"{BASE}/{argv[2]}", body)
        print(f"OK: actualizado {r.get('id')} — estado {r.get('state')} — {r.get('name')}")

    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv)
