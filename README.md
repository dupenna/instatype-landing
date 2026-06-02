# InstaType — landing

Site público da extensão [InstaType](https://chromewebstore.google.com/) (Chrome Web Store).

Publicado em **https://instatype.s3web.com.br/** via GitHub Pages.

O código-fonte da extensão vive em outro repositório (privado). Este repo contém apenas a landing, a política de privacidade, screenshots e artefatos da Chrome Web Store.

## Deploy

Push para `main` → workflow `pages.yml` → GitHub Pages.

DNS: `CNAME instatype.s3web.com.br` → `dupenna.github.io`.

## Estrutura

- `index.html`, `index-en.html`, `index-es.html` — landing nos três idiomas
- `politica-privacidade.html` — política de privacidade (PT)
- `screenshots/` — 5 narrativas × 3 idiomas (PNG + HTML fonte)
- `promo/` — banners da Chrome Web Store (small + marquee)
- `store-listing.md` — texto pronto da loja (rascunho de trabalho)
- `translate-landing.py`, `translate-shots.py` — geram as variantes EN/ES a partir das versões PT
