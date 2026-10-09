# Configuración — Comunicados de Aduanas

Valores que usa el subagente `comunicados-aduanas`. Edita aquí, no en el prompt del agente.

## HubSpot

- Plantilla: **Genérica Visual Trans**
- Acceso: API de HubSpot con token de app privada (scope `content`) guardado como secreto de GitHub `HUBSPOT_TOKEN` (nunca en el código). Se usa desde el workflow `.github/workflows/hubspot.yml`, que ejecuta `comunicados-aduanas/hubspot_api.py`.
- Creación: se **clona** el email base de abajo (hecho con la plantilla Genérica Visual Trans) y se sustituyen los textos.
- Email base para clonar (`marketingEmailObjectId`): **PENDIENTE** — crea en HubSpot un email vacío con la plantilla "Genérica Visual Trans", llámalo `BASE comunicados aduanas` y pon aquí su ID.
- Nombre interno: `AAAA MM <tema corto>_aduanas` (ej. `2026 10 cambios DUA_aduanas`), igual que el resto de emails del portal.
- Remitente: los comunicados anteriores salen de `soporte@visualtrans.com`. Si se clona el email base se heredan; si no, confirmar con el usuario (`LIST_FROM_ADDRESSES`, `LIST_SUBSCRIPTION_TYPES`) y anotarlo aquí.
- Tipo: BATCH. Se deja siempre guardado como **borrador**; nunca se programa ni se envía.
