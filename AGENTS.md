# Mashi Memory

## Project
Mashi — asistente multilingüe Kichwa-Español-Inglés para MAPPED (ecoturismo + comercio justo, Amazonía peruana). Competencia UTP.

## Critical Context
- Python 3.14.6, Streamlit (puerto 8501), FastAPI ai-service (puerto 8000)
- **Gemini API preconfigurada**: `.streamlit/secrets.toml` + env var `GEMINI_API_KEY` persistente
- Orden de resolución de API key: session > env var > secrets.toml
- **mock_response() = fallback offline**: si Gemini falla (sin internet), responde con datos locales y aviso "🌐 Respondo offline"
- Mashi NO se llama "mashi" en ES/EN — usa "amigo" (ES) / "friend" (EN). Solo Kichwa mantiene "mashi"
- Kichwa: saludo "Allianllachu"
- **Tema**: fondo `#021B15`, cards `#0A2B1F`, accent `#10b981` (emerald), glass-morphism
- Diseño responsive con bottom nav
- Tres modos: Ecoturista, Emprendedor Local, Inversionista/Empresa + Cámara IA
- **app.py** monolítico (~2300 líneas)
- **database.py**: SQLite3 con 9 comunidades, 27 productos, 23 reseñas
- **test_app.py**: 14 tests unitarios (todos pasan)
- **Google Maps API key**: configurada via secrets.toml

## Timeline

### Jul 2 — Inicio
- MVP con mock_response() offline, 3 emprendedores, CSS básico
- Mashi_server.py + ai-service/ creados

### Jul 4 — Refactor
- Intento de modularizar mashi/ (parcial)
- expandido a 9 emprendedores, KICHWA~203 palabras
- render_inversionista() reescrita: dark table, KPIs, Plotly, ROI calculator, Maps

### Jul 5 (mañana) — Modo inversionista + Gemini default
- mock_response() expandida: 6 topics inversionista (ROI, invertir, sectores, logística, comparar, mercado)
- API key preconfigurada: secrets.toml + env var
- Gemini es default

### Jul 5 (tarde) — Dashboard real + IA
- Eliminado random.Random() de proyecciones (fórmula determinística + estacionalidad)
- Botón "Análisis Mashi con IA": filtra por sector del inversionista, llama Gemini
- Portafolio de inversión: multiselect + KPIs combinados
- Descargar Reporte HTML con empresa, KPIs, top comunidades
- Badge de fuente: "Datos de comunidades registradas en MAPPED"
- SQLite (database.py): get_full_dataset() prueba DB → fallback hardcode
- test_app.py: 14 tests (clean_mashi, strip_emojis, _L, get_full_dataset)
- Limpieza: eliminado OllamaSetup.exe (1.36 GB)
- Driver Intel UHD Graphics actualizado (solucionó congelamientos Brave/Canva)

### Jul 9 — Offline-first
- **mock_response() reutilizado como fallback offline**: cuando Gemini falla (sin internet, error de API), `get_mashi_response()` ahora llama a `mock_response()` en vez de mostrar un mensaje genérico
- Aviso visible "🌐 Respondo offline — Sin internet uso mis datos locales"
- Sidebar actualizado: "🌐 Modo offline-first" en vez de "Modo demostración"
- HTML móvil modificado para usar API real de Gemini via servidor, con fallback offline cuando el server no responde

### Jul 10 — Competitividad
- **Qwen3-TTS restaurado**: reemplazó XTTS espacio muerto con `qwen-qwen3-tts.hf.space`, usa `/generate_voice_design` con voice description. gTTS como fallback gratuito
- **Offline sync queue**: indicador Online/Offline en tienda + cola de acciones offline
- **QR por producto**: `_generate_qr_base64()` con toggle en cards de tienda
- **Guía offline**: botón "Descargar guía offline" genera .txt con comunidades, productos, precios
- **Market price intelligence**: `_suggest_price_for_product()` devuelve 9 valores (precios, tendencia, confianza, insight); mostrado en chat y emprendedor
- **WhatsApp integration**: wa.me links en store, entrepreneur, product detail; "Comprar por WhatsApp" abre mensaje al artesano
- **Phone contacts**: `PHONE_CONTACTS` dict con 17 números demo +51
- **System prompts**: todos los modos mencionan WhatsApp, tendencias de mercado, ventas directas
- **Impact dashboard**: `_impact_metrics()` en render_ecotourist() muestra banner con 17 comunidades, 27 productos, S/ 245k, 51 familias, 33 reseñas
- **Trend badges**: 🔥 Alta demanda / 📈 Popular / 💚 Precio justo según reseñas vs precio
- **Product detail view**: `_render_product_detail()` con imagen, historia, materiales, comparación de precios, reseñas, WhatsApp

### Jul 15 — Diferenciación única
- **Impact calculator per product**: familias apoyadas, árboles protegidos, impacto económico en detail view (`_render_product_detail()`)
- **Sounds of Amazon**: botón 🔊 Escuchar historia en detail view — usa `SpeechSynthesis` del navegador (gratis, sin tokens); texto sanitizado (sin quotes/html/markdown)
- **Enhanced trip planner**: presupuesto estimado (transporte + comida + compras), productos recomendados por comunidad, descarga de itinerario HTML completo

## Files
| File | Purpose |
|------|---------|
| `app.py` | Streamlit app monolítica (~2300 lines) |
| `database.py` | SQLite3: communities, products, reviews |
| `test_app.py` | 14 unit tests |
| `mashi_server.py` | HTTP proxy (legacy) |
| `ai-service/` | FastAPI backend (legacy) |
| `.streamlit/secrets.toml` | Gemini API key |
| `backups/` | Auto-backups de app.py |
| `AGENTS.md` | Memoria del proyecto |

## Key Design Decisions
- Monolítico > modular (app.py único, menos riesgo de corrupción)
- **Offline-first**: `mock_response()` es el salvavidas cuando no hay internet — útil para demos en Loreto donde el internet falla. Aviso "🌐 Respondo offline" visible en cada respuesta offline
- Proyecciones sin random — fórmula basada en reseñas, productos, años, estacionalidad
- DB first con fallback a hardcode — migración segura

## Pending / Next Steps
1. **Plan de competencia** — guión 12 min (ES→EN→QW), demo script, Q&A
2. **QR para público** — ngrok + QR code para el stand
3. **Limpiar duplicados** entre ai-service/, mashi_server.py, app.py
4. **Cámara IA** — mejorar identificación de productos por foto (Gemini Vision)
5. **Más comunidades** — ampliar dataset en DB (10+ comunidades reales)

## Recovery Notes
- app.py se corrompió una vez (166KB, 1 línea sin newlines) tras `Get-Content | Set-Content -NoNewLine`
- Restaurado como monolítico con #021B15 · Emerald · #10b981
- **Protección activa**: auto-backup en startup a `backups/app-auto-*.py`
- **Backup manual**: `.\backup_mashi.ps1`
- **Safe edit**: siempre `Copy-Item` para backups. NUNCA `Get-Content | Set-Content -NoNewLine`
- **Safe edit**: usar Python con `encoding='utf-8'`, nunca PowerShell Get-Content
