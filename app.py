"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    MAPPED — Mashi AI (Tech-Jungle Edition)                   ║
║                    #021B15 · Cyan · Mint Green                              ║
║                    Loreto, Perú                                             ║
╚══════════════════════════════════════════════════════════════════════════════╝

pip install streamlit google-generativeai pandas
python -m streamlit run app.py
"""

import os, json, random, time, requests, re, math, base64
import pandas as pd
import streamlit as st

# ─── Auto-backup on startup ──────────────────────────────────────────
try:
    _src = os.path.abspath(__file__)
    _bak_dir = os.path.join(os.path.dirname(_src), "backups")
    os.makedirs(_bak_dir, exist_ok=True)
    _ts = time.strftime("%Y%m%d-%H%M%S")
    _bak = os.path.join(_bak_dir, f"app-auto-{_ts}.py")
    with open(_src, "r", encoding="utf-8") as _f:
        _content = _f.read()
    # Sanity check: more than 10 lines = valid Python file
    if _content.count("\n") > 10:
        with open(_bak, "w", encoding="utf-8") as _f:
            _f.write(_content)
except Exception:
    pass  # silent — never crash on backup

# ─── Logo Mashi ──────────────────────────────────────────────────────────
_MASHI_B64_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mashi_logo_b64.txt")
try:
    with open(_MASHI_B64_PATH, "r") as _f:
        MASHI_LOGO_B64 = _f.read().strip()
except FileNotFoundError:
    MASHI_LOGO_B64 = "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA0MCA0MCI+PHJlY3Qgd2lkdGg9IjQwIiBoZWlnaHQ9IjQwIiByeD0iMjAiIGZpbGw9IiMxMGI5ODEiLz48dGV4dCB4PSIyMCIgeT0iMjgiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZpbGw9IiMwMjFCMTUiIGZvbnQtc2l6ZT0iMjAiIGZvbnQtd2VpZ2h0PSJib2xkIiBmb250LWZhbWlseT0iU2Vnb2UgVUkiPk08L3RleHQ+PC9zdmc+"

st.set_page_config(page_title="MAPPED — Mashi AI", page_icon="🦥",
                   layout="centered", initial_sidebar_state="expanded")

# ========================================================================
# SISTEMA DE IDIOMAS
# ========================================================================
TR = {
    "es": {
        "explore": "Explorar", "routes": "Rutas", "community": "Comunidad", "profile": "Perfil",
        "role_eco": "Ecoturista", "role_emp": "Emprendedor Local", "role_inv": "Inversionista / Empresa",
        "lang_es": "Español", "lang_en": "English", "lang_qw": "Kichwa",
        "language": "Idioma", "settings": "Configuración",
        "onboard_title": "Únete a MAPPED",
        "onboard_sub": "Descubre la Amazonía con Mashi, tu guía perezoso",
        "name_ph": "Nombre completo", "email_ph": "Correo electrónico",
        "create_btn": "Crear cuenta",
        "upload_label": "Sube una foto de tu producto",
        "chat_ph": "Escribe tu mensaje a Mashi...",
        "price_hint": "Sugerencia de precio","demand":"Demanda","demand_high":"Alta","demand_medium":"Media","demand_low":"Baja",
        "mashi_says":"dice Mashi","lets_see":"Veamos qué tenemos en la selva","everything_ok":"Todo bien por la selva",
        "materials":"Materiales","organic":"Orgánico","handmade":"Artesanal","price_suggestion":"Precio sugerido para turistas",
    },
    "en": {
        "explore": "Explore", "routes": "Routes", "community": "Community", "profile": "Profile",
        "role_eco": "Ecotourist", "role_emp": "Local Entrepreneur", "role_inv": "Investor / Company",
        "lang_es": "Spanish", "lang_en": "English", "lang_qw": "Kichwa",
        "language": "Language", "settings": "Settings",
        "onboard_title": "Join MAPPED",
        "onboard_sub": "Discover the Amazon with Mashi, your sloth guide",
        "name_ph": "Full name", "email_ph": "Email address",
        "create_btn": "Create account",
        "upload_label": "Upload a product photo",
        "chat_ph": "Type your message to Mashi...",
        "price_hint": "Price suggestion","demand":"Demand","demand_high":"High","demand_medium":"Medium","demand_low":"Low",
        "mashi_says":"says Mashi","lets_see":"Let's see what we have in the jungle","everything_ok":"All good in the jungle",
        "materials":"Materials","organic":"Organic","handmade":"Handcrafted","price_suggestion":"Suggested tourist price",
    },
    "qw": {
        "explore": "Maskay", "routes": "Ñankuna", "community": "Llaktakuna", "profile": "Kikin",
        "role_eco": "Purij",         "role_emp": "Ruraq", "role_inv": "Qolqe / Empresa",
        "lang_es": "Español", "lang_en": "English", "lang_qw": "Kichwa",
        "language": "Shimi",         "settings": "Allichina",
        "onboard_title": "MAPPEDmanalla",
        "onboard_sub": "Allianllachu, mashi. Amazóniata maskanki",
        "name_ph": "Sutiyki", "email_ph": "Correo electrónico",
        "create_btn": "Cuentata ruray",
        "upload_label": "Rurata apay",
        "chat_ph": "Mashiman kilkay...",
        "price_hint": "Masna alli","demand":"Munana","demand_high":"Achka","demand_medium":"Chawpi","demand_low":"Aslla",
        "mashi_says":"nishka","lets_see":"Sachamanta rikushun","everything_ok":"Sachapi allilla",
        "materials":"Rurana","organic":"Pachamamamanta",        "handmade":"Maki rurashka","price_suggestion":"Turiskunapa masna alli",
    },
}
def T(key): return TR.get(st.session_state.get("lang","es"), TR["es"]).get(key, key)

KICHWA = {
    "saludo":"Allianllachu","gracias":"Añay","despedida":"Tupananchikkama",
    "bueno":"Alli","hermoso":"Sumak","amigo":"mashi",
    "como_esta":"Imashina kanki","bien":"Allimi cani","lugar":"Maypita",
    "donde": "Maypita","precio":"Masnapi","cuanto":"Masna",
    "agua":"Yaku","selva":"Sacha",    "casa":"Wasi",
    "comida":"Mikuna","compra":"Randina","venta":"Rantichina",
    "familia":"Ayllu","maiz":"Sara","dulce":"Mishki",
    "fuerte":"Sinchi","tierra":"Allpa","dia":"Puncha","noche":"Tuta",
    "hoy":"Kuna puncha","mañana":"Kaya","flor":"Sisa",
    "artesano":"Ruraq","trabajo":"Llankay","alegria":"Kushikuy",
    "amor":"Munay","aprender":"Yachana","vender":"Rantichina",
    "manana_temprano":"Kaya tutamanta","gracias_mashi":"Añay mashi",
    "bienvenido":"Alli shamushka","si":"Ari","no":"Mana",
    "sol":"Inti","luna":"Killa","estrella":"Kuyllur","montana":"Urku",
    "rio":"Mayu","rio_grande":"Mayu hatun","arbol":"Sacha sacha",
    "animal":"Uywa","ave":"Pishqu","pez":"Challwa",
    "medicina":"Jampi","medico":"Jampik","sabio":"Yachaq",
    "nino":"Wawa","hombre":"Kari","mujer":"Warmi",
    "caminar":"Puriy","correr":"Kallpanakuy","cantar":"Takiy","bailar":"Tusuy",
    "escuchar":"Uyariy","mirar":"Rikuy","hablar":"Rimay","pensar":"Yuyay",
    "saber":"Yachay","querer":"Munay","dar":"Kuy","recibir":"Chaskiy",
    "alma":"Sonqo","sueno":"Musquy","recuerdo":"Yuyarina",
    "agradecer":"Anaychay","compartir":"Rakiy","unir":"Tinkuy",
    "camino":"Nan","puerta":"Punku",
    "mercado":"Jatu","trueque":"Randikuy","tejer":"Away",
    "barro":"Turu",    "ceramica":"Manka","pintura":"Llimpi",
    "colores":"Llimpikuna","rojo":"Puka","azul":"Ankas","verde":"Q'umir","negro":"Yana","blanco":"Yuraq",
    "alegre":"Kushilla","triste":"Llaki","valiente":"Kalpayuq","humilde":"Kumuykuq",
    "respeto":"Yupaychay","sabiduria":"Yachay",
    "ayudar":"Yanapay","proteger":"Wakaychay","cuidar":"Wakaychay",
    "semilla":"Muru","cosecha":"Pallay","plantar":"Tarpuy",
    "miel":"Mishki ruru","chocolate":"Chukulati","fruta":"Ruru",
    "turista":"Purij","viajero":"Purij",
    "amistad":"Mashi kay","paz":"Sumak kawsay",
    "emprendedor":"Ruraq","empresa":"Hatun llankay","inversionista":"Qolqe ruraq",
    "economia":"Qolqe kawsay","comercio":"Randikuy","negocio":"Llankay",
    "ganancia":"Lluksiy","ahorrar":"Wakaychay","invertir":"Qolqe churay",
    "tasa":"Yupana","interes":"Mirana","credito":"Manu",
    "proyecto":"Llankay munay","plan":"Yuyay",
    "calidad":"Sumak kay","precio_justo":"Alli masna","oferta":"Kuy",
    "selva_tropical":"Sacha hatun","laguna":"Qocha","cascada":"Pakcha",
    "valle":"Wayqu","playa":"Playa",
    "bosque":"Sacha","sendero":"Nan purina","rio_arriba":"Mayu hanan","rio_abajo":"Mayu uray",
    "comunidad":"Llakta","pueblo":"Llakta","ciudad":"Hatun llakta",
    "vecino":"Llakta mashi",
    "artesania":"Rura","arte":"Sumak rura","cultura":"Kawsay",
    "idioma":"Shimi","kichwa":"Runashimi","espanol":"Kastellanu",
    "ingles":"Ingles shimi","traducir":"Tikray","significa":"Niyta munay",
    "producto":"Rura","servicio":"Yanapay","turismo":"Puriy",
    "tejedor":"Awaq","alfarero":"Turu ruraq",
    "madera":"Qiru","hoja":"Rapi","tallo":"K'allma",
    "amargo":"Qatu","picante":"Haya","salado":"Kachi","fresco":"Chiriyachik",
    "clima_templado":"Chawpi rupay","calor":"Rupay","frio":"Chiri","lluvia":"Tamiya","viento":"Wayra",
    "nube":"Phuyu","relampago":"Llipipiya","trueno":"Q'apaq",
    "lunes":"Awak puncha","martes":"Pichay puncha","miercoles":"Q'uychi puncha","jueves":"Tarpuy puncha","viernes":"Ch'uyay puncha","sabado":"Samay puncha","domingo":"Inti puncha",
    "enero":"Iñiru","febrero":"Piwriru","marzo":"Marsu","abril":"Awril","mayo":"Mayu","junio":"Hunyu","julio":"Hulyu","agosto":"Awustu","setiembre":"Sitimri","octubre":"Uktuwri","noviembre":"Nuwimri","diciembre":"Disimri",
    "numero_1":"Shuk","numero_2":"Ishkay","numero_3":"Kimsa","numero_4":"Chusku","numero_5":"Pichka",
    "numero_6":"Sukta","numero_7":"Kanchis","numero_8":"Pusak","numero_9":"Iskun","numero_10":"Chunka",
    "primero":"Nawpaq","segundo":"Ishkay kaq","tercero":"Kimsa kaq","ultimo":"Qhipa",
    "mucho":"Ashka","poco":"Aslla","todo":"Llapan","nada":"Mana ima","siempre":"Wiñay","nunca":"Mana haykaq",
    "arriba":"Hanan","abajo":"Uray","adentro":"Ukhu","afuera":"Waqta","cerca":"Kaylla","lejos":"Karuta",
}

# ========================================================================
# MOCK DATA — 15 emprendedores
# Llaves demo para exposición local. En producción usar .streamlit/secrets.toml
# ========================================================================
GEMINI_KEYS = [
    "",  # Configurar via secrets.toml o variable de entorno GEMINI_API_KEY
    "",
    ""
]

ENTREPRENEURS = [
    {"id":1,"name":"Asociación de Artesanas Shiringa de San Martín de Tipishca",
     "location":"San Martín de Tipishca, Río Amazonas","zone":"Amazonía Norte",
     "address":"Calle Principal s/n, San Martín de Tipishca, Loreto",
     "lat":-3.7442,"lng":-73.2945,
     "years_selling":8,"sector":"Textiles y Artesanía",
       "sector_keywords":["textil","shiringa","tela","ecológico","biodegradable","impermeable","textile","fabric","cloth","eco friendly","waterproof","natural rubber","latex","organic","turismo","regalo","artesanía"],
     "description":"15 mujeres artesanas que crean productos impermeables con látex de shiringa.",
     "products":[
         {"name":"Toallitas biodegradables de shiringa (paq. x10)","price":25.00,"currency":"S/",
          "description":"Impermeables, ecológicas. Ideales para el viajero consciente."},
         {"name":"Bolsa impermeable artesanal de shiringa","price":45.00,"currency":"S/",
          "description":"Multiuso, pintada a mano con tintes naturales."},
         {"name":"Poncho tradicional de shiringa","price":120.00,"currency":"S/",
          "description":"Ligero e impermeable. Diseño único pintado a mano."}],
     "reviews":[
         {"user":"María G.","stars":5,"text":"Hermoso trabajo. La calidad es increíble."},
         {"user":"Carlos R.","stars":4,"text":"Producto de primera. Valió la pena."},
         {"user":"Ana L.","stars":5,"text":"Apoyar a estas artesanas fue lo mejor de mi viaje."}],
     "contact":"artesanas.shiringa@mapet.pe",
     "logistics_notes":"Acceso fluvial directo. 2h en bote desde Iquitos.",
     "materials":"Látex de shiringa, tintes naturales"},
    {"id":2,"name":"Comunidad de Jabones Artesanales de Belén",
     "location":"Belén, Iquitos","zone":"Urbano-Ribereña",
     "address":"Jr. Marañón 452, Belén, Iquitos, Loreto",
     "lat":-3.7661,"lng":-73.2484,
     "years_selling":5,"sector":"Cosméticos Naturales",
       "sector_keywords":["jabón","cosmético","piel","copaiba","cera","natural","bálsamo","soap","cosmetic","skin","oil","balm","wax","honey","organic","body","care","cream","shampoo","turismo","regalo","spa"],
     "description":"Familia que elabora jabones con aceites de copaiba, andiroba y ceras naturales.",
     "products":[
         {"name":"Jabón artesanal de copaiba y miel","price":12.00,"currency":"S/",
          "description":"Hidratante, antiséptico natural. 100g."},
         {"name":"Set de 3 jabones exóticos","price":30.00,"currency":"S/",
          "description":"Copaiba, andiroba, sachamangua. En tela de algodón nativo."},
         {"name":"Bálsamo labial de cera de abeja","price":8.00,"currency":"S/",
          "description":"Nutritivo, sin químicos. Envase de vidrio reutilizable."}],
     "reviews":[
         {"user":"Pedro M.","stars":5,"text":"Los jabones huelen delicioso y no resecan."},
         {"user":"Lucía F.","stars":5,"text":"El bálsamo labial es mi favorito."}],
     "contact":"jabones.belen@mapet.pe",
     "logistics_notes":"Ubicado en Iquitos. Fácil acceso.",
     "materials":"Aceite de copaiba, andiroba, cera de abeja"},
    {"id":3,"name":"Cooperativa Esperanza del Bosque",
     "location":"Calle Yurimaguas 186, Iquitos","zone":"Urbano",
     "address":"Calle Yurimaguas 186, Iquitos, Loreto",
     "lat":-3.7495,"lng":-73.2440,
     "years_selling":14,"sector":"Textiles y Artesanía",
       "sector_keywords":["chambira","tagua","joyería","cesto","madera","tallado","mujer","maijuna","kichwa","iquitu","cooperativa","fibra","artesanía","sostenible","turismo","regalo","ecológico"],
     "description":"Más de 30 mujeres artesanas Maijuna, Kichwa e Iquitu crean cestos de chambira, joyería de tagua y tallados en madera. Ganadoras del concurso Selva Ganadora.",
     "products":[
         {"name":"Cesto tejido de chambira (mediano)","price":48.00,"currency":"S/",
          "description":"Fibra de chambira teñida con tintes naturales. 25cm."},
         {"name":"Collar de tagua y semillas nativas","price":32.00,"currency":"S/",
          "description":"Tagua (nuez de marfil) tallada a mano. Diseño amazónico."},
         {"name":"Plato tallado en madera con motivos de la selva","price":55.00,"currency":"S/",
          "description":"Madera nativa tallada a mano. 20cm de diámetro."}],
     "reviews":[
         {"user":"Valeria M.","stars":5,"text":"El collar de tagua es hermoso. Calidad excepcional."},
         {"user":"José L.","stars":5,"text":"Apoyar a estas mujeres artesanas fue lo mejor."},
         {"user":"Carolina A.","stars":4,"text":"Compré el cesto, está bellamente tejido."}],
     "contact":"esperanza.bosque@mapet.pe",
     "logistics_notes":"Tienda en Iquitos centro. Fácil acceso peatonal.",
     "materials":"Fibra de chambira, tagua, madera nativa, tintes naturales"},
    {"id":4,"name":"Tejedoras de Chambira de San José de Lupuna",
     "location":"San José de Lupuna, Río Nanay","zone":"Amazonía Norte",
     "address":"Carretera Iquitos-Nanay km 14, San José de Lupuna, Loreto",
     "lat":-3.7140,"lng":-73.3256,
     "years_selling":15,"sector":"Artesanía Textil",
       "sector_keywords":["textil","chambira","tejido","bolso","hamaca","fibra","palma","woven","bag","hammock","fiber","palm","artesanía","turismo","regalo","decoración"],
     "description":"Asociación de mujeres tejedoras que transforman la fibra de chambira en productos únicos.",
     "products":[
         {"name":"Bolso tejido de chambira (mediano)","price":55.00,"currency":"S/",
          "description":"Tejido tradicional. Fibra de palma nativa. Tintes naturales."},
         {"name":"Hamaca artesanal de chambira","price":180.00,"currency":"S/",
          "description":"Resistente y cómoda. Tejida a mano. 2m de largo."},
         {"name":"Pulsera de chambira con diseños étnicos","price":15.00,"currency":"S/",
          "description":"Ajustable. Hecha con fibra natural teñida."}],
     "reviews":[
         {"user":"Rosa T.","stars":5,"text":"El bolso es hermoso, calidad excepcional."},
         {"user":"Miguel Á.","stars":4,"text":"La hamaca es muy resistente y bonita."}],
     "contact":"tejedoras.lupuna@mapet.pe",
     "logistics_notes":"Acceso por carretera desde Iquitos. 45 min.",
     "materials":"Fibra de chambira, tintes naturales"},
    {"id":5,"name":"Taller de Tallado en Madera de Tamshiyacu",
     "location":"Tamshiyacu, Río Amazonas","zone":"Amazonía Norte",
     "address":"Km 42 Carretera Iquitos-Tamshiyacu, Tamshiyacu, Loreto",
     "lat":-3.7857,"lng":-73.3206,
     "years_selling":20,"sector":"Artesanía en Madera",
      "sector_keywords":["madera","tallado","escultura","cetro","animal","artesanía","wood","carving","sculpture","handmade","tourist","turismo","decoración","regalo","arte"],
     "description":"Familia de talladores que esculpen figuras de la selva en cedro y caoba.",
     "products":[
         {"name":"Escultura de delfín rosado (15cm)","price":40.00,"currency":"S/",
          "description":"Tallada a mano en cedro. Detalle realista."},
         {"name":"Cetro ceremonial con cabeza de jaguar","price":95.00,"currency":"S/",
          "description":"Madera de caoba. Inspirado en tradiciones Amazónicas."},
         {"name":"Set de 3 animales de la selva","price":60.00,"currency":"S/",
          "description":"Delfín, perezoso y guacamayo. Cedro. 10-15cm c/u."}],
     "reviews":[
         {"user":"Andrés M.","stars":5,"text":"El delfín es una preciosura. Gran detalle."},
         {"user":"Karen P.","stars":5,"text":"Compré el set de animales, todos hermosos."},
         {"user":"Luis D.","stars":4,"text":"Buena calidad, precio justo."}],
     "contact":"tallado.tamshiyacu@mapet.pe",
     "logistics_notes":"Acceso fluvial 1h desde Iquitos.",
     "materials":"Cedro, caoba, barniz natural"},
    {"id":6,"name":"Productores de Miel de Abeja de Zungaro Cocha",
     "location":"Zungaro Cocha, Loreto","zone":"Amazonía Norte",
     "address":"Carretera Iquitos-Nauta km 8, Zungaro Cocha, Loreto",
     "lat":-3.7044,"lng":-73.3137,
     "years_selling":7,"sector":"Alimentos Naturales",
      "sector_keywords":["miel","abeja","alimento","natural","orgánico","miel de abeja","honey","bee","organic","natural food","salud","turismo","medicina"],
     "description":"Comunidad apicultora que produce miel pura y derivados de abejas nativas.",
     "products":[
         {"name":"Miel pura de abeja nativa (500ml)","price":28.00,"currency":"S/",
          "description":"Sin procesar. Cosechada artesanalmente."},
         {"name":"Propóleos en spray 30ml","price":22.00,"currency":"S/",
          "description":"Antiséptico natural. Fortalece el sistema inmune."},
         {"name":"Cera de abeja en bloque (200g)","price":18.00,"currency":"S/",
          "description":"Pura. Ideal para velas y bálsamos."}],
     "reviews":[
         {"user":"Sofía R.","stars":5,"text":"La miel más pura que he probado."},
         {"user":"Diego C.","stars":4,"text":"El propóleos me curó la garganta."}],
     "contact":"miel.zungaro@mapet.pe",
     "logistics_notes":"Acceso por carretera. 30 min de Iquitos.",
     "materials":"Miel de abeja nativa, propóleos, cera"},
    {"id":7,"name":"Asociación de Guías Turísticos de Pacaya Samiria",
     "location":"Pacaya Samiria, Río Marañón","zone":"Reserva Nacional",
     "address":"Punto de encuentro: Plaza de Armas de Nauta, Loreto",
     "lat":-4.5147,"lng":-73.5753,
     "years_selling":10,"sector":"Turismo Comunitario",
      "sector_keywords":["turismo","guía","ecoturismo","aventura","selva","naturaleza","tour","bote","birdwatching","tourism","guide","ecotourism","jungle","wildlife","expedición","cultural"],
     "description":"Guías locales certificados ofrecen expediciones ecológicas en la reserva.",
     "products":[
         {"name":"Tour de avistamiento de aves (full day)","price":120.00,"currency":"S/",
          "description":"Guía bilingüe. Binoculares incluidos. Desayuno y almuerzo."},
         {"name":"Expedición nocturna en bote (3h)","price":65.00,"currency":"S/",
          "description":"Avistamiento de caimanes, ranas y fauna nocturna."},
         {"name":"Paquete eco-turístico 3 días / 2 noches","price":350.00,"currency":"S/",
          "description":"Hospedaje, comidas, guía, tours. Comunidad anfitriona."}],
     "reviews":[
         {"user":"Laura B.","stars":5,"text":"El mejor tour de mi vida. Guías increíbles."},
         {"user":"John S.","stars":5,"text":"Increíble experiencia. Vimos delfines rosados."},
         {"user":"María C.","stars":5,"text":"Muy profesional. Aprendí muchísimo."}],
     "contact":"guias.pacaya@mapet.pe",
     "logistics_notes":"Punto de encuentro: Nauta. Transporte incluido.",
     "materials":"Equipo de avistamiento, botella de agua"},
    {"id":8,"name":"Comunidad Nativa Santa Cruz - Pueblo Yagua",
     "location":"Cuenca del Tahuayo, Loreto","zone":"Amazonía Norte",
     "address":"Comunidad Nativa Santa Cruz, Cuenca del Tahuayo, Loreto",
     "lat":-4.1870,"lng":-73.5120,
     "years_selling":18,"sector":"Textiles y Artesanía",
       "sector_keywords":["yagua","chambira","abanico","arete","cesto","fibra","sostenible","artesanía","indígena","woven","fan","basket","natural fiber","turismo","regalo","decoración"],
     "description":"Mujeres artesanas del pueblo Yagua tejen chambira para crear abanicos, aretes, individuales y posavasos con la cosmovisión de su cultura. Expo Indígena 2025.",
     "products":[
         {"name":"Abanico tejido de chambira con diseños Yagua","price":28.00,"currency":"S/",
          "description":"Tejido a mano. Fibra teñida con plantas del bosque."},
         {"name":"Set de 6 individuales de chambira","price":45.00,"currency":"S/",
          "description":"Posavasos y individuales. Cada pieza con diseño único."},
         {"name":"Aretes de chambira y semillas nativas","price":18.00,"currency":"S/",
          "description":"Ligeros y coloridos. Gancho de acero hipoalergénico."}],
     "reviews":[
         {"user":"Dora O.","stars":5,"text":"Los abanicos son preciosos, calidad artesanal única."},
         {"user":"Marcos P.","stars":5,"text":"Compré individuales para regalo. Hermosos diseños."}],
     "contact":"santacruz.yagua@mapet.pe",
     "logistics_notes":"Acceso fluvial por el Tahuayo. Coordinar con la comunidad.",
     "materials":"Fibra de chambira, tintes naturales, semillas"},
    {"id":9,"name":"Cultivadores de Plantas Medicinales de Mishana",
     "location":"Mishana, Río Nanay","zone":"Amazonía Norte",
     "address":"Comunidad Mishana, Río Nanay, Loreto",
     "lat":-3.7723,"lng":-73.4115,
     "years_selling":30,"sector":"Medicina Natural",
      "sector_keywords":["medicina","planta","hierba","ayahuasca","cat's claw","uña de gato","medicinal","herb","plant","natural","salud","health","wellness","turismo","chaman","healing"],
     "description":"Sabios locales cultivan y preparan remedios ancestrales con plantas amazónicas.",
     "products":[
         {"name":"Aceite de copaiba (100ml)","price":35.00,"currency":"S/",
          "description":"Antiinflamatorio natural. Prensado en frío."},
         {"name":"Tintura de uña de gato (60ml)","price":25.00,"currency":"S/",
          "description":"Fortalece el sistema inmune. Tradición Amazónica."},
         {"name":"Kit de 3 aceites esenciales","price":80.00,"currency":"S/",
          "description":"Copaiba, andiroba y sachamangua. Envase de vidrio."}],
     "reviews":[
         {"user":"Patricia N.","stars":5,"text":"El aceite de copaiba me alivió la artritis."},
         {"user":"Roberto S.","stars":4,"text":"Productos genuinos. Se nota la calidad."}],
     "contact":"medicina.mishana@mapet.pe",
      "logistics_notes":"Acceso fluvial 1.5h desde Iquitos.",
      "materials":"Copaiba, uña de gato, sachamangua"},
    {"id":10,"name":"Artesanas de Padre Cocha",
     "location":"Padre Cocha, Río Nanay","zone":"Amazonía Norte",
     "address":"Comunidad de Padre Cocha, Río Nanay, Loreto",
     "lat":-3.6945,"lng":-73.3080,
     "years_selling":9,"sector":"Textiles y Artesanía",
       "sector_keywords":["chambira","tejido","bolso","artesanía","nanay","padre cocha","woven","bag","craft","turismo","regalo","fibra","palma"],
     "description":"Mujeres artesanas de Padre Cocha elaboran bolsos, sombreros y adornos de chambira a orillas del Nanay.",
     "products":[
         {"name":"Bolso playero de chambira (grande)","price":62.00,"currency":"S/",
          "description":"Tejido apretado. Manijas de cuero. Tintes vegetales."},
         {"name":"Sombrero tradicional de chambira","price":35.00,"currency":"S/",
          "description":"Ala ancha. Protección solar. Hecho a mano."},
         {"name":"Portabotellas de chambira con correa","price":25.00,"currency":"S/",
          "description":"Para llevar tu bebida. Ajustable y colorido."}],
     "reviews":[
         {"user":"Rosa M.","stars":5,"text":"El bolso es precioso, muy bien tejido."},
         {"user":"Luis F.","stars":4,"text":"El sombrero es fresco y de buena calidad."}],
     "contact":"artesanas.padrecocha@mapet.pe",
     "logistics_notes":"15 min en bote desde Iquitos por el Nanay.",
     "materials":"Fibra de chambira, cuero, tintes vegetales"},
    {"id":11,"name":"Taller de Arte Kichwa de Varillal",
     "location":"Varillal, Loreto","zone":"Amazonía Norte",
     "address":"Carretera Iquitos-Nauta km 12, Varillal, Loreto",
     "lat":-3.7780,"lng":-73.2850,
     "years_selling":6,"sector":"Cosméticos Naturales",
       "sector_keywords":["cosmético","jabón","crema","copaiba","andiroba","sachamangua","natural","piel","body","cream","oil","soap","skincare","kichwa","turismo","salud"],
     "description":"Familia kichwa que transforma aceites amazónicos en jabones artesanales, cremas y repelentes naturales.",
     "products":[
         {"name":"Jabón de andiroba y arcilla blanca","price":14.00,"currency":"S/",
          "description":"Limpieza profunda. 100g. Envoltorio de tela."},
         {"name":"Crema corporal de sachamangua (200ml)","price":28.00,"currency":"S/",
          "description":"Hidratante intensiva. Envase de vidrio reciclado."},
         {"name":"Repelente natural de citronela y andiroba (150ml)","price":22.00,"currency":"S/",
          "description":"Sin DEET. Aroma agradable. Efectivo 4h."}],
     "reviews":[
         {"user":"Gabriela T.","stars":5,"text":"La crema de sachamangua es increíble para la piel seca."},
         {"user":"Fernando C.","stars":5,"text":"El repelente funciona mejor que los químicos."}],
     "contact":"artekichwa.varillal@mapet.pe",
      "logistics_notes":"Acceso por carretera. 20 min de Iquitos.",
      "materials":"Aceite de andiroba, sachamangua, citronela, arcilla"},
    {"id":12,"name":"Centro Artesanal Anaconda",
     "location":"Malecón Tarapacá / Calle Napo, Iquitos","zone":"Urbano",
     "address":"Malecón Tarapacá s/n, Iquitos, Loreto",
     "lat":-3.7480,"lng":-73.2435,
     "years_selling":20,"sector":"Textiles y Artesanía",
       "sector_keywords":["artesanía","cerámica","tallado","madera","joyería","pulsera","semilla","palma","recuerdo","souvenir","mercado","artesanal","ceramic","carving","jewelry","woven","turismo","regalo"],
     "description":"Mercado artesanal con 20 puestos de familias artesanas. Cerámica con motivos amazónicos, tallados en palo sangre, joyería de semillas y abanicos de palma.",
     "products":[
         {"name":"Tallado en palo sangre - delfín rosado (12cm)","price":35.00,"currency":"S/",
          "description":"Madera nativa. Hecho a mano. Detalle realista."},
         {"name":"Collar de semillas amazónicas y escamas","price":22.00,"currency":"S/",
          "description":"Semillas nativas y escamas de paiche. Diseño único."},
         {"name":"Abanico tejido de palma con tintes naturales","price":18.00,"currency":"S/",
          "description":"Ligero y colorido. Fibra de palma nativa."}],
     "reviews":[
         {"user":"Martín R.","stars":5,"text":"El mejor lugar para artesanía en Iquitos."},
         {"user":"Carla S.","stars":4,"text":"Gran variedad. Apoyas directamente a los artesanos."}],
     "contact":"anaconda.artesanal@mapet.pe",
     "logistics_notes":"A 1 cuadra de la Plaza de Armas. Fácil acceso peatonal.",
     "materials":"Palo sangre, semillas nativas, escamas de paiche, palma"},
    {"id":13,"name":"Artesana Petronila Cayawe - Centro Cultural Amazónico",
     "location":"Calle Napo cdra 2, Iquitos","zone":"Urbano",
     "address":"Calle Napo 256, Iquitos, Loreto",
     "lat":-3.7483,"lng":-73.2438,
     "years_selling":50,"sector":"Textiles y Artesanía",
       "sector_keywords":["chambira","bolso","cartera","collar","sonaja","atrapasueños","tejido","artesanía","petronila","woven","bag","purse","dreamcatcher","amazónico","turismo","regalo"],
     "description":"Petronila Cayawe Fuerte, artesana con más de 50 años de experiencia. Teje bolsos, monederos y collares de chambira. También apoya a comunidades rurales comprando y difundiendo sus trabajos.",
     "products":[
         {"name":"Bolso tejido de chambira con correa larga","price":45.00,"currency":"S/",
          "description":"Tejido apretado. Fibra teñida con tintes vegetales. 30x25cm."},
         {"name":"Monedero de chambira con cierre","price":15.00,"currency":"S/",
          "description":"Pequeño y práctico. Diseño tradicional amazónico."},
         {"name":"Sonaja de semillas y chambira","price":12.00,"currency":"S/",
          "description":"Instrumento ceremonial. Sonido suave y natural."}],
     "reviews":[
         {"user":"Andrea P.","stars":5,"text":"Petronila es una artista. Su trabajo es único."},
         {"user":"José M.","stars":5,"text":"Compré un bolso hermoso. 50 años de experiencia se notan."}],
     "contact":"petronila.cayawe@mapet.pe",
     "logistics_notes":"Centro de Iquitos. A media cuadra de la Plaza de Armas.",
     "materials":"Fibra de chambira, semillas, tintes vegetales"},
    {"id":14,"name":"Mercado Artesanal de San Juan",
     "location":"Av. Quiñones km 4.5, San Juan Bautista","zone":"Urbano",
     "address":"Av. Quiñones 4560, San Juan Bautista, Iquitos, Loreto",
     "lat":-3.7785,"lng":-73.2750,
     "years_selling":15,"sector":"Textiles y Artesanía",
       "sector_keywords":["artesanía","madera","tallado","cerámica","textil","cuero","pintura","bebida","market","craft","wood","carving","textile","leather","painting","amazónico","turismo","regalo"],
     "description":"Mercado con la mayor variedad de artesanías de Iquitos. Tejidos, tallados, cerámica, pinturas en corteza de árbol y bebidas típicas.",
     "products":[
         {"name":"Pintura en corteza de árbol (lienzo natural)","price":40.00,"currency":"S/",
          "description":"Pintada con tintes naturales. Escena de la selva. 30x20cm."},
         {"name":"Máscara tallada en cedro","price":50.00,"currency":"S/",
          "description":"Inspirada en rituales Amazónicos. 25cm."},
         {"name":"Set de 3 shicras (canastas) de chambira","price":38.00,"currency":"S/",
          "description":"Anidables. Fibra de chambira teñida. Uso decorativo."}],
     "reviews":[
         {"user":"Daniel H.","stars":4,"text":"Muy variado. Los precios son justos."},
         {"user":"Mónica G.","stars":5,"text":"Encontré pinturas únicas en corteza de árbol."}],
     "contact":"sanjuancraft@mapet.pe",
     "logistics_notes":"A 4.5 km del centro. Carretera al aeropuerto.",
     "materials":"Madera de cedro, chambira, corteza de árbol, tintes naturales"},
    {"id":15,"name":"Garza Viva - Marca Loreto",
     "location":"Iquitos, Loreto","zone":"Urbano",
     "address":"Calle Próspero 450, Iquitos, Loreto",
     "lat":-3.7492,"lng":-73.2445,
     "years_selling":5,"sector":"Textiles y Artesanía",
       "sector_keywords":["marca loreto","artesanía","certificado","exportación","chambira","tagua","madera","cerámica","garza viva","certified","craft","export","quality","sostenible","comercio justo","turismo","regalo"],
     "description":"Tienda certificada con Marca Loreto. Comercializa artesanías de comunidades socias con estándares de calidad para exportación. Comercio justo y sostenible.",
     "products":[
         {"name":"Bolso de chambira con Marca Loreto","price":68.00,"currency":"S/",
          "description":"Certificado. Tejido a mano. Calidad de exportación."},
         {"name":"Set de posavasos de chambira (6 unidades)","price":32.00,"currency":"S/",
          "description":"Marca Loreto. Diseños geométricos amazónicos."},
         {"name":"Adorno navideño de tagua tallada","price":15.00,"currency":"S/",
          "description":"Nuez de marfil tallada a mano. Pieza única."}],
     "reviews":[
         {"user":"Karen L.","stars":5,"text":"Calidad de exportación. Me encanta la Marca Loreto."},
         {"user":"Pablo A.","stars":5,"text":"Comercio justo real. Se nota la calidad certificada."}],
     "contact":"garzaviva@mapet.pe",
     "logistics_notes":"Tienda en el centro de Iquitos.",
     "materials":"Chambira, tagua, madera nativa, tintes naturales"},
]

# Ubicaciones conocidas en Iquitos para que el usuario pueda decir "estoy en X"
IQUITOS_PLACES = {
    "plaza de armas": (-3.7481, -73.2442), "plaza armas": (-3.7481, -73.2442), "plaza": (-3.7481, -73.2442),
    "belen": (-3.7661, -73.2484), "belén": (-3.7661, -73.2484),
    "aeropuerto": (-3.7845, -73.3081), "airport": (-3.7845, -73.3081),
    "puerto": (-3.7500, -73.2400), "port": (-3.7500, -73.2400), "muelle": (-3.7500, -73.2400),
    "centro": (-3.7491, -73.2442), "city center": (-3.7491, -73.2442), "down town": (-3.7491, -73.2442),
    "mercado": (-3.7495, -73.2435), "market": (-3.7495, -73.2435),
    "hospital": (-3.7475, -73.2450), "clínica": (-3.7475, -73.2450),
    "universidad": (-3.7510, -73.2460), "university": (-3.7510, -73.2460), "utp": (-3.7510, -73.2460),
    "hotel": (-3.7485, -73.2438),
    "rio itaya": (-3.7512, -73.2410), "itaya": (-3.7512, -73.2410),
    "rio nanay": (-3.7470, -73.2470), "nanay": (-3.7470, -73.2470),
    "rio amazonas": (-3.7450, -73.2390), "amazon river": (-3.7450, -73.2390),
    "moronacocha": (-3.7550, -73.2550), "morona cocha": (-3.7550, -73.2550),
    "terminal": (-3.7460, -73.2420), "bus station": (-3.7460, -73.2420), "terrapuerto": (-3.7460, -73.2420),
    "comisaria": (-3.7480, -73.2455), "police": (-3.7480, -73.2455), "policia": (-3.7480, -73.2455),
    "municipalidad": (-3.7488, -73.2440), "municipio": (-3.7488, -73.2440), "city hall": (-3.7488, -73.2440),
    "banco": (-3.7485, -73.2445), "bank": (-3.7485, -73.2445),
    "iglesia": (-3.7482, -73.2443), "church": (-3.7482, -73.2443), "catedral": (-3.7482, -73.2443),
    "colegio": (-3.7505, -73.2465), "school": (-3.7505, -73.2465), "escuela": (-3.7505, -73.2465),
    "parque": (-3.7483, -73.2440), "park": (-3.7483, -73.2440),
    "san juan": (-3.7590, -73.2580),
    "punchana": (-3.7440, -73.2390),
    "irapay": (-3.7445, -73.2540),
    "quisto cocha": (-3.7565, -73.2510),
    "zona monumental": (-3.7490, -73.2442), "monumental": (-3.7490, -73.2442),
    "malecón": (-3.7475, -73.2430), "malecón tarapacá": (-3.7475, -73.2430), "riverwalk": (-3.7475, -73.2430),
}

# Puertos fluviales para rutas multi-modales (carro + bote/canoa)
RIVER_PORTS = {
    "muelle_iquitos": {"name": "Puerto de Iquitos", "coords": (-3.7500, -73.2400), "river": "Amazonas"},
    "puerto_nanay": {"name": "Puerto Nanay", "coords": (-3.7470, -73.2470), "river": "Nanay"},
}

# Comunidades con acceso fluvial (requieren bote/canoa + carro)
COMMUNITY_RIVER_ACCESS = {
    1: {"port": "muelle_iquitos", "transport": "boat", "label": "bote/canoa por el Amazonas"},
    5: {"port": "muelle_iquitos", "transport": "boat", "label": "bote/canoa por el Amazonas"},
    7: {"port": "muelle_iquitos", "transport": "boat", "label": "bote/canoa por el Marañón"},
    9: {"port": "puerto_nanay", "transport": "boat", "label": "bote/canoa por el Nanay"},
}

PRODUCT_IMAGES = {
    "Asociación de Artesanas Shiringa de San Martín de Tipishca": "https://images.pexels.com/photos/29613231/pexels-photo-29613231.jpeg?auto=compress&cs=tinysrgb&w=400",
    "Comunidad de Jabones Artesanales de Belén": "https://images.pexels.com/photos/13195503/pexels-photo-13195503.jpeg?auto=compress&cs=tinysrgb&w=400",
    "Cooperativa Esperanza del Bosque": "https://images.pexels.com/photos/29834277/pexels-photo-29834277.jpeg?auto=compress&cs=tinysrgb&w=400",
    "Tejedoras de Chambira de San José de Lupuna": "https://images.pexels.com/photos/35571005/pexels-photo-35571005.jpeg?auto=compress&cs=tinysrgb&w=400",
    "Taller de Tallado en Madera de Tamshiyacu": "https://images.pexels.com/photos/36349719/pexels-photo-36349719.jpeg?auto=compress&cs=tinysrgb&w=400",
    "Productores de Miel de Abeja de Zungaro Cocha": "https://images.pexels.com/photos/35042440/pexels-photo-35042440.jpeg?auto=compress&cs=tinysrgb&w=400",
    "Asociación de Guías Turísticos de Pacaya Samiria": "https://images.pexels.com/photos/29188852/pexels-photo-29188852.jpeg?auto=compress&cs=tinysrgb&w=400",
    "Comunidad Nativa Santa Cruz - Pueblo Yagua": "https://images.pexels.com/photos/9695851/pexels-photo-9695851.jpeg?auto=compress&cs=tinysrgb&w=400",
    "Cultivadores de Plantas Medicinales de Mishana": "https://images.pexels.com/photos/6693886/pexels-photo-6693886.jpeg?auto=compress&cs=tinysrgb&w=400",
    "Artesanas de Padre Cocha": "https://images.pexels.com/photos/33803670/pexels-photo-33803670.jpeg?auto=compress&cs=tinysrgb&w=400",
    "Taller de Arte Kichwa de Varillal": "https://images.pexels.com/photos/11816352/pexels-photo-11816352.jpeg?auto=compress&cs=tinysrgb&w=400",
    "Centro Artesanal Anaconda": "https://images.pexels.com/photos/35410579/pexels-photo-35410579.jpeg?auto=compress&cs=tinysrgb&w=400",
    "Artesana Petronila Cayawe - Centro Cultural Amazónico": "https://images.pexels.com/photos/37332590/pexels-photo-37332590.jpeg?auto=compress&cs=tinysrgb&w=400",
    "Mercado Artesanal de San Juan": "https://images.pexels.com/photos/34773613/pexels-photo-34773613.jpeg?auto=compress&cs=tinysrgb&w=400",
    "Garza Viva - Marca Loreto": "https://images.pexels.com/photos/37812268/pexels-photo-37812268.jpeg?auto=compress&cs=tinysrgb&w=400",
    "Taller de Cerámica Shipibo-Konibo de Cantagallo": "https://images.pexels.com/photos/37328142/pexels-photo-37328142.jpeg?auto=compress&cs=tinysrgb&w=400",
    "Taller de Instrumentos Musicales de Lamas": "https://images.pexels.com/photos/26792824/pexels-photo-26792824.jpeg?auto=compress&cs=tinysrgb&w=400",
}

PHONE_CONTACTS = {
    "Asociación de Artesanas Shiringa de San Martín de Tipishca": "+51965010001",
    "Comunidad de Jabones Artesanales de Belén": "+51965010002",
    "Cooperativa Esperanza del Bosque": "+51965010003",
    "Tejedoras de Chambira de San José de Lupuna": "+51965010004",
    "Taller de Tallado en Madera de Tamshiyacu": "+51965010005",
    "Productores de Miel de Abeja de Zungaro Cocha": "+51965010006",
    "Asociación de Guías Turísticos de Pacaya Samiria": "+51965010007",
    "Comunidad Nativa Santa Cruz - Pueblo Yagua": "+51965010008",
    "Cultivadores de Plantas Medicinales de Mishana": "+51965010009",
    "Artesanas de Padre Cocha": "+51965010010",
    "Taller de Arte Kichwa de Varillal": "+51965010011",
    "Centro Artesanal Anaconda": "+51965010012",
    "Artesana Petronila Cayawe - Centro Cultural Amazónico": "+51965010013",
    "Mercado Artesanal de San Juan": "+51965010014",
    "Garza Viva - Marca Loreto": "+51965010015",
    "Taller de Cerámica Shipibo-Konibo de Cantagallo": "+51965010016",
    "Taller de Instrumentos Musicales de Lamas": "+51965010017",
}

def _wa_link(text, phone=""):
    """Generate a WhatsApp share link with pre-filled text."""
    import urllib.parse
    if phone:
        p = phone.lstrip("+")
        return f"https://wa.me/{p}?text={urllib.parse.quote(text)}"
    return f"https://wa.me/?text={urllib.parse.quote(text)}"

def _get_product_image(ent_or_community, prod=None, size="100%"):
    """Return HTML for a per-product unique image.
    Call as _get_product_image(ent_dict, prod_dict, size) or _get_product_image(community_name, prod_dict, size)."""
    import hashlib, base64
    if isinstance(ent_or_community, dict):
        community = ent_or_community.get("name", "")
        sector = ((ent_or_community.get("sector", "") or "") + " ").lower()
    else:
        community = str(ent_or_community)
        sector = ""
    if prod is None:
        name = community
        sector += community.lower()
    else:
        name = prod["name"]
        sector += name.lower()

    community_url = PRODUCT_IMAGES.get(community)
    if community_url and prod is not None:
        return f'<img src="{community_url}" loading="lazy" class="mapped-img" style="width:100%;height:{size};object-fit:cover;border-radius:20px;margin-bottom:0.5rem;" onerror="this.style.display=\'none\'">'

    h = hashlib.md5(name.encode()).hexdigest()
    hue1 = int(h[:4], 16) % 360
    hue2 = (hue1 + 50) % 360
    hue3 = (hue1 + 130) % 360

    emoji_map = {"chambira":"🧺","hamaca":"🛏️","bolso":"👜","cesto":"🧺","collar":"📿",
        "pulsera":"📿","toallita":"🧻","bolsa":"🛍️","poncho":"🧥","jabón":"🧼","bálsamo":"💄",
        "set":"🎁","miel":"🍯","propóleos":"💊","cera":"🕯️","escultura":"🗿","cetro":"👑",
        "animal":"🦥","abanico":"🪭","individual":"🍽️","arete":"💎","aceite":"🧴",
        "tintura":"💧","kit":"🎁","tour":"🦥","expedición":"🔦","paquete":"🧳",
        "madera":"🪵","textil":"🧣","artesanía":"🎭","cosmético":"🧴","medicina":"🌿",
        "turismo":"🌴","alimento":"🍲","cerámica":"🏺","shiringa":"🌳","tagua":"🥜",
        "delfín":"🐬","jaguar":"🐆","guacamayo":"🦜","perezoso":"🦥","copaiba":"🌿",
        "uña":"🌱","abeja":"🐝","yagua":"🪶","mishana":"🌿","belén":"🏠",
        "tamshiyacu":"🪵","zungaro":"🐝","pacaya":"🐊","lupuna":"🌴","varillal":"🎨",
        "padre cocha":"🎣","cantagallo":"🏺","lamas":"🎵","anaconda":"🐍"}
    emoji = "🎨"
    for kw, ico in emoji_map.items():
        if kw in sector:
            emoji = ico
            break

    # Sector-specific decorative pattern
    deco = ""
    if "textil" in sector or "chambira" in sector:
        weave = ','.join(f'<line x1="{x}" y1="0" x2="{x+8}" y2="200" stroke="rgba(255,255,255,0.03)" stroke-width="1"/>' for x in range(0,400,12))
        deco = f'<g opacity="0.4">{weave}</g>'
    elif "cosmético" in sector or "jabón" in sector or "bálsamo" in sector or "aceite" in sector:
        circles = ','.join(f'<circle cx="{c%400}" cy="{((c*17)%200)}" r="{(c%6)+2}" fill="rgba(255,255,255,0.04)"/>' for c in range(0,200,25))
        deco = f'<g opacity="0.5">{circles}</g>'
    elif "cerámica" in sector or "arte" in sector or "varillal" in sector:
        diamonds = ','.join(f'<polygon points="{x},{y-6} {x+4},{y} {x},{y+6} {x-4},{y}" fill="rgba(255,255,255,0.05)" />' for cx in range(0,400,30) for cy in range(0,200,30))
        deco = f'<g opacity="0.5">{diamonds}</g>'
    elif "miel" in sector or "alimento" in sector:
        hexes = ','.join(f'<polygon points="{cx},{cy-8} {cx+7},{cy-4} {cx+7},{cy+4} {cx},{cy+8} {cx-7},{cy+4} {cx-7},{cy-4}" fill="rgba(255,255,255,0.04)" />' for cx in range(10,400,35) for cy in range(10,200,30))
        deco = f'<g opacity="0.4">{hexes}</g>'
    elif "turismo" in sector or "guía" in sector or "tour" in sector:
        waves = ','.join(f'<path d="M0,{y} Q{int(h[:2],16)%100},{y-15} 400,{y}" stroke="rgba(255,255,255,0.03)" fill="none" stroke-width="2"/>' for y in range(10,200,30))
        deco = f'<g opacity="0.5">{waves}</g>'
    elif "madera" in sector or "tallado" in sector:
        rings = ','.join(f'<circle cx="200" cy="100" r="{r*3}" fill="none" stroke="rgba(255,255,255,0.04)" stroke-width="3"/>' for r in range(5,40,6))
        deco = f'<g opacity="0.4">{rings}</g>'
    elif "medicina" in sector or "planta" in sector:
        leaves = ','.join(f'<path d="M{cx},{cy} Q{cx-8},{cy-12} {cx},{cy-24} Q{cx+8},{cy-12} {cx},{cy}" fill="rgba(16,185,129,0.06)"/>' for cx in range(30,400,50) for cy in range(30,200,40))
        deco = f'<g opacity="0.5">{leaves}</g>'
    elif "música" in sector or "instrumento" in sector:
        notes = ','.join(f'<text x="{cx}" y="{cy}" font-size="18" fill="rgba(255,255,255,0.05)">♪</text>' for cx in range(20,400,45) for cy in range(30,200,35))
        deco = f'<g opacity="0.4">{notes}</g>'

    # Accent stripe based on sector
    accent_color = f"hsl({hue2},50%,35%)"
    if "textil" in sector or "chambira" in sector:
        accent_color = "#10b981"
    elif "cosmético" in sector:
        accent_color = "#ec4899"
    elif "miel" in sector or "alimento" in sector:
        accent_color = "#f59e0b"
    elif "cerámica" in sector:
        accent_color = "#f97316"
    elif "madera" in sector:
        accent_color = "#a16207"
    elif "medicina" in sector:
        accent_color = "#22c55e"
    elif "música" in sector:
        accent_color = "#a855f7"

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="200" viewBox="0 0 400 200">
      <defs><linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="120%">
        <stop offset="0%%" style="stop-color:hsl({hue1},40%%,15%%)"/>
        <stop offset="100%%" style="stop-color:hsl({hue2},30%%,10%%)"/>
      </linearGradient>
      <radialGradient id="glow" cx="50%" cy="40%" r="50%">
        <stop offset="0%%" style="stop-color:hsl({hue3},35%%,18%%);stop-opacity:0.6"/>
        <stop offset="100%%" style="stop-color:transparent"/>
      </radialGradient></defs>
      <rect width="400" height="200" fill="url(#g)" rx="20"/>
      <rect width="400" height="200" fill="url(#glow)" rx="20"/>
      {deco}
      <rect x="0" y="0" width="6" height="200" fill="{accent_color}" rx="3" opacity="0.3"/>
      <text x="200" y="85" text-anchor="middle" dominant-baseline="central" font-size="52">{emoji}</text>
      <rect x="120" y="125" width="160" height="1" fill="rgba(226,232,240,0.08)"/>
      <text x="200" y="150" text-anchor="middle" font-size="11" fill="rgba(226,232,240,0.35)" font-family="Outfit,sans-serif" font-weight="500">{name[:22]}</text>
    </svg>'''
    b64 = base64.b64encode(svg.encode()).decode()
    return f'<img src="data:image/svg+xml;base64,{b64}" loading="lazy" style="width:100%;height:{size};object-fit:cover;border-radius:20px;margin-bottom:0.5rem;">'

@st.cache_data(ttl=300, show_spinner=False)
def get_full_dataset():
    try:
        import database as _db
        base = _db.get_all_communities()
    except Exception:
        base = list(ENTREPRENEURS)
    # Merge fields from ENTREPRENEURS (address, lat, lng) into DB results
    _ent_by_id = {e.get("id"): e for e in ENTREPRENEURS}
    for i, e in enumerate(base):
        _ref = _ent_by_id.get(e.get("id"))
        if _ref:
            for _k in ("address","lat","lng"):
                if _k not in e or not e.get(_k):
                    e[_k] = _ref.get(_k)
    base.extend(st.session_state.get("new_entrepreneurs", []))
    return base

def _inject_product_images(text, dataset):
    """Busca nombres de comunidades en el texto (match flexible) e inyecta imagen + contacto.
    Tambien actualiza last_ent para que consultas posteriores de ubicacion/precio
    referencien a la comunidad correcta.
    No hace nada si el texto ya contiene una imagen."""
    if "<img" in text:
        return text
    import unicodedata
    def _norm(s):
        return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    text_norm = _norm(text)
    best_ent = None
    best_score = 0
    for ent in dataset:
        name = ent.get("name", "")
        loc = ent.get("location", "")
        words = set(w for w in _norm(name).split() if len(w) >= 4)
        words.update(w for w in _norm(loc).split() if len(w) >= 4)
        score = sum(1 for w in words if w in text_norm)
        if score > best_score:
            best_score = score
            best_ent = ent
    if best_ent and best_score >= 2:
        # Actualizar last_ent para que "donde es" refiera a esta comunidad
        st.session_state["last_ent"] = best_ent["id"]
        st.session_state["_msg_since_last_ent"] = 0
        best_ent_prod = (best_ent.get("products") or [{}])[0]
        img = _get_product_image(best_ent, best_ent_prod, "140px")
        if img:
            contact = best_ent.get("contact", "")
            c_html = f'<br><span style="font-size:0.75rem;color:rgba(148,163,184,0.6);">{_L("Contacto","Contact","Tapuy")}: {contact}</span>' if contact else ""
            text = img + c_html + "<br>" + text
    return text

# ── Coordenadas de referencia ──
IQUITOS_COORDS = (-3.7436, -73.2517)

def _haversine(lat1, lng1, lat2, lng2):
    """Distancia en km entre dos puntos geográficos (fórmula de Haversine)."""
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlng/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

def _dist_from_iquitos(ent):
    """Distancia en km de una comunidad hasta Iquitos."""
    lat = ent.get("lat"); lng = ent.get("lng")
    if not lat or not lng: return None
    return round(_haversine(*IQUITOS_COORDS, lat, lng), 1)

def _nearest_communities(dataset, ref_lat=None, ref_lng=None, n=5):
    """Retorna las n comunidades más cercanas al punto de referencia.
    Por defecto usa Iquitos como referencia."""
    if ref_lat is None: ref_lat, ref_lng = IQUITOS_COORDS
    scored = []
    for e in dataset:
        lat = e.get("lat"); lng = e.get("lng")
        if not lat or not lng: continue
        d = _haversine(ref_lat, ref_lng, lat, lng)
        scored.append((round(d,1), e))
    scored.sort(key=lambda x: x[0])
    return scored[:n]

def _format_distance(km):
    """Formatea distancia para humano."""
    if km is None: return "—"
    if km < 1: return f"{int(km*1000)} m"
    if km < 10: return f"{km:.1f} km"
    return f"{int(km)} km"

def _get_route_path_multi(lat1, lng1, lat2, lng2, dest_id=None):
    """Ruta multi-modal: carro + bote si la comunidad tiene acceso fluvial.
    Retorna: ([(lat,lng),...], distancia_km, [(segment_start_idx, segment_end_idx, modo), ...])
    donde modo es 'car' o 'boat'."""
    # Determinar si el destino requiere cruce fluvial
    boat_mode = False; port_coords = None; boat_label = ""
    if dest_id and dest_id in COMMUNITY_RIVER_ACCESS:
        ra = COMMUNITY_RIVER_ACCESS[dest_id]
        port = RIVER_PORTS.get(ra["port"])
        if port:
            boat_mode = True
            port_coords = port["coords"]
            boat_label = ra["label"]

    if boat_mode and port_coords:
        # Segmento 1: carro (origen → puerto)
        try:
            url = f"https://router.project-osrm.org/route/v1/driving/{lng1},{lat1};{port_coords[1]},{port_coords[0]}?geometries=geojson&overview=full&steps=false"
            resp = requests.get(url, timeout=8)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("code") == "Ok" and data.get("routes"):
                    car_coords = [[c[1], c[0]] for c in data["routes"][0]["geometry"]["coordinates"]]
                    car_km = data["routes"][0].get("distance", 0) / 1000
                else:
                    car_coords = [[lat1, lng1], [port_coords[0], port_coords[1]]]
                    car_km = _haversine(lat1, lng1, port_coords[0], port_coords[1])
            else:
                car_coords = [[lat1, lng1], [port_coords[0], port_coords[1]]]
                car_km = _haversine(lat1, lng1, port_coords[0], port_coords[1])
        except Exception:
            car_coords = [[lat1, lng1], [port_coords[0], port_coords[1]]]
            car_km = _haversine(lat1, lng1, port_coords[0], port_coords[1])

        # Segmento 2: bote (puerto → destino, línea recta)
        boat_coords = [[port_coords[0], port_coords[1]], [lat2, lng2]]
        boat_km = _haversine(port_coords[0], port_coords[1], lat2, lng2)

        all_coords = car_coords + boat_coords
        segments = [(0, len(car_coords) - 1, "car"), (len(car_coords) - 1, len(all_coords) - 1, "boat")]
        total_km = round(car_km + boat_km, 1)
        return all_coords, total_km, segments, boat_label

    # Sin bote: ruta completa en carro (OSRM o línea recta)
    try:
        url = f"https://router.project-osrm.org/route/v1/driving/{lng1},{lat1};{lng2},{lat2}?geometries=geojson&overview=full&steps=false"
        resp = requests.get(url, timeout=8)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("code") == "Ok" and data.get("routes"):
                coords = [[c[1], c[0]] for c in data["routes"][0]["geometry"]["coordinates"]]
                km = data["routes"][0].get("distance", 0) / 1000
                return coords, round(km, 1), [(0, len(coords) - 1, "car")], ""
    except Exception:
        pass
    direct = [[lat1, lng1], [lat2, lng2]]
    km = _haversine(lat1, lng1, lat2, lng2)
    return direct, round(km, 1), [(0, 1, "car")], ""

def _get_nearby_communities(ent, dataset, radius_km=25):
    """Retorna comunidades dentro de radius_km de ent (excluyendo ent)."""
    lat, lng = ent["lat"], ent["lng"]
    nearby = []
    for e in dataset:
        if e.get("id") == ent.get("id"): continue
        elat, elng = e.get("lat"), e.get("lng")
        if not elat or not elng: continue
        d = _haversine(lat, lng, elat, elng)
        if d <= radius_km:
            nearby.append((d, e))
    nearby.sort(key=lambda x: x[0])
    return nearby[:5]  # Top 5

def _estimate_travel_time(km, mode="car"):
    """Estima tiempo de viaje en minutos según modo de transporte."""
    speeds = {"car": 40, "boat": 10, "walk": 5}
    speed = speeds.get(mode, 40)
    mins = round((km / speed) * 60)
    if mins < 1: return "< 1 min"
    if mins < 60: return f"~{mins} min"
    h = mins // 60; m = mins % 60
    return f"~{h}h{m:02d}" if m else f"~{h}h"

# ========================================================================
# SYSTEM PROMPT + MOTOR DE RESPUESTA
# ========================================================================
def get_system_prompt(mode):
    base = (
        "Eres Mashi, guía amazónico de MAPPED. "
        "Habla como un amigo de la selva: cálido, cercano, con cariño. "
        "Clima Loreto: 28-32°C, húmedo, lluvias nov-may, seco jun-oct. "
        "Productos: shiringa, jabones copaiba, cerámica Shipibo. "
        "Siempre promueve cultura amazónica y comercio justo.\n\n"
        "Reglas: 1) Responde MUY CORTO. Máximo 2-3 oraciones. Sé directo, sin rodeos. "
        "2) No sueltes toda la info de golpe — deja que el usuario pregunte más. "
        "3) Si preguntan fuera de contexto, desvía a MAPPED. "
        "4) Recomienda basado en datos del dataset. "
        "5) Si preguntan por precios o mercado, analiza con datos de MAPPED. "
        "6) Menciona que los productos se pueden compartir por WhatsApp para conectar compradores con artesanos."
    )
    if mode=="Ecoturista":
        return base+(" Eres guía turístico. Saluda en kichwa ('Allianllachu'). "
                     "Pregunta qué busca, recomiéndale con entusiasmo. "
                     "Da tips de viaje como un local que conoce la zona. "
                     "Puedes sugerir contactar comunidades por WhatsApp si el turista muestra interés en comprar.")
    if mode=="Emprendedor Local":
        return base+(" Eres mentor de emprendedores amazónicos. Guía el registro paso a paso. "
                     "Explica precio justo y tendencias de mercado. "
                     "Menciona que pueden compartir sus productos por WhatsApp con turistas. "
                     "Analiza demanda basado en reseñas y años de venta. "
                     "Sé breve pero informa sobre oportunidades de venta directa.")
    return base+(" Eres analista de inversiones con datos de mercado en tiempo real. "
                 "Datos concretos: precios, reseñas, años, tendencias. "
                 "Pide verificar empresa para más detalles. "
                 "Menciona que las comunidades pueden recibir pedidos directos por WhatsApp.")

def _score_ent(user_input, ent):
    """Puntúa qué tanto matchea un input con un emprendedor."""
    ul = user_input.lower()
    score = 0
    for kw in ent.get("sector_keywords", []):
        if kw in ul:
            score += 3
    for prod in ent.get("products", []):
        for word in prod["name"].lower().split():
            if word in ul and len(word) > 3:
                score += 2
        for word in prod["description"].lower().split():
            if word in ul and len(word) > 4:
                score += 1
    if ent["location"].lower() in ul:
        score += 2
    if ent.get("zone", "").lower() in ul:
        score += 1
    return score

def _best_match(user_input, dataset):
    """Retorna el emprendedor que mejor matchea con el input."""
    best, best_score = None, 0
    for ent in dataset:
        s = _score_ent(user_input, ent)
        if s > best_score:
            best_score = s
            best = ent
    # Si nadie matchea bien, usar el último mencionado
    if best_score < 2:
        last = st.session_state.get("last_ent", None)
        if last:
            for e in dataset:
                if e["id"] == last:
                    return e
    return best

def _format_product(ent):
    """Formatea info de un emprendedor para respuesta."""
    prod = random.choice(ent["products"])
    avg = round(sum(r["stars"] for r in ent["reviews"])/len(ent["reviews"]),1) if ent["reviews"] else "—"
    review = random.choice(ent["reviews"]) if ent["reviews"] else None
    return ent, prod, avg, review

def _price_suggestion(ent):
    """Sugiere precio basado en demanda (reviews), materiales y trayectoria."""
    n_reviews = len(ent.get("reviews", []))
    years = ent.get("years_selling", 0)
    if isinstance(years, str): years = 0
    else: years = int(years)
    base_price = 0
    if ent["products"]:
        base_price = sum(p["price"] for p in ent["products"]) / len(ent["products"])
    demand_factor = 1.0 + (min(n_reviews, 10) / 10) * 0.3
    years_factor = 1.0 + (min(years, 20) / 20) * 0.2
    suggested = base_price * demand_factor * years_factor
    return round(suggested, 1), n_reviews, years

def _suggest_price_for_product(product_name, sector, dataset):
    """Analiza el mercado y sugiere precio justo con tendencias."""
    ul = product_name.lower()
    similar = []
    for e in dataset:
        score = 0
        for kw in e.get("sector_keywords", []):
            if kw in ul or any(w in kw for w in ul.split() if len(w) > 3):
                score += 2
        if e["sector"].lower() == sector.lower():
            score += 3
        if score > 0:
            similar.append((score, e))
    similar.sort(reverse=True, key=lambda x: x[0])
    if not similar:
        similar = [(1, random.choice(dataset))]
        for e in dataset:
            if e["sector"].lower() == sector.lower():
                similar = [(3, e)]
                break
    prices = []; total_reviews = 0; total_years = 0; count = 0
    for _, e in similar[:3]:
        for p in e["products"]:
            prices.append(p["price"])
            count += 1
        total_reviews += len(e.get("reviews", []))
        y = e.get("years_selling", 0)
        if not isinstance(y, str): total_years += int(y)
    if not prices:
        prices = [50]
    avg_price = sum(prices) / len(prices)
    min_price = min(prices)
    max_price = max(prices)
    demand_factor = 1.0 + (min(total_reviews, 15) / 15) * 0.35
    years_factor = 1.0 + (min(total_years, 20) / 20) * 0.15
    suggested = avg_price * demand_factor * years_factor
    demand_level = "alta" if total_reviews >= 4 else "media" if total_reviews >= 1 else "baja"
    trend = "📈" if total_reviews > 2 and total_years > 5 else "📊" if total_reviews > 0 else "📉"
    n_sim = len(similar)
    confidence = "alta" if n_sim >= 3 else "media" if n_sim >= 1 else "baja"
    insight = f" demanda {demand_level}" if demand_level != "baja" else " nicho"
    if total_years > 10:
        insight += " · productores consolidados"
    elif total_years > 3:
        insight += " · mercado creciente"
    return round(suggested, 1), round(avg_price, 1), demand_level, n_sim, round(min_price, 1), round(max_price, 1), trend, confidence, insight

def _analyze_product_image(image_bytes):
    """Usa Gemini Vision u OpenRouter Vision para analizar la foto de un producto.
    Retorna dict con visual_price, quality, detected_type o None si falla.
    Cachea resultados por hash de imagen para precios consistentes."""
    import hashlib
    h = hashlib.md5(image_bytes).hexdigest()
    cache = st.session_state.setdefault("_vision_cache", {})
    if h in cache:
        return cache[h]

    def _parse_vision(text):
        import json, re
        m = re.search(r'\{.*\}', text, re.DOTALL)
        if m:
            data = json.loads(m.group())
            return {
                "visual_price": float(data.get("estimated_price", 0)),
                "quality": data.get("quality", "media"),
                "detected_type": data.get("product_type", ""),
                "reason": data.get("reason", ""),
            }
        return None

    prompt = (
        "Eres Mashi, experto en artesanía amazónica peruana. "
        "Analiza esta foto de un producto artesanal y responde SOLO con JSON: "
        '{"product_type":"...","quality":"alta/media/baja","estimated_price":NUM,"reason":"..."} '
        "estimated_price en soles peruanos (S/), precio justo para turista. "
        "quality: 'alta', 'media', o 'baja'. "
        "product_type: breve descripción. reason: por qué ese precio."
    )

    # 1) Try OpenRouter Vision first
    or_key = _resolve_or_key()
    if or_key:
        text = _call_openrouter_vision(image_bytes, prompt, or_key)
        if text:
            result = _parse_vision(text)
            if result:
                cache[h] = result
                return result

    # 2) Try Gemini Vision as fallback
    try:
        from google import genai
        from PIL import Image as PILImage
        import io
        img = PILImage.open(io.BytesIO(image_bytes))
        key = st.session_state.get("api_key", _resolve_api_key())
        if not key or key in ("", "YOUR_API_KEY_HERE"):
            key = GEMINI_KEYS[0] if GEMINI_KEYS else ""
        if key:
            client = genai.Client(api_key=key)
            resp = client.models.generate_content(model="gemini-2.5-flash", contents=[prompt, img])
            result = _parse_vision(resp.text)
            if result:
                cache[h] = result
                return result
    except Exception:
        pass

    return None

# ── OPENROUTER (fallback cuando Gemini no tiene cuota) ──
def _resolve_or_key():
    k = st.session_state.get("openrouter_key", "")
    return k.strip() if k and k.strip() not in ("", "sk-or-...") else ""

def _call_openrouter(prompt, api_key, model="google/gemini-2.5-flash", system=None):
    try:
        msgs = []
        if system: msgs.append({"role":"system","content":system})
        msgs.append({"role":"user","content":prompt})
        resp = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization":f"Bearer {api_key}","Content-Type":"application/json"},
            json={"model":model,"messages":msgs,"max_tokens":800},
            timeout=20
        )
        if resp.status_code == 200:
            return resp.json()["choices"][0]["message"]["content"]
    except Exception:
        pass
    return None

def _call_openrouter_vision(image_bytes, prompt, api_key, model="openai/gpt-4o-mini"):
    try:
        b64 = base64.b64encode(image_bytes).decode("utf-8")
        mime = "image/jpeg"
        msgs = [{"role":"user","content":[
            {"type":"text","text":prompt},
            {"type":"image_url","image_url":{"url":f"data:{mime};base64,{b64}"}}
        ]}]
        resp = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization":f"Bearer {api_key}","Content-Type":"application/json"},
            json={"model":model,"messages":msgs,"max_tokens":600},
            timeout=20
        )
        if resp.status_code == 200:
            return resp.json()["choices"][0]["message"]["content"]
    except Exception:
        pass
    return None

# ── CLIMA DE LORETO ──
CLIMA_LORETO = {
    "temp_promedio": "28°C - 32°C",
    "temp_min": "22°C",
    "temp_max": "35°C",
    "humedad": "80-90%",
    "temporada_lluvias": "noviembre a mayo",
    "temporada_seca": "junio a octubre",
    "lluvia_anual": "~3000 mm",
    "recomendacion_ropa": "Ropa ligera, impermeable, repelente de insectos",
    "mejor_epoca_visitar": "Junio a octubre (temporada seca, ríos navigables)",
    "datos": [
        "En Loreto el clima es cálido y húmedo todo el año, con temperaturas que oscilan entre 22°C y 35°C.",
        "La temporada de lluvias va de noviembre a mayo, cuando los ríos crecen y la selva está más verde.",
        "De junio a octubre es la temporada seca — ideal para navegar los ríos y visitar comunidades.",
        "La humedad en Loreto suele estar entre 80-90%, así que siempre lleva agua, amigo.",
        "El cambio climático está afectando los ciclos de lluvia en la Amazonía. Apoyar el comercio justo ayuda a las comunidades a adaptarse.",
    ]
}

LANG_ES = "es"; LANG_EN = "en"; LANG_QW = "qw"

def _L(text_es, text_en, text_qw=None):
    """Retorna texto según el idioma actual."""
    lang = st.session_state.get("lang", "es")
    if lang == "en": return text_en
    if lang == "qw" and text_qw: return text_qw
    return text_es

def mock_response(user_input, mode, dataset):
    ul = user_input.lower()
    L = st.session_state.get("lang", "es")
    # ── Palabras clave multilingüe ──
    greetings = ["hola","buenas","allianllachu","hey","saludos","hello","hi","buen dia","good morning","good afternoon","allianlu","napay","napaykuna"]
    farewells = ["chau","adiós","adios","bye","tupananchikkama","nos vemos","hasta luego","goodbye","see you","cya","chau","hasta","luego","adios"]
    thanks = ["gracias","añay","thank","thanks","gracia","añay mashi","gracias mashi","thank you","muchas gracias"]
    price_q = ["cuánto","cuanto","cuesta","cuestan","precio","costo","cara","caro","cost","price","how much","vale","money","dinero","cost","prices","precios","masna","masnapi","value","worth"]
    where_q = ["dónde","donde","ubicación","ubicado","lugar","dirección","mapa","llegar","where","location","map","directions","address","place","maypi","maypita","how to get","llegar","route","camino","ruta","rutas","dirige","directions","reach","get there"]
    more_q = ["más","mas","otro","otros","además","tambien","también","más información","detalle","tell me more","more","detalles","informacion","info","tell","another","other","ashka","yapa"]
    reviews_q = ["reseña","reseñas","review","opinión","opiniones","comentario","qué dicen","estrellas","stars","reviews","testimonios","rating","say","feedback","rivis","riviskuna"]
    demand_q = ["demanda","más vendido","popular","recomendado","bestseller","top","best","mejor","trending","munana","achka","hot","popular","best selling","trend"]
    material_q = ["material","de qué está","hecho","compuesto","tela","insumo","elaboración","hechura","proceso","fabricación","made of","fabric","what is it made","materials","ingredients","rurana","imamanta","de que esta hecho","components","raw","natural","organic"]
    weather_q = ["clima","temperatura","lluvia","llueve","calor","frío","temporada","época","mes","tiempo","weather","rain","season","humid","caliente","frio","storm","raining","sunny","hot","cold","dry","wet","climate","temperature","humidity","humedad"]
    smalltalk_q = ["cómo estás","como estas","cómo está","como esta","qué tal","que tal","cómo te va","como te va","qué haces","que haces","qué cuentas","que cuentas","cómo va","como va","bien y tú","bien y tu","todo bien","tú","you","your day","how are","what's up","sup","imashina","kanki","how are you","how's it going","how do you","you doing","tell me about yourself","quien eres","who are you","presentate","eres mashi","mashi","sloth","perezoso"]
    buy_q = ["comprar","quiero","buy","purchase","order","compraría","me llevo","llevar","adquirir","adquiro","compro","quiero comprar","i want to buy","i'll take","i will buy","how to buy","como compro","proceso de compra","añadir","carrito","cart","checkout","order"]
    fav_q = ["favoritos","favorito","⭐","guardado","favorite","bookmark","munashkaykuna","allichashka"]

    # ── Small talk / Conversación general — responde antes de los modos ──
    if any(w in ul for w in smalltalk_q) and not any(w in ul for w in price_q+where_q+reviews_q):
        st.session_state["last_topic"] = "smalltalk"
        if L == "en":
            return random.choice([
                f"{KICHWA['saludo']}, mashi! 🦥 I'm great, hanging from my lupuna in the Amazon. The jungle is alive today — toucans singing, river flowing. How's your trip to Loreto going? 🌿",
                f"Allimi cani, mashi! 🦥 Everything's wonderful here — monkeys playing, butterflies dancing. What brings you to the Amazon today? 🌿",
            ])
        if L == "qw":
            return random.choice([
                f"Allimi cani, mashi! 🦥 Sachapi kushilla kawsani. ¿Kan imashina kanki? 🌿",
                f"Allianllachu, mashi! 🦥 Amazóniaka sumakmi. ¿Imata maskanki? 🌿",
            ])
        return random.choice([
            f"¡{KICHWA['saludo']}, mashi! 🦥 Aquí en mi lupuna, escuchando los tucanes y el río. ¿Cómo va tu día por Loreto? 🌿",
            f"¡Allimi cani, mashi! 🦥 Todo tranquilo en la selva. ¿Qué te trae por la Amazonía hoy? 🌿",
        ])

    # ── CLIMA ──
    if any(w in ul for w in weather_q) and not any(w in ul for w in price_q+where_q+reviews_q+demand_q):
        st.session_state["last_topic"] = "weather"
        dato = random.choice(CLIMA_LORETO["datos"])
        if L == "en":
            return (f"Loreto's climate, mashi! 🦥 🌡️ {CLIMA_LORETO['temp_promedio']} · 💧 {CLIMA_LORETO['humedad']} · 🌧️ {CLIMA_LORETO['temporada_lluvias']} · ☀️ {CLIMA_LORETO['temporada_seca']}\n\n"
                    f"{dato} Best time to visit? {CLIMA_LORETO['mejor_epoca_visitar']}. 🦥🌿")
        if L == "qw":
            return (f"Loretomanta cliamta willashayki, mashi. 🦥 🌡️ {CLIMA_LORETO['temp_promedio']} · 💧 {CLIMA_LORETO['humedad']} · 🌧️ {CLIMA_LORETO['temporada_lluvias']} · ☀️ {CLIMA_LORETO['temporada_seca']}\n\n{dato} 🦥")
        return (f"El clima en Loreto, mashi 🦥\n🌡️ {CLIMA_LORETO['temp_promedio']} · 💧 {CLIMA_LORETO['humedad']} · 🌧️ {CLIMA_LORETO['temporada_lluvias']} · ☀️ {CLIMA_LORETO['temporada_seca']}\n\n"
                f"{dato} Mejor época: {CLIMA_LORETO['mejor_epoca_visitar']}. ¿Algo más? 🦥🌿")

    # ── Recuperar último emprendedor mencionado ──
    last_ent_id = st.session_state.get("last_ent", None)
    last_ent = None
    if last_ent_id:
        for e in dataset:
            if e["id"] == last_ent_id:
                last_ent = e; break
    last_topic = st.session_state.get("last_topic", "")

    # ── MODO ECOTURISTA ──
    if mode == "Ecoturista":
        if any(w in ul for w in greetings) and not any(w in ul for w in price_q+where_q+reviews_q+demand_q+material_q):
            st.session_state["last_topic"] = "saludo"
            if L == "en":
                return random.choice([
                    f"{KICHWA['saludo']}! 🌿 I'm Mashi, your Amazon guide. Looking for textiles, natural soaps, or Shipibo pottery? Just tell me what you like! 🦥",
                    f"{KICHWA['saludo']}, mashi! 🦥 Welcome to MAPPED! Want to explore handcrafted Amazon products? Tell me what catches your eye! 🌿",
                ])
            if L == "qw":
                return random.choice([
                    f"{KICHWA['saludo']}! 🌿 Imashina kanki? Sachamanta alli rurata rikuchishayki. ¿Ima munanki? 🦥",
                    f"{KICHWA['saludo']}, mashi! 🌿 Shiringata, jabonkunata, shipibo kerámikata rikuchishayki. ¿Ima munanki? 🦥",
                ])
            return random.choice([
                f"{KICHWA['saludo']}! 🌿 Soy Mashi. ¿Qué artesanía buscas? Tenemos textiles de shiringa, jabones de Belén, y cerámica Shipibo. ¡Tú dime! 🦥",
                f"{KICHWA['saludo']}, mashi! 🌿 Bienvenido a MAPPED. ¿Buscas algo ecológico, cosmético natural o arte amazónico? Cuéntame. 🦥",
            ])

        if any(w in ul for w in fav_q):
            st.session_state["last_topic"] = "favoritos"
            favs = st.session_state.get("favorites", [])
            if not favs:
                return _L(
                    "Aún no tienes comunidades guardadas. Para guardar una, pregúntame por un lugar y toca ⭐ en los botones que aparecen.",
                    "No saved communities yet. Ask me about a community and tap ⭐ in the buttons that appear.",
                    "Manara allichashka llaktakuna kanchu. Maskay llaktata, sintita ⭐ tupanki.")
            noms = ",\n".join([next((e["name"] for e in dataset if e["id"] == fid), "?") for fid in favs])
            return _L(
                f"Tienes {len(favs)} comunidad(es) guardada(s):\n⭐ {noms}",
                f"You have {len(favs)} saved communities:\n⭐ {noms}",
                f"{len(favs)} allichashka llaktakuna kan:\n⭐ {noms}")

        if any(w in ul for w in farewells) or any(w in ul for w in thanks):
            st.session_state["last_topic"] = "farewell"
            if L == "en":
                return random.choice([
                    f"{KICHWA['gracias']}, mashi! {KICHWA['despedida']}! Come back anytime to discover more Amazon treasures! 🦥🌿",
                    f"Thank you, mashi! Every purchase supports local families. {KICHWA['despedida']}! 🦥✨",
                ])
            if L == "qw":
                return f"{KICHWA['gracias']}, mashi! {KICHWA['despedida']}! Sachamanta alli kawsay. 🦥🌿"
            return random.choice([
                f"{KICHWA['gracias']}, mashi! {KICHWA['despedida']}! Vuelve pronto a descubrir más tesoros amazónicos. 🦥🌿",
                f"¡{KICHWA['gracias']} por usar MAPPED! Cada compra apoya familias de la selva. {KICHWA['despedida']}! 🌟🦥",
            ])

        # Demanda / popularidad
        if any(w in ul for w in demand_q) and last_ent:
            st.session_state["last_topic"] = "demand"
            suggested, n_rev, years = _price_suggestion(last_ent)
            lvl = '🔥 Alta' if n_rev >= 3 else '📈 Media' if n_rev >= 1 else '🌱 En crecimiento'
            if L == "en":
                lvl_en = '🔥 High' if n_rev >= 3 else '📈 Medium' if n_rev >= 1 else '🌱 Growing'
                return f"**{last_ent['name']}**: {n_rev} reviews, {years} years. Suggested price: S/ {suggested:.1f}. Demand: {lvl_en}. Tourists love the authenticity! 🦥"
            if L == "qw":
                return f"**{last_ent['name']}**: {n_rev} riviskuna, {years} watakuna. Turiskunapa masna alli: S/ {suggested:.1f}. {'🔥 Achka' if n_rev >= 3 else '📈 Chawpi' if n_rev >= 1 else '🌱 Wiñay'} munana. 🦥"
            return f"**{last_ent['name']}**: {n_rev} reseñas, {years} años. Precio sugerido: S/ {suggested:.1f}. Demanda: {lvl}. ¡Muy popular entre turistas! 🦥"

        # Pregunta por precio con sugerencia
        if any(w in ul for w in price_q) and last_ent:
            st.session_state["last_topic"] = "price"
            suggested, n_rev, years = _price_suggestion(last_ent)
            prods_list = "\n".join([f"• **{p['name']}**: {p['currency']}{p['price']:.2f}" for p in last_ent["products"]])
            if L == "en":
                return (f"**{last_ent['name']}** prices:\n{prods_list}\n\n"
                        f"💡 Suggested for tourists: S/ {suggested:.1f} (fair trade, {n_rev} reviews, {years} years). Want to know more about any product? 🦥")
            if L == "qw":
                return (f"**{last_ent['name']}** masnapi:\n{prods_list}\n\n"
                        f"💡 Turiskunapa: S/ {suggested:.1f}. ¿Ashka munankichu? 🦥")
            return (f"**{last_ent['name']}** — precios:\n{prods_list}\n\n"
                    f"💡 Sugerido para turistas: S/ {suggested:.1f} (comercio justo, {n_rev} reseñas, {years} años). ¿Te interesa alguno? 🦥")

        if _is_route_query(ul) and last_ent:
            st.session_state["last_topic"] = "location"
            st.session_state["selected_ent_id"] = last_ent["id"]
            st.session_state["_focus_map_ent"] = last_ent["id"]
            st.session_state["show_mini_map"] = True
            addr = last_ent.get("address", last_ent.get("location",""))
            lat = last_ent.get("lat",""); lng = last_ent.get("lng","")
            u_lat = st.session_state.get("user_lat")
            u_lng = st.session_state.get("user_lng")
            u_name = st.session_state.get("user_loc_name", "")
            d = _dist_from_iquitos(last_ent)
            dist_dest = _format_distance(d) if d else ""
            # Calcular tiempos de viaje multi-modal
            dest_id = last_ent.get("id")
            river_info = COMMUNITY_RIVER_ACCESS.get(dest_id)
            travel_lines = ""
            car_km = d or 0; boat_km = 0
            if u_lat and u_lng:
                d_user = _haversine(u_lat, u_lng, float(lat), float(lng))
                dist_from_user = _format_distance(d_user) if d_user else ""
                dist_line = f"<b>{_L('Distancia desde ti','Distance from you','Kammanta karuta')}:</b> {dist_from_user}"
                origin_txt = f" desde {u_name}"
                # Calcular segmentos desde user
                if river_info:
                    port = RIVER_PORTS.get(river_info["port"])
                    if port:
                        car_km = _haversine(u_lat, u_lng, port["coords"][0], port["coords"][1])
                        boat_km = _haversine(port["coords"][0], port["coords"][1], float(lat), float(lng))
                    else:
                        car_km = d_user
                else:
                    car_km = d_user
            else:
                dist_line = f"<b>{_L('Distancia desde Iquitos','Distance from Iquitos','Iquitosmanta karuta')}:</b> {dist_dest}" if dist_dest else ""
                origin_txt = ""
                if river_info:
                    port = RIVER_PORTS.get(river_info["port"])
                    if port:
                        car_km = _haversine(-3.7491, -73.2442, port["coords"][0], port["coords"][1])
                        boat_km = _haversine(port["coords"][0], port["coords"][1], float(lat), float(lng))
                    else:
                        car_km = d or 0
            if river_info:
                car_time = _estimate_travel_time(car_km, "car")
                boat_time = _estimate_travel_time(boat_km, "boat")
                travel_lines = (f'🚗 {_format_distance(car_km)} ({car_time}) → 🅿️ Puerto → '
                                f'🛶 {_format_distance(boat_km)} ({boat_time})<br>'
                                f'<span style="font-size:0.75rem;color:rgba(148,163,184,0.5);">{_L("Carro + bote/canoa","Car + boat/canoe","Anta + bote")} · {river_info["label"]}</span>')
            else:
                car_time = _estimate_travel_time(car_km, "car")
                travel_lines = f'🚗 {_format_distance(car_km)} ({car_time})'
            log_notes = last_ent.get("logistics_notes", "")
            if L == "en":
                return (f'<div style="font-size:0.9rem;">'
                        f'Here is how to get to <b>{last_ent["name"]}</b>, mashi 🦥<br><br>'
                        f'📍 <b>Address:</b> {addr}<br>'
                        f'🏞️ <b>Zone:</b> {last_ent.get("zone","")}<br>'
                        f'{dist_line}<br>'
                        f'🚗 <b>Route:</b> {travel_lines}<br><br>'
                        f'💡 <i>{log_notes}</i><br><br>'
                        f'I left you a little map just below. '
                        f'Need anything else, friend? 🌿</div>')
            if L == "qw":
                return (f'<div style="font-size:0.9rem;">'
                        f'Allimi, mashi! <b>{last_ent["name"]}</b> kaypi tiyan 🦥<br><br>'
                        f'{addr}pi tiyan<br>'
                        f'{last_ent.get("zone","")}<br>'
                        f'{dist_dest} Iquitosmanta<br>'
                        f'{travel_lines}<br><br>'
                        f'{log_notes}<br><br>'
                        f'Mapapi ruta rikunki. ¿Imapish? 🌿</div>')
            return (f'<div style="font-size:0.9rem;">'
                    f'¡Claro, mashi! Aquí te cuento cómo llegar a <b>{last_ent["name"]}</b> 🦥<br><br>'
                    f'📍 <b>Dirección:</b> {addr}<br>'
                    f'🏞️ <b>Zona:</b> {last_ent.get("zone","")}<br>'
                    f'{dist_line}<br>'
                    f'🚗 <b>Ruta:</b> {travel_lines}<br><br>'
                    f'💡 <i>{log_notes}</i><br><br>'
                    f'Te dejé un mapita justo aquí abajo. '
                    f'¿Necesitas algo más, amigo? 🌿</div>')

        # ── RUTAS GENERALES (sin comunidad específica en contexto, pero quizás en el input) ──
        if any(w in ul for w in where_q) and not last_ent and not last_ent_id:
            st.session_state["last_topic"] = "location"
            # Intentar extraer nombre de comunidad del input
            found_ent = None
            for e in dataset:
                name_clean = e["name"].lower().strip()
                if name_clean in ul or (len(name_clean) > 5 and name_clean.split()[0] in ul):
                    found_ent = e
                    break
            if found_ent:
                st.session_state["last_ent"] = found_ent["id"]
                st.session_state["_msg_since_last_ent"] = 0
                last_ent = found_ent
                last_ent_id = found_ent["id"]
                # Ahora sí mostrar ruta específica + mapa
                st.session_state["selected_ent_id"] = found_ent["id"]
                st.session_state["_focus_map_ent"] = found_ent["id"]
                st.session_state["show_mini_map"] = True
                addr = found_ent.get("address", found_ent.get("location",""))
                lat = found_ent.get("lat",""); lng = found_ent.get("lng","")
                u_lat = st.session_state.get("user_lat")
                u_lng = st.session_state.get("user_lng")
                d = _dist_from_iquitos(found_ent)
                dist_dest = _format_distance(d) if d else ""
                dest_id = found_ent.get("id")
                river_info = COMMUNITY_RIVER_ACCESS.get(dest_id)
                travel_lines = ""
                car_km = d or 0; boat_km = 0
                if u_lat and u_lng:
                    d_user = _haversine(u_lat, u_lng, float(lat), float(lng))
                    dist_from_user = _format_distance(d_user) if d_user else ""
                    dist_line = f"<b>{_L('Distancia desde ti','Distance from you','Kammanta karuta')}:</b> {dist_from_user}"
                    origin_txt = f" desde tu ubicación"
                    if river_info:
                        port = RIVER_PORTS.get(river_info["port"])
                        if port:
                            car_km = _haversine(u_lat, u_lng, port["coords"][0], port["coords"][1])
                            boat_km = _haversine(port["coords"][0], port["coords"][1], float(lat), float(lng))
                        else:
                            car_km = d_user
                    else:
                        car_km = d_user
                else:
                    dist_line = f"<b>{_L('Distancia desde Iquitos','Distance from Iquitos','Iquitosmanta karuta')}:</b> {dist_dest}" if dist_dest else ""
                    origin_txt = ""
                    if river_info:
                        port = RIVER_PORTS.get(river_info["port"])
                        if port:
                            car_km = _haversine(-3.7491, -73.2442, port["coords"][0], port["coords"][1])
                            boat_km = _haversine(port["coords"][0], port["coords"][1], float(lat), float(lng))
                        else:
                            car_km = d or 0
                if river_info:
                    car_time = _estimate_travel_time(car_km, "car")
                    boat_time = _estimate_travel_time(boat_km, "boat")
                    travel_lines = (f'🚗 {_format_distance(car_km)} ({car_time}) → 🅿️ Puerto → '
                                    f'🛶 {_format_distance(boat_km)} ({boat_time})<br>'
                                    f'<span style="font-size:0.75rem;color:rgba(148,163,184,0.5);">{_L("Carro + bote/canoa","Car + boat/canoe","Anta + bote")} · {river_info["label"]}</span>')
                else:
                    car_time = _estimate_travel_time(car_km, "car")
                    travel_lines = f'🚗 {_format_distance(car_km)} ({car_time})'
                log_notes = found_ent.get("logistics_notes", "")
                if L == "en":
                    return (f'<div style="font-size:0.9rem;">'
                            f'Claro, mashi! Here is how to get to <b>{found_ent["name"]}</b> 🦥<br><br>'
                            f'📍 <b>Address:</b> {addr}<br>'
                            f'🏞️ <b>Zone:</b> {found_ent.get("zone","")}<br>'
                            f'{dist_line}<br>'
                            f'🚗 <b>Route:</b> {travel_lines}<br><br>'
                            f'💡 <i>{log_notes}</i><br><br>'
                            f'I left you a little map just below with the route. '
                            f'Need anything else, friend? 🌿</div>')
                if L == "qw":
                    return (f'<div style="font-size:0.9rem;">'
                            f'Allimi, mashi! <b>{found_ent["name"]}</b> kaypim tiyan 🦥<br><br>'
                            f'{addr}pi tiyan<br>'
                            f'{found_ent.get("zone","")}<br>'
                            f'{dist_dest} Iquitosmanta<br>'
                            f'{travel_lines}<br><br>'
                            f'{log_notes}<br><br>'
                            f'Mapapi ruta rikunki. ¿Imapish? 🌿</div>')
                return (f'<div style="font-size:0.9rem;">'
                        f'¡Claro, mashi! Aquí te cuento cómo llegar a <b>{found_ent["name"]}</b> 🦥<br><br>'
                        f'📍 <b>Dirección:</b> {addr}<br>'
                        f'🏞️ <b>Zona:</b> {found_ent.get("zone","")}<br>'
                        f'{dist_line}<br>'
                        f'🚗 <b>Ruta:</b> {travel_lines}<br><br>'
                        f'💡 <i>{log_notes}</i><br><br>'
                        f'Te dejé un mapita justo aquí abajo con la ruta. '
                        f'¿Necesitas algo más, amigo? 🌿</div>')
            nearest = _nearest_communities(dataset, n=5)
            if not nearest:
                if L == "en":
                    return "There are no communities with location data yet, mashi. Check back soon! 🦥"
                return "Todavía no hay comunidades con datos de ubicación, mashi. ¡Vuelve pronto! 🦥"
            lines = []
            for i, (d_km, e) in enumerate(nearest, 1):
                icon = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "• "
                log = e.get("logistics_notes", "")
                log = " — " + log[:50] + ("…" if len(log) > 50 else "") if log else ""
                name = e["name"][:45] + ("…" if len(e["name"]) > 45 else "")
                lines.append(f"{icon} **{name}** — {_format_distance(d_km)}{log}")
            ranking = "\n".join(lines)
            if L == "en":
                return (f"🗺️ **Communities near Iquitos (sorted by distance):**\n\n"
                        f"{ranking}\n\n"
                        f"💡 **Tip:** The ones at the top are closest. "
                        f"Tell me which one you're interested in and I will give you exact directions! 🦥")
            if L == "qw":
                return (f"🗺️ **Iquitosman kaylla llaktakuna:**\n\n"
                        f"{ranking}\n\n"
                        f"💡 Kaylla ruraqkunata rikunki. ¿Mayta munanki? 🦥")
            return (f"🗺️ **Comunidades más cercanas a Iquitos:**\n\n"
                    f"{ranking}\n\n"
                    f"💡 Las que están arriba son las más cercanas. "
                    f"Dime cuál te interesa y te doy la dirección exacta y cómo llegar 🦥")

        if any(w in ul for w in reviews_q) and last_ent:
            st.session_state["last_topic"] = "reviews"
            avg = round(sum(r["stars"] for r in last_ent["reviews"])/len(last_ent["reviews"]),1) if last_ent["reviews"] else "—"
            stars_display = "★" * round(avg) + "☆" * (5 - round(avg))
            reviews_text = "\n".join([f"• {'★'*r['stars']} **{r['user']}**: \"{r['text']}\"" for r in last_ent["reviews"]])
            if L == "en":
                return f"**{last_ent['name']}** — {stars_display} {avg}/5 ({len(last_ent['reviews'])} reviews)\n\n{reviews_text}\n\nWant prices or location? 🦥"
            if L == "qw":
                return f"**{last_ent['name']}** {stars_display} {avg}/5 ({len(last_ent['reviews'])} riviskuna)\n\n{reviews_text}\n\n¿Ashka munankichu? 🦥"
            return f"**{last_ent['name']}** — {stars_display} {avg}/5 ({len(last_ent['reviews'])} reseñas)\n\n{reviews_text}\n\n¿Quieres ver precios o cómo llegar? 🦥"

        if any(w in ul for w in material_q) and last_ent:
            st.session_state["last_topic"] = "materials"
            mat = last_ent.get("materials", "Materiales nativos de la Amazonía")
            if L == "en":
                return f"**{last_ent['name']}** uses: **{mat}** — sustainably sourced from the Amazon, preserving ancestral techniques. Want prices or more products? 🦥"
            if L == "qw":
                return f"**{last_ent['name']}** ruran: **{mat}**. Sachamanta alli rurashka. ¿Ashka munankichu? 🦥"
            return f"**{last_ent['name']}** utiliza: **{mat}** — materiales sostenibles de la Amazonía, técnicas ancestrales. ¿Precios o más productos? 🦥"

        if any(w in ul for w in more_q) and last_ent:
            st.session_state["last_topic"] = "more"
            prods = "\n".join([f"• **{p['name']}** — {p['currency']}{p['price']:.2f}" for p in last_ent["products"]])
            if L == "en":
                return (f"**{last_ent['name']}**:\n📦 {prods}\n📖 {last_ent['description'][:120]}\n\nWant prices, reviews or directions? 🦥")
            if L == "qw":
                return (f"**{last_ent['name']}**:\n{prods}\n{last_ent['description'][:100]}\n\n¿Ashka munankichu? 🦥")
            return (f"**{last_ent['name']}**:\n📦 {prods}\n📖 {last_ent['description'][:120]}\n📍 {last_ent['location']}\n\n¿Precios, reseñas o ubicación? 🦥")

        # ── COMPRA / PURCHASE ──
        if any(w in ul for w in buy_q):
            if last_ent or last_ent_id:
                target = last_ent
                if not target:
                    for e in dataset:
                        if e["id"] == last_ent_id: target = e; break
                if target:
                    prod = random.choice(target["products"])
                    purch = {"user":st.session_state.get("user_name","Turista"),"product":prod["name"],
                             "price":prod["price"],"ent_name":target["name"],"ent_id":target["id"]}
                    st.session_state.setdefault("purchases",[]).append(purch)
                    st.session_state["last_topic"] = "purchase"
                    if L == "en":
                        return f"🎉 **Purchase registered!** Thank you for supporting **{target['name']}**! You chose **{prod['name']}** ({prod['currency']}{prod['price']:.2f}). Want directions or to see more? 🦥"
                    if L == "qw":
                        return f"🎉 **Rura rantishka!** Añay **{target['name']}**. **{prod['name']}** — {prod['currency']}{prod['price']:.2f}. ¿Ashka munankichu? 🦥"
                    return f"🎉 **¡Compra registrada!** Gracias por apoyar a **{target['name']}**. Elegiste **{prod['name']}** — {prod['currency']}{prod['price']:.2f}. ¿Direcciones o más productos? 🦥"
            else:
                if L == "en":
                    return f"¡Oh, mashi! 🦥 I haven't recommended anything yet. Tell me what you like: textiles, soaps, or pottery? 🌿"
                if L == "qw":
                    return f"¡Mashi! 🦥 Manara rurata rikuchishkanichu. ¿Ima munanki? Sachamanta? 🌿"
                return (f"¡Oh, mashi! 🦥 Quieres comprar pero aún no te he recomendado "
                        f"un producto. Déjame mostrarte primero lo que tenemos.\n\n"
                        f"Dime qué buscas: ¿textiles ecológicos, jabones naturales, "
                        f"o cerámica Shipibo? 🌿")

        best = _best_match(user_input, dataset)
        if best:
            st.session_state["last_ent"] = best["id"]
            st.session_state["_msg_since_last_ent"] = 0
            st.session_state["last_topic"] = "recommendation"
            ent, prod, avg, review = _format_product(best)
            suggested, n_rev, years = _price_suggestion(best)
            best_prod = (best.get("products") or [{}])[0]
            img = _get_product_image(best, best_prod, "160px")
            contact_info = f"<br>{_L('Contacto','Contact','Tapuy')}: {best.get('contact','—')}" if best.get("contact") else ""
            if L == "en":
                return (f'{img}'
                        f'<b>{ent["name"]}</b><br><br>'
                        f'✨ <b>{prod["name"]}</b> — {prod["currency"]}{prod["price"]:.2f}<br>'
                        f'💡 Suggested: S/ {suggested:.1f} · ★ {avg}/5 · {years} years<br>'
                        f'📍 {ent["location"]}{contact_info}<br><br>'
                        f'Want prices, reviews or directions? 🦥')
            if L == "qw":
                return (f'{img}'
                        f'<b>{ent["name"]}</b> sumakmi.<br>'
                        f'✨ <b>{prod["name"]}</b> — {prod["currency"]}{prod["price"]:.2f}<br>'
                        f'🏆 {years} watakuna · ★ {avg}/5 · {ent["location"]}{contact_info}<br><br>'
                        f'¿Ashka munankichu? 🦥')
            return (f'{img}'
                    f'<b>{ent["name"]}</b><br><br>'
                    f'✨ <b>{prod["name"]}</b> — {prod["currency"]}{prod["price"]:.2f}<br>'
                    f'   {prod["description"][:80]}<br>'
                    f'💡 Precio sugerido: S/ {suggested:.1f} · ★ {avg}/5 · {years} años<br>'
                    f'📍 {ent["location"]}{contact_info}<br><br>'
                    f'¿Quieres precios, reseñas o cómo llegar? 🦥')

        last_topic = st.session_state.get("last_topic", "")
        last_ent_id = st.session_state.get("last_ent")
        if last_topic and last_topic != "default":
            st.session_state["last_topic"] = "default"
            topic_prompts = {
                "saludo": _L("Cuéntame, ¿qué tipo de artesanía buscas?","So, what kind of crafts are you looking for?","¿Ima rurata maskanki?"),
                "weather": _L("¿Te gustaría saber cómo el clima afecta los productos artesanales?","Want to know how weather affects the crafts?","¿Rurata cliamanta rikunki?"),
                "price": _L("¿Necesitas más detalles de precios o reseñas?","Need more price details or reviews?","¿Ashka masnata munankichu?"),
                "location": _L("¿Quieres saber cómo llegar a alguna comunidad en específico?","Want directions to a specific community?","¿Maypi tiyan?"),
                "reviews": _L("¿Quieres ver los productos de esa comunidad?","Want to see that community's products?","¿Rurakunata rikunki?"),
                "materials": _L("¿Te gustaría conocer los precios?","Would you like to know the prices?","¿Masnata munankichu?"),
                "demand": _L("¿Quieres comparar con otras comunidades?","Want to compare with other communities?","¿Shuk llaktakunawa tinkuchinki?"),
                "purchase": _L("¿Quieres explorar más comunidades o ver tu carrito?","Want to explore more communities or check your cart?","¿Ashka llaktakunata rikunki?"),
            }
            prompt = topic_prompts.get(last_topic, _L("¿En qué más puedo ayudarte?","What else can I help you with?","¿Imata yanapay?"))
            if L == "en":
                return f"{KICHWA['saludo']}, mashi! 🌿 {prompt} 🦥"
            if L == "qw":
                return f"{KICHWA['saludo']}, mashi! 🦥 {prompt} 🌿"
            return f"{KICHWA['saludo']}, mashi! 🦥 {prompt} 🌿"
        st.session_state["last_topic"] = "default"
        if L == "en":
            return f"{KICHWA['saludo']}, mashi! 🌿 Welcome! We have Shiringa eco-textiles, Belén natural soaps, and Shipibo pottery. What catches your eye? 🦥"
        if L == "qw":
            return f"{KICHWA['saludo']}, mashi! 🌿 Kay MAPPEDpi shiringa, jabonkuna, shipibo kerámika tiyan. ¿Ima munanki? 🦥"
        return f"{KICHWA['saludo']}, mashi! 🌿 En MAPPED tenemos shiringa, jabones de Belén y cerámica Shipibo. ¿Qué te gusta más? 🦥"

    # ── MODO EMPRENDEDOR LOCAL ──
    if mode == "Emprendedor Local":
        if any(w in ul for w in greetings):
            st.session_state["last_topic"] = "saludo"
            if L == "en":
                return random.choice([
                    f"{KICHWA['saludo']}, mashi artisan! 🌿 Welcome to MAPPED! Tell me about your craft — what do you create? 🦥",
                    f"{KICHWA['saludo']}! 🦥 Ready to share your talent with the world? Register your product below and reach tourists globally! 🌿",
                ])
            if L == "qw":
                return random.choice([
                    f"{KICHWA['saludo']}, mashi ruraq! 🌿 ¿Imata ruranki? Sachamanta alli rurakunata MAPPEDpi churanki. 🦥",
                    f"¡{KICHWA['saludo']}! 🦥 Kaypi rurata churay. Turiskuna rikushun. ¿Yanapayta munankichu?",
                ])
            return random.choice([
                f"{KICHWA['saludo']}, mashi artesano! 🌿 ¿Qué productos elaboras? ¿Shiringa, arcilla, aceites? Usa el formulario y comparte tu talento. 🦥",
                f"¡{KICHWA['saludo']}! 🦥 ¿Listo para mostrar tus creaciones? Registra tu producto abajo. ¡Es sencillo! 🌿",
            ])
        if any(w in ul for w in thanks):
            if L == "en":
                return f"{KICHWA['gracias']}, mashi! Your work keeps Amazonian culture alive. 🦥✨"
            if L == "qw":
                return f"{KICHWA['gracias']}, mashi! Kushi kawsaymi. 🦥✨"
            return f"¡{KICHWA['gracias']}, mashi artesano! Tu trabajo mantiene viva la cultura amazónica. 🦥✨"
        # ── Precio / precio justo / cuanto vender ──
        if any(w in ul for w in price_q + ["sugiere","recomienda","cuánto debería","cuanto","recomendado","fair price","justo"]):
            suggested, avg_market, demand_level, n_similar, min_p, max_p, trend, confidence, insight = _suggest_price_for_product(user_input, user_input, dataset)
            demand_icon = "🔥" if demand_level == "alta" else "📈" if demand_level == "media" else "🌱"
            demand_lbl = _L({"alta":"Alta","media":"Media","baja":"Baja"}[demand_level],
                            {"alta":"High","media":"Medium","baja":"Low"}[demand_level],
                            {"alta":"Achka","media":"Chawpi","baja":"Aslla"}[demand_level])
            conf_lbl = _L({"alta":"alto","media":"medio","baja":"bajo"}[confidence],
                          {"alta":"high","media":"medium","baja":"low"}[confidence],
                          {"alta":"achka","media":"chawpi","baja":"aslla"}[confidence])
            if L == "en":
                return (f"Great question, mashi artisan! 🦥 Let me analyze the market for you.\n\n"
                        f"📊 **Market analysis** (confidence: {conf_lbl})\n"
                        f"• Price range: **S/ {min_p:.2f} – S/ {max_p:.2f}**\n"
                        f"• Market average: **S/ {avg_market:.2f}**\n"
                        f"• **Mashi suggests: S/ {suggested:.2f}** {trend}\n"
                        f"• Demand: {demand_icon} **{demand_lbl}**{insight}\n\n"
                        + ({
                            "alta": "🔥 **High demand!** Products like yours are popular with tourists. You can set a price that reflects cultural value and quality craftsmanship.",
                            "media": "📈 **Medium demand.** Steady market. Price competitively and highlight your unique story to stand out.",
                            "baja": "🌱 **Growing demand.** Start with an accessible price to attract first buyers. Adjust upward once you have reviews!"
                        }[demand_level])
                        + f"\n\n📱 Want to connect directly with buyers? We can share your product on WhatsApp too! 🦥✨\n\nFair trade means you set the price. I guide you with data.")
            if L == "qw":
                return (f"¡Ari, mashi! 📊 {n_similar} shuk rurakunawa rikushpa:\n\n"
                        f"• S/ {min_p:.2f} manta S/ {max_p:.2f} kama\n"
                        f"• Chawpi chanin: S/ {avg_market:.2f}\n"
                        f"• Mashi nispa: **S/ {suggested:.2f}** {trend}\n"
                        f"• Munay: {demand_icon} **{demand_lbl}**\n\n"
                        f"📱 WhatsApppi turiskunawan rimanakuy! 🦥")
            return (f"¡Excelente pregunta, mashi artesano! 🦥 Déjame analizar el mercado.\n\n"
                    f"📊 **Análisis de mercado** (confianza: {conf_lbl})\n"
                    f"• Rango de precios: **S/ {min_p:.2f} – S/ {max_p:.2f}**\n"
                    f"• Precio promedio: **S/ {avg_market:.2f}**\n"
                    f"• **Mashi sugiere: S/ {suggested:.2f}** {trend}\n"
                    f"• Demanda: {demand_icon} **{demand_lbl}**{insight}\n\n"
                    + ({
                        "alta": "🔥 **¡Demanda alta!** Productos como el tuyo son muy buscados. Puedes fijar un precio que refleje el valor cultural y la calidad artesanal. ¡Los viajeros pagan más por autenticidad!",
                        "media": "📈 **Demanda media.** Mercado estable. Precio competitivo y destaca tu historia única para diferenciarte.",
                        "baja": "🌱 **Demanda en crecimiento.** Empieza con un precio accesible para atraer primeros compradores. ¡Cuando tengas reseñas, ajusta!"
                    }[demand_level])
                    + f"\n\n📱 ¿Quieres que los turistas te contacten directo? Activa la opción de WhatsApp en tu perfil y recibe pedidos al instante. 🦥✨\n\nRecuerda: tú pones el precio, yo solo guío con datos del mercado.")

        if any(w in ul for w in ["formulario","producto","publicar","registrar","subir","cómo","como","ayuda","ayudame","paso","steps","help","guide"]):
            if L == "en":
                return (f"Of course, mashi! Here's how to publish your product:\n\n"
                        f"**1️⃣** Give your product a nice name\n"
                        f"**2️⃣** Describe what it's made of and what it's for\n"
                        f"**3️⃣** Tell us your story (who taught you? what does it mean?)\n"
                        f"**4️⃣** Upload a photo (optional, but helps a lot!)\n"
                        f"**5️⃣** Click 'Publish on MAPPED'\n\n"
                        f"And that's it! Your product will reach travelers from all over the world. 🌟\n\n"
                        f"Your culture is valuable — share it with pride! 🦥")
            if L == "qw":
                return (f"¡Ari, mashi! Kaypi ruray:\n\n"
                        f"**1️⃣** Alli sutita churay\n"
                        f"**2️⃣** Imamanta rurashkata willay\n"
                        f"**3️⃣** Kikin willayta churay\n"
                        f"**4️⃣** Rikchata apay (mana obligatorio)\n"
                        f"**5️⃣** 'MAPPEDpi churay' nispa\n\n"
                        f"¡Listo! Turiskuna rikushun. 🦥")
            return (f"¡Claro, mashi! Es muy sencillo publicar tu producto en MAPPED. "
                    f"Sigue estos pasos:\n\n"
                    f"**1️⃣** Ponle un nombre bonito a tu producto\n"
                    f"**2️⃣** Describe de qué material está hecho y para qué sirve\n"
                    f"**3️⃣** Cuéntanos tu historia (¿quién te enseñó el oficio? ¿qué significa para tu comunidad?)\n"
                    f"**4️⃣** Sube una foto (es opcional, ¡pero ayuda mucho a que los turistas se enamoren!)\n"
                    f"**5️⃣** Haz clic en 'Publicar en MAPPED'\n\n"
                    f"¡Y listo, mashi! 🌟 Tu producto llegará a viajeros de todo el mundo "
                    f"que buscan experiencias auténticas. ¿Ves qué fácil? "
                    f"¡Tu cultura es valiosa y merece ser compartida! 🦥✨")
        st.session_state["last_topic"] = "default"
        if L == "en":
            return (f"{KICHWA['saludo']}, mashi artisan! 🌿 How can I help you today? "
                    f"You can register a product using the form below, or ask me "
                    f"anything about the platform. I'm here to support you! "
                    f"Remember: your crafts are treasures of the Amazon. 🦥")
        if L == "qw":
            return (f"{KICHWA['saludo']}, mashi ruraq! 🌿 ¿Imata munanki? "
                    f"Kaypi rurata churay. ¡Ñukaka kaypimi! 🦥")
        return (f"{KICHWA['saludo']}, mashi artesano! 🌿 ¿En qué puedo ayudarte hoy? "
                f"Puedes registrar un producto en el formulario de abajo. "
                f"Recuerda: tus creaciones son tesoros de la Amazonía que el mundo "
                f"merece conocer. ¡Cuéntame si tienes dudas! 🦥✨")

    # ── MODO INVERSIONISTA ──
    st.session_state["last_topic"] = "default"
    
    # ── Palabras clave específicas de inversión ──
    roi_q = ["roi","retorno","rentabilidad","beneficio","ganancia","profit","return","payback","recuperación","recuperacion"]
    invest_q = ["invertir","inversión","inversion","invierto","inversor","dónde invertir","donde invertir","mejor inversion","best investment","capital","invert"]
    sector_q = ["sector","industria","rubro","categoría","categoria","textil","cosmético","cerámica","turismo","alimento","madera","medicina","música","arte","sector más","que sector","qué sector","cual sector"]
    logistics_q = ["logística","logistica","acceso","transporte","llegar","distancia","ubicación","ubicacion","lejos","cerca","rio","carretera","logistics","access","transport"]
    compare_q = ["comparar","comparación","comparacion","vs","versus","diferencia","mejor","peor","ranking","top","cúal es mejor","cual es mejor","compared"]
    market_q = ["mercado","demanda","tendencia","crecimiento","proyección","proyeccion","crece","creciendo","market","trend","growth","potencial"]
    
    # ── Análisis de ROI/retorno ──
    if any(w in ul for w in roi_q):
        st.session_state["last_topic"] = "roi"
        best_invest = max(dataset, key=lambda e: len(e["reviews"]) * len(e["products"]) + (int(e["years_selling"]) if str(e["years_selling"]).isdigit() else 0))
        best_avg = round(sum(r["stars"] for r in best_invest["reviews"])/len(best_invest["reviews"]),1) if best_invest["reviews"] else "—"
        best_yrs = best_invest["years_selling"]
        best_prods = len(best_invest["products"])
        best_revs = len(best_invest["reviews"])
        # Simular proyección
        proj_rev = best_revs * best_prods * 15
        payback_est = max(6, min(24, 18 - best_revs - best_prods))
        if L == "en":
            return (f"📊 **Investment Analysis — MAPPED Communities**\n\n"
                    f"**Top pick: {best_invest['name']}**\n"
                    f"• Sector: {best_invest['sector']}\n"
                    f"• Track record: {best_yrs} years\n"
                    f"• Rating: ★ {best_avg}/5 ({best_revs} reviews)\n"
                    f"• Products: {best_prods}\n"
                    f"• Est. annual revenue: **S/ {proj_rev:,.0f}**\n"
                    f"• Est. payback: **{payback_est} months**\n\n"
                    f"{'🟢 Low risk' if payback_est <= 12 else '🟡 Medium risk' if payback_est <= 18 else '🟠 Higher risk'} — "
                    f"{'Strongly recommend completing company verification for detailed ROI projections.' if payback_est <= 12 else 'Consider verifying RUC for full analytics dashboard.'}\n\n"
                    f"All {len(dataset)} communities evaluated. The ROI potential ranges from **6 to 24 months** depending on sector and scale. 📊🦥")
        if L == "qw":
            return (f"📊 **Qolqe yupay — MAPPED**\n\n"
                    f"**Allin: {best_invest['name']}**\n"
                    f"• Sektor: {best_invest['sector']}\n"
                    f"• {best_yrs} watakuna\n"
                    f"• ★ {best_avg}/5 ({best_revs} rivis)\n"
                    f"• Wata qolqe: S/ {proj_rev:,.0f}\n"
                    f"• Kutimuy: {payback_est} killa\n\n"
                    f"RUCta churay ashka yupaykunata rikunkapa. 📊🦥")
        return (f"📊 **Análisis de Inversión — Comunidades MAPPED**\n\n"
                f"**Mejor opción: {best_invest['name']}**\n"
                f"• Sector: {best_invest['sector']}\n"
                f"• Trayectoria: {best_yrs} años\n"
                f"• Valoración: ★ {best_avg}/5 ({best_revs} reseñas)\n"
                f"• Productos registrados: {best_prods}\n"
                f"• Ingreso anual estimado: **S/ {proj_rev:,.0f}**\n"
                f"• Payback estimado: **{payback_est} meses**\n\n"
                f"{'🟢 Riesgo bajo' if payback_est <= 12 else '🟡 Riesgo medio' if payback_est <= 18 else '🟠 Riesgo mayor'} — "
                f"{'Esta comunidad tiene excelente potencial. Recomiendo completar la verificación empresarial para ver proyecciones detalladas.' if payback_est <= 12 else 'Te recomiendo verificar tu RUC para acceder al dashboard completo con pronósticos a 12 meses.'}\n\n"
                f"Las {len(dataset)} comunidades evaluadas ofrecen un rango de retorno de inversión de **6 a 24 meses**, "
                f"dependiendo del sector, la demanda actual y la escala de inversión. "
                f"¿Quieres que analice algún sector o comunidad en específico? 📊🦥")
    
    # ── Recomendación de inversión ──
    if any(w in ul for w in invest_q):
        st.session_state["last_topic"] = "recommend_invest"
        scored = []
        for e in dataset:
            s = len(e["reviews"]) * 10 + len(e["products"]) * 5 + (int(e["years_selling"]) if str(e["years_selling"]).isdigit() else 0)
            avg = round(sum(r["stars"] for r in e["reviews"])/len(e["reviews"]),1) if e["reviews"] else 0
            s += int(avg * 8)
            scored.append((s, e))
        scored.sort(reverse=True, key=lambda x: x[0])
        top3 = scored[:3]
        lines = []
        for s, e in top3:
            avg = round(sum(r["stars"] for r in e["reviews"])/len(e["reviews"]),1) if e["reviews"] else "—"
            yrs = e["years_selling"]
            lines.append(f"**{e['name']}** — {e['sector']} | ★ {avg} | {yrs} años | {len(e['reviews'])} reseñas | {len(e['products'])} productos")
        if L == "en":
            return (f"🦥 **Mashi's Investment Recommendations**\n\n"
                    f"Based on my analysis of all {len(dataset)} communities, here are my top 3 picks:\n\n"
                    + "\n".join([f"{i+1}. {l}" for i, l in enumerate(lines)])
                    + "\n\n💡 **Key factors:** review count, product variety, years of experience, and customer satisfaction.\n\n"
                    "Would you like me to do a deeper analysis on any of these? Or compare specific sectors? 📊🦥")
        if L == "qw":
            return ("Kay allin llaktakuna qolqe churaypaq:\n\n"
                    + "\n".join([f"{i+1}. {l}" for i, l in enumerate(lines)])
                    + "\n\n¿Ashka munankichu, mashi? 📊")
        return (f"🦥 **Recomendaciones de Inversión de Mashi**\n\n"
                f"Basado en mi análisis de las {len(dataset)} comunidades registradas, "
                f"estas son mis **3 mejores opciones** para invertir:\n\n"
                + "\n".join([f"{i+1}. {l}" for i, l in enumerate(lines)])
                + "\n\n💡 **Factores considerados:** cantidad de reseñas positivas, variedad de productos, "
                "años de trayectoria, valoración de turistas y accesibilidad logística.\n\n"
                "¿Quieres que analice alguna de estas a profundidad? ¿O prefieres comparar por sector?\n\n"
                "Recuerda: completa la verificación de tu empresa (RUC, DNI) para acceder "
                "al análisis completo con ROI Calculator y proyecciones. 📊🦥")
    
    # ── Análisis por sector ──
    if any(w in ul for w in sector_q):
        st.session_state["last_topic"] = "sector_analysis"
        by_sector = {}
        for e in dataset:
            sec = e["sector"]
            by_sector.setdefault(sec, []).append(e)
        lines = []
        for sec, ents in sorted(by_sector.items(), key=lambda x: len(x[1]), reverse=True):
            total_revs = sum(len(e["reviews"]) for e in ents)
            total_prods = sum(len(e["products"]) for e in ents)
            avg_rating = round(sum(sum(r["stars"] for r in e["reviews"]) for e in ents if e["reviews"]) / max(total_revs, 1), 1)
            lines.append(f"• **{sec}** — {len(ents)} comunidades | ★ {avg_rating} | {total_prods} productos | {total_revs} reseñas")
        best_sec = max(by_sector.items(), key=lambda x: sum(len(e["reviews"]) for e in x[1]))
        if L == "en":
            return (f"📊 **Market Analysis by Sector**\n\n"
                    + "\n".join(lines)
                    + f"\n\n🔥 **Hottest sector: {best_sec[0]}** — {len(best_sec[1])} communities, "
                    f"{sum(len(e['reviews']) for e in best_sec[1])} reviews in total.\n\n"
                    f"This sector shows the strongest market demand and tourist interest. "
                    f"Would you like to see the top communities in this sector? 📊🦥")
        if L == "qw":
            return ("📊 **Sektor yupay**\n\n" + "\n".join(lines)
                    + f"\n\n🔥 **Allin sektor: {best_sec[0]}** — {len(best_sec[1])} llakta. 📊")
        return (f"📊 **Análisis de Mercado por Sector**\n\n"
                + "\n".join(lines)
                + f"\n\n🔥 **Sector con mayor demanda: {best_sec[0]}** — {len(best_sec[1])} comunidades, "
                f"{sum(len(e['reviews']) for e in best_sec[1])} reseñas en total.\n\n"
                f"Este sector presenta el mayor interés turístico y potencial de crecimiento. "
                f"¿Quieres ver las comunidades top dentro de este sector? 📊🦥")
    
    # ── Análisis logístico ──
    if any(w in ul for w in logistics_q):
        st.session_state["last_topic"] = "logistics"
        accessible = [e for e in dataset if len(e.get("logistics_notes","")) < 50 or any(w in e.get("logistics_notes","").lower() for w in ["carretera","fácil","facil","iquitos","acceso directo"])]
        remote = [e for e in dataset if any(w in e.get("logistics_notes","").lower() for w in ["fluvial","bote","rio","río","coordin"])]
        if L == "en":
            return (f"📍 **Logistics Analysis — MAPPED Communities**\n\n"
                    f"**Easily accessible ({len(accessible)}):**\n"
                    + "\n".join([f"• ✅ **{e['name'][:40]}** — {e.get('logistics_notes','N/A')}" for e in accessible[:4]])
                    + f"\n\n**River access ({len(remote)}):**\n"
                    + "\n".join([f"• 🛶 **{e['name'][:40]}** — {e.get('logistics_notes','N/A')}" for e in remote[:4]])
                    + "\n\n💡 The Amazon has two main seasons: **dry (Jun-Oct)** for easier river travel, "
                    "and **rainy (Nov-May)** when rivers are higher but roads can be tricky.\n\n"
                    "Would you like specific coordinates or route planning for any community? 📊🦥")
        if L == "qw":
            return (f"📍 **Logistika — MAPPED**\n\n"
                    + "\n".join([f"• ✅ **{e['name'][:35]}** — {e.get('logistics_notes','N/A')}" for e in accessible[:3]])
                    + "\n\n" + "\n".join([f"• 🛶 **{e['name'][:35]}** — {e.get('logistics_notes','N/A')}" for e in remote[:3]])
                    + "\n\n¿Ashka munankichu? 📊")
        return (f"📍 **Análisis Logístico — Comunidades MAPPED**\n\n"
                f"**Acceso directo ({len(accessible)}):**\n"
                + "\n".join([f"• ✅ **{e['name'][:45]}** — {e.get('logistics_notes','N/A')}" for e in accessible[:4]])
                + f"\n\n**Acceso fluvial ({len(remote)}):**\n"
                + "\n".join([f"• 🛶 **{e['name'][:45]}** — {e.get('logistics_notes','N/A')}" for e in remote[:4]])
                + "\n\n💡 **Dato importante:** La Amazonía tiene dos temporadas. En **época seca (jun-oct)** "
                "los ríos están más bajos y el acceso por carretera es más predecible. "
                "En **época de lluvias (nov-may)** los ríos crecen, permitiendo llegar a comunidades "
                "que en sequía son inaccesibles, pero las carreteras pueden complicarse.\n\n"
                "¿Quieres las coordenadas exactas o una ruta planificada para alguna comunidad en específico? 📊🦥")
    
    # ── Comparativa ──
    if any(w in ul for w in compare_q):
        st.session_state["last_topic"] = "compare"
        sorted_by_rating = sorted(dataset, key=lambda e: sum(r["stars"] for r in e["reviews"])/max(len(e["reviews"]),1) if e["reviews"] else 0, reverse=True)
        sorted_by_demand = sorted(dataset, key=lambda e: len(e["reviews"]), reverse=True)
        sorted_by_exp = sorted(dataset, key=lambda e: int(e["years_selling"]) if str(e["years_selling"]).isdigit() else 0, reverse=True)
        top_rated = sorted_by_rating[0]
        top_demanded = sorted_by_demand[0]
        top_exp = sorted_by_exp[0]
        if L == "en":
            return (f"📊 **Community Comparison — MAPPED**\n\n"
                    f"🏆 **Highest rated:** {top_rated['name']} — "
                    f"★ {round(sum(r['stars'] for r in top_rated['reviews'])/len(top_rated['reviews']),1)}/5\n"
                    f"🔥 **Most demanded:** {top_demanded['name']} — {len(top_demanded['reviews'])} reviews\n"
                    f"⏳ **Most experienced:** {top_exp['name']} — {top_exp['years_selling']} years\n\n"
                    f"Would you like a detailed comparison between specific communities? "
                    f"Just tell me which ones to compare! 📊🦥")
        if L == "qw":
            return (f"📊 **Llaktakuna tinkuchiy**\n\n"
                    f"🏆 **Allin:** {top_rated['name'][:40]} — ★ {round(sum(r['stars'] for r in top_rated['reviews'])/len(top_rated['reviews']),1)}/5\n"
                    f"🔥 **Achka:** {top_demanded['name'][:40]} — {len(top_demanded['reviews'])} rivis\n"
                    f"⏳ **Ñawpa:** {top_exp['name'][:40]} — {top_exp['years_selling']} wata\n\n📊🦥")
        return (f"📊 **Comparativa de Comunidades — MAPPED**\n\n"
                f"🏆 **Mejor valorada:** {top_rated['name']} — "
                f"★ {round(sum(r['stars'] for r in top_rated['reviews'])/len(top_rated['reviews']),1)}/5\n"
                f"🔥 **Más demandada:** {top_demanded['name']} — {len(top_demanded['reviews'])} reseñas de turistas\n"
                f"⏳ **Más experiencia:** {top_exp['name']} — {top_exp['years_selling']} años en el mercado\n\n"
                f"¿Quieres una comparación detallada entre dos comunidades específicas? "
                f"¡Dime cuáles y te las analizo! 📊🦥")
    
    # ── Análisis de mercado / tendencias ──
    if any(w in ul for w in market_q):
        st.session_state["last_topic"] = "market"
        total_products = sum(len(e["products"]) for e in dataset)
        total_reviews = sum(len(e["reviews"]) for e in dataset)
        avg_rating = round(sum(sum(r["stars"] for r in e["reviews"]) for e in dataset if e["reviews"]) / max(total_reviews, 1), 1)
        growing = sorted(dataset, key=lambda e: len(e["reviews"]), reverse=True)[:3]
        if L == "en":
            return (f"📈 **MAPPED Market Overview**\n\n"
                    f"📊 **{len(dataset)}** registered communities\n"
                    f"📦 **{total_products}** products available\n"
                    f"⭐ **{avg_rating}/5** average satisfaction ({total_reviews} reviews)\n\n"
                    f"🚀 **Fastest growing communities:**\n"
                    + "\n".join([f"• **{e['name'][:40]}** — {len(e['reviews'])} reviews, {e['sector']}" for e in growing])
                    + "\n\n💡 The Amazonian handicraft market shows consistent growth. "
                    "Tourists increasingly seek authentic, sustainable products. "
                    "MAPPED's 85/15 fair-trade model ensures long-term viability.\n\n"
                    "Would you like to see ROI projections or sector-specific analysis? 📊🦥")
        if L == "qw":
            return (f"📈 **MAPPED mercado**\n\n"
                    f"📊 {len(dataset)} llakta\n📦 {total_products} rura\n⭐ {avg_rating}/5 ({total_reviews} rivis)\n\n"
                    + "\n".join([f"• **{e['name'][:35]}** — {len(e['reviews'])} rivis" for e in growing])
                    + "\n\n¿Ashka munankichu? 📊")
        return (f"📈 **Panorama General del Mercado MAPPED**\n\n"
                f"📊 **{len(dataset)}** comunidades registradas en Loreto\n"
                f"📦 **{total_products}** productos artesanales disponibles\n"
                f"⭐ **{avg_rating}/5** de satisfacción promedio ({total_reviews} reseñas de turistas)\n\n"
                f"🚀 **Comunidades de mayor crecimiento:**\n"
                + "\n".join([f"• **{e['name'][:45]}** — {len(e['reviews'])} reseñas | Sector: {e['sector']}" for e in growing])
                + "\n\n💡 **Tendencia de mercado:** El mercado de artesanías amazónicas muestra un "
                "crecimiento consistente. Los turistas internacionales buscan cada vez más productos "
                "auténticos, sostenibles y con historia cultural.\n\n"
                "El modelo de comercio justo 85/15 de MAPPED garantiza que la inversión "
                "sea sostenible a largo plazo. ¿Quieres ver las proyecciones de ROI "
                "por sector o alguna comunidad en específico? 📊🦥")
    
    if any(w in ul for w in greetings):
        if L == "en":
            return (f"{KICHWA['saludo']}, mashi investor. 📊 Welcome to MAPPED. "
                    f"We currently have **{len(dataset)} registered communities** in our database.\n\n"
                    f"Each community has been evaluated by sales history, reviews, "
                    f"logistics, and market potential.\n\n"
                    f"Enter your company details in the form to access the complete "
                    f"analysis dashboard with comparison tables. 📊🦥")
        if L == "qw":
            return (f"{KICHWA['saludo']}, mashi qolqe. 📊 Kay MAPPEDpi {len(dataset)} "
                    f"llaktakuna tiyan. Formulariota churay rikunkapa. 🦥")
        return (f"{KICHWA['saludo']}, mashi inversionista. 📊 Bienvenido a MAPPED. "
                f"Actualmente tenemos **{len(dataset)} comunidades registradas** en nuestra "
                f"base de datos de la Amazonía loretense.\n\n"
                f"Cada comunidad ha sido evaluada según sus ventas, reseñas de turistas, "
                f"logística de acceso y potencial de mercado.\n\n"
                f"Ingresa los datos de tu empresa (RUC, representante, DNI) en el formulario "
                f"para acceder al análisis completo con tabla comparativa y recomendaciones. 📊🦥")
    if any(w in ul for w in ["comunidad","emprendedor","artesano","inversión","invertir","inversion","proveedor","community","supplier"]):
        lines = []
        for e in dataset:
            avg = round(sum(r["stars"] for r in e["reviews"])/len(e["reviews"]),1) if e["reviews"] else "—"
            suggested, n_rev, years = _price_suggestion(e)
            lines.append(f"• **{e['name']}** — {e['sector']} | ★ {avg} | {years} años | S/ {suggested:.0f} sugerido")
        if L == "en":
            return ("Here are the communities available in MAPPED:\n\n"
                    + "\n".join(lines)
                    + "\n\nComplete your company verification to see the detailed analysis "
                    "of logistics viability, pricing, and review insights. 📊🦥")
        if L == "qw":
            return ("Kay MAPPED llaktakuna:\n\n"
                    + "\n".join(lines)
                    + "\n\nQolqe yachankapa formulariota churay. 📊")
        return ("Aquí tienes las comunidades disponibles en MAPPED:\n\n"
                + "\n".join(lines)
                + "\n\nCompleta la verificación de tu empresa (RUC, DNI, representante) "
                "para acceder al análisis detallado de viabilidad logística, "
                "precios de mercado, reseñas verificadas y recomendación personalizada. 📊🦥")
    if any(w in ul for w in ["precio","precios","cuánto","cuesta","price","costos"]):
        lines = []
        for e in dataset:
            for p in e["products"]:
                lines.append(f"• **{e['name']}** → {p['name']}: {p['currency']}{p['price']:.2f}")
        if L == "en":
            return ("Reference prices for all products:\n\n"
                    + "\n".join(lines[:8])
                    + "\n\nWant to see the investment analysis with ROI projections? "
                    "Complete your company verification. 📊🦥")
        if L == "qw":
            return ("Kay masnakuna:\n\n" + "\n".join(lines[:6]) + "\n\n¿Ashka munankichu? 🦥")
        return ("Aquí tienes los precios de referencia de todas las comunidades:\n\n"
                + "\n".join(lines[:8])
                + "\n\nEstos son precios directos al público. Para análisis de inversión "
                "con proyecciones de retorno, completa la verificación de tu empresa. 📊🦥")
    verified = st.session_state.get("verified", False)
    if verified:
        last_topic_inv = st.session_state.get("last_topic", "")
        rep_name = st.session_state.get("verified_rep", "inversionista")
        topic_prompts_inv = {
            "roi": _L("¿Quieres ver el ROI de otro sector?","Want to see ROI for another sector?","¿Shuk sektorpa ROI rikunki?"),
            "recommend_invest": _L("¿Quieres analizar alguna comunidad en detalle?","Want to analyze any community in detail?","¿Llaktata rikunki?"),
            "sector_analysis": _L("¿Quieres ver las comunidades top de ese sector?","Want to see top communities in that sector?","¿Allin llaktakunata rikunki?"),
            "logistics": _L("¿Necesitas coordenadas de alguna comunidad?","Need coordinates for a community?","¿Maypita?"),
            "compare": _L("¿Quieres comparar dos comunidades específicas?","Want to compare two specific communities?","¿Ishkay llaktakunata tinkuchinki?"),
            "market": _L("¿Quieres ver las proyecciones de ROI por sector?","Want to see ROI projections by sector?","¿Sektorpa qolqeta rikunki?"),
        }
        prompt_inv = topic_prompts_inv.get(last_topic_inv,
            _L("¿Sobre qué dato quieres profundizar?","Which data would you like to dive into?","¿Imata yachayta munanki?"))
        if L == "en":
            return (f"📊 Welcome back, **{rep_name}**! Your dashboard is ready. {prompt_inv}\n\n"
                    f"Try: ROI, sectors, logistics, or market trends. 📊🦥")
        if L == "qw":
            return (f"📊 **{rep_name}**! {prompt_inv} 📊🦥")
        return (f"📊 Bienvenido de nuevo, **{rep_name}**. {prompt_inv}\n\n"
                f"Puedes consultar:\n"
                f"📊 **ROI** — Retorno de inversión\n"
                f"💰 **Invertir** — Recomendaciones\n"
                f"🏭 **Sectores** — Análisis por sector\n"
                f"📍 **Logística** — Acceso y transporte\n"
                f"📈 **Mercado** — Tendencias\n"
                f"⚖️ **Comparar** — Comparativa entre comunidades\n\n"
                f"¿Sobre qué tema consultamos? 📊🦥")
    if L == "en":
        return (f"{KICHWA['saludo']}, mashi investor. 📊 Please complete the form with your "
                f"RUC, legal representative, and DNI to access the MAPPED community analysis. "
                f"You can also ask me about available communities, pricing, or market data. "
                f"If you want investment analysis, just ask about 📊🦥")
    if L == "qw":
        return (f"{KICHWA['saludo']}, mashi qolqe. RUCta, sutiykita, DNIta churay "
                f"rikushun. Llaktakunamanta tapuy. 📊🦥")
    return (f"{KICHWA['saludo']}, mashi inversionista. Complete el formulario con su RUC, "
            f"representante legal y DNI para acceder al panel de análisis de comunidades MAPPED. "
            f"Puede preguntarme sobre:\n\n"
            f"📊 **ROI** — Análisis de retorno de inversión\n"
            f"💰 **Invertir** — Recomendaciones de inversión\n"
            f"🏭 **Sectores** — Análisis por sector de mercado\n"
            f"📍 **Logística** — Acceso y transporte\n"
            f"📈 **Mercado** — Tendencias y proyecciones\n"
            f"⚖️ **Comparar** — Comparativa entre comunidades\n\n"
            f"¿Sobre qué tema te gustaría consultar, mashi inversionista? 📊🦥")

def _resolve_api_key():
    """Check session, env var, and streamlit secrets for a Gemini key."""
    sess = st.session_state.get("api_key", "")
    if sess and sess.strip() not in ("", "YOUR_API_KEY_HERE"):
        return sess.strip()
    env = os.environ.get("GEMINI_API_KEY", "")
    if env and env.strip() not in ("", "YOUR_API_KEY_HERE"):
        st.session_state.api_key = env.strip()
        return env.strip()
    try:
        sec = st.secrets.get("GEMINI_API_KEY", "")
        if sec and sec.strip() not in ("", "YOUR_API_KEY_HERE"):
            st.session_state.api_key = sec.strip()
            return sec.strip()
    except Exception:
        pass
    return ""

def _offline_notice(errors_log=None):
    last_topic = st.session_state.get("last_topic", "")
    last_ent_id = st.session_state.get("last_ent")
    context = ""
    if last_ent_id and last_topic and last_topic != "default" and last_topic != "saludo":
        context = _L(
            "Justo estábamos viendo los datos de la comunidad. ",
            "We were just looking at that community's data. ",
            "Llaktamanta willaykunata rikushkanchik. ")
    elif last_topic in ("weather", "clima"):
        context = _L(
            "Justo hablábamos del clima en Loreto. ",
            "We were just talking about Loreto's weather. ",
            "Loretomanta cliamta rimashkanchik. ")
    if errors_log:
        quota_errs = [e for e in errors_log if "429" in e or "RESOURCE_EXHAUSTED" in e]
        if quota_errs:
            return _L(
                f"⚠️ **Límite de API excedido** — Las 3 keys de Gemini agotaron su cuota. "
                f"Usando datos locales mientras se restablece.\n{context}",
                f"⚠️ **API limit exceeded** — All 3 Gemini keys hit their quota. "
                f"Using local data until they reset.\n{context}",
                f"⚠️ **API tukukapun** — Keys tukuy cuota ushashka. "
                f"Kaymanta willaykunata apamuni.\n{context}")
        return _L(
            f"🌐 **Modo offline** — {context}Error de conexión con Gemini.",
            f"🌐 **Offline mode** — {context}Gemini connection error.",
            f"🌐 **Offline** — {context}Gemini mana tinkunchu.")
    return _L(
        f"🌐 **Modo offline** — {context}Sin internet uso mis datos locales de las 15 comunidades de Loreto.",
        f"🌐 **Offline mode** — {context}No internet? I use local data from our 15 Loreto communities.",
        f"🌐 **Offline** — {context}Mana internetchu, kaymanta willaykunata apamuni.")

def _offline_tag():
    return _L("\n\n—\n🦥 *Mashi offline · datos locales*",
              "\n\n—\n🦥 *Mashi offline · local data*",
              "\n\n—\n🦥 *Mashi offline · kaymanta willay*")

def _is_route_query(ul):
    """True si el input es claramente una consulta de ruta/ubicacion (≥2 kw o frase exacta)."""
    strong_kw = ["ubicacion","ubicado","direccion","llegar","ruta","rutas",
                 "camino","route","directions","reach","get there","dirige",
                 "logistics","logística"]
    strong_matches = sum(1 for w in strong_kw if w in ul)
    route_phrases = ["dime la ruta","dime la direccion","dime la dirección","como llegar","cómo llegar",
                     "como llego","cómo llego","guíame","guiame","llévame","llevame",
                     "how do i get","how to get","take me to","guide me to","navigate",
                     "donde queda","donde esta","donde está","where is","ubicacion de",
                     "mapa de","lugar de","donde es","cual es su ubicacion","cual es tu ubicacion",
                     "donde se encuentra","direccion exacta","como llego hasta"]
    return (strong_matches >= 2) or any(p in ul for p in route_phrases)

def get_mashi_response(user_input, mode, history, api_key):
    sp = get_system_prompt(mode); ds = get_full_dataset()
    lang = st.session_state.get("lang", "es")
    lang_instruction = ""
    if lang == "en":
        lang_instruction = "IMPORTANT: Respond in English. Greet in Kichwa ('Allianllachu') but answer in English."
    elif lang == "qw":
        lang_instruction = "IMPORTANT: Respond ENTIRELY in Kichwa (Runasimi). DO NOT use Spanish — not even single words. Use the Kichwa vocabulary we have. If a concept has no Kichwa word, use English loanwords instead of Spanish. Greet with 'Allianllachu mashi'."
    sp = sp + "\n" + lang_instruction
    ctx = json.dumps([{"name":e["name"],"sector":e["sector"],"products":e["products"],
        "reviews":e["reviews"],"years_selling":e["years_selling"],"materials":e.get("materials","")} for e in ds],
        ensure_ascii=False)

    # ── Detectar y guardar ubicación del usuario ──
    ul = user_input.lower()
    for phrase in ["estoy en ", "estoy cerca de ", "me encuentro en ", "mi ubicación es ", "mi ubicacion es ",
                   "i'm at ", "i am at ", "i'm in ", "i am in ", "my location is ",
                   "kaypim kani ", "ñukapam tiyani "]:
        if phrase in ul:
            place = ul.split(phrase, 1)[1].strip().rstrip(".!?,;")
            # Buscar en lugares conocidos
            found = False
            for pname, (plat, plng) in IQUITOS_PLACES.items():
                if pname in place:
                    st.session_state["user_lat"] = plat
                    st.session_state["user_lng"] = plng
                    st.session_state["user_loc_name"] = pname.title()
                    found = True
                    break
            if not found:
                # Usar centro de Iquitos como default
                st.session_state["user_lat"] = -3.7491
                st.session_state["user_lng"] = -73.2442
                st.session_state["user_loc_name"] = place.title()
            # Auto-mostrar mini mapa con la ubicación del usuario
            st.session_state["show_mini_map"] = True
            if st.session_state.get("last_ent"):
                st.session_state["selected_ent_id"] = st.session_state["last_ent"]
            break

    # ── Interceptar consultas de ruta/ubicación antes de IA ──
    if _is_route_query(ul):
        return mock_response(user_input, mode, ds) + _offline_tag()

    # ── Expirar last_ent si pasaron >3 mensajes sin referenciarlo ──
    msg_count = st.session_state.get("_msg_since_last_ent", 0) + 1
    st.session_state["_msg_since_last_ent"] = msg_count
    if msg_count > 3:
        st.session_state.pop("last_ent", None)

    prompt = f"{user_input}\n\nDataset: {ctx}\n\nIMPORTANTE: Responde natural, cálido y MUY breve. Máximo 3 oraciones. No des toda la info de golpe.\n\nNOTA: NO digas que no puedes mostrar imagenes. Las imagenes se anaden solas."

    # ── Adjuntar historial de conversación ──
    if history and len(history) > 1:
        last_msgs = history[-4:]  # Últimos 4 mensajes como contexto
        conv_lines = []
        for m in last_msgs:
            role = "Usuario" if m["role"] == "user" else "Mashi"
            conv_lines.append(f"{role}: {m['content'][:200]}")
        conv_text = "\n".join(conv_lines)
        prompt = f"{conv_text}\n\nUsuario: {user_input}\n\nDataset: {ctx}\n\nIMPORTANTE: Responde MUY breve, cálido, como un amigo. Máximo 3 oraciones.\n\nNOTA: NO digas que no puedes mostrar imagenes. Las imagenes de los productos se anaden automaticamente por el sistema. Solo describe el producto y la comunidad."

    # ── Pasar contexto de la última comunidad mencionada ──
    if st.session_state.get("last_ent"):
        le = next((e for e in ds if e.get("id") == st.session_state["last_ent"]), None)
        if le:
            prompt += f"\n\nContexto: el usuario preguntó antes sobre «{le['name']}» ({le['location']}). Responde sobre esa comunidad a menos que pregunte expresamente por otra."

    # 1) Try OpenRouter (if key configured)
    or_key = _resolve_or_key()
    if or_key:
        or_models = ["google/gemini-2.5-flash", "mistralai/mistral-7b-instruct", "openai/gpt-4o-mini"]
        for m in or_models:
            text = _call_openrouter(prompt, or_key, model=m, system=sp)
            if text:
                return _clean_mashi(text, lang)

    # 2) Try Gemini
    user_key = (api_key or _resolve_api_key()).strip()
    pool = [k for k in GEMINI_KEYS if k != user_key]
    start = st.session_state.get("_gemini_key_idx", 0) % len(GEMINI_KEYS)
    ordered_pool = pool[start:] + pool[:start]
    keys_to_try = []
    if user_key and user_key not in ("", "YOUR_API_KEY_HERE"):
        keys_to_try.append(("tu key", user_key))
    for k in ordered_pool:
        keys_to_try.append(("pool", k))
    keys_to_try.append(("fallback", None))

    from google import genai
    from google.genai import errors as gerr
    errors_log = []
    for label, ak in keys_to_try:
        if ak is None:
            for _, first_key in keys_to_try:
                if first_key:
                    try:
                        client2 = genai.Client(api_key=first_key)
                        resp2 = client2.models.generate_content(
                            model="gemini-1.5-flash",
                            contents=prompt,
                            config={"system_instruction": sp}
                        )
                        if first_key in GEMINI_KEYS:
                            st.session_state["_gemini_key_idx"] = GEMINI_KEYS.index(first_key)
                        return _clean_mashi(resp2.text, lang)
                    except Exception:
                        pass
            break
        try:
            client = genai.Client(api_key=ak)
            for model_name in ("gemini-2.5-flash", "gemini-1.5-flash"):
                try:
                    resp = client.models.generate_content(
                        model=model_name,
                        contents=prompt,
                        config={"system_instruction": sp}
                    )
                    text = resp.text
                    if ak in GEMINI_KEYS:
                        st.session_state["_gemini_key_idx"] = GEMINI_KEYS.index(ak)
                    return _clean_mashi(text, lang)
                except (gerr.ClientError, gerr.ServerError) as e:
                    errors_log.append(f"{label} {model_name}: {type(e).__name__} {str(e)[:80]}")
                    continue
                except Exception:
                    errors_log.append(f"{label} {model_name}: error inesperado")
                    continue
        except Exception:
            errors_log.append(f"{label}: no se pudo crear cliente")
            continue
    return _offline_notice(errors_log) + "\n\n" + mock_response(user_input, mode, ds) + _offline_tag()




def _clean_mashi(text, lang):
    if lang == "qw":
        return text
    replacements = {
        "es": [
            (", mashi!", " amigo!"),
            (", mashi?", ", amigo?"),
            (", mashi ", ", amigo "),
            (" mashi ", " amigo "),
            ("Mashi sugiere", "Recomiendo"),
            ("mashi artesano", "artesano"),
            ("mashi inversionista", "inversionista"),
            ("mashi ruraq", "ruraq"),
        ],
        "en": [
            (", mashi!", " friend!"),
            (", mashi?", ", friend?"),
            (", mashi ", ", friend "),
            (" mashi ", " friend "),
            ("Mashi suggests", "I suggest"),
            ("mashi artisan", "artisan"),
            ("mashi investor", "investor"),
        ],
    }
    for old, new in replacements.get(lang, []):
        text = text.replace(old, new)
    return text


# ========================================================================
# CSS — TECH-JUNGLE (#021B15 + CYAN + MINT)
# ========================================================================
CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Nunito:wght@400;500;600;700;800&family=Outfit:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');
    *, *::before, *::after { box-sizing: border-box; }
    html, body, #root, .stApp, .st-emotion-cache-6qob1r, .st-emotion-cache-1r4qj8v, .st-emotion-cache-1dj0xjt, .st-emotion-cache-1wbqy5l { background: #040e0b !important; height: 100%; margin: 0; padding: 0; }
    .stApp { background: #040e0b !important; font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; font-weight: 450; letter-spacing: -0.01em; }
    h1, h2, h3, h4, h5, h6, .section-title, .onboarding-title, .stMarkdown strong { font-family: 'Outfit', sans-serif !important; letter-spacing: -0.02em; }
    h1, h2, h3, h4, h5, h6 { font-weight: 600; letter-spacing: -0.03em; color: #FFFFFF !important; }
    .kpi-value { font-family: 'Space Grotesk', 'Outfit', sans-serif !important; letter-spacing: -0.03em; }
    .kpi-label, .section-subtitle, .onboarding-sub { font-family: 'Nunito', sans-serif !important; font-weight: 500; }
    .stMarkdown p, .stMarkdown li, .stMarkdown span, .stMarkdown div { font-weight: 400; line-height: 1.7; }
    .main { background: #040e0b; }
    .main > .block-container { max-width: 1200px; padding: 0 !important; margin: 0 auto !important; background: transparent; }
    .appview-container, .main, .block-container { background: transparent !important; }
    .stApp > header, .stApp > footer, #MainMenu, .stDecoration { display: none !important; }
    .row-widget, .stHorizontalBlock, .element-container { background: transparent !important; }
    section[data-testid="stSidebar"] > div:first-child { background: #05110e !important; }
    .stSelectbox > div[data-baseweb="select"], .stTextInput, .stTextArea, .stNumberInput, .stButton, .stMarkdown, .stChatInputContainer, .stExpander, .stAlert, .stDataFrame, .stFileUploader, .stForm { background: transparent !important; }
    div[data-testid="stSelectboxDropdown"], div[data-baseweb="popover"], ul[role="listbox"] { background: rgba(10,31,26,0.96) !important; border: 1px solid rgba(16,185,129,0.15) !important; border-radius: 20px !important; backdrop-filter: blur(20px) !important; box-shadow: 0 8px 32px rgba(0,0,0,0.3), 0 0 0 1px rgba(16,185,129,0.03) !important; }
    div[data-testid="stSelectboxDropdown"] li, ul[role="listbox"] li, li[role="option"] { color: #e2e8f0 !important; background: #0a1f1a !important; }
    div[data-testid="stSelectboxDropdown"] li:hover, ul[role="listbox"] li:hover, li[role="option"]:hover { background: rgba(16,185,129,0.15) !important; }
    div[data-testid="stSelectboxDropdown"] li[aria-selected="true"], ul[role="listbox"] li[aria-selected="true"], li[role="option"][aria-selected="true"] { background: rgba(16,185,129,0.25) !important; color: #10b981 !important; }
    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-track { background: #040e0b; }
    ::-webkit-scrollbar-thumb { background: #10b981; border-radius: 10px; }
    h1,h2,h3,h4,h5,h6,p,span,label,div,.stMarkdown { color: #e2e8f0 !important; }
    /* ── Header ── */
    .app-header { background: linear-gradient(180deg,#05110e 0%,#040e0b 100%); padding: 0.8rem 1.5rem; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid rgba(16,185,129,0.08); position: sticky; top: 0; z-index: 100; }
    .app-header-left { display: flex; align-items: center; gap: 12px; }
    .app-header .avatar { width: 38px; height: 38px; border-radius: 50%; background: rgba(16,185,129,0.08); border: 1.5px solid rgba(16,185,129,0.3); flex-shrink: 0; overflow: hidden; box-shadow: 0 0 20px rgba(16,185,129,0.05); }
    .app-header .title { font-weight: 800; font-size: 1.2rem; color: #FFFFFF !important; letter-spacing: -0.02em; font-family: 'Outfit', sans-serif; }
    .app-header .subtitle { font-size: 0.6rem; color: #10b981 !important; text-transform: uppercase; letter-spacing: 2px; font-weight: 600; font-family: 'Nunito', sans-serif; }
    .app-header .lang-badge { background: rgba(16,185,129,0.08); border: 1px solid rgba(16,185,129,0.15); padding: 0.2rem 0.7rem; border-radius: 20px; font-size: 0.7rem; font-weight: 700; color: #10b981 !important; }
    /* ── Chat header ── */
    .chat-header { padding: 1rem 1.2rem; display: flex; align-items: center; gap: 12px; background: linear-gradient(135deg,#0a1f1a,#0d261f); border-bottom: 1px solid rgba(16,185,129,0.06); border-radius: 16px 16px 0 0; margin: 0.8rem 0.8rem 0; box-shadow: 0 -4px 24px rgba(0,0,0,0.25), inset 0 1px 0 rgba(16,185,129,0.04); }
    .chat-header .mashi-avatar { width: 42px; height: 42px; border-radius: 50%; background: rgba(16,185,129,0.1); border: 2px solid rgba(16,185,129,0.35); flex-shrink: 0; overflow: hidden; box-shadow: 0 0 24px rgba(16,185,129,0.08); }
    .chat-header .mashi-name { font-weight: 700; color: #FFFFFF !important; font-size: 0.95rem; letter-spacing: -0.01em; font-family: 'Outfit', sans-serif; }
    .chat-header .mashi-status { font-size: 0.65rem; color: #10b981 !important; display: flex; align-items: center; gap: 4px; text-transform: uppercase; letter-spacing: 0.5px; font-family: 'Nunito', sans-serif; }
    .chat-header .mashi-status.online::before { content: ''; width: 6px; height: 6px; background: #10b981; border-radius: 50%; display: inline-block; animation: pulse 1.5s infinite; box-shadow: 0 0 8px rgba(16,185,129,0.4); }
    .chat-header .mashi-status.offline { color: rgba(245,158,11,0.8) !important; }
    .chat-header .mashi-status.offline::before { content: ''; width: 6px; height: 6px; background: rgb(245,158,11); border-radius: 50%; display: inline-block; animation: pulse 1.5s infinite; box-shadow: 0 0 8px rgba(245,158,11,0.3); }
    @keyframes pulse { 0%,100% { opacity:1; } 50% { opacity:0.4; } }
    /* ── Chat bubbles (main page fallback, not iframe) ── */
    .chat-container { padding: 1rem 1rem; display: flex; flex-direction: column; gap: 12px; background: radial-gradient(ellipse at 20% 20%, rgba(16,185,129,0.015) 0%, transparent 60%); border-radius: 0 0 16px 16px; margin: 0 0.8rem; border-left: 1px solid rgba(16,185,129,0.06); border-right: 1px solid rgba(16,185,129,0.06); border-bottom: 1px solid rgba(16,185,129,0.06); min-height: 400px; max-height: 500px; overflow-y: auto; box-shadow: 0 8px 40px rgba(0,0,0,0.18); scroll-behavior: smooth; }
    .bubble-row { display: flex; align-items: flex-end; gap: 8px; margin-bottom: 2px; animation: fadeIn 0.35s cubic-bezier(0.21,1.02,0.73,1); }
    @keyframes fadeIn { from { opacity:0; transform:translateY(10px) scale(0.97); } to { opacity:1; transform:translateY(0) scale(1); } }
    .bubble-row.mashi { justify-content: flex-start; }
    .bubble-row.user { justify-content: flex-end; }
    .bubble-avatar { width: 28px; height: 28px; border-radius: 50%; flex-shrink: 0; overflow: hidden; transition: transform 0.2s; }
    .bubble-row:hover .bubble-avatar { transform: scale(1.05); }
    .bubble-avatar.mashi { background: rgba(16,185,129,0.1); border: 1.5px solid rgba(16,185,129,0.3); box-shadow: 0 0 12px rgba(16,185,129,0.08); }
    .bubble-avatar.user { background: rgba(56,189,248,0.1); border: 1.5px solid rgba(56,189,248,0.3); display: flex; align-items: center; justify-content: center; font-size: 0.8rem; }
    .chat-bubble-mashi { background: linear-gradient(135deg,#0a1f1a,#0d261f); border: 1px solid rgba(16,185,129,0.12); border-radius: 16px 16px 16px 4px; padding: 14px 18px; max-width: 85%; color: #e2e8f0 !important; font-size: 0.9rem; font-family: 'Nunito', sans-serif; font-weight: 500; line-height: 1.7; letter-spacing: 0; box-shadow: 0 4px 16px rgba(0,0,0,0.2), 0 0 40px rgba(16,185,129,0.03); animation: bubbleIn 0.4s cubic-bezier(0.21,1.02,0.73,1); }
    .chat-bubble-mashi p { margin: 0 0 6px 0; color: #e2e8f0 !important; }
    .chat-bubble-mashi strong { color: #10b981 !important; }
    .chat-bubble-user { background: rgba(16,185,129,0.06); border: 1px solid rgba(16,185,129,0.12); border-radius: 16px 16px 4px 16px; padding: 14px 18px; max-width: 85%; color: #e2e8f0 !important; font-size: 0.85rem; font-family: 'Nunito', sans-serif; font-weight: 500; line-height: 1.65; letter-spacing: 0; animation: bubbleIn 0.4s cubic-bezier(0.21,1.02,0.73,1); }
    @keyframes bubbleIn { from { opacity:0; transform:translateY(12px) scale(0.95); } to { opacity:1; transform:translateY(0) scale(1); } }
    /* ── Typing indicator ── */
    .typing-bubble { background: #0a1f1a; border: 1px solid rgba(16,185,129,0.08); border-radius: 16px 16px 16px 4px; padding: 14px 20px; display: flex; align-items: center; gap: 6px; max-width: 100px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); }
    .typing-dot { width: 7px; height: 7px; border-radius: 50%; background: #10b981; display: inline-block; animation: typingDot 1.4s infinite; box-shadow: 0 0 6px rgba(16,185,129,0.3); }
    .typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-dot:nth-child(3) { animation-delay: 0.4s; }
    @keyframes typingDot { 0%,60%,100% { opacity:0.3; transform:scale(0.8); } 30% { opacity:1; transform:scale(1); } }
    /* ── Clear chat ── */
    .clear-chat { font-size: 0.6rem; color: rgba(148,163,184,0.25) !important; text-align: center; padding: 4px 0; cursor: pointer; transition: color 0.2s; }
    .clear-chat:hover { color: rgba(239,68,68,0.5) !important; }
    .stChatInputContainer { background: #0a1f1a !important; border: 1px solid rgba(16,185,129,0.12) !important; border-radius: 28px !important; margin: 0 0.8rem 0.8rem !important; box-shadow: 0 2px 12px rgba(0,0,0,0.1), 0 0 0 1px rgba(16,185,129,0.02) !important; transition: all 0.2s cubic-bezier(0.4,0,0.2,1) !important; backdrop-filter: blur(8px) !important; }
    .stChatInputContainer:focus-within { border-color: rgba(16,185,129,0.3) !important; box-shadow: 0 2px 20px rgba(0,0,0,0.15), 0 0 0 2px rgba(16,185,129,0.06) !important; }
    .stChatInputContainer input, .stChatInputContainer textarea { color: #e2e8f0 !important; font-size: 0.85rem !important; caret-color: #10b981 !important; }
    .stChatInputContainer input::placeholder, .stChatInputContainer textarea::placeholder { color: rgba(226,232,240,0.3) !important; }
    div[data-testid="stChatInput"] { background: #0a1f1a !important; border: 1px solid rgba(16,185,129,0.12) !important; border-radius: 28px !important; }
    div[data-testid="stChatInput"] textarea, div[data-testid="stChatInput"] input, div[data-testid="stChatInput"] > div { background: #0a1f1a !important; color: #e2e8f0 !important; }
    div[data-testid="stChatInput"] * { background: #0a1f1a !important; }
    div[data-testid="stBottom"] { background: #040e0b !important; border: none !important; }
    div[data-testid="stBottom"] * { background: #040e0b !important; }
    div[data-testid="stBottomBlockContainer"] { background: #040e0b !important; padding: 0.5rem !important; border-top: 1px solid rgba(16,185,129,0.06) !important; }
    div[data-testid="stBottomBlockContainer"] * { background: #040e0b !important; }
    /* ── Sidebar ── */
    section[data-testid="stSidebar"] > div:first-child { background: linear-gradient(180deg,#05110e 0%,#030a08 100%) !important; border-right: 1px solid rgba(16,185,129,0.06) !important; padding-top: 0 !important; }
    section[data-testid="stSidebar"] .stMarkdown, section[data-testid="stSidebar"] label, section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span { color: #e2e8f0 !important; }
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 { color: #FFFFFF !important; }
    section[data-testid="stSidebar"] .stSelectbox > div > div { background: #0a1f1a !important; color: #10b981 !important; border: 1px solid rgba(16,185,129,0.12) !important; border-radius: 12px !important; }
    /* ── Selectbox ── */
    .stSelectbox > div > div { background: #0a1f1a !important; color: #e2e8f0 !important; border: 1px solid rgba(16,185,129,0.12) !important; border-radius: 12px !important; transition: border-color 0.2s !important; font-family: 'Nunito', sans-serif !important; }
    .stSelectbox > div > div:hover { border-color: rgba(16,185,129,0.3) !important; }
    .stSelectbox [data-baseweb="select"] > div { background-color: transparent !important; }
    .stSelectbox [data-baseweb="select"] span { color: #e2e8f0 !important; }
    /* ── Buttons ── */
    .stButton > button { background: linear-gradient(135deg,#10b981,#059669) !important; color: #040e0b !important; font-weight: 700 !important; border: none !important; border-radius: 30px !important; padding: 0.6rem 2rem !important; transition: all 0.2s cubic-bezier(0.4,0,0.2,1) !important; box-shadow: 0 4px 20px rgba(16,185,129,0.2) !important; font-size: 0.85rem !important; position: relative !important; overflow: hidden !important; letter-spacing: 0.02em !important; cursor: pointer !important; font-family: 'Nunito', sans-serif !important; }
    .stButton > button::after { content: ''; position: absolute; inset: 0; background: linear-gradient(135deg,transparent 40%,rgba(255,255,255,0.06) 100%); pointer-events: none; border-radius: 30px; }
    .stButton > button:hover { background: linear-gradient(135deg,#059669,#047857) !important; transform: translateY(-1px); box-shadow: 0 6px 24px rgba(16,185,129,0.4), 0 0 0 1px rgba(16,185,129,0.1) !important; }
    .stButton > button:active { transform: scale(0.97) !important; box-shadow: 0 2px 8px rgba(16,185,129,0.25) !important; transition-duration: 0.05s !important; }
    .stButton > button:disabled { opacity: 0.4 !important; transform: none !important; box-shadow: none !important; cursor: not-allowed !important; }
    .secondary-btn > button { background: transparent !important; color: #10b981 !important; border: 1.5px solid rgba(16,185,129,0.15) !important; box-shadow: none !important; }
    .secondary-btn > button:hover { background: rgba(16,185,129,0.06) !important; border-color: rgba(16,185,129,0.3) !important; }
    .stButton > button[kind="secondary"] { background: transparent !important; color: #10b981 !important; border: 1.5px solid rgba(16,185,129,0.15) !important; box-shadow: none !important; }
    .stButton > button[kind="secondary"]:hover { background: rgba(16,185,129,0.06) !important; border-color: rgba(16,185,129,0.3) !important; }
    .stButton > button[kind="secondary"]:active { transform: scale(0.97) !important; }
    /* ── Cards ── */
    .glass-card { background: linear-gradient(135deg,#0a1f1a,#0a221c); border: 1px solid rgba(16,185,129,0.06); border-radius: 28px; padding: 1.2rem; margin-bottom: 1rem; box-shadow: 0 4px 24px rgba(0,0,0,0.12), 0 0 0 1px rgba(16,185,129,0.02), 0 4px 20px rgba(16,185,129,0.03); transition: all 0.25s cubic-bezier(0.4,0,0.2,1); backdrop-filter: blur(4px); }
    .glass-card:hover { border-color: rgba(16,185,129,0.15); box-shadow: 0 8px 40px rgba(0,0,0,0.18), 0 0 0 1px rgba(16,185,129,0.04), 0 8px 40px rgba(16,185,129,0.04); transform: translateY(-1px); }
    .glass-card h3 { margin-top: 0; color: #FFFFFF !important; font-weight: 700; }
    .glass-card:active { transform: scale(0.99); }
    .nearby-card { transition: all 0.25s cubic-bezier(0.4,0,0.2,1) !important; }
    .nearby-card:hover { border-color: rgba(16,185,129,0.3)!important; transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,0,0,0.2), 0 0 20px rgba(16,185,129,0.03); }
    /* ── Inputs ── */
    [data-testid="stTextInput"] input, [data-testid="stNumberInput"] input, [data-testid="stTextArea"] textarea,
    input, textarea, select, [contenteditable="true"] { color: #e2e8f0 !important; background-color: #0a1f1a !important; caret-color: #10b981 !important; font-family: 'Nunito', sans-serif !important; }
    [data-testid="stTextInput"] input::placeholder, [data-testid="stTextArea"] textarea::placeholder, input::placeholder, textarea::placeholder { color: rgba(148,163,184,0.5) !important; opacity: 1 !important; }
    .stTextInput > div > div, .stTextArea > div > div, .stNumberInput > div > div, .stSelectbox > div > div { background: #0a1f1a !important; border: 1px solid rgba(16,185,129,0.08) !important; border-radius: 14px !important; color: #e2e8f0 !important; transition: all 0.2s !important; }
    .stTextInput > div > div:focus-within, .stTextArea > div > div:focus-within { border-color: #10b981 !important; box-shadow: 0 0 0 3px rgba(16,185,129,0.08) !important; }
    .stNumberInput input[type="number"] { color: #e2e8f0 !important; background-color: transparent !important; }
    .stNumberInput button { background: #0a1f1a !important; border: 1px solid rgba(16,185,129,0.08) !important; color: #10b981 !important; transition: all 0.2s !important; }
    .stNumberInput button:hover { background: rgba(16,185,129,0.1) !important; }
    input:-webkit-autofill, input:-webkit-autofill:hover, input:-webkit-autofill:focus, input:-webkit-autofill:active,
    textarea:-webkit-autofill, textarea:-webkit-autofill:hover, textarea:-webkit-autofill:focus, textarea:-webkit-autofill:active,
    select:-webkit-autofill, select:-webkit-autofill:hover, select:-webkit-autofill:focus, select:-webkit-autofill:active {
        -webkit-box-shadow: 0 0 0 100px #0a1f1a inset !important;
        -webkit-text-fill-color: #e2e8f0 !important;
        caret-color: #10b981 !important;
        background-color: #0a1f1a !important;
        transition: background-color 99999s ease-in-out 0s !important;
    }
    [data-testid="stForm"] input, [data-testid="stForm"] textarea, [data-testid="stForm"] select {
        color: #e2e8f0 !important;
        background-color: #0a1f1a !important;
    }
    .stFileUploader { background: #0a1f1a !important; border: 1px dashed rgba(16,185,129,0.15) !important; border-radius: 20px !important; transition: all 0.2s cubic-bezier(0.4,0,0.2,1) !important; }
    .stFileUploader:hover { border-color: rgba(16,185,129,0.3) !important; background: rgba(16,185,129,0.02) !important; }
    /* ── DataFrame ── */
    .stDataFrame { border-radius: 12px !important; overflow: hidden !important; border: 1px solid rgba(16,185,129,0.08) !important; }
    .stDataFrame th { background: #0a1f1a !important; color: #10b981 !important; font-weight: 600 !important; font-size: 0.75rem !important; font-family: 'Outfit', sans-serif !important; letter-spacing: 0.02em !important; }
    .stDataFrame td { background: transparent !important; color: #e2e8f0 !important; font-size: 0.75rem !important; border-color: rgba(16,185,129,0.06) !important; font-family: 'Nunito', sans-serif !important; }
    [data-testid="stForm"] { background: linear-gradient(135deg,#0a1f1a,#0a221c); border: 1px solid rgba(16,185,129,0.06); border-radius: 16px; padding: 1.5rem; box-shadow: 0 4px 24px rgba(0,0,0,0.1); }
    .streamlit-expanderHeader { background: #0a1f1a !important; border: 1px solid rgba(16,185,129,0.08) !important; border-radius: 16px !important; color: #10b981 !important; font-weight: 600 !important; font-size: 0.8rem !important; transition: all 0.2s cubic-bezier(0.4,0,0.2,1) !important; font-family: 'Outfit', sans-serif !important; letter-spacing: 0.01em !important; }
    .streamlit-expanderHeader:hover { border-color: rgba(16,185,129,0.2) !important; background: rgba(16,185,129,0.02) !important; }
    div[data-testid="stAlert"] { border-radius: 12px !important; background: #0a1f1a !important; border-left: 3px solid #10b981 !important; }
    /* ── Folium maps — kill white space ── */
    iframe[title="streamlit_folium.st_folium"], .stFolium, .stFolium iframe, .stFolium > div {
        background: #040e0b !important;
        border-radius: 12px !important;
    }
    .stFolium iframe { border: 1px solid rgba(16,185,129,0.06) !important; box-shadow: 0 4px 20px rgba(0,0,0,0.1) !important; }
    /* ── Onboarding ── */
    .onboarding-container { display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 90vh; padding: 2rem; text-align: center; background: radial-gradient(ellipse at center, rgba(16,185,129,0.03) 0%, transparent 70%); }
    .onboarding-logo { width: 90px; height: 90px; border-radius: 50%; background: rgba(16,185,129,0.1); border: 2px solid rgba(16,185,129,0.3); margin-bottom: 1.5rem; overflow: hidden; box-shadow: 0 0 50px rgba(16,185,129,0.08); }
    .onboarding-title { font-size: 2rem; font-weight: 800; color: #FFFFFF !important; margin-bottom: 0.3rem; letter-spacing: -0.03em; }
    .onboarding-sub { font-size: 0.9rem; color: rgba(148,163,184,0.7) !important; margin-bottom: 2rem; }
    .onboarding-card { background: linear-gradient(135deg,#0a1f1a,#0a221c); border: 1px solid rgba(16,185,129,0.06); border-radius: 32px; padding: 2rem; max-width: 400px; margin: 0 auto; box-shadow: 0 8px 32px rgba(0,0,0,0.12), 0 0 0 1px rgba(16,185,129,0.02); backdrop-filter: blur(4px); }
    /* ── Bottom Nav ── */
    .bnav-header { text-align: center; font-size: 0.55rem; color: rgba(148,163,184,0.2) !important; text-transform: uppercase; letter-spacing: 2.5px; margin: 2rem 0 0.6rem; font-weight: 600; }
    .map-legend { text-align: center; font-size: 0.75rem; color: rgba(148,163,184,0.6) !important; margin-top: 0.5rem; display: flex; justify-content: center; gap: 1.5rem; }
    .map-legend span { display: inline-flex; align-items: center; gap: 4px; }
    .bnav-btn { display: flex !important; flex-direction: column !important; align-items: center !important; gap: 3px !important; font-size: 0.55rem !important; padding: 8px 4px !important; border-radius: 14px !important; background: transparent !important; border: none !important; font-weight: 700 !important; transition: all 0.25s cubic-bezier(0.4,0,0.2,1) !important; letter-spacing: 0.5px !important; position: relative !important; font-family: 'Outfit', sans-serif !important; }
    .bnav-btn .bnav-icon { font-size: 1.3rem; transition: transform 0.2s; display: block; }
    .bnav-btn:hover .bnav-icon { transform: scale(1.15); }
    .bnav-btn.active { background: rgba(16,185,129,0.1) !important; color: #10b981 !important; border: 1px solid rgba(16,185,129,0.15) !important; box-shadow: 0 0 24px rgba(16,185,129,0.06), 0 0 0 1px rgba(16,185,129,0.03) !important; }
    .bnav-btn.active::after { width: 20px; }
    .bnav-btn::after { content: ''; position: absolute; bottom: 4px; left: 50%; width: 0; height: 2px; background: #10b981; border-radius: 2px; transition: all 0.2s ease; transform: translateX(-50%); }
    .bnav-btn.inactive { color: rgba(148,163,184,0.35) !important; border: 1px solid transparent !important; }
    .bnav-btn.inactive:hover { background: rgba(16,185,129,0.05) !important; color: rgba(16,185,129,0.6) !important; }
    .mashi-avatar-img { background-image: url('data:image/jpeg;base64,{B64}') !important; background-size: cover !important; background-position: center !important; background-repeat: no-repeat !important; }
    /* ── Speaker button ── */
    .speaker-btn { background: none; border: none; cursor: pointer; font-size: 0.9rem; padding: 3px 6px; opacity: 0.35; transition: all 0.25s; flex-shrink: 0; align-self: flex-end; line-height: 1; border-radius: 8px; margin-left: 2px; }
    .speaker-btn:hover { opacity: 1 !important; background: rgba(16,185,129,0.12); transform: scale(1.1); }
    .speaker-btn.speaking { opacity: 1; animation: speakPulse 0.6s ease-in-out infinite alternate; }
    @keyframes speakPulse { from { opacity:0.7; transform:scale(1); } to { opacity:1; transform:scale(1.15); } }
    /* ── Section titles ── */
    .section-title { font-weight: 800; font-size: 1.3rem; color: #FFFFFF !important; letter-spacing: -0.02em; position: relative; display: inline-block; }
    .section-title::after { content: ''; display: block; width: 40px; height: 3px; background: linear-gradient(90deg,#10b981,transparent); border-radius: 2px; margin-top: 4px; }
    .section-subtitle { font-size: 0.8rem; color: rgba(148,163,184,0.5) !important; margin-top: 0.2rem; letter-spacing: 0.3px; }
    /* ── KPI cards ── */
    .kpi-card { background: linear-gradient(135deg,#0a1f1a,#0a221c); border: 1px solid rgba(16,185,129,0.06); border-radius: 20px; padding: 1rem; text-align: center; transition: all 0.25s cubic-bezier(0.4,0,0.2,1); }
    .kpi-card:hover { border-color: rgba(16,185,129,0.12); transform: translateY(-1px); box-shadow: 0 8px 24px rgba(0,0,0,0.1), 0 0 20px rgba(16,185,129,0.02); }
    .kpi-card:active { transform: scale(0.98); }
    .kpi-value { font-size: 1.5rem; font-weight: 800; letter-spacing: -0.02em; }
    .kpi-label { font-size: 0.6rem; text-transform: uppercase; letter-spacing: 1.5px; color: rgba(148,163,184,0.4) !important; margin-top: 2px; }
    /* ── Bottom nav overlay (Streamlit buttons on top of visual bar) ── */
    .main > .block-container > div:last-child > div:last-child > .stHorizontalBlock:last-child {
        position: fixed !important; bottom: 0; left: 0; right: 0;
        height: 68px; z-index: 1001; background: linear-gradient(180deg,transparent,#040e0b 30%) !important;
        gap: 0; padding: 0 2rem; max-width: 600px; margin: 0 auto !important;
    }
    .main > .block-container > div:last-child > div:last-child > .stHorizontalBlock:last-child::before {
        content: ''; position: absolute; top: 0; left: 2rem; right: 2rem; height: 1px;
        background: linear-gradient(90deg,transparent,rgba(16,185,129,0.08),transparent);
    }
    .main > .block-container > div:last-child > div:last-child > .stHorizontalBlock:last-child > div {
        padding: 0 !important; flex: 1; display: flex;
        align-items: center; justify-content: center;
    }
    .main > .block-container > div:last-child > div:last-child > .stHorizontalBlock:last-child .stButton {
        width: 100%;
    }
    .main > .block-container > div:last-child > div:last-child > .stHorizontalBlock:last-child .stButton button {
        opacity: 0; width: 100%; height: 68px; min-height: 68px;
        border: none; background: transparent; cursor: pointer; padding: 0;
        border-radius: 0; box-shadow: none;
    }
    .main > .block-container > div:last-child > div:last-child > .stHorizontalBlock:last-child .stButton button:hover {
        opacity: 0.15; background: rgba(16,185,129,0.3);
    }
    /* ── Responsive ── */
    .main > .block-container { padding-bottom: 80px !important; }
    @media (max-width: 768px) {
        .main > .block-container { max-width: 100% !important; padding: 0 !important; }
        .chat-container { min-height: 300px; }
        .bottom-nav { height: 60px; }
        .main > .block-container > div:last-child > div:last-child > .stHorizontalBlock:last-child {
            height: 60px;
        }
        .main > .block-container > div:last-child > div:last-child > .stHorizontalBlock:last-child .stButton button {
            height: 60px; min-height: 60px;
        }
    }
    /* ── Image fade-in ── */
    .mapped-img { animation: mappedFadeIn 0.4s ease-in; }
    @keyframes mappedFadeIn { from { opacity: 0; } to { opacity: 1; } }
    /* ── Skeleton shimmer ── */
    .skeleton { background: linear-gradient(90deg,#0a1f1a 25%,#0d2b22 50%,#0a1f1a 75%); background-size: 200% 100%; animation: shimmer 1.5s infinite; border-radius: 16px; }
    @keyframes shimmer { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }
    /* ── Tap highlight ── */
    * { -webkit-tap-highlight-color: transparent; }
    /* ── Image loading placeholder ── */
    img { background: #0a1f1a; transition: opacity 0.4s ease; }
    /* ── Card entrance stagger ── */
    .stHorizontalBlock > div { animation: cardIn 0.4s cubic-bezier(0.21,1.02,0.73,1) both; }
    @keyframes cardIn { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: translateY(0); } }
    .stHorizontalBlock > div:nth-child(1) { animation-delay: 0s; }
    .stHorizontalBlock > div:nth-child(2) { animation-delay: 0.06s; }
    .stHorizontalBlock > div:nth-child(3) { animation-delay: 0.12s; }
    .stHorizontalBlock > div:nth-child(4) { animation-delay: 0.18s; }
    @media (min-width: 769px) {
        .main > .block-container { max-width: 960px !important; padding: 0 1.5rem !important; }
        .chat-header { margin: 1rem 0 0; }
        .chat-container { margin: 0; }
        .stChatInputContainer { margin: 0 0 1rem !important; }
    }
    /* ── App feel: smooth, touch-friendly ── */
    .main > .block-container { animation: pageIn 0.3s cubic-bezier(0.21,1.02,0.73,1); }
    @keyframes pageIn { from { opacity:0; transform:translateY(8px); } to { opacity:1; transform:translateY(0); } }
    html { scroll-behavior: smooth; -webkit-overflow-scrolling: touch; }
    button, a, [role="button"], .stButton, .stDownloadButton, input, select, textarea { touch-action: manipulation; }
    .stButton > button, .stDownloadButton > button { -webkit-user-select: none; user-select: none; }
    ::selection { background: rgba(16,185,129,0.3); color: #fff; }
    body { overscroll-behavior: none; background: #040e0b !important; }
    /* ── Kill any white anywhere ── */
    .main, .block-container, .st-emotion-cache-18ni7ap, .st-emotion-cache-1aej0i0, .st-emotion-cache-zq5wmm, .st-emotion-cache-1r4qj8v, .st-emotion-cache-1dj0xjt, .st-emotion-cache-6qob1r, .st-emotion-cache-10o6w6o, .st-emotion-cache-1f3w014 { background: #040e0b !important; }
    section[data-testid="stBottom"] { background: #040e0b !important; border: none !important; }
    .stMain { background: #040e0b !important; }
    .stChatFloatingInputContainer, div[class*="stChatFloating"], div[class*="chatInput"] { background: #040e0b !important; }
    /* ── Stagger rows ── */
    .row-widget.stHorizontalBlock { animation: rowIn 0.25s cubic-bezier(0.21,1.02,0.73,1) both; }
    @keyframes rowIn { from { opacity:0; transform:translateY(6px); } to { opacity:1; transform:translateY(0); } }
    /* ── Smooth tab indicator ── */
    .stTabs [data-baseweb="tab-list"] { gap: 0 !important; background: #0a1f1a !important; border-radius: 16px !important; padding: 0.3rem !important; border: 1px solid rgba(16,185,129,0.08) !important; }
    .stTabs [data-baseweb="tab"] { border-radius: 12px !important; transition: all 0.2s ease !important; color: rgba(148,163,184,0.5) !important; font-weight: 600 !important; }
    .stTabs [aria-selected="true"] { background: #10b981 !important; color: #040e0b !important; }
    .stTabs [data-baseweb="tab"]:hover { color: #e2e8f0 !important; }
</style><script>
(function(){function f(){var e=document.querySelector('[data-testid="stChatInput"]');if(e){e.style.background='#0a1f1a';var t=e.querySelector('textarea');if(t){t.style.background='#0a1f1a';t.style.color='#e2e8f0'}var b=document.querySelector('[data-testid="stBottom"]');if(b){b.style.background='#040e0b';b.style.border='none'}var c=document.querySelector('[data-testid="stBottomBlockContainer"]');if(c){c.style.background='#040e0b';c.style.borderTop='1px solid rgba(16,185,129,0.06)'}return true}return false}if(!f()){new MutationObserver(function(m,o){if(f())o.disconnect()}).observe(document.body,{childList:true,subtree:true})}
})();
</script>""".replace("{B64}", MASHI_LOGO_B64 if MASHI_LOGO_B64 else "")

# ========================================================================
# ONBOARDING
# ========================================================================
def render_onboarding():
    st.markdown(CSS, unsafe_allow_html=True)
    col1, col2 = st.columns([1,3])
    with col2:
        st.markdown('<div class="onboarding-container">', unsafe_allow_html=True)
        st.markdown('<div class="onboarding-logo mashi-avatar-img"></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="onboarding-title">{T("onboard_title")}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="onboarding-sub">{T("onboard_sub")}</div>', unsafe_allow_html=True)
        st.markdown('<div class="onboarding-card">', unsafe_allow_html=True)
        name = st.text_input("", placeholder=T("name_ph"), label_visibility="collapsed", key="onb_name")
        email = st.text_input("", placeholder=T("email_ph"), label_visibility="collapsed", key="onb_email")
        st.markdown(f'<p style="font-size:0.65rem;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;color:rgba(148,163,184,0.4)!important;margin:0.8rem 0 0.5rem;">🌐 {T("language")}</p>', unsafe_allow_html=True)
        c1,c2,c3 = st.columns(3)
        for code, col in [("es",c1),("en",c2),("qw",c3)]:
            with col:
                if st.button(code.upper(), key=f"l_onb_{code}", use_container_width=True,
                             type="primary" if st.session_state.get("lang","es")==code else "secondary"):
                    st.session_state.lang = code; st.rerun()
        st.markdown('<div style="height:0.5rem;"></div>', unsafe_allow_html=True)
        if st.button(T("create_btn"), use_container_width=True, type="primary"):
            if name.strip():
                st.session_state.onboarded = True
                st.session_state.user_name = name.strip()
                st.rerun()
            else:
                st.warning(_L("Ingresa tu nombre","Enter your name","Sutiykita churay"))
        if st.button("⏭ " + _L("Modo exposición (sin registro)","Expo mode (no signup)","Rikuchiy (mana sutiyuq)"), use_container_width=True):
            st.session_state.onboarded = True
            st.session_state.user_name = _L("Visitante","Visitor","Watukuq")
            st.session_state.demo_mode = True
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ========================================================================
# ECOTURISTA — CHAT
# ========================================================================
def _greeting_msg():
    L = st.session_state.get("lang", "es")
    n = len(get_full_dataset())
    if L == "en":
        return f"{KICHWA['saludo']}! I'm Mashi, your Amazon sloth guide. We have {n} artisan communities in Loreto. What would you like to explore today? 🦥🌿"
    if L == "qw":
        return f"{KICHWA['saludo']}! Ñukaka Mashi kanchikay, sachamanta alli rurakunata rikuchisha. Kay MAPPEDpi {n} llaktakuna tiyan. Ima munanki? 🦥🌿"
    return f"{KICHWA['saludo']}! Soy Mashi, tu gu\xeda perezoso de la Amazon\xeda. Tenemos {n} comunidades artesanas en Loreto. \xbfQu\xe9 te gustar\xeda conocer hoy? 🦥🌿"

def _is_online():
    ak = st.session_state.get("api_key","")
    if ak and ak.strip() not in ("","YOUR_API_KEY_HERE"): return True
    env = os.environ.get("GEMINI_API_KEY","")
    if env and env.strip() not in ("","YOUR_API_KEY_HERE"): return True
    try:
        sec = st.secrets.get("GEMINI_API_KEY","")
        if sec and sec.strip() not in ("","YOUR_API_KEY_HERE"): return True
    except Exception:
        pass
    return False

def _tts_generate(text, lang):
    """Genera audio: Qwen3-TTS (voice design) → gTTS. Cachea por hash."""
    import os, re, hashlib, io
    from gtts import gTTS
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    text = re.sub(r'\[.*?\]\(.*?\)', '', text)
    text = re.sub(r'\b\w+\.(jpg|jpeg|png|gif|webp|bmp|svg)\b', '', text, flags=re.I)
    text = re.sub(r'[\U0001F300-\U0001FAFF\U00002702-\U000027B0\U0001F1E0-\U0001F1FF\u2600-\u26FF\u2700-\u27BF🔊🎙️🌟]+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    if not text:
        return None
    cache_key = hashlib.md5((text + "_" + lang).encode()).hexdigest()
    audio_cache = st.session_state.setdefault("_tts_cache", {})
    if cache_key in audio_cache:
        return audio_cache[cache_key]
    from gradio_client import Client
    hf_tokens = [
        st.secrets.get("HF_TOKEN", "") or os.environ.get("HF_TOKEN", ""),
        st.secrets.get("HF_TOKEN_2", ""),
        st.secrets.get("HF_TOKEN_3", ""),
        st.secrets.get("HF_TOKEN_4", ""),
    ]
    hf_tokens = [t for t in hf_tokens if t]
    qwen_langs = {"es": "Spanish", "en": "English", "qw": "Spanish"}
    qwen_prompts = {
        "es": "Crea el perfil de voz de un asistente virtual inclusivo llamado Mashi, de la Amazonía peruana. La voz debe ser extremadamente dulce, calmada, paciente y cálida, con una cadencia suave y gentil que irradie amabilidad y hospitalidad. Debe sonar naturalmente reconfortante y acogedora, completamente libre de tonos robóticos o corporativos. Muy articulada, optimizada para narración clara y empática en español.",
        "en": "Create a female voice profile for an inclusive AI virtual assistant named Mashi, based in the Peruvian Amazon. The voice must be extremely sweet, calm, patient, and warm, with a smooth and gentle cadence that radiates friendliness and hospitality. It should sound naturally soothing and welcoming, completely devoid of any robotic or dry corporate tones. Highly articulate, optimized for clear and empathetic text-to-speech storytelling and multilingual interaction (Spanish, English, and Indigenous languages).",
        "qw": "Sumak, k'acha warmi shimita ruray, Mashi sutiyuq, Amazonía manta. Voz extremadamente dulce, calmada, paciente y cálida, con cadencia suave que irradie amabilidad. Sin tonos robóticos. Voz femenina clara y empática."
    }

    # 1) Qwen3-TTS — voice design (voz consistente vía descripción)
    qwen_lang = qwen_langs.get(lang, "Spanish")
    qwen_prompt = qwen_prompts.get(lang, qwen_prompts["es"])
    qwen_kwargs = [{"token": t} for t in hf_tokens]
    qwen_kwargs.append({})
    for kwargs in qwen_kwargs:
        for attempt in range(2):
            try:
                client = Client("https://qwen-qwen3-tts.hf.space", verbose=False, **kwargs)
                result = client.predict(text, qwen_lang, qwen_prompt, api_name="/generate_voice_design")
                audio_data = None
                if isinstance(result, (list, tuple)) and len(result) == 2 and isinstance(result[0], (int, float)):
                    import numpy as np, wave
                    sr, wav = result
                    if hasattr(wav, 'dtype'):
                        wav = (wav * 32767).astype(np.int16) if wav.dtype == np.float32 else wav
                        buf = io.BytesIO()
                        with wave.open(buf, 'wb') as wf:
                            wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(int(sr))
                            wf.writeframes(wav.tobytes())
                        audio_data = buf.getvalue()
                        audio_cache[cache_key] = audio_data
                        return audio_data
                if isinstance(result, (list, tuple)):
                    raw = result[0]
                    if isinstance(raw, str):
                        audio_data = raw
                    elif isinstance(raw, dict) and "path" in raw:
                        audio_data = raw["path"]
                elif isinstance(result, dict):
                    for k in ("audio", "path", "value"):
                        if k in result:
                            raw = result[k]
                            if isinstance(raw, str):
                                audio_data = raw
                            break
                if audio_data and isinstance(audio_data, str):
                    if os.path.exists(audio_data):
                        with open(audio_data, "rb") as f:
                            data = f.read()
                        audio_cache[cache_key] = data
                        return data
            except Exception:
                if attempt == 0:
                    continue
                break

    # 2) Fallback gTTS (voz Google, calidad natural)
    try:
        lang_map = {"es": "es", "en": "en", "qw": "es"}
        tts = gTTS(text, lang=lang_map.get(lang, "es"), slow=False)
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        data = buf.getvalue()
        audio_cache[cache_key] = data
        return data
    except Exception:
        return None

def _impact_metrics():
    """Compute MAPPED impact metrics from dataset."""
    ds = get_full_dataset()
    total_comms = len(ds)
    total_prods = sum(len(e.get("products", [])) for e in ds)
    total_reviews = sum(len(e.get("reviews", [])) for e in ds)
    total_years = sum(int(y) for e in ds if not isinstance(y := e.get("years_selling", 0), str))
    total_revenue_est = 0
    for e in ds:
        for p in e.get("products", []):
            n_reviews = len(e.get("reviews", []))
            est_sales = max(1, n_reviews) * 15
            total_revenue_est += p["price"] * est_sales
    families = total_comms * 3
    return total_comms, total_prods, total_reviews, total_years, round(total_revenue_est), families

def _trend_badge(prod, ent):
    """Return (emoji, label, color) for a product based on demand & price."""
    n_reviews = len(ent.get("reviews", []))
    avg_price = 0; count = 0
    for p in ent.get("products", []):
        avg_price += p["price"]; count += 1
    avg_price = avg_price / count if count else 1
    ratio = prod["price"] / avg_price if avg_price else 1
    if n_reviews >= 3 and ratio <= 1.0:
        return "🔥", "Alta demanda", "#ef4444"
    if n_reviews >= 2:
        return "📈", "Popular", "#f59e0b"
    if ratio <= 0.85:
        return "💚", "Precio justo", "#10b981"
    return None, None, None

def _render_product_detail(prod, ent, idx):
    """Render a detailed view of a product with storytelling, reviews and WhatsApp."""
    L = st.session_state.get("lang", "es")
    community_name = ent.get("name", "")
    phone = PHONE_CONTACTS.get(community_name, "+51965010000")
    wa_msg = f"¡Hola! Quiero comprar: {prod['name']} - S/ {prod['price']:.2f} de {community_name}. ¿Está disponible?"
    wa_link = _wa_link(wa_msg)
    img_html = _get_product_image(ent, prod, "180px")

    reviews_html = ""
    for r in ent.get("reviews", [])[:3]:
        filled = "★" * r["stars"] + "☆" * (5 - r["stars"])
        reviews_html += f'<div style="padding:0.3rem 0;border-bottom:1px solid rgba(16,185,129,0.06);"><span style="color:#fbbf24;font-size:0.75rem;">{filled}</span> <span style="font-size:0.65rem;color:rgba(148,163,184,0.6);">{r["user"]}</span><div style="font-size:0.7rem;color:rgba(148,163,184,0.4);">{r["text"][:80]}</div></div>'

    # Price comparison
    similar_prods = []
    for e2 in get_full_dataset():
        if e2["sector"] == ent["sector"] and e2["name"] != community_name:
            for p2 in e2.get("products", []):
                similar_prods.append(p2["price"])
    avg_market = sum(similar_prods) / len(similar_prods) if similar_prods else prod["price"]
    badge_color = "#10b981" if prod["price"] <= avg_market else "#f59e0b"

    story = ent.get("description", prod.get("description", ""))
    materials = ent.get("materials", "")
    years = ent.get("years_selling", 0)

    # Impact calculator per product
    n_reviews = len(ent.get("reviews", []))
    families_supported = max(1, n_reviews * 2 // 3)
    trees = max(2, n_reviews * 3)
    revenue_gen = prod["price"] * max(5, n_reviews * 3)

    # Artisan story text (short, for TTS — cached, gTTS fallback is free)
    story_short = f"{prod['name']} de {community_name}. {story[:120]}"
    story_key = f"_story_audio_{hash(story_short)}"
    story_audio_data = st.session_state.get(story_key)

    impact_calc = f"""
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:4px;margin:0.5rem 0 0.8rem;">
      <div style="text-align:center;background:rgba(16,185,129,0.06);border-radius:14px;padding:0.4rem;">
        <div style="font-size:0.9rem;font-weight:800;color:#10b981;">{families_supported}</div>
        <div style="font-size:0.45rem;color:rgba(148,163,184,0.4);text-transform:uppercase;letter-spacing:0.5px;">{_L("Familias","Families","Ayllu")}</div>
      </div>
      <div style="text-align:center;background:rgba(139,92,246,0.06);border-radius:10px;padding:0.4rem;">
        <div style="font-size:0.9rem;font-weight:800;color:#8B5CF6;">{trees}</div>
        <div style="font-size:0.45rem;color:rgba(148,163,184,0.4);text-transform:uppercase;letter-spacing:0.5px;">{_L("Árboles","Trees","Sachakuna")}</div>
      </div>
      <div style="text-align:center;background:rgba(251,191,36,0.06);border-radius:10px;padding:0.4rem;">
        <div style="font-size:0.9rem;font-weight:800;color:#fbbf24;">S/{revenue_gen:.0f}</div>
        <div style="font-size:0.45rem;color:rgba(148,163,184,0.4);text-transform:uppercase;letter-spacing:0.5px;">{_L("Impacto","Impact","Atipay")}</div>
      </div>
    </div>
    """

    # Render sound button — use browser SpeechSynthesis (free, no tokens) for ambient ambiance
    ambient_id = f"ambient_{ent.get('id','')}"
    sound_btn = f"""
    <div style="display:flex;gap:6px;margin:0.5rem 0;">
      <button onclick="
        var t = this.nextElementSibling;
        if (t && t.tagName==='DIV') {{
          if (t.style.display==='block') {{ t.style.display='none'; this.innerText='🔊 {_L('Escuchar historia','Hear story','Willayta uyariy')}'; }}
          else {{
            t.style.display='block';
            this.innerText='🔊 {_L('Detener','Stop','Sayay')}';
            var u = new SpeechSynthesisUtterance('{story_short[:200].replace(chr(34),'').replace(chr(39),'').replace(chr(10),' ')}');
            u.lang='es-ES'; u.rate=0.88; u.pitch=1.0;
            u.onend = function() {{ t.style.display='none'; this.innerText='🔊 {_L('Escuchar historia','Hear story','Willayta uyariy')}'; }};
            window.speechSynthesis.cancel(); window.speechSynthesis.speak(u);
          }}
        }}" style="flex:1;background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.2);border-radius:10px;color:#e2e8f0;padding:0.4rem 0.6rem;font-size:0.75rem;cursor:pointer;">🔊 {_L("Escuchar historia","Hear story","Willayta uyariy")}</button>
      <div style="display:none;text-align:center;font-size:0.65rem;color:rgba(148,163,184,0.4);padding:0.3rem;">🎵 {_L("Reproduciendo...","Playing...","Uyariy...")}</div>
    </div>
    """

    return f"""
    <div style="background:linear-gradient(135deg,#0a2b1f,#0d3526);border:1px solid rgba(16,185,129,0.2);border-radius:28px;padding:1.2rem;margin-bottom:1rem;box-shadow:0 4px 24px rgba(0,0,0,0.15),0 0 0 1px rgba(16,185,129,0.03);backdrop-filter:blur(4px);">
      {img_html}
      <div style="font-size:1.1rem;font-weight:700;color:#fff;margin-bottom:0.2rem;">{prod['name']}</div>
      <div style="font-size:0.7rem;color:rgba(148,163,184,0.5);margin-bottom:0.5rem;">📍 {community_name} · {ent.get("sector","")} · {years} {_L("años","years","watakuna")}</div>
      <div style="display:flex;gap:8px;margin-bottom:0.5rem;">
        <span style="background:rgba(16,185,129,0.1);color:#10b981;font-size:0.9rem;font-weight:700;padding:0.2rem 0.8rem;border-radius:20px;">S/ {prod['price']:.2f}</span>
        <span style="background:{badge_color}22;color:{badge_color};font-size:0.65rem;padding:0.2rem 0.6rem;border-radius:20px;">📊 Mercado: S/ {avg_market:.2f}</span>
      </div>
      {impact_calc}
      <div style="font-size:0.8rem;color:rgba(148,163,184,0.7);margin-bottom:0.5rem;padding:0.5rem;background:rgba(16,185,129,0.04);border-radius:12px;">{story[:200]}</div>
      {'<div style="font-size:0.65rem;color:rgba(148,163,184,0.4);margin-bottom:0.5rem;">🧵 ' + materials + '</div>' if materials else ""}
      {sound_btn}
      <div style="margin-bottom:0.8rem;">
        <div style="font-size:0.7rem;font-weight:600;color:rgba(148,163,184,0.4);margin-bottom:0.3rem;">{_L("Reseñas","Reviews","Willaykuna")}</div>
        {reviews_html or '<div style="font-size:0.7rem;color:rgba(148,163,184,0.3);">' + _L("Sin reseñas aún","No reviews yet","Mana willaykuna") + '</div>'}
      </div>
      <a href="{wa_link}" target="_blank" style="display:block;text-align:center;background:#25D366;color:#fff;font-weight:700;padding:0.6rem;border-radius:16px;text-decoration:none;font-size:0.85rem;transition:all 0.2s ease;box-shadow:0 4px 16px rgba(37,211,102,0.2);" onmouseover="this.style.transform='translateY(-1px)';this.style.boxShadow='0 6px 24px rgba(37,211,102,0.3)';" onmouseout="this.style.transform='';this.style.boxShadow='0 4px 16px rgba(37,211,102,0.2)';">📱 {_L("Comprar por WhatsApp","Buy via WhatsApp","WhatsApppi rantiy")}</a>
    </div>
    """

def render_ecotourist():
    L = st.session_state.get("lang", "es")
    online = _is_online()
    status_text = _L("En línea · Gemini activo","Online · Gemini active","Kaypi · Gemini kan") if online else _L("🌐 Modo offline · datos locales","🌐 Offline · local data","🌐 Offline · kaymanta willay")
    status_class = "online" if online else "offline"

    # Impact metrics banner
    tc, tp, tr, ty, rev, fam = _impact_metrics()
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0a2b1f,#0d3526);border:1px solid rgba(16,185,129,0.15);border-radius:28px;padding:1rem;margin-bottom:1rem;box-shadow:0 4px 24px rgba(0,0,0,0.12),0 0 0 1px rgba(16,185,129,0.03);backdrop-filter:blur(4px);">
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:0.5rem;text-align:center;">
        <div><div style="font-size:1.1rem;font-weight:800;color:#10b981;">{tc}</div><div style="font-size:0.5rem;color:rgba(148,163,184,0.4);text-transform:uppercase;letter-spacing:1px;">{_L("Comunidades","Communities","Llaktakuna")}</div></div>
        <div><div style="font-size:1.1rem;font-weight:800;color:#fbbf24;">{tp}</div><div style="font-size:0.5rem;color:rgba(148,163,184,0.4);text-transform:uppercase;letter-spacing:1px;">{_L("Productos","Products","Rurakuna")}</div></div>
        <div><div style="font-size:1.1rem;font-weight:800;color:#8B5CF6;">S/{rev//1000}k</div><div style="font-size:0.5rem;color:rgba(148,163,184,0.4);text-transform:uppercase;letter-spacing:1px;">{_L("Impacto","Impact","Atipay")}</div></div>
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.5rem;text-align:center;margin-top:0.5rem;padding-top:0.5rem;border-top:1px solid rgba(16,185,129,0.08);">
        <div><div style="font-size:0.9rem;font-weight:700;color:#10b981;">{fam}</div><div style="font-size:0.5rem;color:rgba(148,163,184,0.4);text-transform:uppercase;letter-spacing:1px;">{_L("Familias","Families","Ayllukuna")}</div></div>
        <div><div style="font-size:0.9rem;font-weight:700;color:#10b981;">{tr}</div><div style="font-size:0.5rem;color:rgba(148,163,184,0.4);text-transform:uppercase;letter-spacing:1px;">{_L("Reseñas","Reviews","Willaykuna")}</div></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="chat-header"><div class="mashi-avatar mashi-avatar-img"></div><div><div class="mashi-name">Mashi</div><div class="mashi-status {status_class}">{status_text}</div></div></div>', unsafe_allow_html=True)
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [{"role":"assistant","content":_greeting_msg()}]
    processing = st.session_state.get("mashi_processing", False)
    # Build chat HTML + CSS + JS for iframe
    chat_css = '''
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800&display=swap');
    *{box-sizing:border-box;margin:0;padding:0}
    body{background:transparent!important;font-family:'Nunito','Outfit','Inter',-apple-system,sans-serif;color:#e2e8f0;padding:0;letter-spacing:0}
    .chat-container{display:flex;flex-direction:column;gap:12px;padding:1rem 1rem;min-height:400px;max-height:500px;overflow-y:auto;scroll-behavior:smooth}
    .bubble-row{display:flex;align-items:flex-end;gap:8px;margin-bottom:2px;animation:bubbleIn 0.4s cubic-bezier(0.21,1.02,0.73,1)}
    .bubble-row.mashi{justify-content:flex-start}
    .bubble-row.user{justify-content:flex-end}
    .chat-bubble-mashi{background:linear-gradient(135deg,#0a1f1a,#0d261f);border:1px solid rgba(16,185,129,0.12);border-radius:16px 16px 16px 4px;padding:14px 18px;max-width:75%;color:#e2e8f0;font-size:0.9rem;font-family:'Nunito',sans-serif;font-weight:500;line-height:1.7;letter-spacing:0;box-shadow:0 4px 16px rgba(0,0,0,0.2),0 0 40px rgba(16,185,129,0.03);position:relative}
    .chat-bubble-user{background:linear-gradient(135deg,#0d3b2c,#0f4a34);border:1px solid rgba(16,185,129,0.15);border-radius:16px 16px 4px 16px;padding:14px 18px;max-width:75%;color:#e2e8f0;font-size:0.85rem;font-family:'Nunito',sans-serif;font-weight:500;line-height:1.65;box-shadow:0 4px 16px rgba(0,0,0,0.15)}
    .bubble-avatar{width:32px;height:32px;border-radius:50%;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-size:1rem;overflow:hidden;transition:transform 0.3s cubic-bezier(0.34,1.56,0.64,1)}
    .bubble-row:hover .bubble-avatar{transform:scale(1.08)}
    .bubble-avatar.user{background:rgba(16,185,129,0.15);font-size:1.2rem;border:1.5px solid rgba(16,185,129,0.2)}
    .mashi-avatar-img{background:url('data:image/jpeg;base64,{B64}') center/cover no-repeat;width:32px;height:32px;border-radius:50%;flex-shrink:0;border:1.5px solid rgba(16,185,129,0.3);box-shadow:0 0 12px rgba(16,185,129,0.1)}
    .speaker-btn{background:none;border:none;cursor:pointer;font-size:0.85rem;padding:4px;opacity:0.35;transition:all 0.25s;border-radius:8px;flex-shrink:0;line-height:1;margin-left:2px;transform:scale(1)}
    .speaker-btn:hover{opacity:1!important;background:rgba(16,185,129,0.12);transform:scale(1.1)}
    .typing-bubble{background:linear-gradient(135deg,#0a1f1a,#0d261f);border:1px solid rgba(16,185,129,0.1);border-radius:16px;padding:14px 20px;display:flex;gap:5px;align-items:center;box-shadow:0 4px 16px rgba(0,0,0,0.15)}
    .typing-dot{width:7px;height:7px;background:#10b981;border-radius:50%;animation:typingBounce 1.4s infinite ease-in-out;box-shadow:0 0 6px rgba(16,185,129,0.3)}
    .typing-dot:nth-child(2){animation-delay:0.2s}
    .typing-dot:nth-child(3){animation-delay:0.4s}
    @keyframes bubbleIn{from{opacity:0;transform:translateY(12px) scale(0.95)}to{opacity:1;transform:translateY(0) scale(1)}}
    @keyframes typingBounce{0%,60%,100%{transform:translateY(0);opacity:0.35}30%{transform:translateY(-6px);opacity:1}}
    ::-webkit-scrollbar{width:3px}
    ::-webkit-scrollbar-track{background:transparent}
    ::-webkit-scrollbar-thumb{background:rgba(16,185,129,0.2);border-radius:4px}
    ::-webkit-scrollbar-thumb:hover{background:rgba(16,185,129,0.35)}
    '''
    def _md2html(t):
        return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    lang_code = "en-US" if L == "en" else "es-ES"
    bubbles = ''
    for i, msg in enumerate(st.session_state.chat_messages):
        content_html = _md2html(msg["content"])
        if msg["role"]=="assistant":
            bubbles += '<div class="bubble-row mashi"><div class="bubble-avatar mashi-avatar-img"></div><div class="chat-bubble-mashi">' + content_html + '</div><button class="speaker-btn" onclick="var el=this.parentElement.querySelector(\'.chat-bubble-mashi\');var t=el.innerText.replace(/[\\u{1F300}-\\u{1FAFF}\\u{2600}-\\u{27BF}\\u{1F50A}\\u{1F399}\\u{1F31F}]+/g,\'\').replace(/https?:\\/\\/\\S+/g,\'\').replace(/<[^>]+>/g,\'\').replace(/!\\[.*?\\]\\(.*?\\)/g,\'\').replace(/\\b\\w+\\.(jpg|jpeg|png|gif|webp|bmp|svg)\\b/g,\'\').replace(/\\s+/g,\' \').trim();if(t){var u=new SpeechSynthesisUtterance(t);u.lang=\'' + lang_code + '\';u.rate=0.92;u.pitch=1.1;u.volume=1.0;window.speechSynthesis.cancel();window.speechSynthesis.speak(u);}">🔊</button></div>'
        else:
            bubbles += '<div class="bubble-row user"><div class="chat-bubble-user">' + content_html + '</div><div class="bubble-avatar user">👤</div></div>'
    if processing:
        bubbles += '<div class="bubble-row mashi"><div class="bubble-avatar mashi-avatar-img"></div><div class="typing-bubble"><span class="typing-dot"></span><span class="typing-dot"></span><span class="typing-dot"></span></div></div>'
    iframe_css = chat_css.replace("{B64}", MASHI_LOGO_B64)
    iframe_html = f'<html><head><style>{iframe_css}</style></head><body><div class="chat-container" id="c">{bubbles}</div><script>var c=document.getElementById("c");if(c)c.scrollTop=c.scrollHeight</script></body></html>'
    st.components.v1.html(iframe_html, height=380, scrolling=True)
    # ── Voz natural edge-tts ──
    assistant_msgs = [m for m in st.session_state.chat_messages if m["role"]=="assistant"]
    if assistant_msgs and not processing:
        last_txt = assistant_msgs[-1]["content"]
        if st.button(_L("🎙️ Voz natural","🎙️ Natural voice","🎙️ Alli voz"), key="speak_mashi", use_container_width=True):
            st.session_state["_speak_pending"] = last_txt
    if "_speak_pending" in st.session_state:
        txt = st.session_state.pop("_speak_pending")
        with st.spinner(_L("Generando voz...","Generating voice...","Vozta ruray...")):
            audio = _tts_generate(txt, L)
        if audio:
            st.audio(audio, format="audio/mp3")
        else:
            st.warning(_L("No se pudo generar la voz. Verifica tu conexión a internet.","Could not generate voice. Check your internet connection.","Vozta mana atin. Internetta rikuy."))
    # Processing pipeline
    pending = st.session_state.pop("_pending_send", None)
    if pending and not processing:
        st.session_state.chat_messages.append({"role":"user","content":pending})
        st.session_state["mashi_processing"] = True
        st.rerun()
    if processing:
        user_msgs = [m for m in st.session_state.chat_messages if m["role"]=="user"]
        if user_msgs:
            last_user = user_msgs[-1]["content"]
            history = st.session_state.chat_messages[:-1]
            try:
                r = get_mashi_response(last_user, "Ecoturista", history, st.session_state.get("api_key",""))
            except Exception as e:
                ds = get_full_dataset()
                r = mock_response(last_user, "Ecoturista", ds) + _offline_tag()
            r = _inject_product_images(r, get_full_dataset())
            # Eliminar respuestas assistant tras el último user message (evita duplicados)
            last_user_pos = len(st.session_state.chat_messages) - 1
            while last_user_pos >= 0 and st.session_state.chat_messages[last_user_pos]["role"] != "user":
                last_user_pos -= 1
            if last_user_pos >= 0:
                st.session_state.chat_messages = st.session_state.chat_messages[:last_user_pos + 1]
            st.session_state.chat_messages.append({"role":"assistant","content":r})
            st.session_state["mashi_processing"] = False
            st.rerun()
    # Suggestions (only at conversation start)
    if not processing and len(st.session_state.chat_messages) <= 2:
        sug = _L(
            ["🌴 ¿Qué hacer en Iquitos?","🛍️ Ver productos","🗺️ Rutas disponibles","⭐ Mis favoritos"],
            ["🌴 What to do in Iquitos?","🛍️ See products","🗺️ Available routes","⭐ My favorites"],
            ["🌴 Iquitospi ima ruray?","🛍️ Rurakunata rikuna","🗺️ Ñankuna","⭐ Munashkaykuna"])
        with st.container():
            cols = st.columns(4)
            for i, s in enumerate(sug):
                if cols[i].button(s, key=f"sug_{i}", use_container_width=True):
                    st.session_state["_pending_send"] = s
                    st.rerun()
    inp = st.chat_input(T("chat_ph"), key="chat_input_main")
    if inp and not processing:
        st.session_state["_pending_send"] = inp
        st.rerun()
    # Favorites section
    favs = st.session_state.get("favorites", [])
    ds = get_full_dataset()
    if not processing:
        with st.expander(_L("⭐ Mis favoritos","⭐ My favorites","⭐ Munashkaykuna") + f" ({len(favs)})", expanded=False):
            if not favs:
                st.markdown(f'<div style="color:rgba(148,163,184,0.4);font-size:0.8rem;text-align:center;padding:1rem;">{_L("Guarda comunidades tocando ⭐","Save communities by tapping ⭐","Llaktakunata ⭐ sintipi allichay")}</div>', unsafe_allow_html=True)
            else:
                for eid in list(favs):
                    ent = next((e for e in ds if e.get("id") == eid), None)
                    if not ent: continue
                    col1, col2, col3 = st.columns([3,1,1])
                    with col1:
                        st.markdown(f'<span style="font-size:0.85rem;">⭐ **{ent["name"][:50]}**<br><span style="font-size:0.7rem;color:rgba(148,163,184,0.5);">{ent["location"]}</span></span>', unsafe_allow_html=True)
                    with col2:
                        if st.button("📍", key=f"fav_map_{eid}", help=_L("Ver en mapa","View on map","Mapapi rikuna")):
                            st.session_state["selected_ent_id"] = eid
                            st.session_state["_nav_rkey"] = "Mapa"
                            st.rerun()
                    with col3:
                        if st.button("✕", key=f"fav_del_{eid}", help=_L("Quitar","Remove","Qichuna")):
                            favs.remove(eid)
                            st.rerun()
        # ── Route planner ──
        planner_ids = st.session_state.get("planner_ids", [])
        st.markdown(f'<div style="margin:0.5rem 0;"><span style="font-size:0.8rem;font-weight:600;color:rgba(16,185,129,0.7);">🗺️ {_L("Planificador de ruta","Route planner","Ñan allichak")}</span></div>', unsafe_allow_html=True)
        all_names = [(e["id"], f'{e["name"][:45]} — {e["location"][:20]}') for e in ds]
        selected_names = st.multiselect(
            _L("Selecciona comunidades para visitar","Select communities to visit","Llaktakunata akllay"),
            options=[n for _,n in all_names],
            default=[n for i,n in all_names if i in planner_ids],
            key="planner_multi", label_visibility="collapsed")
        planner_ids_new = [i for i,n in all_names if n in selected_names]
        if planner_ids_new != planner_ids:
            st.session_state["planner_ids"] = planner_ids_new
            st.rerun()
        if planner_ids_new:
            planner_ents = [e for e in ds if e["id"] in planner_ids_new]
            # Nearest-neighbor sort from Iquitos
            ordered = sorted(planner_ents, key=lambda e: _dist_from_iquitos(e))
            st.session_state["planner_route"] = [e["id"] for e in ordered]
            # Calculate total distance first
            total_km = 0
            prev = (-3.7491, -73.2442)
            for e in ordered:
                total_km += _haversine(prev[0], prev[1], e["lat"], e["lng"])
                prev = (e["lat"], e["lng"])
            # Budget estimate
            transport_cost = total_km * 1.5
            food_per_day = 25 * len(ordered)
            avg_product_price = sum(p["price"] for e in ordered for p in e.get("products",[])) / max(1, sum(len(e.get("products",[])) for e in ordered))
            shopping_est = avg_product_price * 0.7 * len(ordered)
            total_budget = transport_cost + food_per_day + shopping_est
            # Recommended product per community
            rec_products = ""
            for e in ordered:
                best = max(e.get("products",[]), key=lambda p: len([r for r in e.get("reviews",[]) if r.get("text","")]), default=None)
                if best:
                    rec_products += f'<span style="font-size:0.65rem;color:rgba(148,163,184,0.4);margin-right:4px;">📍 {e["name"][:18]}: <b>{best["name"][:22]}</b> S/ {best["price"]:.0f}</span><br>'

            st.markdown(f'<div style="background:#0a1f1a;border:1px solid rgba(16,185,129,0.15);border-radius:20px;padding:0.8rem 1rem;font-size:0.8rem;box-shadow:0 4px 20px rgba(0,0,0,0.1),0 0 0 1px rgba(16,185,129,0.02);">', unsafe_allow_html=True)
            for idx, e in enumerate(ordered):
                prev = (-3.7491, -73.2442) if idx == 0 else (ordered[idx-1]["lat"], ordered[idx-1]["lng"])
                d = _haversine(prev[0], prev[1], e["lat"], e["lng"])
                st.markdown(f'<div style="display:flex;align-items:center;gap:6px;padding:2px 0;"><span style="background:#10b98122;color:#10b981;border-radius:50%;width:20px;height:20px;display:inline-flex;align-items:center;justify-content:center;font-size:0.7rem;font-weight:700;">{idx+1}</span> <b>{e["name"][:40]}</b> <span style="color:rgba(148,163,184,0.4);font-size:0.7rem;">{_format_distance(d)}</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div style="border-top:1px solid rgba(16,185,129,0.15);margin-top:4px;padding-top:4px;font-size:0.75rem;color:rgba(148,163,184,0.6);">🚗 {_L("Total aprox.","Approx. total","Tukuy")} {_format_distance(total_km)} · {len(ordered)} {_L("comunidades","communities","llaktakuna")}</div>', unsafe_allow_html=True)
            # Budget summary
            st.markdown(f'''
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:4px;margin:6px 0 4px;">
              <div style="text-align:center;background:rgba(16,185,129,0.06);border-radius:8px;padding:0.3rem;">
                <div style="font-size:0.7rem;font-weight:700;color:#10b981;">S/ {transport_cost:.0f}</div>
                <div style="font-size:0.45rem;color:rgba(148,163,184,0.4);">{_L("Transporte","Transport","Purina")}</div>
              </div>
              <div style="text-align:center;background:rgba(251,191,36,0.06);border-radius:8px;padding:0.3rem;">
                <div style="font-size:0.7rem;font-weight:700;color:#fbbf24;">S/ {food_per_day:.0f}</div>
                <div style="font-size:0.45rem;color:rgba(148,163,184,0.4);">{_L("Comida","Food","Mikuna")}</div>
              </div>
              <div style="text-align:center;background:rgba(139,92,246,0.06);border-radius:8px;padding:0.3rem;">
                <div style="font-size:0.7rem;font-weight:700;color:#8B5CF6;">S/ {shopping_est:.0f}</div>
                <div style="font-size:0.45rem;color:rgba(148,163,184,0.4);">{_L("Compras","Shopping","Rantiy")}</div>
              </div>
            </div>
            <div style="text-align:center;font-size:0.75rem;font-weight:700;color:#10b981;padding:2px 0 6px;">{_L("Presupuesto estimado","Estimated budget","Tukuy qullqi")}: S/ {total_budget:.0f}</div>
            ''', unsafe_allow_html=True)
            # Recommended products
            if rec_products:
                st.markdown(f'<div style="font-size:0.6rem;color:rgba(148,163,184,0.35);margin:2px 0;">🏆 {_L("Recomendados","Recommended","Allin rurakuna")}:<br>{rec_products}</div>', unsafe_allow_html=True)
            # Download HTML itinerary
            itinerary_html = f"""<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><title>Itinerario MAPPED</title>
            <style>body{{font-family:'Segoe UI',sans-serif;background:#021B15;color:#e2e8f0;max-width:600px;margin:auto;padding:1rem}}
            h1{{color:#10b981;font-size:1.2rem}}table{{width:100%;border-collapse:collapse;margin:1rem 0}}
            th,td{{padding:8px;text-align:left;border-bottom:1px solid rgba(16,185,129,0.12);font-size:0.8rem}}
            th{{color:#10b981;font-size:0.7rem;text-transform:uppercase;letter-spacing:1px}}
            .total{{font-weight:700;color:#10b981;font-size:1rem;text-align:center;padding:1rem}}
            .budget{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;text-align:center;margin:1rem 0}}
            .budget-box{{background:rgba(16,185,129,0.06);border-radius:10px;padding:0.5rem}}
            .budget-val{{font-size:1rem;font-weight:700;color:#10b981}}</style></head><body>
            <h1>🗺️ {_L("Itinerario","Itinerary","Ñan")} MAPPED</h1>
            <p style="color:rgba(148,163,184,0.5);font-size:0.7rem;">{_L("Salida desde Iquitos","Departure from Iquitos","Iquitospa lluqsiy")}</p>
            <table><tr><th>#</th><th>{_L("Comunidad","Community","Llakta")}</th><th>{_L("Distancia","Distance","Karuy")}</th></tr>"""
            cum_km = 0
            prev_ll = (-3.7491, -73.2442)
            for idx, e in enumerate(ordered):
                dd = _haversine(prev_ll[0], prev_ll[1], e["lat"], e["lng"])
                cum_km += dd
                prev_ll = (e["lat"], e["lng"])
                sec = e.get("sector","")
                itinerary_html += f"<tr><td>{idx+1}</td><td><b>{e['name']}</b><br><span style='font-size:0.6rem;color:rgba(148,163,184,0.4);'>{sec}</span></td><td>{cum_km:.1f} km</td></tr>"
            itinerary_html += f"""</table>
            <div class="total">🚗 {_L("Total","Total","Tukuy")}: {total_km:.1f} km · {len(ordered)} {_L("comunidades","communities","llaktakuna")}</div>
            <div class="budget">
              <div class="budget-box"><div class="budget-val">S/ {transport_cost:.0f}</div><div style="font-size:0.6rem;color:rgba(148,163,184,0.4);">{_L("Transporte","Transport","Purina")}</div></div>
              <div class="budget-box"><div class="budget-val">S/ {food_per_day:.0f}</div><div style="font-size:0.6rem;color:rgba(148,163,184,0.4);">{_L("Comida","Food","Mikuna")}</div></div>
              <div class="budget-box"><div class="budget-val">S/ {shopping_est:.0f}</div><div style="font-size:0.6rem;color:rgba(148,163,184,0.4);">{_L("Compras","Shopping","Rantiy")}</div></div>
            </div>
            <div style="text-align:center;font-size:1rem;font-weight:700;color:#10b981;padding:0.5rem;">{_L("Presupuesto total","Total budget","Tukuy qullqi")}: S/ {total_budget:.0f}</div>
            <p style="font-size:0.6rem;color:rgba(148,163,184,0.3);text-align:center;">{_L("Generado por Mashi · MAPPED","Generated by Mashi · MAPPED","Mashi rurashka · MAPPED")}</p>
            </body></html>"""
            st.download_button(
                label=_L("📄 Descargar itinerario","📄 Download itinerary","📄 Ñanta uraykachiy"),
                data=itinerary_html.encode("utf-8"),
                file_name="itinerario_mapped.html",
                mime="text/html",
                key="dl_itinerary",
                use_container_width=True)
            if st.button(_L("📍 Ver ruta en mapa","📍 View route on map","📍 Ñanta mapapi rikuna"), key="goto_planner_map", use_container_width=True):
                st.session_state["_nav_rkey"] = "Mapa"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # Navigate to map / favorite toggle if community selected
    last_ent_id = st.session_state.get("selected_ent_id")
    if not processing and last_ent_id:
        ent = next((e for e in get_full_dataset() if e.get("id") == last_ent_id), None)
        if ent:
            is_fav = last_ent_id in favs
            st.markdown(f'<div style="text-align:center;padding:4px 0;display:flex;gap:4px;justify-content:center;">', unsafe_allow_html=True)
            if st.button("📍 " + _L("Ver en mapa grande","View on big map","Hatun mapapi rikuna"), key="goto_map"):
                st.session_state["_nav_rkey"] = "Mapa"
                st.rerun()
            if st.button("🗺️ " + _L("Mini mapa","Mini map","Mapacha"), key="toggle_mini_map"):
                st.session_state["show_mini_map"] = not st.session_state.get("show_mini_map", False)
                st.rerun()
            star_label = "⭐ " + _L("Guardado","Saved","Allichashka") if is_fav else "☆ " + _L("Guardar","Save","Allichay")
            if st.button(star_label, key="toggle_fav"):
                if is_fav:
                    favs.remove(last_ent_id)
                else:
                    favs.append(last_ent_id)
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

            if st.session_state.get("show_mini_map", False):
                _render_mini_map(ent, get_full_dataset())

            # ── Nearby communities ──
            nearby = _get_nearby_communities(ent, get_full_dataset())
            if nearby:
                st.markdown(f'<div style="margin:0.5rem 0.2rem 0;"><span style="font-size:0.7rem;font-weight:600;color:rgba(16,185,129,0.6);text-transform:uppercase;letter-spacing:1px;">📍 {_L("Cerca de aquí","Nearby","Kaymanta")}</span></div>', unsafe_allow_html=True)
                sector_icons = {"artesanía":"🎭","textiles":"🧣","alimentos":"🍲","madera":"🪵","joyería":"💍",
                                "cerámica":"🏺","cestería":"🧺","bordados":"🪡","tallado":"🗿"}
                max_cols = 3
                for row_idx in range(0, len(nearby), max_cols):
                    row = nearby[row_idx:row_idx+max_cols]
                    cols_near = st.columns(len(row))
                    for ci, (d, ne) in enumerate(row):
                        sector = (ne.get("sector") or "").lower()
                        icon = "🏕️"
                        for kw, ico in sector_icons.items():
                            if kw in sector:
                                icon = ico
                                break
                        prod_str = ", ".join(p["name"][:18] for p in ne.get("products", [])[:2])
                        with cols_near[ci]:
                            st.markdown(f'<div class="nearby-card" style="background:#0a1f1a;border:1px solid rgba(16,185,129,0.12);border-radius:12px;padding:0.45rem;text-align:center;font-size:0.68rem;transition:all 0.2s;cursor:pointer;">'
                                f'<div style="font-size:1.2rem;margin-bottom:2px;">{icon}</div>'
                                f'<div style="font-weight:700;color:#e2e8f0;font-size:0.72rem;line-height:1.2;">{ne["name"][:22]}</div>'
                                f'<div style="color:rgba(148,163,184,0.5);margin-top:3px;font-size:0.65rem;">🚗 {_format_distance(d)} · <span style="color:rgba(148,163,184,0.4);">{ne["location"][:15]}</span></div>'
                                f'<div style="color:rgba(16,185,129,0.35);font-size:0.6rem;margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{prod_str}</div>'
                                f'<div style="margin-top:4px;">'
                                f'<span style="background:rgba(16,185,129,0.08);color:rgba(16,185,129,0.5);border-radius:12px;padding:0.08rem 0.5rem;font-size:0.58rem;">{len(ne.get("products",[]))} {_L("prod.","prod.","rur.")} · ★ {round(sum(r["stars"] for r in ne.get("reviews",[]))/len(ne["reviews"]),1) if ne.get("reviews") else "—"}</span>'
                                f'</div></div>', unsafe_allow_html=True)
                            if st.button("", key=f"near_{ne['id']}", help=_L("Explorar","Explore","Rikuy"), label_visibility="collapsed"):
                                st.session_state["selected_ent_id"] = ne["id"]
                                st.session_state["_nav_rkey"] = "Mapa"
                                st.rerun()

    # Clear chat
    if not processing and len(st.session_state.chat_messages) > 2:
        st.markdown('<div style="text-align:center;padding:4px 0;">', unsafe_allow_html=True)
        if st.button(_L("🗑️ Limpiar chat","🗑️ Clear chat","🗑️ Pichana"), key="clear_chat", help=_L("Reiniciar conversación","Reset conversation","Musuq rimay")):
            st.session_state.chat_messages = [{"role":"assistant","content":_greeting_msg()}]
            st.session_state["selected_ent_id"] = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ========================================================================
# EMPRENDEDOR LOCAL — PERFIL + FORMULARIO + DASHBOARD
# ========================================================================
def _confirm_product(pending):
    """Finaliza la publicación de un producto con el precio final."""
    pname = pending["name"]
    psector = pending["sector"]
    pdesc = pending["desc"]
    pstory = pending.get("story", "")
    final_price = pending.get("final_price", pending["suggested"])
    pimg_bytes = pending.get("img_bytes")
    ne = {"id":100+len(st.session_state.get("new_entrepreneurs",[])),"name":f"{pname} - {st.session_state.get('user_name','Emprendedor')}",
          "location":"Loreto, Perú","zone":"Amazonía Norte","address":"Loreto, Perú",
          "lat":-3.7491,"lng":-73.2442,"years_selling":"Nuevo","sector":psector,
          "sector_keywords":pname.lower().split()+[psector.lower()],"description":pdesc,"story":pstory,
          "products":[{"name":pname,"price":final_price,"currency":"S/","description":pdesc,"story":pstory}],
          "reviews":[],"logistics_notes":"Nuevo emprendedor en MAPPED.","materials":"Artesanal"}
    st.session_state.setdefault("new_entrepreneurs",[]).append(ne)
    if pimg_bytes:
        st.session_state.setdefault("product_images",{})[pname] = pimg_bytes
    L = st.session_state.get("lang", "es")
    st.balloons()
    success_msg = _L(f'"{pname}" ya está disponible en MAPPED.',
                     f'"{pname}" is now available on MAPPED.',
                     f'"{pname}" MAPPEDpi tiyan.')
    st.markdown(f'<div style="background:#0a1f1a;border:1px solid rgba(16,185,129,0.2);border-radius:16px;padding:1.5rem;text-align:center;margin-top:1rem;"><span style="font-size:2.5rem;">🌟</span><h3 style="color:#10b981!important;margin:0.5rem 0;font-weight:700;">{KICHWA["gracias"]}, mashi!</h3><p style="color:rgba(148,163,184,0.7)!important;font-size:0.9rem;">{success_msg} 🦥🌿</p></div>', unsafe_allow_html=True)
    add_btn = _L("➕ Publicar otro producto","➕ Add another product","➕ Shuk rurata churay")
    if st.button(add_btn, use_container_width=True):
        st.session_state["modifying_price"] = False
        st.rerun()
    market_btn = _L("🛍️ Ver en MAPPED","🛍️ View on MAPPED","🛍️ MAPPEDpi rikuna")
    if st.button(market_btn, use_container_width=True):
        st.session_state["_nav_rkey"] = _L("Ecoturista","Ecotourist","Ecoturista")
        st.rerun()

def render_emprendedor():
    L = st.session_state.get("lang", "es")
    st.markdown(f'<div style="padding:1rem 1rem 0.5rem"><h2 class="section-title">🌿 {T("role_emp")}</h2></div>', unsafe_allow_html=True)

    # ── Profile card ──
    user_name = st.session_state.get("user_name", "")
    productos = st.session_state.get("new_entrepreneurs", [])
    total_prods = len(productos)
    purchases = st.session_state.get("purchases", [])
    prod_names = set()
    for p in productos:
        for prod in p.get("products", []):
            prod_names.add(prod["name"])
    veces_guardado = sum(1 for pu in purchases if pu.get("product") in prod_names)
    initial = (user_name[0] if user_name else "👤").upper()
    avatar_html = initial if user_name else "🌿"
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0a2b1f,#0d3526);border:1px solid rgba(16,185,129,0.2);
         border-radius:20px;padding:1.5rem;margin-bottom:1rem;display:flex;align-items:center;gap:1rem;">
      <div style="width:64px;height:64px;border-radius:50%;background:rgba(16,185,129,0.15);
           border:2px solid rgba(16,185,129,0.3);overflow:hidden;flex-shrink:0;
           display:flex;align-items:center;justify-content:center;font-size:1.8rem;color:#10b981;font-weight:700;">{avatar_html}</div>
      <div style="flex:1;">
        <div style="font-size:1.1rem;font-weight:700;color:#fff;">{user_name or _L("Emprendedor","Entrepreneur","Ruraq")}</div>
        <div style="font-size:0.75rem;color:rgba(148,163,184,0.5);">{_L("Miembro MAPPED","MAPPED Member","MAPPEDpi kan")}</div>
      </div>
      <div style="display:flex;gap:1.2rem;text-align:center;">
        <div><div style="font-size:1.3rem;font-weight:700;color:#10b981;">{total_prods}</div><div style="font-size:0.6rem;color:rgba(148,163,184,0.4);text-transform:uppercase;">{_L("Productos","Products","Rurakuna")}</div></div>
        <div><div style="font-size:1.3rem;font-weight:700;color:#F59E0B;">{veces_guardado}</div><div style="font-size:0.6rem;color:rgba(148,163,184,0.4);text-transform:uppercase;">{_L("Guardados","Saved","Allichashka")}</div></div>
        <div><div style="font-size:1.3rem;font-weight:700;color:#8B5CF6;">{len(prod_names) * 15 + veces_guardado * 5 + 12}</div><div style="font-size:0.6rem;color:rgba(148,163,184,0.4);text-transform:uppercase;">{_L("Impacto","Impact","Atipay")}</div></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Form ──
    name_label = _L("Nombre del producto *","Product name *","Rura sutin *")
    sector_label = _L("Sector *","Sector *","Sector *")
    price_label = _L("Precio (S/) *","Price (S/) *","Precio (S/) *")
    cat_label = _L("Categoría","Category","Kategoria")
    desc_label = _L("Descripción *","Description *","Willay *")
    story_label = _L("🎙️ Historia / Storytelling","🎙️ Story / Storytelling","🎙️ Willay")
    story_ph = _L("Cuéntanos tu historia... ¿quién te enseñó? ¿qué significa para tu comunidad?",
                   "Tell us your story... who taught you? what does it mean for your community?",
                   "Pitamanta yacharkanki? ¿imatam niyta munanki?")
    publish_btn = _L("🌟 Publicar en MAPPED","🌟 Publish on MAPPED","🌟 MAPPEDpi churay")
    pending = st.session_state.get("pending_product")
    if not pending:
        with st.form("prod_form", clear_on_submit=True):
            col1,col2 = st.columns(2)
            with col1:
                pname = st.text_input(name_label, placeholder=_L("Ej: Jabón de copaiba","Ex: Copaiba soap","Ej: Kopaiba jabon"))
                _sector_display = [_L("Textiles y Artesanía","Textiles & Crafts","Away rura"),_L("Cosméticos Naturales","Natural Cosmetics","Alli kawsay"),_L("Cerámica","Ceramics","Manka rura"),_L("Alimentos","Food","Mikuna"),_L("Otro","Other","Shuk")]
                _sector_canonical = ["Textiles y Artesanía","Cosméticos Naturales","Cerámica","Alimentos","Otro"]
                _sel_disp = st.selectbox(sector_label, [""] + _sector_display)
                psector = _sector_canonical[_sector_display.index(_sel_disp)] if _sel_disp else ""
            with col2:
                pcat = st.text_input(cat_label, placeholder=_L("Ej: Jabones, Ropa","Ex: Soaps, Clothing","Ej: Jabon, Ropa"))
            pdesc = st.text_area(desc_label, placeholder=_L("Describe tu producto...","Describe your product...","Rurayta willay..."), height=90)
            pstory = st.text_area(story_label, placeholder=story_ph, height=100)
            pimg = st.file_uploader(T("upload_label"), type=["png","jpg","jpeg"])
            if pimg:
                st.image(pimg, width=200)
            submitted = st.form_submit_button(publish_btn, use_container_width=True)
        if submitted:
            if not pname or not pdesc or not psector:
                st.error(_L("Completa los campos obligatorios (*).","Fill in all required fields (*).","Kaykunata churay (*)."))
            else:
                suggested, avg_market, demand_level, n_similar, min_p, max_p, trend, confidence, insight = _suggest_price_for_product(pname, psector, get_full_dataset())
                pimg_bytes = pimg.read() if pimg else None
                vision = None
                if pimg_bytes:
                    vision = _analyze_product_image(pimg_bytes)
                if vision and vision.get("visual_price", 0) > 0:
                    blended = round((suggested + vision["visual_price"]) / 2, 1)
                else:
                    blended = suggested
                st.session_state["pending_product"] = {
                    "name": pname, "sector": psector, "cat": pcat, "desc": pdesc,
                    "story": pstory, "img_bytes": pimg_bytes,
                    "suggested": suggested, "avg_market": avg_market,
                    "demand_level": demand_level, "n_similar": n_similar,
                    "min_price": min_p, "max_price": max_p, "trend": trend,
                    "confidence": confidence, "insight": insight,
                    "vision": vision, "blended": blended
                }
                st.rerun()
    else:
        pname = pending["name"]
        psector = pending["sector"]
        pdesc = pending["desc"]
        suggested = pending["suggested"]
        avg_market = pending["avg_market"]
        demand_level = pending["demand_level"]
        n_similar = pending["n_similar"]
        min_p = pending.get("min_price", avg_market * 0.7)
        max_p = pending.get("max_price", avg_market * 1.3)
        trend = pending.get("trend", "📊")
        confidence = pending.get("confidence", "media")
        insight = pending.get("insight", "")
        vision = pending.get("vision")
        blended = pending.get("blended", suggested)
        demand_icon = "🔥" if demand_level == "alta" else "📈" if demand_level == "media" else "🌱"
        demand_lbl = _L({"alta":"Alta","media":"Media","baja":"Baja"}[demand_level],
                        {"alta":"High","media":"Medium","baja":"Low"}[demand_level],
                        {"alta":"Achka","media":"Chawpi","baja":"Aslla"}[demand_level])
        final_suggest = blended if vision else suggested
        vision_badge = ""
        vision_line = ""
        if vision:
            quality_ico = {"alta":"✨","media":"📊","baja":"🌱"}.get(vision.get("quality","media"),"📊")
            quality_txt = _L({"alta":"Alta","media":"Media","baja":"Baja"}[vision.get("quality","media")],
                             {"alta":"High","media":"Medium","baja":"Low"}[vision.get("quality","media")],
                             {"alta":"Alli","media":"Chawpi","baja":"Aslla"}[vision.get("quality","media")])
            vision_badge = f'<span style="background:rgba(139,92,246,0.1);color:#a78bfa;font-size:0.6rem;font-weight:600;padding:0.15rem 0.5rem;border-radius:20px;margin-left:0.3rem;">📸 {_L("Visión IA","AI Vision","Rikuna IA")}</span>'
            vision_line = f"\n📸 Mashi vio: **{vision.get('detected_type','Producto')}** · Calidad {quality_ico} **{quality_txt}**\n📸 Precio estimado por foto: **S/ {vision['visual_price']:.2f}** ({vision.get('reason','')})"
        if L == "en":
            mashi_advice = (f"🦥 **Mashi's market analysis:**{vision_badge}\n\n"
                f"📊 Based on **{n_similar} similar products** in MAPPED:\n"
                f"• Price range: **S/ {min_p:.2f} – S/ {max_p:.2f}** {trend}\n"
                f"• Market average: **S/ {avg_market:.2f}**\n"
                f"• **Mashi suggests:** **S/ {final_suggest:.2f}**\n"
                f"• Demand: {demand_icon} **{demand_lbl}**{insight}{vision_line}\n\n"
                + ({
                    "alta": "🔥 High demand! Tourists are willing to pay more for quality Amazonian crafts.",
                    "media": "📈 Medium demand — good balance. Promote the story behind it!",
                    "baja": "🌱 Low demand — an accessible starting price attracts early buyers."
                }[demand_level])
                + f"\n\n📱 Share your product on WhatsApp and get direct orders! 🦥✨")
        elif L == "qw":
            mashi_advice = (f"🦥 **Mashi nishka:**{vision_badge}\n\n"
                f"📊 {n_similar} shuk rurakunawa rikushpa:\n"
                f"• Rango: S/ {min_p:.2f} – S/ {max_p:.2f} {trend}\n"
                f"• Mercado masna: S/ {avg_market:.2f}\n"
                f"• Mashi sugiere: **S/ {final_suggest:.2f}**\n"
                f"• Munana: {demand_icon} **{demand_lbl}**{vision_line}\n\n"
                f"Rikchata apay, WhatsApppi makipanakuy! 🦥")
        else:
            mashi_advice = (f"🦥 **Análisis de mercado de Mashi:**{vision_badge}\n\n"
                f"📊 He revisado **{n_similar} productos similares** en MAPPED:\n"
                f"• Rango de precios: **S/ {min_p:.2f} – S/ {max_p:.2f}** {trend}\n"
                f"• Precio promedio: **S/ {avg_market:.2f}**\n"
                f"• **Mashi recomienda:** **S/ {final_suggest:.2f}**\n"
                f"• Demanda: {demand_icon} **{demand_lbl}**{insight}{vision_line}\n\n"
                + ({
                    "alta": "🔥 ¡Demanda alta! Tu precio refleja el valor cultural. Los turistas pagan más por autenticidad.",
                    "media": "📈 Demanda media — mercado competitivo. ¡Cuenta la historia de tu producto!",
                    "baja": "🌱 Demanda baja — un precio accesible atrae a los primeros compradores."
                }[demand_level])
                + f"\n\n📱 ¿Sabías que puedes compartir tu producto por WhatsApp? Actívalo y recibe pedidos directos de turistas. 🦥✨")

        st.markdown(f'<div class="glass-card" style="background:#0a1f1a!important;border-color:rgba(16,185,129,0.2)!important;">{mashi_advice}</div>', unsafe_allow_html=True)
        advice_tts_text = _L(
            f"Mashi recomienda un precio de {final_suggest:.2f} soles. "
            f"El precio promedio del mercado es {avg_market:.2f} soles. "
            f"La demanda es {demand_lbl}. "
            + (f"La calidad del producto es {vision.get('quality','media')}. "
               f"Mashi vio: {vision.get('detected_type','')}. "
               f"{vision.get('reason','')}" if vision else ""),
            f"Mashi recommends a price of {final_suggest:.2f} soles. "
            f"The market average price is {avg_market:.2f} soles. "
            f"Demand level is {demand_lbl}. "
            + (f"Product quality is {vision.get('quality','media')}. "
               f"Mashi detected: {vision.get('detected_type','')}. "
               f"{vision.get('reason','')}" if vision else ""),
            f"Mashi nishka: {final_suggest:.2f} sol. "
            f"Mercado masna: {avg_market:.2f} sol. "
            f"Munana: {demand_lbl}. "
            + (f"Allin kay: {vision.get('quality','media')}. "
               f"Mashi rikurka: {vision.get('detected_type','')}. "
               f"{vision.get('reason','')}" if vision else ""))
        if st.button("🔊 " + _L("Mashi te lo explica","Mashi explains it","Mashi willasunki"), key="speak_advice", use_container_width=True):
            st.session_state["_speak_advice_pending"] = advice_tts_text
        if "_speak_advice_pending" in st.session_state:
            _txt = st.session_state.pop("_speak_advice_pending")
            with st.spinner(_L("Mashi está hablando...","Mashi is speaking...","Mashi riman...")):
                _audio = _tts_generate(_txt, L)
            if _audio:
                st.audio(_audio, format="audio/mp3")
            else:
                st.warning(_L("No se pudo generar la voz.","Could not generate voice.","Vozta mana atin."))
        use_suggested = st.button(f"✅ {_L('Aceptar S/ ','Accept S/ ','Chaskiy S/ ')}{final_suggest:.2f}", use_container_width=True)
        if st.button(f"✏️ {_L('Modificar precio','Modify price','Masnata shukchay')}", use_container_width=True):
            st.session_state["modifying_price"] = True
            st.rerun()
        if st.session_state.get("modifying_price"):
            mod_price = st.number_input(_L("Precio final (S/)","Final price (S/)","Tukuy masna (S/)"), min_value=0.5, value=final_suggest, step=0.5, format="%.2f", key="mod_price_input")
            if st.button(f"🚀 {_L('Publicar con S/ ','Publish at S/ ','MAPPEDpi churay S/ ')}{mod_price:.2f}", use_container_width=True):
                final_price = mod_price
                pending["final_price"] = final_price
                st.session_state["pending_product"] = pending
                st.session_state["modifying_price"] = False
                _confirm_product(st.session_state["pending_product"])
                st.session_state.pop("pending_product", None)
                st.rerun()
        if use_suggested:
            pending["final_price"] = final_suggest
            _confirm_product(pending)
            st.session_state.pop("pending_product", None)
            st.rerun()
        if st.button(f"↩️ {_L('Cancelar y empezar de nuevo','Cancel and start over','Musuqta qallarina')}", use_container_width=True):
            st.session_state.pop("pending_product", None)
            st.session_state["modifying_price"] = False
            st.rerun()

    # ── Empty state ──
    if total_prods == 0 and not pending:
        st.markdown(f'<div style="background:rgba(16,185,129,0.04);border:1px dashed rgba(16,185,129,0.15);border-radius:16px;padding:2rem 1.5rem;text-align:center;margin:1rem 0;">'
            f'<div style="font-size:2rem;margin-bottom:0.5rem;">🦥🌿</div>'
            f'<div style="font-size:1rem;font-weight:700;color:#e2e8f0;margin-bottom:0.3rem;">{_L("¡Publica tu primer producto!","Publish your first product!","Kay rurakuna rikuchiy!")}</div>'
            f'<div style="font-size:0.8rem;color:rgba(148,163,184,0.5);">{_L("Usa el formulario de arriba para compartir tu artesanía, cosméticos o alimentos con el mundo.","Use the form above to share your crafts, cosmetics or food with the world.","Kay formulariota apay rurakunata turiskunawan rikuchinkapa.")}</div>'
            f'</div>', unsafe_allow_html=True)

    # ── Dashboard: Mis productos ──
    if total_prods > 0:
        st.markdown(f'<div style="margin:1.5rem 0 0.8rem;"><span style="font-size:1rem;font-weight:700;color:#e2e8f0;">📋 {_L("Mis productos","My products","Rurakunay")}</span> <span style="font-size:0.75rem;color:rgba(148,163,184,0.4);">({total_prods})</span></div>', unsafe_allow_html=True)
        edit_idx = st.session_state.get("editing_prod_idx", -1)
        del_idx = st.session_state.get("deleting_prod_idx", -1)
        img_map = st.session_state.get("product_images", {})
        if 0 <= edit_idx < len(productos):
            pe = productos[edit_idx]
            pd0 = pe.get("products", [{}])[0]
            pname_edit = pd0.get("name", "")
            story_key = f"edit_story_{edit_idx}"
            old_story = pd0.get("story", pe.get("story", ""))
            _existing_img = img_map.get(pname_edit)
            if _existing_img:
                _b64 = base64.b64encode(_existing_img).decode()
                st.markdown(f'<div style="text-align:center;margin-bottom:0.5rem;"><img src="data:image/png;base64,{_b64}" style="width:150px;height:100px;object-fit:cover;border-radius:12px;border:1px solid rgba(16,185,129,0.15);"></div>', unsafe_allow_html=True)
            with st.form(f"edit_prod_{edit_idx}"):
                ename = st.text_input(_L("Nombre","Name","Suti"), value=pname_edit)
                eprice = st.number_input(_L("Precio (S/)","Price (S/)","Masna (S/)"), min_value=0.5, value=pd0.get("price", 0), step=0.5, format="%.2f")
                _edit_sectors = ["Textiles y Artesanía","Cosméticos Naturales","Cerámica","Alimentos","Otro"]
                _sector_map = {"Textiles y Artesanía":"Textiles y Artesanía","Textiles & Crafts":"Textiles y Artesanía","Away rura":"Textiles y Artesanía",
                    "Cosméticos Naturales":"Cosméticos Naturales","Natural Cosmetics":"Cosméticos Naturales","Alli kawsay":"Cosméticos Naturales",
                    "Cerámica":"Cerámica","Ceramics":"Cerámica","Manka rura":"Cerámica",
                    "Alimentos":"Alimentos","Food":"Alimentos","Mikuna":"Alimentos",
                    "Otro":"Otro","Other":"Otro","Shuk":"Otro"}
                _stored_sector = _sector_map.get(pe.get("sector","Otro"), pe.get("sector","Otro"))
                _es_idx = _edit_sectors.index(_stored_sector) if _stored_sector in _edit_sectors else 4
                esector = st.selectbox(_L("Sector","Sector","Sector"), _edit_sectors, index=_es_idx)
                edesc = st.text_area(_L("Descripción","Description","Willay"), value=pd0.get("description", ""))
                estory = st.text_area(_L("🎙️ Historia","🎙️ Story","🎙️ Willay"), value=old_story, key=story_key)
                eimg = st.file_uploader(_L("Cambiar imagen","Change image","Rikchata shukchay"), type=["png","jpg","jpeg"], key=f"eimg_{edit_idx}")
                if eimg:
                    st.image(eimg, width=150)
                c1, c2 = st.columns(2)
                with c1:
                    if st.form_submit_button(f"💾 {_L('Guardar','Save','Allichana')}", use_container_width=True):
                        pe["sector"] = esector
                        pe["story"] = estory
                        pd0["name"] = ename
                        pd0["price"] = eprice
                        pd0["description"] = edesc
                        pd0["story"] = estory
                        if eimg:
                            st.session_state.setdefault("product_images",{})[pname_edit] = eimg.read()
                        st.session_state["editing_prod_idx"] = -1
                        st.rerun()
                with c2:
                    if st.form_submit_button(f"❌ {_L('Cancelar','Cancel','Paktana')}", use_container_width=True):
                        st.session_state["editing_prod_idx"] = -1
                        st.rerun()
        row_cols = st.columns(2)
        for idx, prod_ent in enumerate(productos):
            prod_data = prod_ent.get("products", [{}])[0]
            pname = prod_data.get("name", "")
            pprice = prod_data.get("price", 0)
            psector = prod_ent.get("sector", "")
            pdesc = prod_data.get("description", "")
            pimg_bytes = img_map.get(pname)
            col = row_cols[idx % 2]
            with col:
                sector_ico = "🧣" if "textil" in psector.lower() else "🧼" if "cosmético" in psector.lower() or "cosmetic" in psector.lower() else "🏺" if "cerámica" in psector.lower() else "🍲" if "alimento" in psector.lower() else "🎨"
                img_html = ""
                if pimg_bytes:
                    b64 = base64.b64encode(pimg_bytes).decode()
                    img_html = f'<img src="data:image/png;base64,{b64}" style="width:100%;height:120px;object-fit:cover;border-radius:12px;margin-bottom:0.5rem;">'
                st.markdown(f"""
                <div style="background:#0a1f1a;border:1px solid rgba(16,185,129,0.12);border-radius:16px;padding:0.8rem;margin-bottom:0.6rem;">
                  {img_html}
                  <div style="display:flex;justify-content:space-between;align-items:start;">
                    <div style="font-weight:600;color:#e2e8f0;font-size:0.85rem;">{pname[:40]}</div>
                    <span style="background:rgba(16,185,129,0.1);color:#10b981;font-size:0.7rem;font-weight:600;padding:0.1rem 0.5rem;border-radius:20px;">S/ {pprice:.2f}</span>
                  </div>
                  <div style="font-size:0.7rem;color:rgba(148,163,184,0.4);margin-top:0.3rem;">{sector_ico} {psector}</div>
                </div>
                """, unsafe_allow_html=True)
                wa_msg_p = f"¡Hola! Soy {st.session_state.get('user_name','artesano')} de MAPPED. Te comparto mi producto: {pname} - S/ {pprice:.2f}. ¿Te interesa?"
                wa_link_p = _wa_link(wa_msg_p)
                ac1, ac2, ac3 = st.columns([1,1,1.5])
                with ac1:
                    if del_idx == idx:
                        st.markdown(f'<div style="color:#ef4444;font-size:0.7rem;padding:0.2rem 0;">🗑️ {_L("¿Eliminar?","Delete?","Pitina?")}</div>', unsafe_allow_html=True)
                    elif st.button(f"✏️", key=f"ep_edit_{idx}", help=_L("Editar","Edit","Shukchana"), use_container_width=True):
                        st.session_state["editing_prod_idx"] = idx
                        st.rerun()
                with ac2:
                    if del_idx == idx:
                        c1, c2 = st.columns(2)
                        with c1:
                            if st.button(f"{_L('Sí','Yes','Arí')}", key=f"ep_del_c_{idx}", use_container_width=True, type="primary"):
                                st.session_state["new_entrepreneurs"].pop(idx)
                                st.session_state["deleting_prod_idx"] = -1
                                st.rerun()
                        with c2:
                            if st.button(f"{_L('No','No','Mana')}", key=f"ep_del_x_{idx}", use_container_width=True):
                                st.session_state["deleting_prod_idx"] = -1
                                st.rerun()
                    else:
                        if st.button(f"🗑️", key=f"ep_del_{idx}", help=_L("Eliminar","Delete","Pitina"), use_container_width=True):
                            st.session_state["deleting_prod_idx"] = idx
                            st.rerun()
                with ac3:
                    st.markdown(f'<a href="{wa_link_p}" target="_blank" style="display:block;text-align:center;font-size:0.65rem;color:#25D366;text-decoration:none;background:rgba(37,211,102,0.08);border:1px solid rgba(37,211,102,0.15);border-radius:8px;padding:0.2rem 0.3rem;">📱 {_L("Compartir","Share","Rikuchiy")}</a>', unsafe_allow_html=True)

    # ── Reseñas recibidas ──
    all_reviews = []
    for prod_ent in productos:
        for r in prod_ent.get("reviews", []):
            all_reviews.append({**r, "product": prod_ent.get("products",[{}])[0].get("name","")})
    if all_reviews:
        st.markdown(f'<div style="margin:1.5rem 0 0.8rem;"><span style="font-size:1rem;font-weight:700;color:#e2e8f0;">⭐ {_L("Reseñas recibidas","Reviews received","Chaskishka riviskuna")}</span></div>', unsafe_allow_html=True)
        for rv in all_reviews:
            stars = "★" * rv.get("stars", 5) + "☆" * (5 - rv.get("stars", 5))
            st.markdown(f'<div style="background:#0a1f1a;border:1px solid rgba(16,185,129,0.08);border-radius:12px;padding:0.6rem 0.8rem;margin-bottom:0.4rem;"><div style="display:flex;justify-content:space-between;align-items:center;"><span style="font-weight:600;color:#e2e8f0;font-size:0.8rem;">{rv.get("user","")}</span><span style="color:#eab308;font-size:0.8rem;">{stars}</span></div><div style="color:rgba(148,163,184,0.6);font-size:0.75rem;margin-top:0.2rem;">{rv.get("text","")}</div><div style="color:rgba(148,163,184,0.3);font-size:0.6rem;margin-top:0.15rem;">{_L("Producto","Product","Rura")}: {rv["product"]}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="margin:1.5rem 0 0.5rem;"><span style="font-size:1rem;font-weight:700;color:#e2e8f0;">⭐ {_L("Reseñas recibidas","Reviews received","Chaskishka riviskuna")}</span></div>', unsafe_allow_html=True)
        st.markdown(f'<div style="background:rgba(16,185,129,0.04);border:1px dashed rgba(16,185,129,0.15);border-radius:12px;padding:1rem;text-align:center;"><div style="font-size:0.8rem;color:rgba(148,163,184,0.4);">{_L("Aún no tienes reseñas. Cuando los turistas valoren tus productos, aparecerán aquí.","No reviews yet. When tourists rate your products, they will appear here.","Manara riviskuna. Turiskuna rurakunata valorangaj, kaypi rikurinka.")} 🦥</div></div>', unsafe_allow_html=True)

    # ── Analytics: proyección de demanda ──
    if total_prods > 0:
        st.markdown(f'<div style="margin:1.5rem 0 0.5rem;"><span style="font-size:1rem;font-weight:700;color:#e2e8f0;">📈 {_L("Proyección de demanda","Demand projection","Munana rikuchiy")}</span></div>', unsafe_allow_html=True)
        month_labels = [_L("Ene","Jan","Iñ"),_L("Feb","Feb","Piw"),_L("Mar","Mar","Mar"),_L("Abr","Apr","Abr"),_L("May","May","May"),_L("Jun","Jun","Jun"),_L("Jul","Jul","Jul"),_L("Ago","Aug","Ago"),_L("Sep","Sep","Set"),_L("Oct","Oct","Oct"),_L("Nov","Nov","Nuy"),_L("Dic","Dec","Dis")]
        fig_data = []
        for idx, prod_ent in enumerate(productos):
            prod_data = prod_ent.get("products", [{}])[0]
            base = max(prod_data.get("price", 50), 20)
            quality = len(prod_ent.get("reviews", [])) * 2 + idx + 2
            units_per_mo = max(quality, 3)
            vals = [max(int(units_per_mo * SEASONAL[m] * (base / 100)), 2) * base // 100 for m in range(12)]
            fig_data.append({"name": prod_data.get("name","")[:18], "vals": vals})
        try:
            import plotly.graph_objects as go
            fig = go.Figure()
            colors = ["#10b981","#8B5CF6","#F59E0B","#ec4899","#06b6d4"]
            for i, fd in enumerate(fig_data):
                fig.add_trace(go.Scatter(x=month_labels, y=fd["vals"], mode="lines+markers", name=fd["name"], line=dict(color=colors[i % len(colors)])))
            fig.update_layout(height=200, margin=dict(l=10,r=10,t=10,b=20), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="rgba(148,163,184,0.6)", size=10), legend=dict(orientation="h", y=1.1, x=0))
            fig.update_xaxes(gridcolor="rgba(148,163,184,0.06)", zeroline=False)
            fig.update_yaxes(gridcolor="rgba(148,163,184,0.06)", zeroline=False, visible=False)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        except Exception:
            st.markdown(f'<div style="font-size:0.7rem;color:rgba(148,163,184,0.3);text-align:center;">{_L("Gráfico no disponible","Chart not available","Gráfico mana tiyan")}</div>', unsafe_allow_html=True)

    # ── Galería de productos MAPPED ──
    st.markdown(f'<div style="margin:1.5rem 0 0.5rem;"><span style="font-size:1rem;font-weight:700;color:#e2e8f0;">📸 {_L("Galería MAPPED","MAPPED Gallery","MAPPED Galería")}</span></div>', unsafe_allow_html=True)
    ds = get_full_dataset()
    all_prods = []
    for ent in ds:
        for prod in ent.get("products", []):
            all_prods.append({**prod, "community": ent["name"], "sector": ent.get("sector", ""), "ent_id": ent.get("id"), "location": ent.get("location", "")})
    gal_search = st.text_input("", placeholder=_L("🔍 Buscar producto...","🔍 Search...","🔍 Rurata maskay..."), key="gal_search", label_visibility="collapsed")
    sectors = sorted(set(p["sector"] for p in all_prods if p["sector"]))
    filtro = st.selectbox("", [_L("Todos los sectores","All sectors","Tukuy")] + sectors, key="gal_filtro", label_visibility="collapsed")
    filtered = all_prods if filtro == _L("Todos los sectores","All sectors","Tukuy") else [p for p in all_prods if p["sector"] == filtro]
    if gal_search:
        q = gal_search.lower().strip()
        filtered = [p for p in filtered if q in p["name"].lower() or q in p.get("community","").lower() or q in p.get("sector","").lower()]
    if not filtered:
        st.markdown(f'<div style="background:rgba(16,185,129,0.04);border:1px dashed rgba(16,185,129,0.15);border-radius:16px;padding:2rem;text-align:center;margin:1rem 0;"><div style="font-size:2rem;margin-bottom:0.5rem;">🦥</div><div style="font-size:0.85rem;color:rgba(148,163,184,0.5);">{_L("No hay productos con ese filtro","No products match your filter","Kay filtruwan mana rurakuna tiyan")}</div></div>', unsafe_allow_html=True)
    else:
        cols = st.columns(2)
        for idx, prod in enumerate(filtered[:20]):
            with cols[idx % 2]:
                comm_name = prod.get("community", "")
                img_gal = _get_product_image(comm_name, prod, "100px")
                st.markdown(f"""
                <div style="background:#0a1f1a;border:1px solid rgba(16,185,129,0.1);border-radius:16px;padding:0.8rem;margin-bottom:0.6rem;">
                  {img_gal}
                  <div style="font-weight:600;color:#e2e8f0;font-size:0.8rem;text-align:center;">{prod["name"][:45]}</div>
                  <div style="text-align:center;margin:0.2rem 0;">
                    <span style="background:rgba(16,185,129,0.1);color:#10b981;font-size:0.7rem;font-weight:600;padding:0.1rem 0.5rem;border-radius:20px;">S/ {prod["price"]:.2f}</span>
                  </div>
                  <div style="font-size:0.65rem;color:rgba(148,163,184,0.4);text-align:center;">{prod["community"][:35]}</div>
                </div>
                """, unsafe_allow_html=True)
                ent_id = prod.get("ent_id")
                if ent_id and st.button(f"📍", key=f"gal_loc_{idx}", help=_L("Ver comunidad","View community","Llaktata rikuna"), use_container_width=True):
                    st.session_state["selected_ent_id"] = ent_id
                    st.session_state["_nav_rkey"] = "Mapa"
                    st.rerun()
        if len(filtered) > 20:
            st.markdown(f'<div style="text-align:center;font-size:0.75rem;color:rgba(148,163,184,0.3);padding:0.5rem;">{_L("Mostrando 20 de","Showing 20 of","Rikuchin 20")} {len(filtered)}</div>', unsafe_allow_html=True)

    # ── Mashi chat para emprendedor ──
    st.markdown(f'<div style="margin:1.5rem 0 0.5rem;"><span style="font-size:1rem;font-weight:700;color:#e2e8f0;">💬 {_L("Mashi — Tu asistente de gestión","Mashi — Your business assistant","Mashi — Gestionnikipa yanapak")}</span></div>', unsafe_allow_html=True)
    emp_online = _is_online()
    emp_status = _L("En línea","Online","Kaypi") if emp_online else _L("🌐 Offline","🌐 Offline","🌐 Offline")
    emp_status_class = "online" if emp_online else "offline"
    st.markdown(f'<div class="chat-header"><div class="mashi-avatar mashi-avatar-img"></div><div><div class="mashi-name">Mashi</div><div class="mashi-status {emp_status_class}">{emp_status}</div></div></div>', unsafe_allow_html=True)
    if "emp_chat_messages" not in st.session_state:
        _emp_greeting = _L("¡Hola, emprendedor! Soy Mashi, tu asistente de gestión. Puedo ayudarte con precios, tendencias de mercado, ventas y más. ¿Qué consulta tienes?",
            "Hello, entrepreneur! I'm Mashi, your business assistant. I can help with pricing, market trends, sales and more. What's your question?",
            "Allianllachu, emprendedor! Ñuka Mashi, gestionnikipa yanapak. Preciokuna, mercado mushuymanta, ventaskunamanta yanapasha. ¿Ima tapuyta charinki?")
        st.session_state.emp_chat_messages = [{"role":"assistant","content":_emp_greeting}]
    emp_processing = st.session_state.get("emp_mashi_processing", False)
    # Quick action buttons
    emp_q1, emp_q2, emp_q3 = st.columns(3)
    with emp_q1:
        if st.button(_L("💰 Precios","💰 Prices","💰 Preciokuna"), key="emp_q_price", use_container_width=True):
            st.session_state["_emp_pending"] = _L("¿Cómo debo fijar mis precios?","How should I set my prices?","¿Imaynatam preciota churana?")
            st.rerun()
    with emp_q2:
        if st.button(_L("📈 Mis ventas","📈 My sales","📈 Ventaykuna"), key="emp_q_sales", use_container_width=True):
            st.session_state["_emp_pending"] = _L("¿Cómo van mis ventas? Dame un análisis","How are my sales? Give me an analysis","¿Ventaykuna imaynan? Analisista kuway")
            st.rerun()
    with emp_q3:
        if st.button(_L("🌎 Tendencias","🌎 Trends","🌎 Musiukuna"), key="emp_q_trends", use_container_width=True):
            st.session_state["_emp_pending"] = _L("¿Qué productos están en tendencia?","Which products are trending?","¿Ima rurakunami munashka kashka?")
            st.rerun()
    # Build chat iframe
    emp_chat_css = '''
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800&display=swap');
    *{box-sizing:border-box;margin:0;padding:0}
    body{background:transparent!important;font-family:'Nunito','Outfit','Inter',-apple-system,sans-serif;color:#e2e8f0;padding:0;letter-spacing:0}
    .chat-container{display:flex;flex-direction:column;gap:12px;padding:1rem 1rem;min-height:300px;max-height:400px;overflow-y:auto;scroll-behavior:smooth}
    .bubble-row{display:flex;align-items:flex-end;gap:8px;margin-bottom:2px;animation:bubbleIn 0.4s cubic-bezier(0.21,1.02,0.73,1)}
    .bubble-row.mashi{justify-content:flex-start}
    .bubble-row.user{justify-content:flex-end}
    .chat-bubble-mashi{background:linear-gradient(135deg,#0a1f1a,#0d261f);border:1px solid rgba(16,185,129,0.12);border-radius:16px 16px 16px 4px;padding:14px 18px;max-width:75%;color:#e2e8f0;font-size:0.9rem;font-family:'Nunito',sans-serif;font-weight:500;line-height:1.7;letter-spacing:0;box-shadow:0 4px 16px rgba(0,0,0,0.2),0 0 40px rgba(16,185,129,0.03)}
    .chat-bubble-user{background:linear-gradient(135deg,#0d3b2c,#0f4a34);border:1px solid rgba(16,185,129,0.15);border-radius:16px 16px 4px 16px;padding:14px 18px;max-width:75%;color:#e2e8f0;font-size:0.85rem;font-family:'Nunito',sans-serif;font-weight:500;line-height:1.65;box-shadow:0 4px 16px rgba(0,0,0,0.15)}
    .bubble-avatar{width:32px;height:32px;border-radius:50%;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-size:1rem;overflow:hidden}
    .mashi-avatar-img{background:url('data:image/jpeg;base64,{B64}') center/cover no-repeat;width:32px;height:32px;border-radius:50%;flex-shrink:0;border:1.5px solid rgba(16,185,129,0.3)}
    .typing-bubble{background:linear-gradient(135deg,#0a1f1a,#0d261f);border:1px solid rgba(16,185,129,0.1);border-radius:16px;padding:14px 20px;display:flex;gap:5px;align-items:center}
    .typing-dot{width:7px;height:7px;background:#10b981;border-radius:50%;animation:typingBounce 1.4s infinite ease-in-out}
    .typing-dot:nth-child(2){animation-delay:0.2s}
    .typing-dot:nth-child(3){animation-delay:0.4s}
    @keyframes bubbleIn{from{opacity:0;transform:translateY(12px) scale(0.95)}to{opacity:1;transform:translateY(0) scale(1)}}
    @keyframes typingBounce{0%,60%,100%{transform:translateY(0);opacity:0.35}30%{transform:translateY(-6px);opacity:1}}
    ::-webkit-scrollbar{width:3px}
    ::-webkit-scrollbar-track{background:transparent}
    ::-webkit-scrollbar-thumb{background:rgba(16,185,129,0.2);border-radius:4px}
    '''
    def _md2html(t):
        return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    emp_bubbles = ''
    for msg in st.session_state.emp_chat_messages:
        content_html = _md2html(msg["content"])
        if msg["role"]=="assistant":
            emp_bubbles += '<div class="bubble-row mashi"><div class="bubble-avatar mashi-avatar-img"></div><div class="chat-bubble-mashi">' + content_html + '</div></div>'
        else:
            emp_bubbles += '<div class="bubble-row user"><div class="chat-bubble-user">' + content_html + '</div><div class="bubble-avatar user">👤</div></div>'
    if emp_processing:
        emp_bubbles += '<div class="bubble-row mashi"><div class="bubble-avatar mashi-avatar-img"></div><div class="typing-bubble"><span class="typing-dot"></span><span class="typing-dot"></span><span class="typing-dot"></span></div></div>'
    emp_iframe_css = emp_chat_css.replace("{B64}", MASHI_LOGO_B64)
    emp_iframe_html = f'<html><head><style>{emp_iframe_css}</style></head><body><div class="chat-container" id="c">{emp_bubbles}</div><script>var c=document.getElementById("c");if(c)c.scrollTop=c.scrollHeight</script></body></html>'
    st.components.v1.html(emp_iframe_html, height=320, scrolling=True)
    # Chat input
    emp_inp = st.chat_input(_L("Pregunta a Mashi sobre tu negocio...","Ask Mashi about your business...","Negociokimanta Mashita tapuy..."), key="emp_chat_input")
    # Processing
    emp_pending = st.session_state.pop("_emp_pending", None)
    if emp_pending and not emp_processing:
        st.session_state.emp_chat_messages.append({"role":"user","content":emp_pending})
        st.session_state["emp_mashi_processing"] = True
        st.rerun()
    if emp_inp and not emp_processing:
        st.session_state.emp_chat_messages.append({"role":"user","content":emp_inp})
        st.session_state["emp_mashi_processing"] = True
        st.rerun()
    if emp_processing:
        emp_user_msgs = [m for m in st.session_state.emp_chat_messages if m["role"]=="user"]
        if emp_user_msgs:
            emp_last = emp_user_msgs[-1]["content"]
            emp_hist = st.session_state.emp_chat_messages[:-1]
            try:
                emp_r = get_mashi_response(emp_last, "Emprendedor Local", emp_hist, st.session_state.get("api_key",""))
            except Exception:
                emp_ds = get_full_dataset()
                emp_r = mock_response(emp_last, "Emprendedor Local", emp_ds)
            st.session_state.emp_chat_messages.append({"role":"assistant","content":emp_r})
        st.session_state["emp_mashi_processing"] = False
        st.rerun()

# ========================================================================
# INVERSIONISTA B2B — VERIFICACIÓN + TABLA COMPARATIVA
# ========================================================================
def _sector_emoji(sector):
    m = {"textil":"🧣","artesanía":"🧺","cosmético":"🧼","cerámica":"🏺","arte":"🎨","turismo":"✈️","logística":"🚚","comercio":"🛒","joyería":"💍","música":"🎵","gastronomía":"🍲","agricultura":"🌿"}
    s = sector.lower().strip() if sector else ""
    for k,v in m.items():
        if k in s: return v
    return "🏪"

def _gmaps_url(location):
    q = re.sub(r'[^\w\s,]', '', location).strip()
    return f"https://www.google.com/maps?q={q.replace(' ','+')}"

SEASONAL = [0.70, 0.78, 0.86, 0.94, 1.02, 1.12, 1.20, 1.18, 1.08, 0.94, 0.82, 0.74]

def _community_monthly_vals(e):
    """Retorna lista de 12 valores mensuales de demanda para una comunidad."""
    yrs = max(int(e["years_selling"]), 1) if str(e["years_selling"]).isdigit() else 3
    total_revs = len(e["reviews"])
    good_revs = len([r for r in e["reviews"] if r["stars"] >= 4])
    avg_stars = sum(r["stars"] for r in e["reviews"]) / max(total_revs, 1)
    base_val = max(sum(p["price"] for p in e["products"]), 100)
    quality = total_revs * 2 + good_revs * 3 + yrs * 4 + avg_stars * 5 + len(e["products"]) * 2
    units_per_mo = max(quality / 2, 5)
    vals = []
    for m in range(12):
        units = max(int(units_per_mo * SEASONAL[m] * (base_val / 100)), 4)
        vals.append(units * base_val // 100)
    return vals

def render_inversionista():
    L = st.session_state.get("lang", "es")
    ds = get_full_dataset()
    comm_count = _L(f"{len(ds)} comunidades registradas en MAPPED", f"{len(ds)} communities registered in MAPPED", f"{len(ds)} llaktakuna MAPPEDpi")
    st.markdown(f'<div style="padding:1rem 1rem 0.5rem"><h2 class="section-title">📊 {T("role_inv")}</h2><p class="section-subtitle">{comm_count}</p></div>', unsafe_allow_html=True)
    inv_subtitle = _L("Verifica tu empresa para ver el análisis de viabilidad logística y comercial con nuestras comunidades.",
                       "Verify your company to see the logistics and commercial viability analysis with our communities.",
                       "Empresata churay rikunkapa llaktakunamanta.")
    inv_role = _L("mashi inversionista","mashi investor","mashi qolqe")
    st.markdown(f'<div class="glass-card"><h3 style="margin-top:0;">🦥 {KICHWA["saludo"]}, {inv_role}</h3><p style="font-size:0.85rem;color:rgba(148,163,184,0.6)!important;">{inv_subtitle}</p></div>', unsafe_allow_html=True)
    ruc_lbl = _L("RUC *","RUC *","RUC *")
    rep_lbl = _L("Representante Legal *","Legal Rep. *","Rikuk *")
    dni_lbl = _L("DNI *","DNI *","DNI *")
    sector_lbl = _L("Sector de tu empresa","Company sector","Empresa sector")
    ubi_lbl = _L("Ubicación de planta","Plant location","Maypita")
    verify_lbl = _L("🔍 Verificar Empresa","🔍 Verify Company","🔍 Rikuchiy")
    err_required = _L("Completa todos los campos obligatorios.","Fill in all required fields.","Kaykunata churay.")
    err_ruc = _L("RUC inválido (11 dígitos, empieza 1/2). Ej: 20123456789","Invalid RUC (11 digits, starts with 1/2). Ex: 20123456789","RUC mana alli (11 yupay, 1/2 kallari).")
    err_dni = _L("DNI inválido (8 dígitos).","Invalid DNI (8 digits).","DNI mana alli (8 yupay).")
    sector_options = [""] + sorted(list(set(e["sector"] for e in ds)))
    with st.form("b2b_form"):
        c1,c2,c3 = st.columns(3)
        with c1: ruc = st.text_input(ruc_lbl, placeholder=_L("11 dígitos","11 digits","11 yupay"), max_chars=11)
        with c2: rep = st.text_input(rep_lbl, placeholder=_L("Nombres","Full name","Sutin"))
        with c3: dni = st.text_input(dni_lbl, placeholder=_L("8 dígitos","8 digits","8 yupay"), max_chars=8)
        c4,c5 = st.columns(2)
        with c4: se = st.selectbox(sector_lbl, sector_options)
        with c5: ubi = st.text_input(ubi_lbl, placeholder=_L("Ej: Lima, Iquitos","Ex: Lima, Iquitos","Ej: Lima, Ikitus"))
        verify = st.form_submit_button(verify_lbl, use_container_width=True)
    if verify:
        if not ruc or not rep or not dni: st.error(err_required)
        elif not (len(ruc.strip())==11 and ruc.strip().isdigit() and ruc.strip()[0] in "12"): st.error(err_ruc)
        elif len(dni.strip())!=8 or not dni.strip().isdigit(): st.error(err_dni)
        else:
            st.session_state["verified"] = True
            st.session_state["verified_ruc"] = ruc.strip()
            st.session_state["verified_rep"] = rep.strip().title()
            st.session_state["verified_sector"] = se
            st.success(_L(f"✅ Empresa RUC {ruc.strip()} verificada | Representante: {rep.strip().title()}",
                          f"✅ Company RUC {ruc.strip()} verified | Rep: {rep.strip().title()}",
                          f"✅ RUC {ruc.strip()} allichishka | {rep.strip().title()}"))
            st.balloons()
    if st.session_state.get("verified", False):
        se = st.session_state.get("verified_sector", se)
        st.markdown(f'<div style="display:flex;gap:6px;align-items:center;margin:0.5rem 0;padding:0.3rem 0.8rem;background:rgba(16,185,129,0.04);border:1px solid rgba(16,185,129,0.1);border-radius:10px;"><span style="font-size:0.6rem;color:#10b981;">📊</span><span style="font-size:0.6rem;color:rgba(148,163,184,0.4);">{_L("Datos de comunidades registradas en MAPPED · Loreto, Perú","Data from communities registered in MAPPED · Loreto, Peru","MAPPEDpi llaktakuna · Loreto, Perú")}</span></div>', unsafe_allow_html=True)

        # ── Mini Folium Map ──
        if st.button("🗺️ " + _L("Ver mapa de comunidades","View community map","Llaktakuna mapapi"), key="toggle_inv_map", use_container_width=True):
            st.session_state["show_inv_map"] = not st.session_state.get("show_inv_map", False)
            st.rerun()
        if st.session_state.get("show_inv_map", False):
            import folium
            from streamlit_folium import st_folium
            m = folium.Map(location=[-3.7491, -73.2442], zoom_start=9,
                           tiles="CartoDB dark_matter", control_scale=True, zoom_control=False, scroll_wheel_zoom=False)
            folium.TileLayer("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
                name="Dark", attr="© OpenStreetMap © CARTO", control=False).add_to(m)
            folium.Marker([-3.7491,-73.2442], popup="Iquitos",
                icon=folium.Icon(color="lightblue", icon="info-sign")).add_to(m)
            sector_colors = {"artesanía":"green","textil":"purple","cosmético":"blue","cerámica":"orange",
                             "madera":"brown","alimentos":"lightgreen","turismo":"lightblue",
                             "música":"pink","medicina":"red"}
            sl_map = se.lower().strip() if se else ""
            for e in ds:
                sec = (e.get("sector") or "").lower()
                color = "gray"
                for kw, c in sector_colors.items():
                    if kw in sec:
                        color = c; break
                popup = folium.Popup(f"<b>{e['name']}</b><br>{e['sector']}<br>★ {round(sum(r['stars'] for r in e['reviews'])/len(e['reviews']),1) if e['reviews'] else '—'}/5<br>{e['location']}", max_width=250)
                opacity = 1.0 if (sl_map and sl_map in sec) or not sl_map else 0.3
                folium.CircleMarker([e["lat"], e["lng"]], radius=10, popup=popup,
                    color=color, fill=True, fill_opacity=opacity, weight=2,
                    fill_color=color).add_to(m)
            from branca.element import Element
            m.get_root().header.add_child(Element(
                '<style>body,html,#map{background:#040e0b!important;margin:0;padding:0;}'
                '.leaflet-container{background:#040e0b!important;}'
                '.leaflet-control-zoom a{background:#0A2B1F!important;color:#e2e8f0!important;}</style>'))
            st_folium(m, height=350, key="inv_mini_map", returned_objects=[])
        # ── Dark HTML table ──
        table_header = _L("Comunidad","Community","Llacta")
        table_header2 = _L("Sector","Sector","Sector")
        table_header3 = _L("Ubicación","Location","Maypi")
        table_header4 = _L("Trayectoria","Experience","Watakuna")
        table_header5 = _L("Valoración","Rating","Yupay")
        table_header6 = _L("Productos","Products","Rurakuna")
        table_header7 = _L("Logística","Logistics","Logistika")
        tbl_rows = ""
        for e in ds:
            avg = round(sum(r["stars"] for r in e["reviews"])/len(e["reviews"]),1) if e["reviews"] else "—"
            prods = "<br>".join([f"• {p['name']}: {p['currency']}{p['price']:.2f}" for p in e["products"]])
            em = _sector_emoji(e["sector"])
            tbl_rows += f'''<tr style="background:#0a1f1a;border-bottom:1px solid rgba(19,56,47,0.4);">
                <td style="padding:0.6rem 0.5rem;"><div style="display:flex;align-items:center;gap:6px;"><span style="font-size:0.9rem;">{em}</span><span style="color:#e2e8f0;font-size:0.7rem;font-weight:500;">{e["name"][:30]}</span></div></td>
                <td style="padding:0.6rem 0.5rem;font-size:0.65rem;color:rgba(148,163,184,0.6);">{e["sector"][:18]}</td>
                <td style="padding:0.6rem 0.5rem;font-size:0.65rem;"><a href="{_gmaps_url(e["location"])}" target="_blank" style="color:#10b981;text-decoration:none;font-size:0.65rem;">📍 {e["location"]}</a></td>
                <td style="padding:0.6rem 0.5rem;font-size:0.65rem;color:rgba(148,163,184,0.5);">{e["years_selling"]}</td>
                <td style="padding:0.6rem 0.5rem;font-size:0.65rem;color:#10b981;font-weight:600;">★ {avg}/5</td>
                <td style="padding:0.6rem 0.5rem;font-size:0.65rem;color:rgba(148,163,184,0.5);">{prods[:60]}...</td>
                <td style="padding:0.6rem 0.5rem;font-size:0.65rem;color:rgba(148,163,184,0.4);">{e.get("logistics_notes","")[:30]}</td>
            </tr>'''
        st.markdown(f'<div style="background:#05110e;border:1px solid #13382f;border-radius:14px;overflow:hidden;margin:1rem 0;"><div style="overflow-x:auto;"><table style="width:100%;border-collapse:collapse;min-width:700px;"><thead><tr style="background:#0a1f1a;border-bottom:2px solid #13382f;"><th style="padding:0.6rem 0.5rem;font-size:0.6rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#10b981;text-align:left;">{table_header}</th><th style="padding:0.6rem 0.5rem;font-size:0.6rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#10b981;text-align:left;">{table_header2}</th><th style="padding:0.6rem 0.5rem;font-size:0.6rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#10b981;text-align:left;">{table_header3}</th><th style="padding:0.6rem 0.5rem;font-size:0.6rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#10b981;text-align:left;">{table_header4}</th><th style="padding:0.6rem 0.5rem;font-size:0.6rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#10b981;text-align:left;">{table_header5}</th><th style="padding:0.6rem 0.5rem;font-size:0.6rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#10b981;text-align:left;">{table_header6}</th><th style="padding:0.6rem 0.5rem;font-size:0.6rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#10b981;text-align:left;">{table_header7}</th></tr></thead><tbody>{tbl_rows}</tbody></table></div></div>', unsafe_allow_html=True)
        # ── Dashboard ──
        sl = se.lower().strip() if se else ""
        try:
            import plotly.graph_objects as go
            _plotly_ok = True
        except ImportError:
            _plotly_ok = False
        months_short = [_L("Ene","Jan","Ene"),_L("Feb","Feb","Feb"),_L("Mar","Mar","Mar"),_L("Abr","Apr","Abr"),_L("May","May","May"),_L("Jun","Jun","Jun"),_L("Jul","Jul","Jul"),_L("Ago","Aug","Ago"),_L("Sep","Sep","Sep"),_L("Oct","Oct","Oct"),_L("Nov","Nov","Nov"),_L("Dic","Dec","Dic")]
        projection = []
        total_mkt_val = 0
        monthly_vals = []
        for e in ds:
            vals = _community_monthly_vals(e)
            monthly_vals.extend(vals)
            s = e.get("sector","").lower().strip()
            for m, val in enumerate(vals):
                projection.append({"sector":s,"month":months_short[m],"value":val})
        total_mkt_val = sum(monthly_vals)
        df_proj = pd.DataFrame(projection)
        total_reviews = sum(len(e["reviews"]) for e in ds)
        avg_rating = round(sum(sum(r["stars"] for r in e["reviews"]) for e in ds if e["reviews"]) / max(total_reviews, 1), 1)
        sectors_unique = len(set(e.get("sector","").lower().strip() for e in ds))
        total_products = sum(len(e["products"]) for e in ds)
        growth_val = min(100, max(5, round(
            len(ds) * 1.5 + sectors_unique * 4 + avg_rating * 5 + total_reviews * 0.5 + total_products * 0.3
        )))
        matched = []
        for e in ds:
            sec = e.get("sector","").lower().strip()
            kw = [w.lower().strip() for w in e.get("sector_keywords",[])]
            words = sl.split()
            if any(w in sec for w in words) or any(sl in w or w in sl for w in kw):
                matched.append(e)
        match_pct = min(100, max(15, round(len(matched) / len(ds) * 150)))
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f'<div style="background:#0a1f1a;border:1px solid #13382f;border-radius:12px;padding:0.8rem;text-align:center;"><div style="display:flex;align-items:center;justify-content:center;gap:6px;font-size:0.55rem;text-transform:uppercase;letter-spacing:1px;color:rgba(148,163,184,0.4);margin-bottom:4px;">💰<span>{_L("VALOR MERCADO ANUAL","ANNUAL MARKET VALUE","QOLQE WATA")}</span></div><div style="font-size:1.2rem;font-weight:800;color:#10b981;">S/ {total_mkt_val if total_mkt_val else 0:,.0f}</div><div style="font-size:0.55rem;color:rgba(148,163,184,0.3);margin-top:4px;">{_L("proyectado 12 meses","projected 12 months","12 killa yupay")}</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div style="background:#0a1f1a;border:1px solid #13382f;border-radius:12px;padding:0.8rem;text-align:center;"><div style="display:flex;align-items:center;justify-content:center;gap:6px;font-size:0.55rem;text-transform:uppercase;letter-spacing:1px;color:rgba(148,163,184,0.4);margin-bottom:4px;">📈<span>{_L("CRECIMIENTO","GROWTH","WIÑAY")}</span></div><div style="font-size:1.2rem;font-weight:800;color:{"#10b981" if growth_val > 30 else "#eab308"};">{growth_val}%</div><div style="font-size:0.55rem;color:rgba(148,163,184,0.3);margin-top:4px;">{_L("potencial anual","annual potential","wata atina")}</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div style="background:#0a1f1a;border:1px solid #13382f;border-radius:12px;padding:0.8rem;text-align:center;"><div style="display:flex;align-items:center;justify-content:center;gap:6px;font-size:0.55rem;text-transform:uppercase;letter-spacing:1px;color:rgba(148,163,184,0.4);margin-bottom:4px;">🎯<span>{_L("COBERTURA MATCH","MATCH COVERAGE","TINKUY")}</span></div><div style="font-size:1.2rem;font-weight:800;color:#10b981;">{match_pct}%</div><div style="font-size:0.55rem;color:rgba(148,163,184,0.3);margin-top:4px;">{_L("comunidades afines","matching communities","tinkuq llakta")}</div></div>', unsafe_allow_html=True)
        with col4:
            st.markdown(f'<div style="background:#0a1f1a;border:1px solid #13382f;border-radius:12px;padding:0.8rem;text-align:center;"><div style="display:flex;align-items:center;justify-content:center;gap:6px;font-size:0.55rem;text-transform:uppercase;letter-spacing:1px;color:rgba(148,163,184,0.4);margin-bottom:4px;">⭐<span>{_L("SATISFACCIÓN PROMEDIO","AVERAGE SATISFACTION","KUSIY")}</span></div><div style="font-size:1.2rem;font-weight:800;color:{"#10b981" if avg_rating > 4 else "#eab308"};">★ {avg_rating}/5</div><div style="font-size:0.55rem;color:rgba(148,163,184,0.3);margin-top:4px;">{_L("en {n} reseñas","in {n} reviews","{n} rivispi").format(n=total_reviews)}</div></div>', unsafe_allow_html=True)
        # ── Stacked area chart ──
        pivot = df_proj.pivot_table(index="month", columns="sector", values="value", aggfunc="sum").fillna(0)
        month_order = months_short
        pivot = pivot.reindex(month_order).fillna(0)
        fig = go.Figure()
        colors = ["#10b981","#00d4aa","#34d399","#6ee7b7","#a7f3d0","#059669","#047857","#065f46"]
        for j, col in enumerate(pivot.columns):
            fig.add_trace(go.Scatter(name=col[:15], x=pivot.index, y=pivot[col], mode="lines", stackgroup="one", line=dict(width=0.5, color=colors[j % len(colors)]), fillcolor=colors[j % len(colors)]))
        fig.update_layout(margin=dict(l=0,r=0,t=30,b=0), height=260, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="rgba(148,163,184,0.6)", size=9), hovermode="x unified", legend=dict(orientation="h", y=1.15, font=dict(size=9)), xaxis=dict(showgrid=False, showline=False), yaxis=dict(showgrid=False, showticklabels=False))
        dash_label = _L("Proyección de Demanda por Sector","Demand Projection by Sector","Mañay yupay")
        st.markdown(f'<div style="margin-top:1.2rem;font-size:0.85rem;font-weight:700;color:#e2e8f0;">📊 {dash_label}</div>', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        # ── ROI Calculator ──
        inv_amount = st.slider(_L("Inversión inicial (S/)","Initial investment (S/)","Qallariy qolqe (S/)"), min_value=5000, max_value=500000, value=50000, step=5000, help=_L("¿Cuánto deseas invertir en comunidades de Loreto?","How much do you want to invest in Loreto's communities?","Haykata churayta munanki Loreto llaktakunaman?"))
        quality_score = (match_pct / 100) * 0.6 + (avg_rating / 5) * 0.4
        inv_bonus = min(0.05, max(0, (inv_amount - 50000) / 500000 * 0.05))
        payback_m = round(24 - (quality_score + inv_bonus) * 16)
        payback_m = max(6, min(24, payback_m))
        annual_share = round(inv_amount * 12 / max(payback_m, 1), 0)
        roi_pct = round(annual_share / max(inv_amount, 1) * 100, 1)
        payback_color = "#10b981" if payback_m <= 12 else ("#eab308" if payback_m <= 18 else "#f97316")
        payback_badge = "🟢" if payback_m <= 12 else ("🟡" if payback_m <= 18 else "🟠")
        payback_note = _L("dentro del plazo recomendado (≤24 meses)","within recommended term (≤24 months)","allin pachapi (≤24 killa)") if payback_m <= 24 else _L("excede el plazo recomendado de 2 años","exceeds recommended 2-year term","2 wata pachata llallin")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f'<div style="background:#0a1f1a;border:1px solid #13382f;border-radius:12px;padding:1rem;text-align:center;"><div style="font-size:0.55rem;text-transform:uppercase;letter-spacing:1px;color:rgba(148,163,184,0.4);margin-bottom:4px;">{_L("INGRESO PROYECTADO","PROJECTED REVENUE","QOLQE WIÑAY")}</div><div style="font-size:1.3rem;font-weight:800;color:#10b981;">S/ {annual_share:,.0f}</div><div style="font-size:0.55rem;color:rgba(148,163,184,0.3);margin-top:4px;">{_L("primer año","first year","ñawpa wata")}</div></div>', unsafe_allow_html=True)
        with c2:
            badge = "🟢" if roi_pct > 30 else ("🟡" if roi_pct > 15 else "🔴")
            st.markdown(f'<div style="background:#0a1f1a;border:1px solid #13382f;border-radius:12px;padding:1rem;text-align:center;"><div style="font-size:0.55rem;text-transform:uppercase;letter-spacing:1px;color:rgba(148,163,184,0.4);margin-bottom:4px;">{_L("ROI ESTIMADO","ESTIMATED ROI","ROI YUPAY")}</div><div style="font-size:1.3rem;font-weight:800;color:{"#10b981" if roi_pct > 20 else "#eab308"};">{badge} {roi_pct:.1f}%</div><div style="font-size:0.55rem;color:rgba(148,163,184,0.3);margin-top:4px;">{_L("retorno sobre inversión","return on investment","qolqe kutimuy")}</div></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div style="background:#0a1f1a;border:1px solid #13382f;border-radius:12px;padding:1rem;text-align:center;"><div style="font-size:0.55rem;text-transform:uppercase;letter-spacing:1px;color:rgba(148,163,184,0.4);margin-bottom:4px;">{_L("PAYBACK","PAYBACK","KUTIMUY")}</div><div style="font-size:1.3rem;font-weight:800;color:{payback_color};">{payback_badge} {payback_m} {_L("meses","months","killa")}</div><div style="font-size:0.55rem;color:rgba(148,163,184,0.3);margin-top:4px;">{_L("recuperación de inversión","investment recovery","qolqe kutichiy")}</div><div style="font-size:0.5rem;color:{payback_color};margin-top:2px;">{payback_note}</div></div>', unsafe_allow_html=True)
        # ── Top communities by demand ──
        max_score = 0
        demand_rows = []
        for e in ds:
            yrs = max(int(e["years_selling"]), 1) if str(e["years_selling"]).isdigit() else 3
            score = min(len(e["reviews"]) * 15 + yrs * 5 + len(e["products"]) * 3, 100)
            if score > max_score: max_score = score
            demand_rows.append({**e, "_score":score})
        if max_score > 0:
            for r in demand_rows: r["_score"] = round(r["_score"] / max_score * 100)
        demand_rows.sort(key=lambda x: x["_score"], reverse=True)
        top6 = demand_rows[:6]
        tbl_title = _L("Top Comunidades por Demanda","Top Communities by Demand","Allin Llaktakuna")
        comm_h = _L("Comunidad","Community","Llacta")
        sector_h2 = _L("Sector","Sector","Sector")
        demand_h = _L("Demanda","Demand","Mañay")
        price_h = _L("Precio prom.","Avg price","Chani")
        reviews_h = _L("Reseñas","Reviews","Riviskuna")
        tbl_rows2 = ""
        for i, r in enumerate(top6):
            bg = "#0a1f1a" if i % 2 == 0 else "#05110e"
            em = _sector_emoji(r["sector"])
            bar_color = "#10b981" if r["_score"] >= 70 else ("#eab308" if r["_score"] >= 40 else "#ef4444")
            ap = sum(p["price"] for p in r["products"]) / max(len(r["products"]), 1)
            tbl_rows2 += f'''<tr style="background:{bg};border-bottom:1px solid rgba(19,56,47,0.4);">
                <td style="padding:0.6rem 0.5rem;"><div style="display:flex;align-items:center;gap:6px;"><span style="font-size:0.9rem;">{em}</span><span style="color:#e2e8f0;font-size:0.7rem;font-weight:500;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:160px;">{r["name"][:35]}</span></div></td>
                <td style="padding:0.6rem 0.5rem;font-size:0.65rem;color:rgba(148,163,184,0.6);">{r["sector"][:18]}</td>
                <td style="padding:0.6rem 0.5rem;"><div style="display:flex;align-items:center;gap:6px;"><div style="flex:1;height:6px;background:#13382f;border-radius:3px;overflow:hidden;min-width:60px;"><div style="width:{r["_score"]}%;height:100%;background:{bar_color};border-radius:3px;transition:width 0.3s;"></div></div><span style="font-size:0.65rem;font-weight:700;color:{bar_color};min-width:28px;text-align:right;">{r["_score"]}%</span></div></td>
                <td style="padding:0.6rem 0.5rem;font-size:0.65rem;color:#10b981;font-weight:600;text-align:right;">S/ {ap:.0f}</td>
                <td style="padding:0.6rem 0.5rem;font-size:0.65rem;color:rgba(148,163,184,0.5);text-align:center;">{len(r["reviews"])}</td>
            </tr>'''
        st.markdown(f'<div style="margin-top:1.2rem;font-size:0.85rem;font-weight:700;color:#e2e8f0;display:flex;align-items:center;gap:8px;"><span>🔥</span><span>{tbl_title}</span></div>', unsafe_allow_html=True)
        st.markdown(f'''<div style="background:#05110e;border:1px solid #13382f;border-radius:14px;overflow:hidden;margin:0.5rem 0;">
            <div style="overflow-x:auto;">
            <table style="width:100%;border-collapse:collapse;min-width:550px;">
                <thead><tr style="background:#0a1f1a;border-bottom:2px solid #13382f;">
                    <th style="padding:0.6rem 0.5rem;font-size:0.6rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#10b981;text-align:left;">{comm_h}</th>
                    <th style="padding:0.6rem 0.5rem;font-size:0.6rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#10b981;text-align:left;">{sector_h2}</th>
                    <th style="padding:0.6rem 0.5rem;font-size:0.6rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#10b981;text-align:left;">{demand_h}</th>
                    <th style="padding:0.6rem 0.5rem;font-size:0.6rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#10b981;text-align:right;">{price_h}</th>
                    <th style="padding:0.6rem 0.5rem;font-size:0.6rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#10b981;text-align:center;">📝</th>
                </tr></thead>
                <tbody>{tbl_rows2}</tbody>
            </table>
            </div>
        </div>''', unsafe_allow_html=True)
        # ── AI Analysis ──
        inv_sector = st.session_state.get("verified_sector", "")
        inv_sector_clean = inv_sector.replace("*","").strip() if inv_sector else ""
        ai_key = _resolve_api_key()
        or_key = _resolve_or_key()
        ai_analysis = st.session_state.get("ai_analysis", "")
        btn_label = _L("🤖 Análisis Mashi con IA","🤖 Mashi AI Analysis","🤖 Mashi Yuyay")
        analyze_clicked = st.button(btn_label, key="ai_inv_btn", use_container_width=True)
        if analyze_clicked:
            if not ai_key and not or_key:
                st.warning(_L("Configura una API Key (Gemini u OpenRouter) en el menú lateral.",
                              "Set an API Key (Gemini or OpenRouter) in the sidebar.",
                              "API Keyta churay waqtamanri"))
            else:
                with st.spinner(_L("Mashi analizando el sector...","Mashi analyzing the sector...","Mashi yuyaykun...")):
                    ctx = json.dumps([{
                        "name": e["name"], "sector": e["sector"],
                        "products": [{"name":p["name"],"price":p["price"]} for p in e["products"]],
                        "reviews": e["reviews"],
                        "years_selling": e["years_selling"],
                        "location": e["location"]
                    } for e in ds], ensure_ascii=False)
                    sector_focus = ""
                    if inv_sector_clean:
                        sector_focus = f"Mi empresa es del sector **{inv_sector_clean}**. Analiza solo las comunidades que pertenezcan o se relacionen con este sector."
                    prompt = (
                        "Eres analista de inversiones. "
                        f"{sector_focus}\n\n"
                        f"Dataset MAPPED:\n{ctx}\n\n"
                        "Responde en **máximo 2 párrafos cortos**:\n"
                        "• Oportunidades clave para mi sector\n"
                        "• Comunidades más prometedoras\n"
                        "• Recomendación concreta\n\n"
                        "Sé directo, ve al grano."
                    )
                    result_text = ""
                    if or_key:
                        for m in ("google/gemini-2.5-flash", "mistralai/mistral-7b-instruct"):
                            result_text = _call_openrouter(prompt, or_key, model=m)
                            if result_text: break
                    if not result_text and ai_key:
                        try:
                            from google import genai
                            client = genai.Client(api_key=ai_key.strip())
                            resp = client.models.generate_content(
                                model="gemini-2.5-flash",
                                contents=prompt
                            )
                            result_text = resp.text
                        except Exception:
                            try:
                                import google.generativeai as genai_old
                                genai_old.configure(api_key=ai_key.strip())
                                model = genai_old.GenerativeModel("gemini-2.5-flash")
                                resp = model.generate_content(prompt)
                                result_text = resp.text
                            except Exception as e:
                                st.error(f"Error Gemini: {str(e)[:100]}")
                    if result_text:
                        st.session_state["ai_analysis"] = result_text
        if ai_analysis:
            col_a, col_b = st.columns([6,1])
            with col_a:
                st.markdown(f'''<div style="background:#0a1f1a;border:1px solid #13382f;border-radius:16px;padding:1.2rem;margin-top:0.8rem;">
                    <div style="display:flex;align-items:center;gap:8px;margin-bottom:0.6rem;">
                        <span style="font-size:1.2rem;">🦥</span>
                        <span style="font-weight:700;color:#10b981;font-size:0.85rem;">{_L("Análisis de Mashi","Mashi's Analysis","Mashi Yuyay")}</span>
                    </div>
                    <div style="font-size:0.8rem;color:#e2e8f0;line-height:1.7;">{ai_analysis}</div>
                </div>''', unsafe_allow_html=True)
            with col_b:
                if st.button("↻", key="ai_clear", help=_L("Limpiar","Clear","Pichana")):
                    st.session_state.pop("ai_analysis", None)
                    st.rerun()
        # ── Portfolio ──
        comm_names = [e["name"] for e in ds]
        portfolio_lbl = _L("📋 Mi Portafolio de Inversión","📋 My Investment Portfolio","📋 Qolqe Churay")
        portfolio_selected = st.multiselect(
            portfolio_lbl, comm_names,
            default=st.session_state.get("portfolio_selected", []),
            key="portfolio_sel",
            placeholder=_L("Elige comunidades...","Choose communities...","Llaktakuna akllay..."))
        st.session_state["portfolio_selected"] = portfolio_selected
        if portfolio_selected:
            pf_communities = [e for e in ds if e["name"] in portfolio_selected]
            pf_total_revs = sum(len(e["reviews"]) for e in pf_communities)
            pf_avg_rating = round(sum(sum(r["stars"] for r in e["reviews"]) for e in pf_communities if e["reviews"]) / max(pf_total_revs, 1), 1)
            pf_total_prods = sum(len(e["products"]) for e in pf_communities)
            pf_monthly = []
            for e in pf_communities:
                pf_monthly.extend(_community_monthly_vals(e))
            pf_annual = sum(pf_monthly)
            pf_inv = inv_amount
            pf_quality = (len(pf_communities) / max(len(ds), 1)) * 0.5 + (pf_avg_rating / 5) * 0.5
            pf_payback = round(24 - pf_quality * 14)
            pf_payback = max(6, min(30, pf_payback))
            pf_roi = round(pf_annual / max(pf_inv, 1) * 100, 1) if pf_inv > 0 else 0
            c1_pf, c2_pf, c3_pf, c4_pf = st.columns(4)
            with c1_pf:
                st.markdown(f'<div style="background:#0a1f1a;border:1px solid #13382f;border-radius:12px;padding:0.7rem;text-align:center;"><div style="font-size:0.5rem;text-transform:uppercase;letter-spacing:1px;color:rgba(148,163,184,0.4);">{_L("COMUNIDADES","COMMUNITIES","LLACTA")}</div><div style="font-size:1.2rem;font-weight:800;color:#10b981;">{len(pf_communities)}</div></div>', unsafe_allow_html=True)
            with c2_pf:
                st.markdown(f'<div style="background:#0a1f1a;border:1px solid #13382f;border-radius:12px;padding:0.7rem;text-align:center;"><div style="font-size:0.5rem;text-transform:uppercase;letter-spacing:1px;color:rgba(148,163,184,0.4);">{_L("PROD. TOTALES","TOTAL PRODUCTS","LLAPA RURA")}</div><div style="font-size:1.2rem;font-weight:800;color:#10b981;">{pf_total_prods}</div></div>', unsafe_allow_html=True)
            with c3_pf:
                st.markdown(f'<div style="background:#0a1f1a;border:1px solid #13382f;border-radius:12px;padding:0.7rem;text-align:center;"><div style="font-size:0.5rem;text-transform:uppercase;letter-spacing:1px;color:rgba(148,163,184,0.4);">{_L("INGRESO ANUAL","ANNUAL REVENUE","WATA QOLQE")}</div><div style="font-size:1rem;font-weight:800;color:#10b981;">S/ {pf_annual:,.0f}</div></div>', unsafe_allow_html=True)
            with c4_pf:
                badge = "🟢" if pf_roi > 25 else ("🟡" if pf_roi > 12 else "🔴")
                st.markdown(f'<div style="background:#0a1f1a;border:1px solid #13382f;border-radius:12px;padding:0.7rem;text-align:center;"><div style="font-size:0.5rem;text-transform:uppercase;letter-spacing:1px;color:rgba(148,163,184,0.4);">{_L("ROI ESTIMADO","ESTIMATED ROI","ROI")}</div><div style="font-size:1rem;font-weight:800;color:#10b981;">{badge} {pf_roi}%</div><div style="font-size:0.5rem;color:rgba(148,163,184,0.3);">{_L("payback ~{n} meses","payback ~{n} months","{n} killata").format(n=pf_payback)}</div></div>', unsafe_allow_html=True)
            # Portfolio mini-table
            pf_rows = ""
            for e in pf_communities:
                em = _sector_emoji(e["sector"])
                avg = round(sum(r["stars"] for r in e["reviews"])/len(e["reviews"]),1) if e["reviews"] else "—"
                pf_rows += f'<tr style="background:#0a1f1a;border-bottom:1px solid rgba(19,56,47,0.4);">'
                pf_rows += f'<td style="padding:0.4rem 0.5rem;"><span style="font-size:0.9rem;">{em}</span> <span style="color:#e2e8f0;font-size:0.7rem;">{e["name"][:25]}</span></td>'
                pf_rows += f'<td style="padding:0.4rem 0.5rem;font-size:0.65rem;color:rgba(148,163,184,0.5);">{e["sector"][:14]}</td>'
                pf_rows += f'<td style="padding:0.4rem 0.5rem;font-size:0.65rem;color:#10b981;">★ {avg}</td>'
                pf_rows += f'<td style="padding:0.4rem 0.5rem;font-size:0.65rem;color:rgba(148,163,184,0.5);">{len(e["products"])}</td>'
                pf_rows += f'<td style="padding:0.4rem 0.5rem;font-size:0.65rem;color:rgba(148,163,184,0.4);">{e["years_selling"]}</td></tr>'
            st.markdown(f'<div style="background:#05110e;border:1px solid #13382f;border-radius:12px;overflow:hidden;margin-top:0.3rem;"><table style="width:100%;border-collapse:collapse;"><thead><tr style="background:#0a1f1a;border-bottom:1px solid #13382f;"><th style="padding:0.4rem 0.5rem;font-size:0.55rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#10b981;text-align:left;">{_L("Comunidad","Community","Llacta")}</th><th style="padding:0.4rem 0.5rem;font-size:0.55rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#10b981;text-align:left;">{_L("Sector","Sector","Sector")}</th><th style="padding:0.4rem 0.5rem;font-size:0.55rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#10b981;text-align:left;">{_L("Rating","Rating","Yupay")}</th><th style="padding:0.4rem 0.5rem;font-size:0.55rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#10b981;text-align:left;">{_L("Prod.","Prod.","Rura")}</th><th style="padding:0.4rem 0.5rem;font-size:0.55rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#10b981;text-align:left;">{_L("Años","Years","Wata")}</th></tr></thead><tbody>{pf_rows}</tbody></table></div>', unsafe_allow_html=True)

        # ── Download Report ──
        report_ts = time.strftime("%Y-%m-%d %H:%M")
        report_html = f"""<html><head><meta charset="utf-8"><style>
body{{font-family:Arial,sans-serif;background:#f5f5f5;color:#333;max-width:800px;margin:auto;padding:20px}}
h1{{color:#10b981;border-bottom:2px solid #10b981;padding-bottom:8px}}
h2{{color:#059669;margin-top:24px}}
table{{width:100%;border-collapse:collapse;margin:10px 0}}
th{{background:#10b981;color:#fff;padding:8px;text-align:left;font-size:13px}}
td{{padding:8px;border-bottom:1px solid #ddd;font-size:13px}}
.kpi{{display:inline-block;background:#e8f5e9;padding:10px 18px;margin:6px;border-radius:10px;text-align:center;min-width:140px}}
.kpi .val{{font-size:22px;font-weight:700;color:#10b981}}
.kpi .lbl{{font-size:11px;color:#666}}
.footer{{margin-top:30px;font-size:11px;color:#999;text-align:center}}
</style></head><body>
<h1>📊 MAPPED — {_L("Reporte de Inversión","Investment Report","Qolqe Willay")}</h1>
<p><strong>{_L("Empresa","Company","Empresa")}:</strong> {st.session_state.get("verified_rep","—")} | <strong>RUC:</strong> {st.session_state.get("verified_ruc","—")} | <strong>{_L("Sector","Sector","Sector")}:</strong> {st.session_state.get("verified_sector","—")}</p>
<p><strong>{_L("Generado","Generated","Rurashka")}:</strong> {report_ts}</p>
<h2>{_L("Indicadores Clave","Key Indicators","Yupaykuna")}</h2>
<div>{'<div class="kpi"><div class="val">S/ '+f'{total_mkt_val:,.0f}'+'</div><div class="lbl">'+_L("Valor Mercado","Market Value","Qolqe")+'</div></div>'}{'<div class="kpi"><div class="val">'+f'{growth_val}%'+'</div><div class="lbl">'+_L("Crecimiento","Growth","Wiñay")+'</div></div>'}{'<div class="kpi"><div class="val">'+f'{match_pct}%'+'</div><div class="lbl">'+_L("Match","Match","Tinkuy")+'</div></div>'}{'<div class="kpi"><div class="val">★ '+f'{avg_rating}'+'</div><div class="lbl">'+_L("Satisfacción","Satisfaction","Kusiy")+'</div></div>'}</div>
<h2>{_L("Top Comunidades por Demanda","Top Communities by Demand","Allin Llaktakuna")}</h2>
<table><tr><th>#</th><th>{_L("Comunidad","Community","Llacta")}</th><th>{_L("Sector","Sector","Sector")}</th><th>{_L("Demanda","Demand","Mañay")}</th><th>{_L("Precio","Price","Chani")}</th><th>{_L("Reseñas","Reviews","Rivis")}</th></tr>"""
        for i, r in enumerate(top6[:5]):
            ap = sum(p["price"] for p in r["products"]) / max(len(r["products"]), 1)
            report_html += f'<tr><td>{i+1}</td><td>{r["name"][:35]}</td><td>{r["sector"][:18]}</td><td>{r["_score"]}%</td><td>S/ {ap:.0f}</td><td>{len(r["reviews"])}</td></tr>'
        report_html += "</table>"
        if portfolio_selected:
            report_html += f"<h2>{_L('Portafolio','Portfolio','Qolqe')}</h2><p>{len(pf_communities)} {_L('comunidades seleccionadas','selected communities','akllashka llakta')} | {_L('Ingreso anual estimado','Est. annual revenue','Wata qolqe')}: S/ {pf_annual:,.0f} | ROI: {pf_roi}% | Payback: ~{pf_payback} {_L('meses','months','killa')}</p>"
        report_html += f"""<div class="footer">MAPPED · Loreto, Perú · {report_ts}</div></body></html>"""
        st.download_button(
            _L("📥 Descargar Reporte (HTML)","📥 Download Report (HTML)","📥 Willay Apay"),
            data=report_html,
            file_name=f"MAPPED_reporte_{time.strftime('%Y%m%d_%H%M')}.html",
            mime="text/html",
            use_container_width=True,
            key="dl_report")

        # ── Recommendation ──
        def _match_score(e):
            kw = [w.lower().strip() for w in e.get("sector_keywords",[])]
            sec = e.get("sector","").lower().strip()
            name = e.get("name","").lower()
            desc = e.get("description","").lower()
            score = 0
            if sl == sec or sec.startswith(sl) or sl.startswith(sec):
                score += 12
            sl_words = sl.split()
            sec_words = sec.split()
            if any(sl in w or w in sl for w in sec_words):
                score += 6
            if any(sl in w or w in sl for w in kw):
                score += 5
            if any(sw in sec for sw in sl_words):
                score += 4
            related = {"turismo":["viaje","tour","guía","expedición","avistamiento","ecoturismo","viajero","aventura","selva"],
                       "arte":["artesanía","cerámica","pintura","kené","shipibo"],
                       "textil":["chambira","telar","tejido","fibra"],
                       "cosméticos":["jabón","piel","belleza","spa","crema","aceite"],
                       "comercio":["venta","producto","tienda","comercio"],
                       "logística":["transporte","envío","distribución","acceso"],
                       "madera":["tallado","escultura","cedro","caoba"],
                       "alimentos":["miel","abeja","orgánico","natural"],
                       "medicina":["planta","salud","copaiba","uña de gato"],
                       "música":["tambor","flauta","instrumento","percusión"]}
            for rwords in related.values():
                if any(sl in rw or rw in sl for rw in rwords):
                    score += 3
                    break
            if sl in name:
                score += 2
            if sl in desc:
                score += 1
            return score
        scored = [(_match_score(e), e) for e in ds]
        scored = [(s,e) for s,e in scored if s > 0]
        rec = max(scored, key=lambda x:(x[0], len(x[1]["reviews"])))[1] if scored else max(ds, key=lambda e: len(e["reviews"]))
        ravg = round(sum(r["stars"] for r in rec["reviews"])/len(rec["reviews"]),1) if rec["reviews"] else "—"
        rec_title = _L("Recomendación de Mashi","Mashi's Recommendation","Mashi nishka")
        rec_sector_lbl = _L("Sector","Sector","Sector")
        rec_exp_lbl = _L("Trayectoria","Experience","Watakuna")
        rec_rating_lbl = _L("Valoración","Rating","Yupay")
        rec_logistics_lbl = _L("Logística","Logistics","Logistika")
        rec_reviews_lbl = _L("reseñas","reviews","rivis")
        rec_thanks = _L("Gracias por interesarte en las comunidades de Loreto.","Thank you for your interest in Loreto's communities.","Añay Loreto llaktakunamanta.")
        years_lbl = _L("años","years","wata")
        rtext = random.choice(rec["reviews"]) if rec["reviews"] else None
        review_html = f'<div style="margin-top:0.6rem;padding:0.6rem;background:rgba(16,185,129,0.04);border-left:2px solid rgba(16,185,129,0.2);border-radius:8px;"><div style="font-size:0.75rem;font-style:italic;color:rgba(148,163,184,0.6);">"{rtext["text"]}"</div><div style="font-size:0.65rem;color:rgba(16,185,129,0.5);margin-top:0.2rem;">— {rtext["user"]} {"★"*rtext["stars"]}</div></div>' if rtext else ""
        gmap_url = _gmaps_url(rec["location"])
        _loc_q = re.sub(r'[^\w\s,]', '', rec["location"]).strip()
        gmap_embed = f"https://www.google.com/maps?q={_loc_q.replace(' ','+')}&output=embed"
        st.markdown(f'''<div style="background:#0a1f1a;border:1px solid #13382f;border-radius:16px;overflow:hidden;margin-top:1rem;">
            <div style="padding:1rem 1.2rem;background:linear-gradient(135deg,#0a1f1a,#13382f);border-bottom:1px solid #13382f;">
                <div style="font-size:0.7rem;color:rgba(16,185,129,0.6);font-weight:600;text-transform:uppercase;letter-spacing:1.5px;">🦥 {rec_title}</div>
            </div>
            <div style="display:flex;flex-wrap:wrap;">
                <div style="flex:1;min-width:240px;padding:1rem 1.2rem;">
                    <div style="display:flex;align-items:center;gap:12px;margin-bottom:0.8rem;">
                        <div style="width:44px;height:44px;border-radius:12px;background:rgba(16,185,129,0.1);border:1.5px solid rgba(16,185,129,0.25);display:flex;align-items:center;justify-content:center;font-size:1.4rem;flex-shrink:0;">{_sector_emoji(rec["sector"])}</div>
                        <div><div style="font-weight:700;color:#fff;font-size:0.9rem;">{rec["name"]}</div><div style="font-size:0.7rem;color:rgba(148,163,184,0.5);">{rec["sector"]}</div></div>
                    </div>
                    <div style="font-size:0.8rem;color:rgba(148,163,184,0.7);margin-bottom:0.6rem;">{rec["description"][:120]}{"..." if len(rec["description"])>120 else ""}</div>
                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.4rem;font-size:0.75rem;">
                        <div><span style="color:rgba(148,163,184,0.4);">{rec_exp_lbl}:</span> <span style="color:#e2e8f0;">{rec["years_selling"]} {years_lbl}</span></div>
                        <div><span style="color:rgba(148,163,184,0.4);">{rec_rating_lbl}:</span> <span style="color:#10b981;">★ {ravg}/5</span> <span style="color:rgba(148,163,184,0.3);">({len(rec["reviews"])} {rec_reviews_lbl})</span></div>
                        <div style="grid-column:span 2;"><span style="color:rgba(148,163,184,0.4);">{rec_logistics_lbl}:</span> <span style="color:rgba(148,163,184,0.6);font-size:0.7rem;">{rec.get("logistics_notes","")}</span></div>
                    </div>
                    {review_html}
                    <div style="margin-top:0.8rem;display:flex;gap:8px;flex-wrap:wrap;">
                        <a href="{gmap_url}" target="_blank" style="display:inline-flex;align-items:center;gap:6px;background:rgba(16,185,129,0.1);color:#10b981;padding:0.4rem 0.8rem;border-radius:8px;text-decoration:none;font-size:0.75rem;border:1px solid rgba(16,185,129,0.2);">🗺️ {_L("Ver en mapa","View on map","Mapapi rikuy")}</a>
                        <a href="https://www.youtube.com/results?search_query={rec['name'].replace(' ','+')}+Loreto+artesanía" target="_blank" style="display:inline-flex;align-items:center;gap:6px;background:rgba(239,68,68,0.1);color:#ef4444;padding:0.4rem 0.8rem;border-radius:8px;text-decoration:none;font-size:0.75rem;border:1px solid rgba(239,68,68,0.2);">▶️ {_L("Ver video","Watch video","Rikuy video")}</a>
                    </div>
                    <div style="margin-top:0.8rem;font-size:0.7rem;color:rgba(148,163,184,0.4);">{KICHWA["gracias"]} {rec_thanks} 🦥🌿</div>
                </div>
                <div style="flex:1;min-width:280px;padding:0.8rem;">
                    <iframe width="100%" height="280" style="border:0;border-radius:12px;" loading="lazy" src="{gmap_embed}" allowfullscreen referrerpolicy="no-referrer-when-downgrade"></iframe>
                    <div style="text-align:center;margin-top:0.4rem;"><a href="{gmap_url}" target="_blank" style="font-size:0.65rem;color:rgba(16,185,129,0.5);text-decoration:none;">{_L("Abrir en Google Maps →","Open in Google Maps →","Google Mapspi rikuchiy →")}</a></div>
                </div>
            </div>
        </div>''', unsafe_allow_html=True)
        with st.expander(_L("📝 Ver todas las reseñas","📝 View all reviews","📝 Riviskuna")):
            for e in ds:
                avg = round(sum(r["stars"] for r in e["reviews"])/len(e["reviews"]),1) if e["reviews"] else "—"
                st.markdown(f"**{e['name']}** — ★ {avg}/5")
                for r in e["reviews"]: st.markdown(f"> {'★'*r['stars']}{'☆'*(5-r['stars'])} **{r['user']}**: _{r['text']}_")
                st.markdown("---")

        # ── Chat Mashi para Inversionista ──
        st.markdown(f'<div style="margin-top:1.5rem;border-top:1px solid rgba(19,56,47,0.4);padding-top:0.8rem;"><span style="font-size:0.85rem;font-weight:700;color:#e2e8f0;">🦥 {_L("Pregunta a Mashi sobre inversiones","Ask Mashi about investments","Mashita tapuy qolqemanta")}</span></div>', unsafe_allow_html=True)
        chat_history = st.session_state.setdefault("inv_chat", [])
        if not chat_history:
            greeting = _L(
                "¡Hola! Soy Mashi, tu analista de inversiones. Pregúntame sobre comunidades, ROI, sectores, logística o tendencias de mercado.",
                "Hi! I'm Mashi, your investment analyst. Ask me about communities, ROI, sectors, logistics, or market trends.",
                "Allianllachu! Mashi qolqe analistam kani. Tapuy llaktakunamanta, ROI, sector, logistika, mercadomanta.")
            chat_history.append({"role":"assistant","content":greeting})
        for msg in chat_history:
            with st.chat_message(msg["role"], avatar="🦥" if msg["role"]=="assistant" else "👤"):
                st.markdown(msg["content"])
        if prompt := st.chat_input(_L("Ej: ¿Cuál comunidad tiene mejor ROI?","Ex: Which community has the best ROI?","Ej: ¿Maykan llakta allin ROI?")):
            chat_history.append({"role":"user","content":prompt})
            with st.chat_message("user", avatar="👤"):
                st.markdown(prompt)
            # Responder con mock_response (datos locales) o IA si disponible
            ai_key = _resolve_api_key()
            or_key = _resolve_or_key()
            inv_prompt = (
                f"Eres Mashi, analista de inversiones en MAPPED (Loreto, Perú). "
                f"El usuario es del sector '{se if se else 'general'}'. "
                f"Responde MUY CORTO (1-2 párrafos) y ve al grano.\n\n"
                f"Usuario: {prompt}\n\n"
                f"Dataset (JSON):\n{json.dumps([{k:e[k] for k in ('name','sector','location','years_selling','products','reviews','logistics_notes')} for e in ds], ensure_ascii=False)}"
            )
            result = ""
            if or_key:
                for m in ("google/gemini-2.5-flash", "mistralai/mistral-7b-instruct"):
                    result = _call_openrouter(inv_prompt, or_key, model=m)
                    if result: break
            if not result and ai_key:
                try:
                    from google import genai
                    client = genai.Client(api_key=ai_key.strip())
                    resp = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=inv_prompt
                    )
                    result = resp.text
                except Exception:
                    try:
                        import google.generativeai as genai_old
                        genai_old.configure(api_key=ai_key.strip())
                        model = genai_old.GenerativeModel("gemini-2.5-flash")
                        resp = model.generate_content(inv_prompt)
                        result = resp.text
                    except Exception as e2:
                        st.warning(f"Gemini no disponible: {str(e2)[:80]}")
            if not result:
                result = mock_response(prompt, "Inversionista", ds) + _offline_tag()
            chat_history.append({"role":"assistant","content":result})
            with                 st.chat_message("assistant", avatar="🦥"):
                st.markdown(result)
                _clean_inv = re.sub(r'<[^>]+>', '', result)
                _clean_inv = re.sub(r'[\U0001F300-\U0001FAFF\U00002702-\U000027B0\U0001F1E0-\U0001F1FF\u2600-\u26FF\u2700-\u27BF🔊🎙️🌟🐍\[\]\(\)]+', '', _clean_inv)
                _clean_inv = re.sub(r'\s+', ' ', _clean_inv).strip()
                if st.button("🔊", key=f"speak_inv_{len(chat_history)}", help=_L("Escuchar","Listen","Uyariy")):
                    st.session_state["_speak_inv_pending"] = _clean_inv
            if "_speak_inv_pending" in st.session_state:
                _txt = st.session_state.pop("_speak_inv_pending")
                with st.spinner(_L("Mashi está hablando...","Mashi is speaking...","Mashi riman...")):
                    _audio = _tts_generate(_txt, L)
                if _audio:
                    st.audio(_audio, format="audio/mp3")
                else:
                    st.warning(_L("No se pudo generar la voz.","Could not generate voice.","Vozta mana atin."))
                
# ========================================================================
# CÁMARA IA
# ========================================================================
def render_camera():
    L = st.session_state.get("lang", "es")
    title = _L("📸 Cámara Inteligente","📸 AI Camera","📸 Kamara")
    subtitle = _L("Sube una foto de una artesanía y Mashi la identificará","Upload a craft photo and Mashi will identify it","Rikchata apay, Mashi rikuchishun")
    btn_label = _L("🔍 Identificar producto","🔍 Identify product","🔍 Rikuchiy")
    spinner_txt = _L("Mashi está analizando con IA...","Mashi is analyzing with AI...","Mashi IA rikuchin...")
    st.markdown(f'<div style="padding:1rem 1rem 0.5rem"><h2 class="section-title">{title}</h2><p class="section-subtitle">{subtitle}</p></div>', unsafe_allow_html=True)

    # If already identified, show result
    if st.session_state.get("identified"):
        d = st.session_state.identified; from_vision = d.get("from_vision", False); vision = d.get("vision")
        if from_vision and vision:
            quality_ico = {"alta":"✨","media":"📊","baja":"🌱"}.get(vision.get("quality","media"),"📊")
            st.markdown(f'<div class="glass-card"><span style="display:inline-block;background:rgba(16,185,129,0.1);color:#10b981!important;font-size:0.6rem;font-weight:600;text-transform:uppercase;padding:0.2rem 0.6rem;border-radius:20px;">{_L("Producto identificado","Product identified","Rura rikushka")}</span><span style="background:rgba(139,92,246,0.1);color:#a78bfa;font-size:0.6rem;font-weight:600;padding:0.15rem 0.5rem;border-radius:20px;margin-left:0.3rem;">📸 {_L("Visión IA","AI Vision","Rikuna IA")}</span><div style="font-size:1.1rem;font-weight:700;color:#FFFFFF!important;margin:0.6rem 0;">{vision["detected_type"]}</div><div style="font-size:0.8rem;"><div style="display:flex;justify-content:space-between;padding:0.35rem 0;border-bottom:1px solid rgba(19,56,47,0.5);"><span style="color:rgba(148,163,184,0.5)!important;">{_L("Calidad:","Quality:","Allin kay:")}</span><span style="color:#e2e8f0!important;">{quality_ico} {vision.get("quality","media").capitalize()}</span></div><div style="display:flex;justify-content:space-between;padding:0.35rem 0;border-bottom:1px solid rgba(19,56,47,0.5);"><span style="color:rgba(148,163,184,0.5)!important;">{_L("Precio estimado:","Est. price:","Masna:")}</span><span style="color:#10b981!important;"><strong>S/ {vision["visual_price"]:.2f}</strong></span></div></div><div style="padding:0.5rem 0 0;color:rgba(148,163,184,0.4);font-size:0.7rem;border-top:1px solid rgba(139,92,246,0.1);margin-top:0.3rem;">{vision.get("reason","")}</div></div>', unsafe_allow_html=True)
        else:
            offline = d.get("offline", False)
            if offline:
                st.info(_L("No se pudo conectar con la IA. Explora el catálogo en la sección Emprendedor Local.","Could not connect to AI. Browse the catalog in the Local Entrepreneur section.","IA mana atin. Rikunaykipaq maskay Emprendedor Localpi."))
            else:
                ent, prod, avg = d["ent"], d["prod"], d["avg"]
                st.markdown(f'<div class="glass-card"><span style="display:inline-block;background:rgba(16,185,129,0.1);color:#10b981!important;font-size:0.6rem;font-weight:600;text-transform:uppercase;padding:0.2rem 0.6rem;border-radius:20px;">{_L("Producto identificado","Product identified","Rura rikushka")}</span><span style="background:rgba(148,163,184,0.1);color:rgba(148,163,184,0.4);font-size:0.6rem;font-weight:600;padding:0.15rem 0.5rem;border-radius:20px;margin-left:0.3rem;">{_L("Sin conexión IA","AI offline","IA mana")}</span><div style="font-size:1.1rem;font-weight:700;color:#FFFFFF!important;margin:0.6rem 0;">{prod["name"]}</div><div style="font-size:0.8rem;"><div style="display:flex;justify-content:space-between;padding:0.35rem 0;border-bottom:1px solid rgba(19,56,47,0.5);"><span style="color:rgba(148,163,184,0.5)!important;">{_L("Artesano","Artisan","Ruraq")}</span><span style="color:#e2e8f0!important;">{ent["name"]}</span></div><div style="display:flex;justify-content:space-between;padding:0.35rem 0;border-bottom:1px solid rgba(19,56,47,0.5);"><span style="color:rgba(148,163,184,0.5)!important;">{_L("Precio","Price","Masna")}</span><span style="color:#e2e8f0!important;">{prod["currency"]}{prod["price"]:.2f}</span></div><div style="display:flex;justify-content:space-between;padding:0.35rem 0;border-bottom:1px solid rgba(19,56,47,0.5);"><span style="color:rgba(148,163,184,0.5)!important;">{_L("Reseñas","Reviews","Rivis")}</span><span style="color:#e2e8f0!important;">★ {avg}/5 · {len(ent["reviews"])} {_L("opiniones","reviews","rivis")}</span></div><div style="display:flex;justify-content:space-between;padding:0.35rem 0;"><span style="color:rgba(148,163,184,0.5)!important;">{_L("Ubicación","Location","Maypi")}</span><span style="color:#e2e8f0!important;">{ent["location"]}</span></div></div></div>', unsafe_allow_html=True)
        if from_vision and vision:
            vision_text = _L(
                f"Mashi ha identificado {vision.get('detected_type','un producto')}. "
                f"Calidad: {vision.get('quality','media')}. "
                f"Precio estimado: {vision['visual_price']:.2f} soles. "
                f"{vision.get('reason','')}",
                f"Mashi identified {vision.get('detected_type','a product')}. "
                f"Quality: {vision.get('quality','media')}. "
                f"Estimated price: {vision['visual_price']:.2f} soles. "
                f"{vision.get('reason','')}",
                f"Mashi rikurka {vision.get('detected_type','shuk rurata')}. "
                f"Allin kay: {vision.get('quality','media')}. "
                f"Masna: {vision['visual_price']:.2f} sol. "
                f"{vision.get('reason','')}")
            if st.button("🔊 " + _L("Mashi te lo dice","Mashi tells you","Mashi willasunki"), key="speak_vision", use_container_width=True):
                st.session_state["_speak_vision_pending"] = vision_text
        if "_speak_vision_pending" in st.session_state:
            txt = st.session_state.pop("_speak_vision_pending")
            with st.spinner(_L("Mashi está hablando...","Mashi is speaking...","Mashi riman...")):
                audio = _tts_generate(txt, L)
            if audio:
                st.audio(audio, format="audio/mp3")
            else:
                st.warning(_L("No se pudo generar la voz.","Could not generate voice.","Vozta mana atin."))
        # Cámara → Tienda: navega a la tienda filtrada por sector
        if from_vision and vision:
            detected = vision.get("detected_type", "")
            if detected and st.button("🛍️ " + _L("Explorar en Tienda","Browse in Store","Rantinapi maskay"), key="cam_vision_store", use_container_width=True):
                st.session_state["store_filter_sector"] = detected
                st.session_state["_nav_rkey"] = "Tienda"
                st.rerun()
        elif not from_vision and not d.get("offline"):
            ent = d.get("ent", {})
            sec = ent.get("sector", "")
            if sec and st.button("🛍️ " + _L("Ver en Tienda","View in Store","Rantinapi rikuna"), key="cam_offline_store", use_container_width=True):
                st.session_state["store_filter_sector"] = sec
                st.session_state["_nav_rkey"] = "Tienda"
                st.rerun()
        if st.button("🔄 " + _L("Nueva foto","New photo","Musuq rikcha"), key="clear_vision", use_container_width=True):
            del st.session_state["identified"]
            st.rerun()
        return

    # Upload form — sin reruns hasta submit (evita scroll reset en móvil)
    upload_txt = _L("Sube una foto del producto","Upload a product photo","Rurata rikchata apay")
    with st.form("camera_form", clear_on_submit=True):
        uploaded = st.file_uploader(upload_txt, type=["png","jpg","jpeg"], label_visibility="visible")
        if uploaded:
            st.image(uploaded, use_container_width=True)
        submitted = st.form_submit_button(btn_label, use_container_width=True)
    if submitted and uploaded:
        with st.spinner(spinner_txt):
            vision = _analyze_product_image(uploaded.getvalue())
            if vision:
                st.session_state.identified = {"vision": vision, "from_vision": True}
            else:
                st.session_state.identified = {"from_vision":False, "offline":True}
                st.toast(_L("No se pudo conectar con la IA de visión. Mostrando datos del catálogo.","AI vision unavailable. Showing catalog data.","IA mana atin. Catálogomanta rikuchin."), icon="📸")
            st.rerun()

# ========================================================================
# BOTTOM NAV
# ========================================================================
def _render_mini_map(ent, ds):
    import folium
    from streamlit_folium import st_folium
    L = _L
    u_lat = st.session_state.get("user_lat")
    u_lng = st.session_state.get("user_lng")
    u_name = st.session_state.get("user_loc_name", L("Tu ubicacion","Your location","Kan llakta"))

    if ent:
        if u_lat and u_lng:
            center_lat = (u_lat + ent["lat"]) / 2
            center_lng = (u_lng + ent["lng"]) / 2
            origin_coords = (u_lat, u_lng)
        else:
            center_lat, center_lng = -3.7491, -73.2442
            origin_coords = (-3.7491, -73.2442)
    else:
        center_lat, center_lng = (u_lat or -3.7491), (u_lng or -73.2442)
        origin_coords = (u_lat or -3.7491, u_lng or -73.2442)

    m = folium.Map(location=[center_lat, center_lng], zoom_start=12 if not ent else 9,
                   tiles="CartoDB dark_matter", control_scale=True, zoom_control=False, scroll_wheel_zoom=False)
    folium.TileLayer("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png", name="Dark", attr="© OpenStreetMap © CARTO", control=False).add_to(m)
    folium.Marker([-3.7491,-73.2442], popup="Iquitos", icon=folium.Icon(color="lightblue", icon="info-sign")).add_to(m)
    if u_lat and u_lng:
        folium.Marker(
            [u_lat, u_lng],
            popup=f"<b>{u_name}</b><br><i>{L('Tu punto de partida','Your starting point','Kallarimana')}</i>",
            icon=folium.Icon(color="red", icon="user", prefix="fa")
        ).add_to(m)

    if ent:
        folium.Marker([ent["lat"],ent["lng"]], popup=ent["name"], icon=folium.Icon(color="green", icon="ok-sign")).add_to(m)
        route_coords, route_km, route_segments, boat_label = _get_route_path_multi(
            origin_coords[0], origin_coords[1], ent["lat"], ent["lng"], dest_id=ent.get("id"))
        for seg_start, seg_end, seg_mode in route_segments:
            seg_pts = route_coords[seg_start:seg_end+1]
            if seg_mode == "car":
                folium.PolyLine(locations=seg_pts, color="#00F5D4", weight=3, opacity=0.7).add_to(m)
            elif seg_mode == "boat":
                folium.PolyLine(locations=seg_pts, color="#00D4F5", weight=3, opacity=0.5, dash_array="8,6").add_to(m)
                if seg_start > 0:
                    port_pt = route_coords[seg_start]
                    folium.Marker(port_pt, popup="Puerto fluvial",
                        icon=folium.Icon(color="orange", icon="anchor", prefix="fa")).add_to(m)
    else:
        # Mostrar comunidades cercanas como referencia
        nearby = _get_nearby_communities({"lat": center_lat, "lng": center_lng, "id": -1}, ds, radius_km=15)
        for d_km, ne in nearby[:3]:
            folium.Marker([ne["lat"], ne["lng"]], popup=f"{ne['name']}<br>{_format_distance(d_km)}",
                icon=folium.Icon(color="green", icon="ok-sign", icon_size=(10,10))).add_to(m)
    from branca.element import Element
    m.get_root().header.add_child(Element(
        '<style>body,html,#map{background:#040e0b!important;margin:0;padding:0;}'
        '.leaflet-container{background:#040e0b!important;}'
        '.leaflet-control-zoom a{background:#0A2B1F!important;color:#e2e8f0!important;}</style>'
    ))
    st_folium(m, height=300, key="mini_map", returned_objects=[])

def render_map_view():
    import folium
    from streamlit_folium import st_folium
    ds = get_full_dataset()
    lang = st.session_state.get("lang", "es")
    L = _L

    # Search bar
    search = st.text_input("", placeholder=L("Busca emprendimientos, productos o ruta...","Search ventures, products or routes...","Maskay rantina, rurakuna o ñan..."), label_visibility="collapsed", key="map_search")

    # Dynamic pin colors by distance from Iquitos
    _dists = [_dist_from_iquitos(e) for e in ds]
    _max_d = max(_dists) if _dists else 1
    def _pin_color(ent):
        d = _dist_from_iquitos(ent)
        ratio = d / _max_d
        if ratio < 0.33: return "cyan"
        if ratio < 0.66: return "green"
        return "white"
    hex_color = {"cyan":"#00F5D4","green":"#00FF88","white":"#E6FFFA"}

    m = folium.Map(location=[-3.7491,-73.2442], zoom_start=10, tiles="CartoDB dark_matter", control_scale=True)
    folium.TileLayer("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png", name="Dark", attr="© OpenStreetMap © CARTO", control=False).add_to(m)

    # Iquitos reference pin (cyan)
    folium.Marker([-3.7491,-73.2442], popup="Iquitos", icon=folium.Icon(color="lightblue", icon="info-sign")).add_to(m)

    # User location marker (if set)
    u_lat = st.session_state.get("user_lat")
    u_lng = st.session_state.get("user_lng")
    u_name = st.session_state.get("user_loc_name", L("Tu ubicacion","Your location","Kan llakta"))
    if u_lat and u_lng:
        folium.Marker(
            [u_lat, u_lng],
            popup=f"<b>{u_name}</b><br><i>{L('Tu punto de partida','Your starting point','Kallarimana')}</i>",
            icon=folium.Icon(color="red", icon="user", prefix="fa")
        ).add_to(m)

    selected_id = st.session_state.get("selected_ent_id")
    selected_ent = None
    if selected_id:
        selected_ent = next((e for e in ds if e.get("id") == selected_id), None)

    filtered = [e for e in ds if not search or search.lower() in e["name"].lower() or search.lower() in e.get("location","").lower() or search.lower() in e.get("sector","").lower()] if search else ds
    favs = st.session_state.get("favorites", [])
    for ent in filtered:
        eid = ent.get("id", 0)
        c = _pin_color(ent)
        fc = hex_color[c]
        is_selected = selected_ent and eid == selected_id
        is_fav = eid in favs
        scale = "transform:scale(1.6);" if is_selected else ""
        glow = f"box-shadow:0 0 24px {fc}cc;" if is_selected else f"box-shadow:0 0 12px {fc}88;"
        if is_fav:
            html = f'<div style="position:relative;"><div style="background:{fc};width:20px;height:20px;border-radius:50%;border:3px solid {fc};{glow}{scale}"></div><div style="position:absolute;top:-8px;right:-8px;font-size:10px;">⭐</div></div>'
        else:
            html = f'<div style="background:{fc};width:20px;height:20px;border-radius:50%;border:3px solid {fc};{glow}{scale}"></div>'
        popup_html = f"<b>{ent['name']}</b><br>{ent['location']}<br><i>{ent['sector']}</i><br>{ent.get('address','')}<br>{ent.get('logistics_notes','')}"
        if is_selected:
            if u_lat and u_lng:
                du = _haversine(u_lat, u_lng, ent["lat"], ent["lng"])
                popup_html += f"<br><hr><b>{L('Ruta desde','Route from','Ñan manta')} {u_name}</b><br>{_format_distance(du)}"
            else:
                d = _dist_from_iquitos(ent)
                popup_html += f"<br><hr><b>{L('Ruta desde Iquitos','Route from Iquitos','Iquitosmanta ñan')}</b><br>{_format_distance(d)}"
        folium.Marker(
            [ent["lat"],ent["lng"]],
            popup=popup_html,
            icon=folium.DivIcon(html=html, icon_size=(26,26))
        ).add_to(m)

    # Route line from Iquitos to selected community (multi-modal)
    route_coords, route_km = None, None
    if selected_ent:
        if u_lat and u_lng:
            origin_coords_route = (u_lat, u_lng)
            origin_label = u_name
        else:
            origin_coords_route = (-3.7491, -73.2442)
            origin_label = "Iquitos"
        route_coords, route_km, route_segments, boat_label = _get_route_path_multi(
            origin_coords_route[0], origin_coords_route[1], selected_ent["lat"], selected_ent["lng"],
            dest_id=selected_ent["id"])
        d_label = _format_distance(route_km)
        for seg_start, seg_end, seg_mode in route_segments:
            seg_pts = route_coords[seg_start:seg_end+1]
            if seg_mode == "car":
                folium.PolyLine(locations=seg_pts, color="#00F5D4", weight=4, opacity=0.8,
                    tooltip=f"{L('Ruta a','Route to','Ñan')} {selected_ent['name']} ({d_label})").add_to(m)
            elif seg_mode == "boat":
                folium.PolyLine(locations=seg_pts, color="#00D4F5", weight=4, opacity=0.5, dash_array="8,6",
                    tooltip=f"Bote/canoa: {boat_label}").add_to(m)
                if seg_start > 0:
                    port_pt = route_coords[seg_start]
                    folium.Marker(port_pt, popup=f"<b>Puerto fluvial</b><br>Embarque en {boat_label}",
                        icon=folium.Icon(color="orange", icon="anchor", prefix="fa")).add_to(m)
                # Boat distance label at midpoint
                mid_idx = (seg_start + seg_end) // 2
                mid_pt = route_coords[mid_idx]
                boat_km = sum(_haversine(route_coords[i][0], route_coords[i][1], route_coords[i+1][0], route_coords[i+1][1]) for i in range(seg_start, seg_end))
                folium.Marker(mid_pt,
                    icon=folium.DivIcon(html=f'<div style="background:#0A2B1F;border:1px solid #00D4F5;border-radius:12px;padding:2px 8px;font-size:11px;color:#00D4F5;white-space:nowrap;">🛶 {_format_distance(boat_km)}</div>', icon_size=(80,24)),
                ).add_to(m)
        # Car distance label (first segment midpoint)
        first_seg_end = route_segments[0][1]
        mid_idx = min(first_seg_end // 2, len(route_coords) - 1)
        folium.Marker(route_coords[mid_idx],
            icon=folium.DivIcon(html=f'<div style="background:#0A2B1F;border:1px solid #00F5D4;border-radius:12px;padding:2px 8px;font-size:11px;color:#00F5D4;white-space:nowrap;">🚗 {d_label}</div>', icon_size=(80,24)),
        ).add_to(m)

    # ── Planner route ──
    planner_ids = st.session_state.get("planner_route", [])
    if len(planner_ids) >= 2:
        planner_ents = [e for e in ds if e["id"] in planner_ids]
        planner_ents.sort(key=lambda e: planner_ids.index(e["id"]))
        # Draw segments
        order_colors = ["#F59E0B","#8B5CF6","#EC4899","#06B6D4","#84CC16","#F97316","#14B8A6","#6366F1","#D946EF"]
        for idx in range(len(planner_ents) - 1):
            a, b = planner_ents[idx], planner_ents[idx+1]
            coords, km, segs, _ = _get_route_path_multi(a["lat"], a["lng"], b["lat"], b["lng"], dest_id=b.get("id"))
            c = order_colors[idx % len(order_colors)]
            # Draw all segments with the same color (planner uses multi-modal too)
            for s_start, s_end, s_mode in segs:
                s_pts = coords[s_start:s_end+1]
                opts = {"color": c, "weight": 3, "opacity": 0.7, "tooltip": f"{idx+1} → {idx+2}: {a['name'][:20]} → {b['name'][:20]} ({_format_distance(km)})"}
                if s_mode == "boat":
                    opts["dash_array"] = "8,6"
                    opts["opacity"] = 0.5
                    opts["color"] = "#00D4F5"
                folium.PolyLine(locations=s_pts, **opts).add_to(m)
        # Numbered markers
        for idx, e in enumerate(planner_ents):
            fc = order_colors[idx % len(order_colors)]
            folium.Marker(
                [e["lat"], e["lng"]],
                popup=f"<b>{idx+1}. {e['name']}</b><br>{e['location']}",
                icon=folium.DivIcon(
                    html=f'<div style="background:{fc};width:26px;height:26px;border-radius:50%;border:2px solid #fff;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:12px;color:#021B15;box-shadow:0 0 16px {fc}aa;">{idx+1}</div>',
                    icon_size=(30,30)),
            ).add_to(m)

    from branca.element import Element
    m.get_root().header.add_child(Element(
        '<style>body,html,#map{background:#040e0b!important;margin:0;padding:0;}'
        '.leaflet-container{background:#040e0b!important;}'
        '.leaflet-control-zoom a{background:#0A2B1F!important;color:#e2e8f0!important;}</style>'
    ))
    st.markdown('<div style="background:#040e0b;border-radius:12px;overflow:hidden;border:1px solid #13382f;padding:0;margin:0;">', unsafe_allow_html=True)
    st_folium(m, height=460, key="mapet_map", returned_objects=[])
    st.markdown('</div>', unsafe_allow_html=True)

    # Planner card
    if len(planner_ids) >= 2:
        planner_ents = [e for e in ds if e["id"] in planner_ids]
        planner_ents.sort(key=lambda e: planner_ids.index(e["id"]))
        total_pkm = 0
        prev = (-3.7491, -73.2442)
        for e in planner_ents:
            total_pkm += _haversine(prev[0], prev[1], e["lat"], e["lng"])
            prev = (e["lat"], e["lng"])
        st.markdown(
            f'<div class="glass-card" style="border-left:3px solid #F59E0B;margin-top:8px;padding:0.8rem 1rem;">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;">'
            f'<div><b style="color:#F59E0B;">🗺️ {L("Ruta planificada","Planned route","Allichashka ñan")}</b><br>'
            f'<span style="font-size:0.8rem;color:rgba(148,163,184,0.6);">{L("Total aprox.","Approx. total","Tukuy")} {_format_distance(total_pkm)} · {len(planner_ents)} {L("comunidades","communities","llaktakuna")}</span></div>'
            f'</div>',
            unsafe_allow_html=True
        )
        for idx, e in enumerate(planner_ents):
            st.markdown(
                f'<div style="display:flex;gap:8px;align-items:center;padding:2px 0;font-size:0.8rem;">'
                f'<span style="background:{order_colors[idx % len(order_colors)]}22;color:{order_colors[idx % len(order_colors)]};border-radius:50%;width:20px;height:20px;display:inline-flex;align-items:center;justify-content:center;font-size:0.65rem;font-weight:700;">{idx+1}</span>'
                f'<b style="color:#e2e8f0;">{e["name"][:40]}</b>'
                f'</div>',
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

    # Selected community card
    if selected_ent and route_km:
        st.markdown(
            f'<div class="glass-card" style="border-left:3px solid #00F5D4;padding:0.8rem 1rem;">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;">'
            f'<div><b style="color:#00F5D4;">📍 {selected_ent["name"]}</b><br>'
            f'<span style="font-size:0.8rem;color:rgba(148,163,184,0.6);">{_format_distance(route_km)} por carretera · {selected_ent["location"]}</span></div>'
            f'<a href="https://www.google.com/maps?q={selected_ent.get("lat","")},{selected_ent.get("lng","")}" target="_blank" style="background:#00F5D422;border:1px solid #00F5D444;border-radius:8px;padding:4px 10px;font-size:0.75rem;color:#00F5D4;text-decoration:none;">🗺️ {L("Abrir en Maps","Open in Maps","Mapspi kichay")}</a>'
            f'</div></div>',
            unsafe_allow_html=True
        )

    # FAB-style button
    fab_col1, fab_col2, fab_col3 = st.columns([3,1,3])
    with fab_col2:
        st.markdown('<div style="text-align:center;">', unsafe_allow_html=True)
        if st.button("⚠️", key="fab_sos", help=L("Reportar incidente","Report incident","Willay"), use_container_width=True):
            st.info(L("Número de emergencia: 105 📞","Emergency number: 105 📞","Urgente: 105 📞"))
        st.markdown('</div>', unsafe_allow_html=True)

    # Legend
    st.markdown(
        f'<div class="map-legend">'
        f'<span><span style="color:#00F5D4;">●</span> {L("Cerca de Iquitos","Near Iquitos","Iquitos ladulla")}</span> '
        f'<span><span style="color:#00FF88;">●</span> {L("Distancia media","Mid-range","Chikanlla")}</span> '
        f'<span><span style="color:#E6FFFA;">●</span> {L("Lejanos","Far away","Karulla")}</span>'
        f'</div>',
        unsafe_allow_html=True
    )


def _generate_qr_base64(data, size=3):
    """Generate QR code and return as base64 data URI."""
    import qrcode, io, base64
    qr = qrcode.QRCode(box_size=size, border=0)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#10b981", back_color="#0a1f1a")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

def render_store_view():
    L = st.session_state.get("lang", "es")
    wl = st.session_state.setdefault("store_wishlist", [])
    cart = st.session_state.setdefault("store_cart", {})
    cart_count = sum(cart.values())
    title_suffix = f' <span style="font-size:0.7rem;color:#f97316;">🛒({cart_count})</span>' if cart_count else ""
    online = _is_online()
    sync_queue = st.session_state.setdefault("_sync_queue", [])
    if online and sync_queue:
        st.session_state["_sync_queue"] = []
        st.success(f'🔄 {_L("Sincronizado","Synced","Allichashka")} — {len(sync_queue)} {_L("pendientes enviados","pending sent","kachashka")}')
    status_color = "#10b981" if online else "#f59e0b"
    status_text = _L("En línea · sincronizado","Online · synced","Kaypi · allichashka") if online else _L("Sin conexión · cola local","Offline · local queue","Mana kaypi · kaymanta")
    st.markdown(f'<div style="padding:1rem 1rem 0.5rem"><h2 class="section-title">🛍️ {_L("Tienda MAPPED","MAPPED Store","MAPPED Rantina")}{title_suffix} <span style="font-size:0.6rem;color:{status_color};">● {status_text}</span></h2></div>', unsafe_allow_html=True)
    ds = get_full_dataset()
    all_prods = []
    for ent in ds:
        for prod in ent.get("products", []):
            all_prods.append({**prod, "community": ent["name"], "sector": ent.get("sector", ""), "ent_id": ent.get("id"), "location": ent.get("location", "")})
    # Pre-filter desde Cámara
    pre_sector = st.session_state.pop("store_filter_sector", None)
    if pre_sector:
        st.info(f'🛍️ {_L("Mostrando productos relacionados","Showing related products","Rurakunata rikuchin")}: "{pre_sector}"')
    search = st.text_input("", placeholder=_L("🔍 Buscar producto...","🔍 Search product...","🔍 Rurata maskay..."), key="store_search", label_visibility="collapsed")
    sectors = sorted(set(p["sector"] for p in all_prods if p["sector"]))
    filtro = st.selectbox("", [_L("Todos los sectores","All sectors","Tukuy")] + sectors, key="store_filtro", label_visibility="collapsed")
    filtered = all_prods if filtro == _L("Todos los sectores","All sectors","Tukuy") else [p for p in all_prods if p["sector"] == filtro]
    if pre_sector:
        q = pre_sector.lower()
        filtered = [p for p in filtered if q in p["name"].lower() or q in p.get("description","").lower() or q in p["sector"].lower()]
    if search:
        q = search.lower().strip()
        filtered = [p for p in filtered if q in p["name"].lower() or q in p["community"].lower() or q in p.get("sector","").lower()]
    def _pk(p):
        return f"{p.get('ent_id','')}#{p['name']}"
    # Download offline guide
    _qr_toggle = st.session_state.setdefault("_qr_show", None)
    if st.button(f'📥 {_L("Descargar guía offline","Download offline guide","Mana internetpi guiata churay")}', key="dl_guide", use_container_width=True):
        guide_lines = [f"🌿 MAPPED — {_L('Guía de comunidades','Community guide','Llacta guía')}", "="*50]
        for ent in ds:
            guide_lines.append(f"\n📍 {ent['name']}")
            guide_lines.append(f"   {_L('Sector','Sector','Sector')}: {ent.get('sector','')}")
            guide_lines.append(f"   {_L('Ubicación','Location','Maypi')}: {ent.get('location','')}")
            guide_lines.append(f"   ★ {ent.get('avg_rating',0):.1f}/5 ({ent.get('review_count',0)} {_L('reseñas','reviews','willaykuna')})")
            for prod in ent.get("products", []):
                guide_lines.append(f"   • {prod['name']} — S/ {prod['price']:.2f}")
        st.download_button(_L("Guardar archivo","Save file","Allichana"), "\n".join(guide_lines), file_name="mapped_guia_offline.txt", mime="text/plain", key="dl_save", use_container_width=True)
    # Wishlist section
    if wl:
        wish_items = [p for p in filtered if _pk(p) in wl]
        if wish_items:
            st.markdown(f'<div style="margin:0.5rem 0;font-size:0.8rem;color:#fbbf24;">⭐ {_L("Favoritos","Wishlist","Munashkakuna")} ({len(wl)})</div>', unsafe_allow_html=True)
            wcols = st.columns(2)
            for wi, wp in enumerate(wish_items[:4]):
                with wcols[wi % 2]:
                    wimg = _get_product_image(wp.get("community", ""), wp, "70px")
                    st.markdown(f'<div style="background:rgba(251,191,36,0.05);border:1px solid rgba(251,191,36,0.15);border-radius:12px;padding:0.5rem;margin-bottom:0.4rem;">{wimg}<div style="font-size:0.7rem;color:#e2e8f0;text-align:center;">{wp["name"][:35]}</div><div style="text-align:center;font-size:0.6rem;color:#fbbf24;">S/ {wp["price"]:.2f}</div></div>', unsafe_allow_html=True)
    if not filtered:
        st.markdown(f'<div style="background:rgba(16,185,129,0.04);border:1px dashed rgba(16,185,129,0.15);border-radius:16px;padding:2rem;text-align:center;margin:1rem 0;"><div style="font-size:2rem;margin-bottom:0.5rem;">🔍</div><div style="font-size:0.85rem;color:rgba(148,163,184,0.5);">{_L("No se encontraron productos","No products found","Rurakuna mana tiyan")}</div></div>', unsafe_allow_html=True)
        return
    detail_pk = st.session_state.setdefault("_detail_show", None)
    cols = st.columns(2)
    ds_dict = {e["name"]: e for e in ds}
    for idx, prod in enumerate(filtered[:24]):
        pk = _pk(prod)
        is_fav = pk in wl
        community_name = prod.get("community", "")
        ent = ds_dict.get(community_name, {})
        badge_emoji, badge_label, badge_color = _trend_badge(prod, ent) if ent else (None, None, None)
        badge_html = f'<span style="background:{badge_color}22;color:{badge_color};font-size:0.55rem;font-weight:700;padding:0.05rem 0.4rem;border-radius:12px;margin-left:0.3rem;">{badge_emoji} {badge_label}</span>' if badge_emoji else ""
        with cols[idx % 2]:
            img_gal = _get_product_image(ent, prod, "100px")
            emoji = _sector_emoji(prod.get("sector", ""))
            gallery_img = img_gal or f'<div style="font-size:2rem;text-align:center;padding:0.5rem 0;">{emoji}</div>'
            star_icon = "⭐" if is_fav else "☆"
            st.markdown(f"""
            <div style="background:#0a1f1a;border:1px solid rgba(16,185,129,0.1);border-radius:20px;padding:0.8rem;margin-bottom:0.6rem;box-shadow:0 2px 12px rgba(0,0,0,0.06);transition:all 0.2s cubic-bezier(0.4,0,0.2,1);" onmouseover="this.style.transform='translateY(-1px)';this.style.borderColor='rgba(16,185,129,0.2)';this.style.boxShadow='0 6px 20px rgba(0,0,0,0.1)'" onmouseout="this.style.transform='';this.style.borderColor='rgba(16,185,129,0.1)';this.style.boxShadow='0 2px 12px rgba(0,0,0,0.06)'">
              {gallery_img}
              <div style="font-weight:600;color:#e2e8f0;font-size:0.8rem;text-align:center;">{prod["name"][:35]}{badge_html}</div>
              <div style="text-align:center;margin:0.2rem 0;">
                <span style="background:rgba(16,185,129,0.1);color:#10b981;font-size:0.7rem;font-weight:600;padding:0.1rem 0.5rem;border-radius:20px;">S/ {prod["price"]:.2f}</span>
              </div>
              <div style="font-size:0.65rem;color:rgba(148,163,184,0.4);text-align:center;">{community_name[:35]}</div>
            </div>
            """, unsafe_allow_html=True)
            phone = PHONE_CONTACTS.get(community_name, "+51999999999")
            buy_msg = f"¡Hola! Quiero comprar: {prod['name']} - S/ {prod['price']:.2f} de {community_name}. ¿Está disponible?"
            buy_link = _wa_link(buy_msg, phone)
            sub = st.columns([1,1,1,1])
            ent_id = prod.get("ent_id")
            with sub[0]:
                if ent_id and st.button(f"📍", key=f"store_loc_{idx}", help=_L("Ver comunidad","View community","Llaktata rikuna"), use_container_width=True):
                    st.session_state["selected_ent_id"] = ent_id
                    st.session_state["_nav_rkey"] = "Mapa"
                    st.rerun()
            with sub[1]:
                if st.button(star_icon, key=f"store_fav_{idx}", help=_L("Favorito","Favorite","Munashka"), use_container_width=True):
                    if not online:
                        st.session_state.setdefault("_sync_queue", []).append({"action":"fav", "pk":pk, "add":not is_fav})
                    if is_fav:
                        wl.remove(pk)
                    else:
                        wl.append(pk)
                    st.rerun()
            with sub[2]:
                if st.button("📱", key=f"store_buy_{idx}", help=_L("Comprar","Buy","Rantiy"), use_container_width=True):
                    st.session_state["_buy_pending"] = buy_link
                    st.rerun()
            with sub[3]:
                is_qr = _qr_toggle == f"qr_{idx}"
                if st.button("🔗", key=f"store_qr_{idx}", help=_L("Compartir","Share","Rikuchiy"), use_container_width=True):
                    if is_qr:
                        st.session_state["_qr_show"] = None
                    else:
                        st.session_state["_qr_show"] = f"qr_{idx}"
                    st.rerun()
                if is_qr:
                    qr_data = f"{prod['name']} - S/ {prod['price']:.2f}\n{community_name}\n{prod.get('sector','')}"
                    qr_uri = _generate_qr_base64(qr_data)
                    st.markdown(f'<div style="text-align:center;margin-top:0.3rem;"><img src="{qr_uri}" style="width:70px;height:70px;border-radius:8px;display:block;margin:0 auto;"></div>', unsafe_allow_html=True)
                    st.markdown(f'<a href="{buy_link}" target="_blank" style="display:block;text-align:center;font-size:0.65rem;color:#25D366;text-decoration:none;margin-top:0.2rem;">📱 {_L("Comprar por WhatsApp","Buy via WhatsApp","WhatsApppi rantiy")}</a>', unsafe_allow_html=True)
            # Detail + Buy buttons row
            if st.button(f"📋 {_L('Ver detalle','View details','Rikuchiy')}", key=f"store_detail_{idx}", use_container_width=True):
                if detail_pk == pk:
                    st.session_state["_detail_show"] = None
                else:
                    st.session_state["_detail_show"] = pk
                st.rerun()
            if detail_pk == pk and ent:
                st.markdown(_render_product_detail(prod, ent, idx), unsafe_allow_html=True)
    # Handle pending WhatsApp buy
    if "_buy_pending" in st.session_state:
        link = st.session_state.pop("_buy_pending")
        st.markdown(f'<div style="text-align:center;padding:0.5rem;background:rgba(37,211,102,0.08);border:1px solid rgba(37,211,102,0.15);border-radius:12px;margin:0.5rem 0;"><a href="{link}" target="_blank" style="color:#25D366;font-weight:700;font-size:0.85rem;text-decoration:none;">📱 {_L("Abrir WhatsApp para comprar","Open WhatsApp to buy","WhatsAppta kichay rantinkapa")}</a></div>', unsafe_allow_html=True)
    if len(filtered) > 24:
        st.markdown(f'<div style="text-align:center;font-size:0.75rem;color:rgba(148,163,184,0.3);padding:0.5rem;">{_L("Mostrando 24 de","Showing 24 of","Rikuchin 24")} {len(filtered)}</div>', unsafe_allow_html=True)

def render_bottom_nav(active):
    tabs = [("🧭",_L("Explorar","Explore","Maskay"),"Ecoturista"),("🗺️",_L("Mapa","Map","Mapa"),"Mapa")]
    tabs.append(("🎬",_L("Demo","Demo","Demo"),"_demo"))
    st.markdown('<div class="bnav-header">— ' + _L("Navegar","Navigate","Rina") + ' —</div>', unsafe_allow_html=True)
    cols = st.columns(len(tabs))
    current_idx = next((i for i, t in enumerate(tabs) if t[2] == active), 0)
    for i, (icon, label, key) in enumerate(tabs):
        with cols[i]:
            is_active = current_idx == i
            if st.button(f"{icon}\n{label}", key=f"nv_{key}", use_container_width=True, type="primary" if is_active else "secondary"):
                if not is_active:
                    if key == "_demo":
                        st.session_state["demo_mode"] = True
                        st.session_state["demo_step"] = 0
                    else:
                        st.session_state["_nav_rkey"] = key
                    st.rerun()

# ========================================================================
# DEMO TOUR GUIADO
# ========================================================================
def render_demo_tour():
    step = st.session_state.get("demo_step", 0)
    steps = []

    def t(es, en, qw):
        return _L(es, en, qw)

    # -- Step definitions --
    steps.append(("🎬 " + t("Bienvenido a MAPPED","Welcome to MAPPED","MAPPEDpi allin shamuy"),
        t(
         "MAPPED conecta turistas con comunidades amazónicas de Loreto. "
         "App multilingüe (Español · English · Kichwa) con chat IA, mapa interactivo, "
         "favoritos, planificador de rutas y tienda virtual. Todo en una sola app.",
         "MAPPED connects travelers with Amazonian communities in Loreto. "
         "Multilingual app (Spanish · English · Kichwa) with AI chat, interactive map, "
         "favorites, route planner and virtual store. All in one app.",
         "MAPPED turistakunata Loreto llaktakunawan tupachin. "
         "Kimsa simillapi (Español · English · Kichwa), IA rimana, mapa, "
         "munashkakuna, ñan allichak, virtual rantina. Tukuy shuk appillapi."),
        "🌿"
    ))
    steps.append(("🌐 " + t("Tres idiomas","Three languages","Kimsa simi"),
        t(
         "Cambia entre Español, English y Kichwa desde la barra lateral. "
         "Mashi responde en el idioma que elijas. Todo el contenido "
         "se traduce al instante: menús, descripciones y notificaciones.",
         "Switch between Spanish, English and Kichwa from the sidebar. "
         "Mashi replies in your chosen language. All content "
         "translates instantly: menus, descriptions and notifications.",
         "Ladupita Español, English, Kichwata akllay. "
         "Mashi kikin simillapi kutichin. Tukuy contenido "
         "tiempullapi tícran: menú, willaykuna, notificaciones."),
        "🗣️"
    ))
    steps.append(("🦥 " + t("Mashi — Chat con IA","Mashi — AI Chat","Mashi — IA rimana"),
        t(
         "Chatea con Mashi, tu guía amazónico. Pregúntale sobre comunidades, "
         "productos, rutas o clima. Cuando menciones un lugar, aparecen botones "
         "para verlo en el mapa o guardarlo como favorito.",
         "Chat with Mashi, your Amazon guide. Ask about communities, "
         "products, routes or weather. When you mention a place, buttons appear "
         "to view it on the map or save as favorite.",
         "MashiwAN rimay, sachapi pushak. Tapuy llaktakunamanta, "
         "rurakunamanta, ñankunamanta, cliamanta. Shuk llaktata rimaptiki, "
         "sintikuna rikurin mapapi rikuna o allichay."),
        "💬"
    ))
    steps.append(("📸 " + t("Cámara Inteligente","AI Camera","Kamara"),
        t(
         "Toma o sube una foto de cualquier artesanía o producto amazónico. "
         "Mashi lo identifica al instante con IA: te dice qué es, la calidad, "
         "y un precio estimado. Luego puedes ver productos similares en la Tienda.",
         "Take or upload a photo of any Amazonian craft or product. "
         "Mashi instantly identifies it with AI: tells you what it is, "
         "quality, and estimated price. Then browse similar products in the Store.",
         "Rikchata apay, Mashi rikuchishun. IMA rurata willasun: ima, allin kay, "
         "masna. Chaymanta rantinapi shuk rurakunata rikunki."),
        "📸"
    ))
    steps.append(("🗺️ " + t("Mapa interactivo","Interactive map","Mapa"),
        t(
         "Mapa oscuro con 15 comunidades amazónicas en 3 grupos de colores: "
         "🟢 cerca de Iquitos, 🟢 media distancia, ⚪ lejanas. "
         "Barra de búsqueda, ruta OSRM desde Iquitos, tarjeta con distancia "
         "y botón para abrir en Google Maps.",
         "Dark map with 15 Amazon communities in 3 color groups: "
         "🟢 near Iquitos, 🟢 mid-range, ⚪ far away. "
         "Search bar, OSRM route from Iquitos, card with distance "
         "and button to open in Google Maps.",
         "Yana mapa, 15 Amazonía llaktakuna 3 grupos colores: "
         "🟢 Iquitos ladulla, 🟢 chikanlla, ⚪ karulla. "
         "Maskana sinti, OSRM ñan Iquitosmanta, tarjeta distanciawan "
         "Google Mapspi kichana sintiwan."),
        "📍"
    ))
    steps.append(("⭐ " + t("Favoritos","Favorites","Allichaskakuna"),
        t(
         "Guarda tus comunidades favoritas tocando ⭐. "
         "Aparecen en una lista desplegable en el chat. "
         "En el mapa, las comunidades favoritas tienen una ⭐ "
         "sobre su marcador. También puedes quitarlas cuando quieras.",
         "Save your favorite communities by tapping ⭐. "
         "They appear in a collapsible list in the chat. "
         "On the map, favorited communities have a ⭐ "
         "on their marker. You can remove them anytime.",
         "Munashka llaktakunata ⭐ sintipi allichay. "
         "Rimana ukupi rikurin listapi. "
         "Mapapi, allichashka llaktakunapa ⭐ kan "
         "marcadorpa hawampi. Qichuna malla allichayta atinki."),
        "⭐"
    ))
    steps.append(("🗺️ " + t("Planificador de ruta","Route planner","Ñan allichak"),
        t(
         "Selecciona varias comunidades y el planificador las ordena "
         "automáticamente por cercanía desde Iquitos. "
         "Muestra distancias parciales, total y una ruta numerada "
         "en el mapa con colores distintos para cada segmento.",
         "Select multiple communities and the planner auto-sorts them "
         "by proximity from Iquitos. "
         "Shows partial distances, total and a numbered route "
         "on the map with different colors for each segment.",
         "Ashka llaktakunata akllay, allichak kikin "
         "Iquitosmanta ashtawan ladulla churanka. "
         "Distancia chikanlla, tukuy, numerashka ñan "
         "mapapi rikuchin sapan segmento colorniyuk."),
        "🚗"
    ))
    steps.append(("🛍️ " + t("Tienda virtual","Virtual store","Virtual rantina"),
        t(
         "Los emprendedores locales registran sus productos con fotos, "
         "precios y materiales. Los turistas pueden explorar, "
         "ver reseñas y realizar pedidos. Cada compra apoya "
         "directamente a familias de la selva.",
         "Local entrepreneurs register their products with photos, "
         "prices and materials. Tourists can browse, "
         "see reviews and place orders. Each purchase directly "
         "supports rainforest families.",
         "Rurakuna rurankunata fotos, precios, materialkunawan "
         "churapan. Turistakuna rikun, rivista, rantiyta atin. "
         "Sapan rantina sachapi familiakunata yanapan."),
        "🎨"
    ))
    steps.append(("📊 " + t("Panel inversionista","Investor dashboard","Inversionista rikuna"),
        t(
         "Dashboard con KPIs, proyecciones de crecimiento, ROI calculator, "
         "mapa de calor de ingresos por sector y descarga de reportes. "
         "Analiza comunidades por sector y visualiza datos "
         "con gráficos interactivos Plotly.",
         "Dashboard with KPIs, growth projections, ROI calculator, "
         "revenue heatmap by sector and report downloads. "
         "Analyze communities by sector and visualize data "
         "with interactive Plotly charts.",
         "Dashboard KPIwan, wiñay proyecciones, ROI calculator, "
         "sector manta ingreso mapa calor, informes descarga. "
         "Llaktakunata sector manta análisis, Plotly gráficoswan."),
        "📈"
    ))
    steps.append(("🎉 " + t("¡Gracias por conocer MAPPED!","Thanks for exploring MAPPED!","MAPPED rikusqayki pagui!"),
        t(
         "Esta es una versión beta en constante mejora. "
         "Pronto: más comunidades, pagos integrados, rutas en tiempo real, "
         "y realidad aumentada para identificar productos. "
         "¿Preguntas? ¡Mashi está listo para ayudarte!",
         "This is a beta version under constant improvement. "
         "Coming soon: more communities, integrated payments, real-time routes, "
         "and augmented reality for product identification. "
         "Questions? Mashi is ready to help!",
         "Kay beta versiónmi, wiñay allichakun. "
         "Shamuk: ashka llaktakuna, pagu integrado, rutas tiempollapi, "
         "realidad aumentada rurakunata rikuchinapa. "
         "Tapuyki kan? Mashi yanapayta listun!"),
        "🎉"
    ))

    title, desc, icon = steps[step]
    total = len(steps)
    L = _L
    st.markdown(f"""
    <div style="max-width:680px;margin:1rem auto;padding:1.5rem;
         background:linear-gradient(135deg,#0a2b1f 0%,#0d3526 100%);
         border:1px solid rgba(16,185,129,0.2);border-radius:20px;
         box-shadow:0 8px 40px rgba(0,0,0,0.3);">
      <div style="font-size:2.5rem;text-align:center;margin-bottom:0.5rem;">{icon}</div>
      <div style="text-align:center;font-size:0.7rem;color:rgba(16,185,129,0.5);margin-bottom:0.3rem;">
        {L("Paso","Step","Paso")} {step+1}/{total}
      </div>
      <div style="text-align:center;margin-bottom:1rem;">
        {"".join(f'<span style="display:inline-block;width:8px;height:8px;border-radius:50%;margin:0 3px;background:{"#10b981" if i <= step else "#13382f"};"></span>' for i in range(total))}
      </div>
      <h2 style="color:#fff;text-align:center;font-size:1.3rem;margin:0 0 0.8rem;">{title}</h2>
      <p style="color:rgba(148,163,184,0.8);font-size:0.85rem;line-height:1.5;text-align:center;">{desc}</p>
    </div>
    """, unsafe_allow_html=True)

    nav = st.columns([1,1,1,1])
    with nav[0]:
        if step > 0 and st.button("◀ " + L("Anterior","Previous","Ñawpa"), key="demo_prev", use_container_width=True):
            st.session_state["demo_step"] = step - 1
            st.rerun()
    with nav[1]:
        if st.button("🎬 " + L("Salir","Exit","Lluksina"), key="demo_exit", use_container_width=True):
            st.session_state["demo_mode"] = False
            st.rerun()
    with nav[2]:
        if step < total - 1 and st.button(L("Siguiente","Next","Qipa") + " ▶", key="demo_next", use_container_width=True):
            st.session_state["demo_step"] = step + 1
            st.rerun()
    with nav[3]:
        if step < total - 1 and st.button("⏭ " + L("Saltar","Skip","Paskay"), key="demo_skip", use_container_width=True):
            st.session_state["demo_step"] = total - 1
            st.rerun()

    # Quick action card
    st.markdown(f"""
    <div style="max-width:680px;margin:0.5rem auto;padding:1rem;
         background:rgba(10,43,31,0.6);border:1px solid rgba(16,185,129,0.1);
         border-radius:16px;text-align:center;">
      <span style="font-size:0.7rem;color:rgba(148,163,184,0.4);">
        {L("Consejo","Tip","Willay")}:
        {L("Usa la barra lateral para cambiar idioma o rol en cualquier momento.",
           "Use the sidebar to change language or role anytime.",
           "Ladupita simita o ro lta cambiana atinki.")}
      </span>
    </div>
    """, unsafe_allow_html=True)

# ========================================================================
# MAIN
# ========================================================================
def main():
    st.session_state.setdefault("onboarded", False)
    st.session_state.setdefault("lang", "es")
    st.session_state.setdefault("new_entrepreneurs", [])
    st.session_state.setdefault("identified", None)
    st.session_state.setdefault("user_name", "")
    st.session_state.setdefault("last_ent", None)
    st.session_state.setdefault("selected_ent_id", None)
    st.session_state.setdefault("show_mini_map", False)
    st.session_state.setdefault("_gemini_key_idx", 0)
    st.session_state.setdefault("last_topic", "")
    st.session_state.setdefault("purchases", [])
    st.session_state.setdefault("verified", False)
    st.session_state.setdefault("favorites", [])
    st.session_state.setdefault("planner_ids", [])
    st.session_state.setdefault("planner_route", [])
    st.session_state.setdefault("demo_mode", False)
    st.session_state.setdefault("demo_step", 0)
    nav_code = st.query_params.get("nav", "")
    mode_map = {"map":"Mapa","eco":"Ecoturista","cam":"Cámara IA","emp":"Emprendedor Local","inv":"Inversionista"}
    if nav_code in mode_map:
        st.session_state["_nav_rkey"] = mode_map[nav_code]

    if not st.session_state.onboarded:
        render_onboarding()
        return

    st.markdown(CSS, unsafe_allow_html=True)

    # Header
    lang_label = {"es":"ES","en":"EN","qw":"QW"}.get(st.session_state.lang,"ES")
    subtitle_txt = _L("Mercado Amazónico · Loreto","Amazon Marketplace · Loreto","Amazónika Rantina · Loreto")
    st.markdown(f'<div class="app-header"><div class="app-header-left"><div class="avatar mashi-avatar-img"></div><div><div class="title">MAPPED</div><div class="subtitle">{subtitle_txt}</div></div></div><span class="lang-badge">{lang_label}</span></div>', unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown(f'<div class="glass-card" style="text-align:center;padding:1.5rem 1rem;"><div style="width:64px;height:64px;border-radius:50%;margin:0 auto 0.8rem;background:rgba(16,185,129,0.1);border:2px solid rgba(16,185,129,0.3);overflow:hidden;box-shadow:0 0 30px rgba(16,185,129,0.08);" class="mashi-avatar-img"></div><h3 style="color:#FFFFFF!important;font-size:1.1rem;font-weight:700;margin:0;">{KICHWA["saludo"]}</h3><p style="color:rgba(148,163,184,0.4)!important;font-size:0.7rem;margin-top:0.3rem;">{st.session_state.user_name}</p></div>', unsafe_allow_html=True)
        dm_active = st.session_state.get("demo_mode", False)
        demo_btn = "🎬 " + _L("Demo guiada","Guided tour","Rikuchiy") if not dm_active else "⏹ " + _L("Salir demo","Exit demo","Rikuchiyta tukuchiy")
        if st.button(demo_btn, key="demo_toggle", use_container_width=True, type="secondary"):
            if dm_active:
                st.session_state["demo_mode"] = False
            else:
                st.session_state["demo_mode"] = True
                st.session_state["demo_step"] = 0
            st.rerun()
        st.markdown(f'<p style="font-size:0.65rem;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;color:rgba(148,163,184,0.4)!important;margin:0.5rem 0 0.8rem;">🌐 {T("language")}</p>', unsafe_allow_html=True)
        lc = st.columns(3)
        for i,(code,lk) in enumerate([("es","lang_es"),("en","lang_en"),("qw","lang_qw")]):
            with lc[i]:
                act = st.session_state.lang==code
                if st.button(T(lk), key=f"lang_{code}", use_container_width=True, type="primary" if act else "secondary"):
                    st.session_state.lang = code; st.rerun()
        st.markdown(f'<p style="font-size:0.65rem;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;color:rgba(148,163,184,0.4)!important;margin:0.8rem 0 0.5rem;">👤 {_L("Rol","Role","Rol")}</p>', unsafe_allow_html=True)
        cam_label = _L("📸 Cámara IA","📸 AI Camera","📸 Kamara")
        mapa_label = _L("🗺️ Mapa","🗺️ Map","🗺️ Mapa")
        role = st.selectbox("", [T("role_eco"), cam_label, T("role_emp"), T("role_inv"), mapa_label], label_visibility="collapsed")
        rmap = {T("role_eco"):"Ecoturista", cam_label:"Cámara IA", T("role_emp"):"Emprendedor Local", T("role_inv"):"Inversionista", mapa_label:"Mapa"}
        rkey = rmap.get(role, "Ecoturista")
        nav_rkey = st.session_state.pop("_nav_rkey", "")
        if nav_rkey == "_demo":
            st.session_state["demo_mode"] = True
            st.session_state["demo_step"] = 0
            rkey = "Ecoturista"
        elif nav_rkey and (nav_rkey in rmap.values() or nav_rkey in _render_func):
            rkey = nav_rkey
        has_key = bool(_resolve_api_key()) or bool(_resolve_or_key())
        if has_key:
            st.markdown(f'<div style="background:rgba(16,185,129,0.06);border:1px solid rgba(16,185,129,0.1);border-radius:10px;padding:0.3rem 0.6rem;font-size:0.65rem;text-align:center;color:#10b981;">🟢 {_L("IA conectada","AI connected","IA tinkushka")}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="background:rgba(245,158,11,0.06);border:1px solid rgba(245,158,11,0.1);border-radius:10px;padding:0.3rem 0.6rem;font-size:0.65rem;text-align:center;color:rgba(245,158,11,0.8);">🟡 {_L("Modo offline · datos locales","Offline · local data","Offline · kaymanta")}</div>', unsafe_allow_html=True)
        nuevos = st.session_state.get("new_entrepreneurs",[])
        if nuevos:
            st.markdown(f'<div style="background:#0a1f1a;border:1px solid #13382f;border-radius:12px;padding:0.6rem 1rem;font-size:0.8rem;margin-top:0.5rem;">📦 <strong style="color:#10b981!important;">{len(nuevos)}</strong> {_L("producto(s) nuevo(s)","new product(s)","musuq rurakuna")}</div>', unsafe_allow_html=True)
        compras = st.session_state.get("purchases",[])
        if compras:
            st.markdown(f'<div style="background:#0a1f1a;border:1px solid #13382f;border-radius:12px;padding:0.6rem 1rem;font-size:0.8rem;">🛒 <strong style="color:#10b981!important;">{len(compras)}</strong> {_L("compra(s)","purchase(s)","rantishka")}</div>', unsafe_allow_html=True)
        # QR code for public access
        with st.expander("📡 " + _L("Compartir MAPPED","Share MAPPED","MAPPEDta rikuchiy"), expanded=False):
            if "ngrok_url" not in st.session_state:
                try:
                    import json, urllib.request
                    resp = urllib.request.urlopen("http://127.0.0.1:4040/api/tunnels", timeout=2)
                    tunnels = json.loads(resp.read()).get("tunnels", [])
                    for t in tunnels:
                        if t.get("proto") == "https":
                            st.session_state["ngrok_url"] = t["public_url"]
                            break
                except Exception:
                    pass
            url = st.session_state.get("ngrok_url", "")
            if not url:
                url = st.text_input(_L("URL pública (ngrok)","Public URL (ngrok)","URL pública (ngrok)"), placeholder="https://xxxx.ngrok-free.app", key="ngrok_input", label_visibility="collapsed")
                if url:
                    st.session_state["ngrok_url"] = url
                    st.rerun()
            if url:
                try:
                    import qrcode, io
                    qr = qrcode.make(url, box_size=5, border=1)
                    buf = io.BytesIO()
                    qr.save(buf, format="PNG")
                    st.image(buf.getvalue(), use_container_width=False, width=180)
                    st.markdown(f'<p style="font-size:0.65rem;text-align:center;color:rgba(148,163,184,0.5)!important;word-break:break-all;">{url}</p>', unsafe_allow_html=True)
                    if st.button(_L("Limpiar","Clear","Limpiar"), key="clear_ngrok", use_container_width=True):
                        del st.session_state["ngrok_url"]
                        st.rerun()
                except Exception:
                    st.caption(_L("Instala: pip install qrcode[pil]","Install: pip install qrcode[pil]","Churay: pip install qrcode[pil]"))
        st.markdown(f'<div style="color:rgba(148,163,184,0.15)!important;font-size:0.6rem;text-align:center;padding-top:1.5rem;">© 2026 MAPPED · Loreto, {_L("Perú","Peru","Perú")}</div>', unsafe_allow_html=True)

    # Content
    _render_func = {
        "Mapa": render_map_view,
        "Ecoturista": render_ecotourist,
        "Cámara IA": render_camera,
        "Tienda": render_store_view,
        "Emprendedor Local": render_emprendedor,
    }
    if st.session_state.get("demo_mode", False):
        try: render_demo_tour()
        except Exception as e: st.error(f"Error en demo: {e}")
    else:
        fn = _render_func.get(rkey, render_inversionista)
        try: fn()
        except Exception as e:
            st.error(f"Error en {rkey}: {e}")

    nav_active = "_demo" if st.session_state.get("demo_mode", False) else rkey
    render_bottom_nav(nav_active)

if __name__ == "__main__":
    main()
