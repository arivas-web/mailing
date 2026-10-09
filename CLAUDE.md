# Mailing — Visual Trans / Visual MS

Agente de mailing. Delega en subagentes especializados de `.claude/agents/`.

## Subagentes

### comunicados-aduanas
Convierte los correos "Novedades AEAT" que llegan a arivas@visualms.com / arivas@visualtrans.com en comunicados para clientes en HubSpot (plantilla "Genérica Visual Trans").

Flujo en tres fases — no te saltes la validación:
1. **Detectar** — el subagente busca en Gmail los correos nuevos (`/aduanas` o la rutina programada).
2. **Borrador** — el subagente redacta el comunicado y tú se lo enseñas al usuario completo en el chat.
3. **Publicar** — solo cuando el usuario lo valide explícitamente, vuelves a lanzar el subagente en modo PUBLICAR con el texto final; crea el email en HubSpot en borrador (nunca lo envía ni lo programa).

Configuración: `comunicados-aduanas/config.md`. Ejemplos de estilo: `comunicados-aduanas/ejemplos.txt`.
