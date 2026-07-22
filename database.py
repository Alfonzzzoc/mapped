import sqlite3, json, os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mapet.db")

_COMMUNITIES = [
    {"id":1,"name":"Asociación de Artesanas Shiringa de San Martín de Tipishca",
     "location":"San Martín de Tipishca, Río Amazonas","zone":"Amazonía Norte",
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
    {"id":10,"name":"Cacao Amazónico de Amazonas Chocolat",
     "location":"Mazán, Río Nanay","zone":"Amazonía Norte",
     "years_selling":6,"sector":"Alimentos Naturales",
      "sector_keywords":["cacao","chocolate","alimento","orgánico","natural","turismo","regalo","dulce","gourmet"],
     "description":"Familia que cultiva cacao orgánico y elabora chocolate artesanal amazónico.",
     "products":[
         {"name":"Chocolate artesanal de cacao amazónico (100g)","price":18.00,"currency":"S/",
          "description":"85% cacao. Sin aditivos. Sabor intenso."},
         {"name":"Set de 4 bombones de cacao (caja)","price":32.00,"currency":"S/",
          "description":"Rellenos de miel de abeja y copoazu."},
         {"name":"Manteca de cacao pura (200g)","price":25.00,"currency":"S/",
          "description":"Prensado en frío. Para piel y cocina."}],
     "reviews":[
         {"user":"Fernando G.","stars":5,"text":"El mejor chocolate que he probado."},
         {"user":"Isabel R.","stars":5,"text":"Los bombones son una delicia."},
         {"user":"Martín P.","stars":4,"text":"Excelente calidad, sabor único."}],
     "contact":"amazonas.chocolat@mapet.pe",
     "logistics_notes":"Acceso por carretera 35 min desde Iquitos.",
     "materials":"Cacao orgánico, miel de abeja, copoazu"},
    {"id":11,"name":"Cerámica Shipibo de San Francisco de Yarinacocha",
     "location":"Yarinacocha, Ucayali","zone":"Ucayali",
     "years_selling":25,"sector":"Cerámica y Arte",
      "sector_keywords":["shipibo","cerámica","kené","diseño","geométrico","pottery","ceramic","art","indigenous","turismo","regalo","arte"],
     "description":"Mujeres Shipibo-Konabo crean cerámicas con diseños kené ancestrales. Premiadas internacionalmente.",
     "products":[
         {"name":"Jarrón cerámico con diseño kené (30cm)","price":85.00,"currency":"S/",
          "description":"Pintado a mano. Diseños ancestrales Shipibo."},
         {"name":"Set de 4 platos ceremoniales","price":120.00,"currency":"S/",
          "description":"Diseños kené inspirados en visions ayahuasca."},
         {"name":"Collar de cerámica y chaquira","price":35.00,"currency":"S/",
          "description":"Pieza única. Chaquira de vidrio + cerámica Shipibo."}],
     "reviews":[
         {"user":"Sandra M.","stars":5,"text":"Arte puro. Los diseños Shipibo son hipnóticos."},
         {"user":"Jorge L.","stars":5,"text":"Compré el jarrón, es una obra de arte."},
         {"user":"María F.","stars":5,"text":"Calidad excepcional."}],
     "contact":"ceramica.shipibo@mapet.pe",
     "logistics_notes":"Envíos a todo el país.",
     "materials":"Arcilla natural, tintes minerales, chaquira"},
    {"id":12,"name":"Productores de Café Amazónico de Lamas",
     "location":"Lamas, San Martín","zone":"San Martín",
     "years_selling":12,"sector":"Alimentos Naturales",
      "sector_keywords":["café","coffee","alimento","orgánico","natural","turismo","regalo","bebida","tostado"],
     "description":"Cooperativa de productores de café orgánico de altura en la selva de San Martín.",
     "products":[
         {"name":"Café orgánico tostado (250g)","price":22.00,"currency":"S/",
          "description":"Tueste medio. Notas de chocolate y frutas tropicales."},
         {"name":"Café en grano especial (500g)","price":38.00,"currency":"S/",
          "description":"Cosecha selectiva. Altura 1200m."},
         {"name":"Set de café + taza artesanal","price":55.00,"currency":"S/",
          "description":"Café 250g + taza de cerámica hecha en Lamas."}],
     "reviews":[
         {"user":"Ricardo T.","stars":5,"text":"El mejor café del Perú."},
         {"user":"Claudia V.","stars":4,"text":"Muy aromático, perfecto para regalo."},
         {"user":"Pablo M.","stars":5,"text":"Cafe de altura con historia."}],
     "contact":"cafe.lamas@mapet.pe",
     "logistics_notes":"Envíos a Lima y principales ciudades.",
     "materials":"Café orgánico arábica, agua de lluvia"},
    {"id":13,"name":"Lodge Ecoamazónico de San Rafael",
     "location":"San Rafael, Río Marañón","zone":"Amazonía Norte",
     "years_selling":8,"sector":"Turismo Comunitario",
      "sector_keywords":["lodge","turismo","ecoturismo","hospedaje","naturaleza","selva","aventura","tourism","birdwatching","fishing","cultural"],
     "description":"Lodge comunitario en la ribera del Marañón. Turismo sostenible con comunidades locales.",
     "products":[
         {"name":"Noche en lodge + desayuno amazónico","price":85.00,"currency":"S/",
          "description":"Cabaña individual. Desayuno con frutas amazónicas."},
         {"name":"Paquete 2 días / 1 noche con tour","price":180.00,"currency":"S/",
          "description":"Hospedaje + tour de avistamiento + pesca."},
         {"name":"Expedición al Pacaya Samiria (3 días)","price":420.00,"currency":"S/",
          "description":"Todo incluido. Hospedaje, comidas, guía, transporte."}],
     "reviews":[
         {"user":"Andrea K.","stars":5,"text":"Experiencia mágica."},
         {"user":"Mark B.","stars":5,"text":"Best jungle lodge near Iquitos."},
         {"user":"Lucía H.","stars":4,"text":"Muy bonito, personal amable."}],
     "contact":"lodge.sanrafael@mapet.pe",
     "logistics_notes":"Acceso fluvial 3h desde Iquitos.",
     "materials":"Madera de tornillo, techo de palma, energía solar"},
    {"id":14,"name":"Teñido Natural de Palma de Michuna",
     "location":"Contamana, Ucayali","zone":"Ucayali",
     "years_selling":10,"sector":"Textiles y Artesanía",
      "sector_keywords":["textil","teñido","natural","palma","bolsa","hamaca","tela","turismo","regalo","ecológico","sostenible"],
     "description":"Asociación de tejedoras que teñen con plantas amazónicas y transforman palma en productos únicos.",
     "products":[
         {"name":"Bolsa tejida de palma teñida (mediano)","price":42.00,"currency":"S/",
          "description":"Teñida con achiote y huito."},
         {"name":"Hamaca doble de palma (2.5m)","price":160.00,"currency":"S/",
          "description":"Resistente y cómoda. Teñida con tintes naturales."},
         {"name":"Set de 3 posavasos de palma","price":20.00,"currency":"S/",
          "description":"Cada uno con color diferente."}],
     "reviews":[
         {"user":"Elena C.","stars":5,"text":"El color natural es hermoso."},
         {"user":"Raúl G.","stars":4,"text":"La hamaca es muy cómoda."}],
     "contact":"palma.michuna@mapet.pe",
     "logistics_notes":"Acceso por carretera 4h desde Lima.",
     "materials":"Fibra de palma, tintes naturales"},
    {"id":15,"name":"Artesanos de la Villa de Combate",
     "location":"Villa de Combate, Río Tahuayo","zone":"Amazonía Norte",
     "years_selling":22,"sector":"Artesanía en Madera",
      "sector_keywords":["madera","tallado","animales","pájaro","jaguar","escultura","wood","carving","animal","turismo","regalo","arte","decoración"],
     "description":"Comunidad de talladores especializados en figuras de fauna amazónica.",
     "products":[
         {"name":"Tucán tallado en cedro (20cm)","price":55.00,"currency":"S/",
          "description":"Detallado plumaje. Madera de cedro macizo."},
         {"name":"Jaguar en caoba (25cm)","price":90.00,"currency":"S/",
          "description":"Tallado a mano. Caoba. Detalle excepcional."},
         {"name":"Set de 6 mini animales amazónicos","price":45.00,"currency":"S/",
          "description":"Tucán, mono, perezoso, delfín, rana, mariposa."}],
     "reviews":[
         {"user":"Diana R.","stars":5,"text":"El tucán es una obra de arte."},
         {"user":"Héctor M.","stars":5,"text":"Compré el jaguar, es espectacular."},
         {"user":"Valentina S.","stars":4,"text":"Artesanía de primera."}],
     "contact":"villacombate@mapet.pe",
     "logistics_notes":"Acceso fluvial 1.5h desde Iquitos.",
     "materials":"Cedro, caoba, chonta, barniz natural"},
]

def _init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS communities (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            location TEXT, zone TEXT,
            years_selling INTEGER, sector TEXT,
            sector_keywords TEXT,
            description TEXT, contact TEXT,
            logistics_notes TEXT, materials TEXT
        );
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            community_id INTEGER NOT NULL,
            name TEXT NOT NULL, price REAL,
            currency TEXT, description TEXT,
            FOREIGN KEY(community_id) REFERENCES communities(id)
        );
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            community_id INTEGER NOT NULL,
            user TEXT, stars INTEGER, text TEXT,
            FOREIGN KEY(community_id) REFERENCES communities(id)
        );
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'tourist',
            avatar_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS entrepreneur_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            business_name TEXT NOT NULL,
            sector TEXT,
            location TEXT,
            description TEXT,
            phone TEXT,
            whatsapp TEXT,
            photo_url TEXT,
            verified INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT NOT NULL,
            description TEXT,
            category TEXT,
            location_name TEXT,
            lat REAL, lng REAL,
            photo_url TEXT,
            status TEXT DEFAULT 'reported',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
    """)
    count = c.execute("SELECT COUNT(*) FROM communities").fetchone()[0]
    if count == 0:
        for comm in _COMMUNITIES:
            c.execute("""INSERT INTO communities
                (id,name,location,zone,years_selling,sector,sector_keywords,description,contact,logistics_notes,materials)
                VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
                (comm["id"], comm["name"], comm["location"], comm["zone"],
                 comm["years_selling"], comm["sector"],
                 json.dumps(comm["sector_keywords"], ensure_ascii=False),
                 comm["description"], comm["contact"],
                 comm["logistics_notes"], comm["materials"]))
            for prod in comm["products"]:
                c.execute("INSERT INTO products (community_id,name,price,currency,description) VALUES (?,?,?,?,?)",
                          (comm["id"], prod["name"], prod["price"], prod["currency"], prod["description"]))
            for rev in comm["reviews"]:
                c.execute("INSERT INTO reviews (community_id,user,stars,text) VALUES (?,?,?,?)",
                          (comm["id"], rev["user"], rev["stars"], rev["text"]))
    conn.commit(); conn.close()

