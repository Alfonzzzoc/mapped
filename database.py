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
