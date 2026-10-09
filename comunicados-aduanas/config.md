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
  | `module-1-0-2` | rich_text | cuerpo (`<p>` separados por `<p>&nbsp;</p>`, negritas con `<strong>`) | sí: todo el cuerpo |
  | `module-1-0-3` | button_email | botón naranja #f15f27 (`text`, `destination`) | sí: texto y enlace |
  | `module-5-0-0` | rich_text | despedida y firma | según remitente (ver abajo) |
  | `module-6-0-0` | follow_me | LinkedIn | no |
  | `module-7-0-0` | email_footer | dirección y baja | no |
  | `preview_text` | text | texto de previsualización (`body.value`) | sí |
- Solo hay un botón. Si el comunicado tiene varias novedades, cada una va en el cuerpo con su enlace "Más información" como `<a href>` en línea; el botón se usa para el enlace principal.
- Al hacer PATCH se envía el objeto `content.widgets` completo (copiado del `get` del clon) con solo esos campos modificados.
- Remitente, firma y listas: **PENDIENTE de decidir**. El email base sale de Emma González (egonzalez@visualtrans.com, firma "Emma González / Marketing en Visual Trans") con sus listas de destinatarios. Los comunicados AEAT anteriores salían de soporte@visualtrans.com, firmados "Equipo de Visual Trans", a las listas Suite + Empuries. El clon hereda remitente y listas del base: ajustarlos en el PATCH cuando se decida.
- Nombre interno: `AAAA MM AEAT DD/MM_Suite + Empuries` (ej. `2026 09 AEAT 23/09_Suite + Empuries`), igual que los comunicados anteriores. Si hay dos el mismo día: `AAAA MM AEAT 2 DD/MM_…`.
- Los IDs para la API son el `hs_origin_asset_id` (el número de la URL del editor de HubSpot), no el `hs_object_id` del CRM.
- Remitente: los comunicados anteriores salen de `soporte@visualtrans.com`. Si se clona el email base se heredan; si no, confirmar con el usuario (`LIST_FROM_ADDRESSES`, `LIST_SUBSCRIPTION_TYPES`) y anotarlo aquí.
- Tipo: BATCH. Se deja siempre guardado como **borrador**; nunca se programa ni se envía.
