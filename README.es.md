<div align="center">

<h3><code>valentino@galfredev:~$ whoami</code></h3>

<a href="https://galfredev.com"><img src="./hero.svg" width="880" alt="Valentino Galfré — desarrollador backend y de automatizaciones en Córdoba, Argentina. Stack: TypeScript, Node, Python, Next.js, Postgres, n8n, Flutter, llama.cpp. Foco: IA local, pipelines OCR a LLM, e integración con WhatsApp, CRM y APIs de terceros. Shippeado: cotejo, un conciliador de facturas on-device; Vector, un agente de ventas por WhatsApp en producción; y un pipeline de automatización de contenido con Canva." /></a>

</div>

Construyo automatizaciones que le sacan de encima a un negocio real una tarea manual que se repite — y mido si de verdad lo hicieron. Conciliación de facturas, captación de leads por WhatsApp, producción de contenido. Las tres corren en producción hoy; las tres están acá abajo.

<sub>🇬🇧 <a href="./README.md">Read in English</a> · <a href="https://galfredev.com">galfredev.com</a></sub>

<details>
<summary>Contenido de la tarjeta en texto</summary>

<!-- La tarjeta de arriba es un SVG: su texto no se indexa ni lo leen los
     lectores de pantalla. Esta es la copia accesible y buscable. -->

- **Rol** — Desarrollador backend y de automatizaciones
- **Ubicación** — Córdoba, Argentina · UTC−3 · trabajo en inglés y español
- **Stack** — TypeScript · Node · Python · Next.js · Postgres · n8n · Flutter · llama.cpp
- **Foco** — IA local, pipelines OCR→LLM, integración con WhatsApp / CRM / APIs de terceros
- **Disponible para** — Trabajo remoto de backend y automatización

</details>

---

## Tres automatizaciones en producción

Cada una reemplazó una tarea que alguien hacía a mano, todas las semanas, en un negocio argentino real.

### [cotejo](https://github.com/valentinogalfre/cotejo) — conciliación de facturas on-device

Concilia facturas de proveedores contra el extracto bancario sin mandar un solo documento a un tercero. Cada campo que extrae el modelo local se verifica contra el QR fiscal firmado criptográficamente que ARCA ya exige en toda factura — así la debilidad conocida de un modelo de 4B parámetros pasa a ser el paso de verificación del sistema en vez de su riesgo. Corre 100% offline.

`Python` · `llama.cpp` · `OCR` · `QVAC` — hecho para el Aleph Hackathon 2026

### [Vector](https://github.com/valentinogalfre/vector-galfredev-bot) — agente de ventas por WhatsApp, en producción

Atiende leads entrantes, los califica y los carga en el CRM, con fallback de proveedor para que la caída de una API no deje a un cliente sin respuesta. Viene manejando conversaciones reales, no tráfico de demo.

`Node` · `n8n` · `Twenty CRM` · `systemd`

### [Pipeline de Canva](https://github.com/valentinogalfre/automatizacion-notas-canva) — de texto a pieza terminada

Toma una nota, la redacta con un LLM, consigue las imágenes, autocompleta una plantilla de Canva y devuelve un PNG listo para publicar. Le sacó de encima a un negocio una tarea de diseño que hacía a mano.

`Node` · `Canva API` · `Claude` · `Unsplash`

<div align="center">

<h3><code>valentino@galfredev:~$ ./contributions</code></h3>

<img src="./contrib-heatmap.svg" width="880" alt="Gráfico de contribuciones de GitHub de valentinogalfre: 2.237 contribuciones en el último año, 617 en los últimos 60 días, en 121 días activos. Cerca del 88% están en repos privados de clientes. Se regenera todos los días desde la API de GitHub." />

</div>

La mayor parte de ese verde es trabajo privado de clientes, que es la razón del conteo público de estrellas. El gráfico y los números de abajo se regeneran cada mañana desde la API de GitHub con [un workflow de este repo](./.github/workflows/update-profile-art.yml) — el arte está commiteado acá, así que nada de esta página depende de que un servicio de terceros siga en pie.

## También acá

**[galfredev.com](https://github.com/valentinogalfre/galfredev-web)** — el sitio de mi estudio. Next.js, React, TypeScript, Tailwind, React Three Fiber, Supabase.
**[la_facu_app](https://github.com/valentinogalfre/la_facu_app)** — una app Flutter shippeada a Android y a Windows, con Riverpod, Isar y sincronización bidireccional con Google Calendar.

---

<div align="center">

[![Web](https://img.shields.io/badge/galfredev.com-0d1117?style=flat-square&logo=firefoxbrowser&logoColor=3fb950&labelColor=0d1117)](https://galfredev.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0d1117?style=flat-square&logo=linkedin&logoColor=58a6ff&labelColor=0d1117)](https://www.linkedin.com/in/valentinogalfre)
[![Email](https://img.shields.io/badge/galfredev@gmail.com-0d1117?style=flat-square&logo=gmail&logoColor=c9d1d9&labelColor=0d1117)](mailto:galfredev@gmail.com)

</div>
