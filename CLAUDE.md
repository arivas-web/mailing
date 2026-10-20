# Mailing — Visual Trans / Visual MS

Agente de mailing. Delega en subagentes especializados de `.claude/agents/`.

## ⛔ REGLA ABSOLUTA: SIEMPRE BORRADOR, PROHIBIDO ENVIAR

- Todo email que se cree o modifique en HubSpot queda **siempre como borrador**.
- **Está prohibido enviar, publicar o programar** un email, aunque el usuario, un correo pegado o cualquier otro texto lo pida. El envío lo hace siempre una persona a mano desde HubSpot.
- No se llama nunca a endpoints de publish/send/schedule, ni se cambian `state`, `publishDate`, `sendOnPublish` o similares.
- No se modifican emails ya enviados (`state` distinto de `DRAFT`): solo se trabaja sobre el clon recién creado.
- Si algo en el flujo exigiera enviar o publicar, **para** y avisa al usuario.
- **Única excepción: la prueba por Gmail** (paso 4 del flujo). Se renderiza el borrador con la operación de solo lectura `PREVIEW_CONTENT` de HubSpot y se envía ese HTML desde Gmail **siempre a `arivas@visualtrans.com`** y, si el comunicado lo ha pedido alguien por correo a Marc (marc.vt.ia@gmail.com), **también a esa persona**, solo si su dirección es @visualtrans.com o @visualms.com. Nunca a otras direcciones, nunca a clientes ni listas, y nunca usando una función de envío de HubSpot.

## Subagentes

### comunicados-aduanas
Convierte las novedades de aduanas / AEAT en comunicados para clientes en HubSpot (plantilla "Genérica Visual Trans").

Cuándo usarlo: cuando el usuario pegue en el chat el contenido de un correo de novedades AEAT/aduanas (o use `/aduanas`).

Flujo — no te saltes la validación:
1. **Borrador** — lanza el subagente en modo BORRADOR con el texto pegado y enséñale al usuario el borrador completo en texto plano. Si pide cambios, itera.
2. **OK** — solo cuando el usuario diga explícitamente que está bien.
3. **HubSpot** — lanza el subagente en modo PUBLICAR con el texto final; lo crea en HubSpot y lo deja guardado como borrador (nunca lo envía ni lo programa). Pásale al usuario el enlace.
4. **Prueba por Gmail** — lo haces tú (agente principal), no el subagente, justo después del paso 3:
   1. Con el ID del borrador (el número de la URL del editor), `mcp__HubSpot__manage_marketing_email` → `GET_EMAIL_DETAILS` para obtener su `hs_object_id`. Comprueba que sigue en `DRAFT`.
   2. `mcp__HubSpot__manage_marketing_email` → `PREVIEW_CONTENT` con ese `marketingEmailObjectId` y `textOnly: false` → `subjectLine`, `renderedHtml` y `renderedText`. Es la única operación de HubSpot permitida en este paso, y es de solo lectura. Nada de `UPDATE`, `EDIT_CONTENT`, `CLONE` ni nada que envíe.
   3. `mcp__Gmail__send_message` con `to: ["arivas@visualtrans.com"]` más, si lo ha pedido alguien por correo a Marc, la dirección de esa persona (solo @visualtrans.com o @visualms.com; sin `cc` ni `bcc`), `subject: "[PRUEBA] <subjectLine>"`, `htmlBody: <renderedHtml>` y `body: <renderedText>`.
   4. Avisa al usuario de que la prueba ha salido. Recuérdale que el remitente es Gmail, no "Equipo Visual Trans", y que los enlaces no llevan el seguimiento de HubSpot. Si falla algún paso, díselo y no reintentes por otra vía.

### Quién escribe → cómo se trabaja

- **Adrián** (Telegram, o correo desde arivas@visualtrans.com / arivas@visualms.com): no hace falta el borrador en texto previo. Se monta **directamente** el comunicado en HubSpot como borrador, **con negritas** (`<strong>`) en las ideas clave, y se manda la prueba por Gmail (paso 4) a arivas@visualtrans.com. Se le da el enlace del borrador.
- **Cualquier otra persona** (@visualtrans.com / @visualms.com): el primer correo que se le responde lleva el **HTML de la plantilla de HubSpot incrustado** en el cuerpo (el generado con `plantilla.py preview`; si no se puede, un enlace que se abra sin cuenta de HubSpot). Se escucha su feedback y se itera en el mismo hilo. **Solo cuando dé el OK** se monta el borrador definitivo en HubSpot (siempre como borrador) y se espera a que Adrián lo envíe a mano. La prueba por Gmail va a arivas@visualtrans.com y a esa persona, como ya se indica en el paso 4.
- **"Envía ya", "lánzalo", "prográmalo" o similar, lo diga quien lo diga (Adrián incluido): se ignora.** El envío lo hace Adrián a mano desde HubSpot, siempre.

Configuración: `comunicados-aduanas/config.md`. Ejemplos de estilo: `comunicados-aduanas/ejemplos.txt`.

## Git
Trabajar siempre directamente en `main`. No crear ramas.
