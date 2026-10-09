---
description: Revisa Gmail en busca de "Novedades AEAT" y propone el comunicado de aduanas
---

Lanza el subagente `comunicados-aduanas` en modo DETECTAR.

- Si devuelve `SIN NOVEDADES`, dilo en una línea.
- Si devuelve borradores, enséñamelos completos tal cual y pregúntame si los valido o qué cambio.
- Cuando yo valide un borrador (con o sin cambios), lanza de nuevo `comunicados-aduanas` en modo PUBLICAR pasándole el texto final y el threadId, y dame el enlace de HubSpot que devuelva.
- No pases a PUBLICAR sin mi validación explícita.

$ARGUMENTS