def get_all_communities():
    _init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    rows = c.execute("SELECT * FROM communities ORDER BY id").fetchall()
    result = []
    for r in rows:
        prods = [dict(p) for p in c.execute("SELECT name,price,currency,description FROM products WHERE community_id=? ORDER BY id", (r["id"],)).fetchall()]
        revs = [dict(rv) for rv in c.execute("SELECT user,stars,text FROM reviews WHERE community_id=? ORDER BY id", (r["id"],)).fetchall()]
        result.append({
            "id": r["id"], "name": r["name"], "location": r["location"],
            "zone": r["zone"], "years_selling": r["years_selling"],
            "sector": r["sector"],
            "sector_keywords": json.loads(r["sector_keywords"]) if r["sector_keywords"] else [],
            "description": r["description"], "contact": r["contact"],
            "logistics_notes": r["logistics_notes"], "materials": r["materials"],
            "products": prods, "reviews": revs
        })
    conn.close()
    return result

def reset_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    _init_db()

# ── User Auth ──
def create_user(name, email, password):
    _init_db()
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute("INSERT INTO users (name,email,password) VALUES (?,?,?)", (name, email, password))
        conn.commit()
        u = conn.execute("SELECT id,name,email,role FROM users WHERE email=?", (email,)).fetchone()
        conn.close()
        return {"id":u[0],"name":u[1],"email":u[2],"role":u[3]} if u else None
    except sqlite3.IntegrityError:
        conn.close()
        return None

