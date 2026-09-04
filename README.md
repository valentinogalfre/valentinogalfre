<div align="center">

<h3><code>valentino@galfredev:~$ whoami</code></h3>

<a href="https://galfredev.com"><img src="./hero.svg" width="880" alt="Valentino Galfré — backend and automation developer in Córdoba, Argentina. Stack: TypeScript, Node, Python, Next.js, Postgres, n8n, Flutter, llama.cpp. Focus: local-first AI, OCR-to-LLM pipelines, and WhatsApp / CRM / third-party API integration. Shipped: cotejo, an on-device invoice reconciler; Vector, a WhatsApp sales agent running in production; and a Canva content-automation pipeline." /></a>

</div>

I build automations that remove a recurring manual job from a real business — and I measure whether they actually did. Invoice reconciliation, WhatsApp lead intake, content production. All three run in production today; all three are below.

<sub>🇦🇷 <b>¿Hablás español?</b> · <a href="./README.es.md">Leer en español</a> · <a href="https://galfredev.com">galfredev.com</a></sub>

<details>
<summary>Card contents as text</summary>

<!-- The card above is an SVG, so its text is neither indexed nor read aloud.
     This mirror is the accessible and searchable copy. -->

- **Role** — Backend & automation developer
- **Based** — Córdoba, Argentina · UTC−3 · works in English and Spanish
- **Stack** — TypeScript · Node · Python · Next.js · Postgres · n8n · Flutter · llama.cpp
- **Focus** — Local-first AI, OCR→LLM pipelines, WhatsApp / CRM / third-party API integration
- **Open to** — Remote backend and automation work

</details>

---

## Three shipped automations

Each one replaced a job somebody was doing by hand, every week, in a real Argentine business.

### [cotejo](https://github.com/valentinogalfre/cotejo) — on-device invoice reconciliation

Matches supplier invoices against a bank statement without sending a single document to a third party. Every field a small local model extracts is checked against the cryptographically signed fiscal QR code the government already mandates on every invoice — so the known weakness of a 4B-parameter model becomes the system's verification step rather than its risk. Runs fully offline.

`Python` · `llama.cpp` · `OCR` · `QVAC` — built for the Aleph Hackathon 2026

### [Vector](https://github.com/valentinogalfre/vector-galfredev-bot) — WhatsApp sales agent, in production

Answers inbound leads, qualifies them and writes them into the CRM, with provider fallback so a single API outage does not drop a customer. It has been handling real conversations, not demo traffic.

`Node` · `n8n` · `Twenty CRM` · `systemd`

### [Canva content pipeline](https://github.com/valentinogalfre/automatizacion-notas-canva) — text to finished graphic

Takes a note, drafts it with an LLM, sources imagery, autofills a Canva template and returns a publish-ready PNG. It removed a recurring design task from a business that was doing it manually.

`Node` · `Canva API` · `Claude` · `Unsplash`

<div align="center">

<h3><code>valentino@galfredev:~$ ./contributions</code></h3>

<img src="./contrib-heatmap.svg" width="880" alt="GitHub contribution graph for valentinogalfre: 2,237 contributions in the last year, 617 in the last 60 days, across 121 active days. Roughly 88% of them are in private client repositories. Refreshed daily from the GitHub API." />

</div>

Most of that green is private client work, which is why the public star count is what it is. The graph and the numbers under it are regenerated every morning from the GitHub API by [a workflow in this repository](./.github/workflows/update-profile-art.yml) — the artwork is committed here, so nothing on this page depends on a third-party service staying up.

## Also here

**[galfredev.com](https://github.com/valentinogalfre/galfredev-web)** — my studio site. Next.js, React, TypeScript, Tailwind, React Three Fiber, Supabase.
**[la_facu_app](https://github.com/valentinogalfre/la_facu_app)** — a Flutter app shipped to both Android and Windows, with Riverpod, Isar and two-way Google Calendar sync.

---

<div align="center">

[![Website](https://img.shields.io/badge/galfredev.com-0d1117?style=flat-square&logo=firefoxbrowser&logoColor=3fb950&labelColor=0d1117)](https://galfredev.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0d1117?style=flat-square&logo=linkedin&logoColor=58a6ff&labelColor=0d1117)](https://www.linkedin.com/in/valentinogalfre)
[![Email](https://img.shields.io/badge/galfredev@gmail.com-0d1117?style=flat-square&logo=gmail&logoColor=c9d1d9&labelColor=0d1117)](mailto:galfredev@gmail.com)

</div>
