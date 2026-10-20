#!/usr/bin/env python3
"""Genera el HTML de un comunicado con la plantilla "Genérica Visual Trans".

Una sola fuente para el cuerpo del email de HubSpot y para la vista previa que Marc
manda por correo, así los dos salen iguales: mismos titulares, párrafos y separaciones.

Entrada: un JSON con el comunicado:
  {
    "titular": "Texto del <h1>",
    "bloques": [
      {"tipo": "p",   "html": "Hola,"},
      {"tipo": "h2",  "texto": "Novedad 1. Título"},
      {"tipo": "h3",  "texto": "Cómo se declara"},
      {"tipo": "ul",  "items": ["<strong>Campo:</strong> …", "…"]},
      {"tipo": "ol",  "items": ["…"]},
      {"tipo": "enlace", "url": "https://…"}          # "Para más información haz clic…"
    ],
    "boton": {"texto": "Más información", "url": "https://…"}
  }
  "html" e "items" admiten <strong>, <em> y <a href>; "texto" es texto plano.

Uso:
  plantilla.py cuerpo  <comunicado.json>   HTML del módulo module-1-0-2 (cuerpo en HubSpot)
  plantilla.py titular <comunicado.json>   HTML del módulo module-1-0-1 (titular <h1>)
  plantilla.py preview <comunicado.json>   Email completo como en HubSpot (logo, h1, cuerpo,
                                           botón, firma, LinkedIn y pie) con estilos en línea,
                                           a partir de plantilla-email.html
"""
import html
import json
import os
import re
import sys

AZUL = "#162846"
NARANJA = "#f15f27"
TEXTO = "#363330"

P = 'style="margin:0; line-height:175%"'
H1 = f'style="margin:0; font-family:Georgia, serif; font-size:28px; color:{AZUL}; line-height:125%; font-weight:normal"'
H2 = f'style="margin:0; font-family:Georgia, serif; font-size:22px; color:{AZUL}; line-height:130%; font-weight:normal"'
H3 = f'style="margin:0; font-family:Arial, sans-serif; font-size:17px; color:{AZUL}; line-height:150%; font-weight:bold"'
LISTA = 'style="line-height:175%; margin:0; padding-left:24px"'
SEPARADOR = f"<p {P}>&nbsp;</p>"
FIRMA = f'<p {P}>Un saludo,</p>\n{SEPARADOR}\n<p {P}><span style="font-weight: bold;">Equipo de Visual Trans</span></p>'


def _enlaces_naranja(fragmento):
    # En la plantilla los enlaces del cuerpo van en naranja.
    return re.sub(r'<a (?![^>]*style=)', f'<a style="color:{NARANJA}" ', fragmento)


def _bloque(b):
    tipo = b["tipo"]
    if tipo == "p":
        return f"<p {P}>{_enlaces_naranja(b['html'])}</p>"
    if tipo == "h2":
        return f"<h2 {H2}>{html.escape(b['texto'])}</h2>"
    if tipo == "h3":
        return f"<h3 {H3}>{html.escape(b['texto'])}</h3>"
    if tipo in ("ul", "ol"):
        items = "\n".join(f"<li>{_enlaces_naranja(i)}</li>" for i in b["items"])
        return f"<{tipo} {LISTA}>\n{items}\n</{tipo}>"
    if tipo == "enlace":
        url = html.escape(b["url"], quote=True)
        texto = html.escape(b.get("texto", "Más información"))
        return (f'<p {P}>Para más información haz clic en el siguiente enlace: '
                f'<a href="{url}" style="color:{NARANJA}">{texto}</a></p>')
    sys.exit(f"ERROR: tipo de bloque desconocido: {tipo}")


def cuerpo(c):
    # Un único separador entre bloques, nunca dos seguidos ni al principio o al final:
    # así todas las separaciones del cuerpo miden lo mismo.
    return f"\n{SEPARADOR}\n".join(_bloque(b) for b in c["bloques"])


def titular(c):
    return f'<h1 style="line-height: 125%; font-weight: normal;">{html.escape(c["titular"])}</h1>'


def preview(c):
    # Copia del HTML real de HubSpot (plantilla-email.html) con los huecos rellenos.
    boton = ""
    if c.get("boton"):
        url = html.escape(c["boton"]["url"], quote=True)
        boton = f"""            <table role="presentation" cellpadding="0" cellspacing="0" width="100%"><tbody><tr><td style="font-family:Arial, sans-serif; font-size:16px; color:{TEXTO}; word-break:break-word; padding:24px 20px">
              <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-collapse:separate;"><tbody><tr>
                <td align="center" valign="middle" bgcolor="{NARANJA}" style="font-family:Arial, sans-serif; font-size:16px; word-break:break-word; border-radius:4px; background-color:{NARANJA}">
                  <a href="{url}" target="_blank" style="font-size:15px; font-family:Arial, sans-serif; text-decoration:none; padding:12px 18px; display:block"><strong style="color:#ffffff;font-weight:bold;text-decoration:none;font-style:normal;">{html.escape(c["boton"]["texto"])}</strong></a>
                </td>
              </tr></tbody></table>
            </td></tr></tbody></table>"""
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "plantilla-email.html"), encoding="utf-8") as f:
        plantilla = f.read()
    plantilla = plantilla[plantilla.index("-->") + 3:].lstrip()
    return (plantilla.replace("{{TITULAR}}", f'<h1 {H1}>{html.escape(c["titular"])}</h1>')
            .replace("{{CUERPO}}", cuerpo(c))
            .replace("{{BOTON}}", boton)
            .replace("{{FIRMA}}", FIRMA))


def main(argv):
    if len(argv) != 3 or argv[1] not in ("cuerpo", "titular", "preview"):
        sys.exit(__doc__)
    with open(argv[2], encoding="utf-8") as f:
        c = json.load(f)
    print({"cuerpo": cuerpo, "titular": titular, "preview": preview}[argv[1]](c))


if __name__ == "__main__":
    main(sys.argv)
