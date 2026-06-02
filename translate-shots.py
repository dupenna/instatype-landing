#!/usr/bin/env python3
"""Generate PT-BR and ES copies of the 5 EN screenshot HTMLs."""
import os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(ROOT, "screenshots")

# Each tuple: EN -> PT -> ES. Keys must be unique strings in the source.
T = {
    # ---------- 01-sidepanel ----------
    "01": [
        ("Side panel", "Painel lateral", "Panel lateral"),
        ("A library for<br>your <span class=\"accent\">text</span>.",
         "Uma biblioteca<br>para seu <span class=\"accent\">texto</span>.",
         "Una biblioteca<br>para tu <span class=\"accent\">texto</span>."),
        ("Create, search, organize and edit your snippets without leaving the tab you're on.",
         "Crie, busque, organize e edite seus snippets sem sair da aba.",
         "Crea, busca, organiza y edita tus fragmentos sin salir de la pestaña."),
        ("Mark a snippet as <b>Global</b> or scope it to a single domain",
         "Marque um snippet como <b>Global</b> ou restrinja a um domínio",
         "Marca un fragmento como <b>Global</b> o restringelo a un dominio"),
        ("Filter by site to focus on what's relevant <b>right now</b>",
         "Filtre por site e foque no que importa <b>agora</b>",
         "Filtra por sitio y enfócate en lo relevante <b>ahora</b>"),
        ("Built-in <b>import &amp; export</b> to back up or sync between devices",
         "<b>Importar e exportar</b> integrado para backup ou sincronizar dispositivos",
         "<b>Importar y exportar</b> integrado para respaldo o sincronizar dispositivos"),
        ("New snippet", "Novo snippet", "Nuevo fragmento"),
        (">All<", ">Tudo<", ">Todo<"),
        (">Global<", ">Globais<", ">Globales<"),
        ("This site", "Deste site", "Este sitio"),
        ("Email signature", "Assinatura de email", "Firma de correo"),
        (">Global</span>", ">Global</span>", ">Global</span>"),  # badge stays
        ("Alex Souza\nProduct designer · Studio Atlas\n+55 48 99999-0000",
         "Alex Souza\nProduct designer · Studio Atlas\n+55 48 99999-0000",
         "Alex Souza\nProduct designer · Studio Atlas\n+55 48 99999-0000"),
        ("Yesterday", "Ontem", "Ayer"),
        ("PR review checklist", "Checklist de revisão de PR", "Lista de revisión de PR"),
        ("### Review checklist\n- [ ] Tests pass\n- [ ] No console logs\n- [ ] Migrations reversible",
         "### Checklist de revisão\n- [ ] Testes passam\n- [ ] Sem console.log\n- [ ] Migrations reversíveis",
         "### Lista de revisión\n- [ ] Tests pasan\n- [ ] Sin console.log\n- [ ] Migraciones reversibles"),
        ("3 days ago", "3 dias atrás", "hace 3 días"),
        (">Tax ID<", ">CPF<", ">RFC<"),
        ("Last week", "Semana passada", "La semana pasada"),
        ("Edit", "Editar", "Editar"),
        ("Delete", "Excluir", "Eliminar"),
        ("Search…", "Buscar…", "Buscar…"),
        ("Shortcut on any field", "Atalho em qualquer campo", "Atajo en cualquier campo"),
    ],

    # ---------- 02-shortcut ----------
    "02": [
        ("Keyboard shortcut", "Atalho de teclado", "Atajo de teclado"),
        ("Summon snippets<br><span class=\"accent\">without leaving</span> the keyboard.",
         "Invoque snippets<br><span class=\"accent\">sem largar</span> o teclado.",
         "Invoca fragmentos<br><span class=\"accent\">sin soltar</span> el teclado."),
        ("Press the shortcut on any input, search, pick — done. No mouse, no detours.",
         "Pressione o atalho em qualquer campo, busque, escolha — pronto. Sem mouse, sem desvio.",
         "Pulsa el atajo en cualquier campo, busca, elige — listo. Sin ratón, sin desvíos."),
        ("Send invoice reminder", "Lembrete de fatura", "Recordatorio de factura"),
        ("Compose your message below. Use a snippet to speed things up.",
         "Escreva sua mensagem abaixo. Use um snippet para acelerar.",
         "Escribe tu mensaje abajo. Usa un fragmento para acelerar."),
        ("Message", "Mensagem", "Mensaje"),
        ("Hi {name}, just a quick reminder about invoice #",
         "Olá {nome}, lembrete rápido sobre a fatura #",
         "Hola {nombre}, recordatorio rápido sobre la factura #"),
        ("Invoice reminder", "Lembrete de fatura", "Recordatorio de factura"),
        ("Hi {name}, just a friendly reminder…",
         "Olá {nome}, um lembrete amigável…",
         "Hola {nombre}, un recordatorio amistoso…"),
        ("Late payment notice", "Aviso de atraso", "Aviso de pago atrasado"),
        ("This is a follow-up regarding invoice…",
         "Este é um follow-up sobre a fatura…",
         "Este es un seguimiento sobre la factura…"),
        ("Remote work request", "Pedido de home office", "Solicitud de teletrabajo"),
        ("Hi team, I'll be working remotely…",
         "Olá time, estarei em home office…",
         "Hola equipo, estaré trabajando remoto…"),
    ],

    # ---------- 03-context-menu ----------
    "03": [
        ("Right-click menu", "Menu de contexto", "Menú contextual"),
        ("Native menu,<br><span class=\"accent\">no extra UI.</span>",
         "Menu nativo,<br><span class=\"accent\">sem UI extra.</span>",
         "Menú nativo,<br><span class=\"accent\">sin UI extra.</span>"),
        ("InstaType lives in the browser's own context menu. Right-click any input — your snippets are right there, filtered by the site you're on.",
         "O InstaType vive no menu de contexto do navegador. Clique direito em qualquer campo — seus snippets estão ali, filtrados pelo site atual.",
         "InstaType vive en el menú contextual del navegador. Clic derecho en cualquier campo — tus fragmentos están ahí, filtrados por el sitio actual."),
        ("Works on all editable fields", "Funciona em qualquer campo editável", "Funciona en cualquier campo editable"),
        ("New support ticket", "Novo chamado de suporte", "Nuevo ticket de soporte"),
        ("Reply with one of your saved templates.",
         "Responda com um de seus templates salvos.",
         "Responde con una de tus plantillas guardadas."),
        ("Subject", "Assunto", "Asunto"),
        ("Issue with deployment", "Problema no deploy", "Problema con el deploy"),
        ("Message", "Mensagem", "Mensaje"),
        ("Hi, thanks for reaching out. Could you share",
         "Olá, obrigado pelo contato. Pode compartilhar",
         "Hola, gracias por escribir. ¿Podrías compartir"),
        ("Back", "Voltar", "Atrás"),
        ("Forward", "Avançar", "Adelante"),
        ("Reload", "Recarregar", "Recargar"),
        ("Save as…", "Salvar como…", "Guardar como…"),
        ("Print…", "Imprimir…", "Imprimir…"),
        ("Save selection to InstaType", "Salvar seleção no InstaType", "Guardar selección en InstaType"),
        ("Inspect", "Inspecionar", "Inspeccionar"),
        ("For this site", "Deste site", "Este sitio"),
        ("Standard reply", "Resposta padrão", "Respuesta estándar"),
        ("Follow-up template", "Template de follow-up", "Plantilla de seguimiento"),
        ("Escalation script", "Script de escalada", "Script de escalación"),
        ("Email signature", "Assinatura de email", "Firma de correo"),
        ("Phone number", "Número de telefone", "Número de teléfono"),
        ("Mailing address", "Endereço postal", "Dirección postal"),
    ],

    # ---------- 04-editor ----------
    "04": [
        ("Per-site scopes", "Escopo por site", "Alcance por sitio"),
        ("One library,<br><span class=\"accent\">smart</span> scopes.",
         "Uma biblioteca,<br>escopos <span class=\"accent\">inteligentes</span>.",
         "Una biblioteca,<br>alcances <span class=\"accent\">inteligentes</span>."),
        ("Mark snippets as global or scope them to a single domain. Right-click and the menu auto-filters to what's relevant for the page you're on.",
         "Marque snippets como globais ou restrinja a um domínio. O clique direito filtra automaticamente o que importa na página atual.",
         "Marca fragmentos como globales o restringelos a un dominio. El clic derecho filtra automáticamente lo relevante para la página actual."),
        ("Snippets you only need on <b>github.com</b>, stay on <b>github.com</b>",
         "Snippets que só precisa no <b>github.com</b> ficam no <b>github.com</b>",
         "Fragmentos que solo usas en <b>github.com</b> se quedan en <b>github.com</b>"),
        ("Toggle between global and site-specific in one click",
         "Alterne entre global e por site com um clique",
         "Alterna entre global y por sitio con un clic"),
        ("Quick-set to the current tab when scoping",
         "Atalho para usar o domínio da aba atual",
         "Atajo para usar el dominio de la pestaña actual"),
        ("New snippet", "Novo snippet", "Nuevo fragmento"),
        ("Compose a snippet.", "Componha um snippet.", "Compón un fragmento."),
        ("Title", "Título", "Título"),
        ("required", "obrigatório", "obligatorio"),
        ("PR review checklist", "Checklist de revisão de PR", "Lista de revisión de PR"),
        ("Content", "Conteúdo", "Contenido"),
        ("96 chars", "96 caracteres", "96 caracteres"),
        ("### Review checklist\n- [ ] Tests pass\n- [ ] No console logs\n- [ ] Migrations reversible",
         "### Checklist de revisão\n- [ ] Testes passam\n- [ ] Sem console.log\n- [ ] Migrations reversíveis",
         "### Lista de revisión\n- [ ] Tests pasan\n- [ ] Sin console.log\n- [ ] Migraciones reversibles"),
        ("Scope", "Escopo", "Alcance"),
        ("Applies to <b>github.com</b>", "Aplica em <b>github.com</b>", "Se aplica a <b>github.com</b>"),
        (">Global<", ">Global<", ">Global<"),
        ("Specific site", "Site específico", "Sitio específico"),
        (">Domain<", ">Domínio<", ">Dominio<"),
        ("Cancel", "Cancelar", "Cancelar"),
        ("Save", "Salvar", "Guardar"),
    ],

    # ---------- 05-i18n-import ----------
    "05": [
        ("Yours, portable", "Seus, portáteis", "Tuyos, portátiles"),
        ("Multi-language.<br><span class=\"accent\">Multi-device.</span>",
         "Multi-idioma.<br><span class=\"accent\">Multi-dispositivo.</span>",
         "Multi-idioma.<br><span class=\"accent\">Multi-dispositivo.</span>"),
        ("UI in English, Portuguese and Spanish — follows your system by default. Export your library, restore on any device.",
         "Interface em Inglês, Português e Espanhol — segue o sistema por padrão. Exporte sua biblioteca, restaure em qualquer dispositivo.",
         "Interfaz en Inglés, Portugués y Español — sigue el sistema por defecto. Exporta tu biblioteca, restaúrala en cualquier dispositivo."),
        ("Export templates", "Exportar templates", "Exportar plantillas"),
        ("Import templates…", "Importar templates…", "Importar plantillas…"),
        ("Language", "Idioma", "Idioma"),
        ("System · English ▶", "Sistema · Português ▶", "Sistema · Español ▶"),
        ("7 templates · 4.1 KB", "7 templates · 4,1 KB", "7 plantillas · 4,1 KB"),
    ],
}

# Update <html lang="…"> attribute
LANG_ATTR = {"pt": "pt-BR", "es": "es-ES"}

for shot_id, subs in T.items():
    candidates = [f for f in os.listdir(SHOTS)
                  if f.startswith(shot_id) and f.endswith(".html")
                  and not f.endswith("-pt.html") and not f.endswith("-es.html")]
    src = candidates[0]
    src_path = os.path.join(SHOTS, src)
    with open(src_path, encoding="utf-8") as f:
        html = f.read()
    for lang_idx, lang_key in enumerate(["pt", "es"], start=1):
        out = html
        for tup in subs:
            en = tup[0]
            tgt = tup[lang_idx]
            out = out.replace(en, tgt)
        # change <html lang>
        out = re.sub(r'<html lang="[^"]*"', f'<html lang="{LANG_ATTR[lang_key]}"', out, count=1)
        out_name = src.replace(".html", f"-{lang_key}.html")
        with open(os.path.join(SHOTS, out_name), "w", encoding="utf-8") as f:
            f.write(out)
        print(f"  wrote {out_name}")

print("done.")
