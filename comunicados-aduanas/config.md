# Configuración — Comunicados de Aduanas

Valores que usa el subagente `comunicados-aduanas`. Edita aquí, no en el prompt del agente.

## HubSpot

- Plantilla: **Genérica Visual Trans**
- La API de HubSpot no lista las plantillas guardadas personalizadas, así que la creación se hace así:
  1. `LIST_TEMPLATES` (DND y CODED) buscando `generica` / `visual`. Si aparece, `CREATE` con ese `templatePath`.
  2. Si no aparece, `CLONE` del email base de abajo (creado con la plantilla Genérica Visual Trans) y `EDIT_CONTENT`.
- Email base para clonar (`marketingEmailObjectId`): **PENDIENTE** — crea en HubSpot un email vacío con la plantilla "Genérica Visual Trans", llámalo `BASE comunicados aduanas` y pon aquí su ID.
- Nombre interno: `AAAA MM <tema corto>_aduanas` (ej. `2026 10 cambios DUA_aduanas`), igual que el resto de emails del portal.
- Remitente: los comunicados anteriores salen de `soporte@visualtrans.com` como "Equipo de Visual Trans". Si se clona el email base se heredan; si no, confirmar con el usuario (`LIST_FROM_ADDRESSES`, `LIST_SUBSCRIPTION_TYPES`) y anotarlo aquí.
- Tipo: BATCH. Se deja siempre guardado como **borrador**; nunca se programa ni se envía.