def login_user(email, password):
    _init_db()
    conn = sqlite3.connect(DB_PATH)
    u = conn.execute("SELECT id,name,email,role FROM users WHERE email=? AND password=?", (email, password)).fetchone()
    conn.close()
    return {"id":u[0],"name":u[1],"email":u[2],"role":u[3]} if u else None

def update_user_role(user_id, role):
    _init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.execute("UPDATE users SET role=? WHERE id=?", (role, user_id))
    conn.commit(); conn.close()

def get_user(user_id):
    _init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    u = conn.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
    conn.close()
    return dict(u) if u else None

def save_entrepreneur_profile(user_id, business_name, sector, location, description, phone, whatsapp):
    _init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO entrepreneur_profiles (user_id,business_name,sector,location,description,phone,whatsapp) VALUES (?,?,?,?,?,?,?)",
                 (user_id, business_name, sector, location, description, phone, whatsapp))
    conn.commit(); conn.close()

def get_entrepreneur_profile(user_id):
    _init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    r = conn.execute("SELECT * FROM entrepreneur_profiles WHERE user_id=?", (user_id,)).fetchone()
    conn.close()
    return dict(r) if r else None

def report_incident(user_id, title, description, category, location_name, lat, lng):
    _init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO incidents (user_id,title,description,category,location_name,lat,lng) VALUES (?,?,?,?,?,?,?)",
                 (user_id, title, description, category, location_name, lat, lng))
    conn.commit(); conn.close()

def get_all_incidents():
    _init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM incidents ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]
