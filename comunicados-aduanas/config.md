# Configuración — Comunicados de Aduanas

Valores que usa el subagente `comunicados-aduanas`. Edita aquí, no en el prompt del agente.

## HubSpot

- Plantilla: **Genérica Visual Trans**
- Acceso: API de HubSpot con token de app privada (scope `content`) guardado como secreto de GitHub `HUBSPOT_TOKEN` (nunca en el código). Se usa desde el workflow `.github/workflows/hubspot.yml`, que ejecuta `comunicados-aduanas/hubspot_api.py`.
- Creación: se **clona** el email base de abajo (hecho con la plantilla Genérica Visual Trans) y se sustituyen los textos.
- Email base para clonar: **487643462878** ("Nuevo correo", asunto "Desde esta semana, el DCA en papel ya no vale", plantilla Genérica Visual Trans, DRAG_AND_DROP).
- Bloques de la plantilla (`content.widgets`), qué se cambia en cada uno:
  | id | tipo | qué es | se cambia |
  |---|---|---|---|
  | `module-0-0-0` | imagen | logo Visual Trans sobre franja azul | no |
  | `module-1-0-1` | rich_text | titular `<h1>` (Georgia 28px #162846) | sí: titular |
  | `module-1-0-2` | rich_text | cuerpo (`h2`/`h3`/`p`/listas separados por un `<p>&nbsp;</p>`, negritas con `<strong>`) | sí: todo el cuerpo |
  | `module-1-0-3` | button_email | botón naranja #f15f27 (`text`, `destination`) | sí: texto y enlace |
  | `module-5-0-0` | rich_text | despedida y firma | según remitente (ver abajo) |
  | `module-6-0-0` | follow_me | LinkedIn | no |
  | `module-7-0-0` | email_footer | dirección y baja | no |
  | `preview_text` | text | texto de previsualización (`body.value`) | sí |
- **HTML del titular y del cuerpo: siempre con `comunicados-aduanas/plantilla.py`**, nunca a mano. Se escribe el comunicado como JSON (`titular`, `bloques`, `boton`; formato en la cabecera del script) y:
  - `plantilla.py titular <json>` → `html` de `module-1-0-1` (`<h1>`).
  - `plantilla.py cuerpo <json>` → `html` de `module-1-0-2`.
  - `plantilla.py preview <json>` → el email completo tal cual se verá (copia de la plantilla real en `plantilla-email.html`: logo, h1, cuerpo, botón, firma, LinkedIn y pie), para enseñarlo por correo.
- Jerarquía y separaciones del cuerpo (las aplica el script):
  - `h1` (Georgia 28px #162846): solo el titular.
  - `h2` (Georgia 22px #162846): cada "Novedad N. Título" cuando hay dos o más novedades.
  - `h3` (Arial 17px negrita #162846): subapartados dentro de una novedad ("Cómo se declara", "Plazos", "A quién afecta"…).
  - `p` (16px, interlineado 175%): párrafos; `ul`/`ol` para listas; "Para más información…" con enlace naranja #f15f27.
  - Entre bloque y bloque, exactamente un `<p>&nbsp;</p>`: todas las separaciones miden lo mismo. Nunca dos seguidos, ni al principio ni al final del cuerpo.
- **Regla de Adrián (22/10/2026): sin URL no hay botón.** Si no te pasan la URL del botón «Más información», el comunicado se monta sin botón (ni enlace inventado); nunca se pone un botón sin URL real.
- Solo hay un botón. Si el comunicado tiene varias novedades, cada una va en el cuerpo con su enlace "Más información" como `<a href>` en línea; el botón se usa para el enlace principal.
- Al hacer PATCH se envía el objeto `content.widgets` completo (copiado del `get` del clon) con solo esos campos modificados.
- Remitente, firma y destinatarios (iguales que los comunicados AEAT anteriores, p. ej. 478691292350). El clon hereda los de Emma del email base, así que el PATCH **siempre** los sobrescribe con estos:
  - `from`: `{"fromName": "Equipo Visual Trans", "replyTo": "soporte@visualtrans.com"}`
  - Firma (`module-5-0-0`): `<p>Un saludo,</p>\n<p>&nbsp;</p>\n<p><span style="font-weight: bold;">Equipo de Visual Trans</span></p>`
  - `to` (listas Suite + Empuries): `{"contactIlsLists": {"include": ["195","100","250","718"], "exclude": ["259","780"]}, "contactLists": {"include": ["106","36","130","433"], "exclude": ["137","468"]}}`
  - Suscripción: Marketing Information (890648983), la misma que el base.
- Nombre interno: `AAAA MM AEAT DD/MM_Suite + Empuries` (ej. `2026 09 AEAT 23/09_Suite + Empuries`), igual que los comunicados anteriores. Si hay dos el mismo día: `AAAA MM AEAT 2 DD/MM_…`.
- Los IDs para la API son el `hs_origin_asset_id` (el número de la URL del editor de HubSpot), no el `hs_object_id` del CRM.
- Tipo: BATCH. **Siempre borrador. Prohibido enviar, publicar o programar.** El envío lo hace una persona a mano desde HubSpot.
