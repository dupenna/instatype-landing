#!/usr/bin/env python3
"""Generate EN and ES copies of index.html (PT source-of-truth)."""
import os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "index.html")

# Each tuple: (PT, EN, ES). Order matters — PT is the source.
# Longer / more-unique strings come first to avoid partial matches.
T = [
    # ---------- <head> ----------
    ('<html lang="pt-BR">', '<html lang="en-US">', '<html lang="es-ES">'),
    ("InstaType — Templates de texto para o Chrome",
     "InstaType — Text snippets for Chrome",
     "InstaType — Plantillas de texto para Chrome"),
    ("Salve trechos de texto e cole em qualquer campo da web com um clique direito, no Side Panel ou pelo atalho de teclado. Privado, offline, gratuito.",
     "Save text snippets and paste them into any web field with a right-click, the Side Panel, or a keyboard shortcut. Private, offline, free.",
     "Guarda fragmentos de texto y pégalos en cualquier campo web con clic derecho, panel lateral o un atajo de teclado. Privado, offline, gratis."),
    ("Salve trechos de texto e cole em qualquer campo da web. Privado, offline, gratuito.",
     "Save text snippets and paste them into any web field. Private, offline, free.",
     "Guarda fragmentos de texto y pégalos en cualquier campo web. Privado, offline, gratis."),

    # ---------- NAV ----------
    (">Recursos<", ">Features<", ">Funciones<"),
    (">Como funciona<", ">How it works<", ">Cómo funciona<"),
    (">Privacidade<", ">Privacy<", ">Privacidad<"),
    (">Política<", ">Policy<", ">Política<"),
    (">Instalar grátis<", ">Install free<", ">Instalar gratis<"),

    # lang switcher — mark the right one as .current
    ('<a href="index.html" class="current">PT</a>\n        <a href="index-en.html">EN</a>\n        <a href="index-es.html">ES</a>',
     '<a href="index.html">PT</a>\n        <a href="index-en.html" class="current">EN</a>\n        <a href="index-es.html">ES</a>',
     '<a href="index.html">PT</a>\n        <a href="index-en.html">EN</a>\n        <a href="index-es.html" class="current">ES</a>'),

    # ---------- HERO ----------
    ("v1.0 · Manifest V3 · Chrome &amp; Edge",
     "v1.0 · Manifest V3 · Chrome &amp; Edge",
     "v1.0 · Manifest V3 · Chrome y Edge"),
    ('Seus snippets,<br>a <span class="accent">um atalho</span> de distância.',
     'Your snippets,<br>one <span class="accent">shortcut</span> away.',
     'Tus fragmentos,<br>a <span class="accent">un atajo</span> de distancia.'),
    ("Salve assinaturas, respostas prontas, endereços, blocos de código — e cole em qualquer campo da web em dois cliques ou com uma única combinação de teclas.",
     "Save signatures, canned replies, addresses, code blocks — and paste them into any web field in two clicks or one keystroke.",
     "Guarda firmas, respuestas guardadas, direcciones, bloques de código — y pégalos en cualquier campo web en dos clics o una combinación de teclas."),
    ("Instalar no Chrome", "Install on Chrome", "Instalar en Chrome"),
    (">GRÁTIS<", ">FREE<", ">GRATIS<"),
    (">Ver como funciona<", ">See how it works<", ">Ver cómo funciona<"),
    (">100% offline<", ">100% offline<", ">100% offline<"),
    (">Sem cadastro<", ">No account<", ">Sin cuenta<"),
    (">Português, English, Español<",
     ">Português, English, Español<",
     ">Português, English, Español<"),
    (">+ Novo snippet<", ">+ New snippet<", ">+ Nuevo fragmento<"),
    (">Assinatura de email<", ">Email signature<", ">Firma de correo<"),
    ('<div class="hp-prev">Alex Souza\nProduct designer · Studio Atlas</div>',
     '<div class="hp-prev">Alex Souza\nProduct designer · Studio Atlas</div>',
     '<div class="hp-prev">Alex Souza\nProduct designer · Studio Atlas</div>'),
    (">Checklist de PR <", ">PR checklist <", ">Lista de PR <"),
    ('<div class="hp-prev">### Checklist\n- [ ] Testes\n- [ ] Sem console.log</div>',
     '<div class="hp-prev">### Checklist\n- [ ] Tests\n- [ ] No console.log</div>',
     '<div class="hp-prev">### Lista\n- [ ] Tests\n- [ ] Sin console.log</div>'),
    ("Assinatura curta", "Short signature", "Firma corta"),
    (">atalho<", ">shortcut<", ">atajo<"),

    # ---------- FEATURES ----------
    ('Tudo que você precisa,<br><span class="accent">nada que atrapalhe.</span>',
     'Everything you need,<br><span class="accent">nothing in the way.</span>',
     'Todo lo que necesitas,<br><span class="accent">nada que estorbe.</span>'),
    (">Menu de contexto nativo<", ">Native context menu<", ">Menú contextual nativo<"),
    ("Seus templates aparecem no clique direito do Chrome, em qualquer campo editável. Sem UI sobreposta — direto no menu que você já conhece.",
     "Your templates show up in Chrome's right-click menu, on any editable field. No overlaid UI — right in the menu you already know.",
     "Tus plantillas aparecen en el clic derecho de Chrome, en cualquier campo editable. Sin UI superpuesta — directamente en el menú que ya conoces."),
    (">Atalho de teclado<", ">Keyboard shortcut<", ">Atajo de teclado<"),
    ("Pressione a combinação em qualquer campo focado e um seletor flutuante aparece para busca rápida com ↑↓ e Enter.",
     "Press the combo on any focused field and a floating picker appears for quick search with ↑↓ and Enter.",
     "Pulsa la combinación en cualquier campo enfocado y aparece un selector flotante con búsqueda rápida con ↑↓ y Enter."),
    (">Escopo por site<", ">Per-site scope<", ">Alcance por sitio<"),
    ("Marque como global ou restrinja a um domínio. Templates do trabalho não invadem seu e-mail pessoal, e os snippets de código ficam onde você programa.",
     "Mark as global or restrict to a single domain. Work templates don't invade your personal inbox, and dev snippets stay where you write code.",
     "Marca como global o restríngela a un dominio. Plantillas de trabajo no invaden tu correo personal, y los fragmentos de código se quedan donde escribes código."),
    (">Side Panel completo<", ">Full Side Panel<", ">Panel lateral completo<"),
    ("Painel lateral para criar, editar, organizar, buscar e filtrar toda sua biblioteca — sem sair da aba que você está usando.",
     "Side panel to create, edit, organize, search and filter your entire library — without leaving the tab you're on.",
     "Panel lateral para crear, editar, organizar, buscar y filtrar toda tu biblioteca — sin salir de la pestaña actual."),
    (">Importar &amp; exportar<", ">Import &amp; export<", ">Importar y exportar<"),
    ("Leve sua biblioteca entre dispositivos com um arquivo JSON. Faça backup, filtre por escopo, restaure quando quiser.",
     "Move your library between devices as a JSON file. Back up, filter by scope, restore whenever.",
     "Mueve tu biblioteca entre dispositivos como un archivo JSON. Respalda, filtra por alcance, restaura cuando quieras."),
    (">Copiar para qualquer lugar<", ">Copy anywhere<", ">Copia donde sea<"),
    ("Um botão de copiar em cada template põe o conteúdo no clipboard — cole em apps desktop, outros navegadores ou onde precisar.",
     "A copy button on every template puts the content on your clipboard — paste it into desktop apps, other browsers, or wherever you need.",
     "Un botón de copiar en cada plantilla pone el contenido en el portapapeles — pégalo en apps de escritorio, otros navegadores o donde lo necesites."),
    (">Multi-idioma<", ">Multi-language<", ">Multi-idioma<"),
    ("Interface em Português, English e Español. Segue o sistema por padrão; pode ser trocada a qualquer momento.",
     "Interface in English, Português and Español. Follows the system by default; switchable any time.",
     "Interfaz en Español, Português y English. Sigue el sistema por defecto; cambiable en cualquier momento."),

    # ---------- HOW IT WORKS ----------
    ('Três jeitos<br>de chegar lá.',
     'Three ways<br>to get there.',
     'Tres caminos<br>para llegar.'),
    ("Cada caminho é otimizado para um momento diferente. Use o que faz sentido na hora.",
     "Each path is optimized for a different moment. Use whichever makes sense at the time.",
     "Cada camino está optimizado para un momento distinto. Usa el que tenga sentido en cada caso."),
    (">Clique direito<", ">Right-click<", ">Clic derecho<"),
    ("Em qualquer campo editável da web, abra o menu do botão direito. O item <b>InstaType</b> aparece com seus templates filtrados pelo site atual.",
     "On any editable field, open the right-click menu. The <b>InstaType</b> item appears with your templates filtered by the current site.",
     "En cualquier campo editable, abre el menú contextual. El elemento <b>InstaType</b> aparece con tus plantillas filtradas por el sitio actual."),
    ('Pressione <kbd>⌥</kbd> <kbd>⇧</kbd> <kbd>T</kbd> em qualquer campo focado. Um seletor flutuante aparece com busca, ↑↓ e Enter para escolher.',
     'Press <kbd>⌥</kbd> <kbd>⇧</kbd> <kbd>T</kbd> on any focused field. A floating picker appears with search, ↑↓ and Enter to choose.',
     'Pulsa <kbd>⌥</kbd> <kbd>⇧</kbd> <kbd>T</kbd> en cualquier campo enfocado. Aparece un selector flotante con búsqueda, ↑↓ y Enter para elegir.'),
    (">Side Panel<", ">Side Panel<", ">Panel lateral<"),
    ("Abra o painel lateral do Chrome para gerenciar tudo: criar, editar, organizar, buscar, filtrar, importar e exportar.",
     "Open Chrome's side panel to manage everything: create, edit, organize, search, filter, import and export.",
     "Abre el panel lateral de Chrome para gestionar todo: crear, editar, organizar, buscar, filtrar, importar y exportar."),

    # ---------- SCREENSHOTS ----------
    (">Capturas<", ">Screenshots<", ">Capturas<"),
    (">Veja em ação.<", ">See it in action.<", ">Velo en acción.<"),
    ("Pequenos detalhes pensados para o dia a dia: badges de escopo, busca instantânea, atalho persistente no rodapé.",
     "Small details made for daily use: scope badges, instant search, the shortcut always pinned at the bottom.",
     "Pequeños detalles pensados para el día a día: badges de alcance, búsqueda instantánea, atajo persistente en el pie."),
    ("Side Panel do InstaType", "InstaType Side Panel", "Panel lateral de InstaType"),
    ("Atalho de teclado", "Keyboard shortcut", "Atajo de teclado"),
    ("Menu de contexto", "Context menu", "Menú contextual"),
    ("Editor de snippets", "Snippet editor", "Editor de fragmentos"),
    ("Multi-idioma e portabilidade", "Multi-language and portability", "Multi-idioma y portabilidad"),

    # screenshot src files
    ("screenshots/01-sidepanel-pt.png", "screenshots/01-sidepanel.png", "screenshots/01-sidepanel-es.png"),
    ("screenshots/02-shortcut-pt.png", "screenshots/02-shortcut.png", "screenshots/02-shortcut-es.png"),
    ("screenshots/03-context-menu-pt.png", "screenshots/03-context-menu.png", "screenshots/03-context-menu-es.png"),
    ("screenshots/04-editor-pt.png", "screenshots/04-editor.png", "screenshots/04-editor-es.png"),
    ("screenshots/05-i18n-import-pt.png", "screenshots/05-i18n-import.png", "screenshots/05-i18n-import-es.png"),

    # ---------- PRIVACY STRIP ----------
    (">Privacidade<", ">Privacy<", ">Privacidad<"),
    ('Seus dados<br>ficam <span class="accent">com você.</span>',
     'Your data<br>stays <span class="accent">with you.</span>',
     'Tus datos<br>se quedan <span class="accent">contigo.</span>'),
    ('Sem contas, sem servidores, sem analytics, sem telemetria. Tudo é armazenado localmente no seu navegador via <code style="background:rgba(255,91,46,0.18);color:white;padding:2px 6px;border-radius:4px;font-family:var(--font-mono);font-size:0.85em">chrome.storage.local</code>. Nada sai do seu dispositivo.',
     'No accounts, no servers, no analytics, no telemetry. Everything is stored locally in your browser via <code style="background:rgba(255,91,46,0.18);color:white;padding:2px 6px;border-radius:4px;font-family:var(--font-mono);font-size:0.85em">chrome.storage.local</code>. Nothing leaves your device.',
     'Sin cuentas, sin servidores, sin analítica, sin telemetría. Todo se guarda localmente en tu navegador vía <code style="background:rgba(255,91,46,0.18);color:white;padding:2px 6px;border-radius:4px;font-family:var(--font-mono);font-size:0.85em">chrome.storage.local</code>. Nada sale de tu dispositivo.'),
    ("Ler a política completa →", "Read the full policy →", "Leer la política completa →"),
    ("<b>Zero coleta.</b> Não enviamos dados para lugar nenhum.",
     "<b>Zero collection.</b> We send no data anywhere.",
     "<b>Cero recolección.</b> No enviamos datos a ningún lado."),
    ("<b>Sem rastreadores.</b> Nenhum analytics ou identificador único.",
     "<b>No trackers.</b> No analytics or unique identifiers.",
     "<b>Sin rastreadores.</b> Sin analítica ni identificadores únicos."),
    ("<b>Aberto.</b> Exporte tudo em JSON quando quiser.",
     "<b>Open.</b> Export everything as JSON whenever.",
     "<b>Abierto.</b> Exporta todo como JSON cuando quieras."),
    ("<b>Mínimo.</b> Cada permissão usada tem propósito visível.",
     "<b>Minimal.</b> Every permission has a visible purpose.",
     "<b>Mínimo.</b> Cada permiso tiene un propósito visible."),

    # ---------- FAQ ----------
    (">FAQ<", ">FAQ<", ">FAQ<"),
    (">Perguntas comuns.<", ">Common questions.<", ">Preguntas comunes.<"),
    ("O InstaType funciona offline?",
     "Does InstaType work offline?",
     "¿InstaType funciona sin conexión?"),
    ("Sim. Toda a funcionalidade roda 100% localmente no seu navegador. Os únicos requisitos de internet são as fontes do Google Fonts no Side Panel (que são cacheadas pelo Chrome após a primeira carga).",
     "Yes. All functionality runs 100% locally in your browser. The only internet requirement is Google Fonts in the Side Panel (cached by Chrome after first load).",
     "Sí. Toda la funcionalidad se ejecuta 100% localmente en tu navegador. El único requisito de internet son las fuentes de Google Fonts en el panel lateral (Chrome las cachea tras la primera carga)."),
    ("Onde meus templates ficam salvos?",
     "Where are my templates stored?",
     "¿Dónde se guardan mis plantillas?"),
    ("No armazenamento local do Chrome, vinculado ao seu perfil de navegador no dispositivo onde a extensão está instalada. Se você usa o mesmo perfil Chrome em vários computadores com sincronização ativa, os dados <em>não</em> são sincronizados automaticamente — para isso use a função <b>Exportar &amp; Importar</b>.",
     "In Chrome's local storage, tied to your browser profile on the device where the extension is installed. If you use the same Chrome profile across machines with sync enabled, data is <em>not</em> automatically synced — use <b>Import &amp; Export</b> for that.",
     "En el almacenamiento local de Chrome, vinculado al perfil del navegador en el dispositivo donde está instalada la extensión. Si usas el mismo perfil Chrome en varios dispositivos con sincronización activa, los datos <em>no</em> se sincronizan automáticamente — para eso usa <b>Importar y exportar</b>."),
    ("Funciona em todos os sites?",
     "Does it work on every site?",
     "¿Funciona en todos los sitios?"),
    ("Sim, em qualquer página com campos editáveis: inputs, textareas e divs <code>contenteditable</code>. Funciona inclusive em editores rich-text modernos que gerenciam a própria entrada de texto.",
     "Yes, on any page with editable fields: inputs, textareas and <code>contenteditable</code> divs. It even works in modern rich-text editors that manage their own text input.",
     "Sí, en cualquier página con campos editables: inputs, textareas y divs <code>contenteditable</code>. Funciona incluso en editores rich-text modernos que gestionan su propia entrada de texto."),
    ("O atalho não está funcionando, e agora?",
     "The shortcut isn't working, what now?",
     "El atajo no funciona, ¿qué hago?"),
    ("Vá em <code>chrome://extensions/shortcuts</code>, encontre <b>InstaType</b> e atribua manualmente a combinação desejada. O Chrome às vezes não atribui o atalho sugerido automaticamente quando há conflito com outra extensão.",
     "Go to <code>chrome://extensions/shortcuts</code>, find <b>InstaType</b>, and assign the combo manually. Chrome sometimes skips the suggested shortcut when there's a conflict with another extension.",
     "Ve a <code>chrome://extensions/shortcuts</code>, busca <b>InstaType</b> y asigna manualmente la combinación. Chrome a veces no asigna el atajo sugerido cuando hay conflicto con otra extensión."),
    ("Os templates suportam variáveis?",
     "Do templates support variables?",
     "¿Las plantillas soportan variables?"),
    ("A versão 1.0 insere o texto exatamente como salvo. Variáveis dinâmicas (como <code>{{nome}}</code>, <code>{{data}}</code>, <code>{{clipboard}}</code>) estão planejadas para uma versão futura.",
     "Version 1.0 inserts text exactly as saved. Dynamic variables (like <code>{{name}}</code>, <code>{{date}}</code>, <code>{{clipboard}}</code>) are planned for a future release.",
     "La versión 1.0 inserta el texto tal cual está guardado. Variables dinámicas (como <code>{{nombre}}</code>, <code>{{fecha}}</code>, <code>{{clipboard}}</code>) están planeadas para una futura versión."),
    ("Custa alguma coisa?",
     "Does it cost anything?",
     "¿Tiene algún costo?"),
    ("Não. É gratuito, sem versão paga, sem anúncios. Software independente, sem modelo de monetização.",
     "No. Free, no paid tier, no ads. Independent software, no monetization model.",
     "No. Gratis, sin versión de pago, sin publicidad. Software independiente, sin modelo de monetización."),

    # ---------- FINAL CTA ----------
    (">Pronto?<", ">Ready?<", ">¿Listo?<"),
    ('Pare de digitar<br>a mesma coisa.',
     'Stop typing<br>the same thing.',
     'Deja de escribir<br>lo mismo.'),
    ("Instale em 10 segundos. Salve o primeiro template em 30. Use pelo resto do dia.",
     "Install in 10 seconds. Save your first template in 30. Use it for the rest of the day.",
     "Instala en 10 segundos. Guarda tu primera plantilla en 30. Úsala el resto del día."),

    # ---------- FOOTER ----------
    ("© 2026 InstaType — feito com café em Florianópolis",
     "© 2026 InstaType — made with coffee in Florianópolis",
     "© 2026 InstaType — hecho con café en Florianópolis"),
    ('<a href="politica-privacidade.html">Privacidade</a>',
     '<a href="politica-privacidade.html">Privacy</a>',
     '<a href="politica-privacidade.html">Privacidad</a>'),
    (">Contato<", ">Contact<", ">Contacto<"),
    (">Topo<", ">Top<", ">Arriba<"),
]


def main():
    with open(SRC, encoding="utf-8") as f:
        src = f.read()

    for lang_idx, lang_code, out_name in [
        (1, "en", "index-en.html"),
        (2, "es", "index-es.html"),
    ]:
        out = src
        for tup in T:
            pt = tup[0]
            tgt = tup[lang_idx]
            out = out.replace(pt, tgt)
        out_path = os.path.join(ROOT, out_name)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"  wrote {out_name}")


if __name__ == "__main__":
    main()
