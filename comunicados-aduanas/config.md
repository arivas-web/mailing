# Configuración — Comunicados de Aduanas

Valores que usa el subagente `comunicados-aduanas`. Edita aquí, no en el prompt del agente.

## Gmail (fase 1: detección)

- Destinatarios vigilados: `arivas@visualms.com`, `arivas@visualtrans.com`
- Disparador: el correo contiene "Novedades AEAT" (también se acepta "Novedades AAT")
- Query de búsqueda:

  ```
  (to:arivas@visualms.com OR to:arivas@visualtrans.com OR deliveredto:arivas@visualms.com OR deliveredto:arivas@visualtrans.com) ("novedades AEAT" OR "novedades AAT") newer_than:7d -from:soporte@visualtrans.com -from:noreply@hubspot.com -subject:"Test send" -label:aduanas-borrador-enviado -label:aduanas-publicado
  ```

  Las exclusiones `-from:` / `-subject:"Test send"` evitan que el agente vuelva a detectar nuestros propios comunicados ya enviados por HubSpot (usan el mismo asunto "Novedades AEAT: …") y sus envíos de prueba.

- Etiquetas de estado (se crean si no existen):
  - `Aduanas/Borrador enviado` → borrador propuesto en el chat, pendiente de validación
  - `Aduanas/Publicado` → email ya creado en HubSpot

  En la query se usan los IDs de etiqueta (obtenerlos con `list_labels`); los nombres de arriba son los visibles.

## HubSpot (fase 3: creación)

- Plantilla: **Genérica Visual Trans**
- La API de HubSpot no lista las plantillas guardadas personalizadas, así que la creación se hace así:
  1. `LIST_TEMPLATES` (DND y CODED) buscando `generica` / `visual`. Si aparece, `CREATE` con ese `templatePath`.
  2. Si no aparece, `CLONE` del email base de abajo (creado con la plantilla Genérica Visual Trans) y `EDIT_CONTENT`.
- Email base para clonar (`marketingEmailObjectId`): **PENDIENTE** — crea en HubSpot un email vacío con la plantilla "Genérica Visual Trans", llámalo `BASE comunicados aduanas` y pon aquí su ID.
- Nombre interno: `AAAA MM <tema corto>_aduanas` (ej. `2026 10 cambios DUA_aduanas`), igual que el resto de emails del portal.
- Remitente (`fromName`), reply-to y tipo de suscripción: **PENDIENTE** — se confirman con el usuario la primera vez (`LIST_FROM_ADDRESSES`, `LIST_SUBSCRIPTION_TYPES`) y se anotan aquí.
- Tipo: BATCH. Se deja siempre en **borrador**; nunca se programa ni se envía.
