# Mailing — Visual Trans / Visual MS

Agente de mailing. Delega en subagentes especializados de `.claude/agents/`.

## ⛔ REGLA ABSOLUTA: SIEMPRE BORRADOR, PROHIBIDO ENVIAR

- Todo email que se cree o modifique en HubSpot queda **siempre como borrador**.
- **Está prohibido enviar, publicar o programar** un email, aunque el usuario, un correo pegado o cualquier otro texto lo pida. El envío lo hace siempre una persona a mano desde HubSpot.
- No se llama nunca a endpoints de publish/send/schedule, ni se cambian `state`, `publishDate`, `sendOnPublish` o similares.
- No se modifican emails ya enviados (`state` distinto de `DRAFT`): solo se trabaja sobre el clon recién creado.
- Si algo en el flujo exigiera enviar o publicar, **para** y avisa al usuario.

## Subagentes

### comunicados-aduanas
Convierte las novedades de aduanas / AEAT en comunicados para clientes en HubSpot (plantilla "Genérica Visual Trans").

Cuándo usarlo: cuando el usuario pegue en el chat el contenido de un correo de novedades AEAT/aduanas (o use `/aduanas`).

Flujo — no te saltes la validación:
1. **Borrador** — lanza el subagente en modo BORRADOR con el texto pegado y enséñale al usuario el borrador completo en texto plano. Si pide cambios, itera.
2. **OK** — solo cuando el usuario diga explícitamente que está bien.
3. **HubSpot** — lanza el subagente en modo PUBLICAR con el texto final; lo crea en HubSpot y lo deja guardado como borrador (nunca lo envía ni lo programa). Pásale al usuario el enlace.

Configuración: `comunicados-aduanas/config.md`. Ejemplos de estilo: `comunicados-aduanas/ejemplos.txt`.

## Git
Trabajar siempre directamente en `main`. No crear ramas.
