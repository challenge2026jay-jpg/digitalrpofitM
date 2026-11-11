"""Plan de montage V2 — voix originale (audio WhatsApp nettoyé), style de la vidéo de référence.

Tous les temps sont donnés en numéro de mot (audio/voix_mots.json) : chaque image, texte et son
arrive sur le mot prononcé auquel il correspond.
"""
M = "media/"
F = {
    "01": "01 - Young entrepreneur packing order in warehouse.jpg",
    "02": "02 - 441775044713248418.jpg",
    "03": "03 - Commandes Wholesale de Noël 🎄 _ Coulisses d'une Petite Entreprise Artisanale.jpg",
    "08": "08 - 233382_medium.mp4",
    "13": "13 - 100 Phone Accessories on Amazon_ Cases, Chargers and Earbuds.jpg",
    "14": "14 - Buisness Ebook _ Buisness Guide.jpg",
    "15": "15 - Crush Ebook Sales on Instagram_ Story Strategies for Faceless Accounts.jpg",
    "16": "16 - aesthetic photo editor MULI.jpg",
    "17": "17 - AMERICAN DOLLAR.jpg",
    "18": "18 - 298645019062415060.jpg",
    "19": "19 - 286930_medium.mp4",
    "20": "20 - Premium Poly Mailer Bags for Ecommerce Shipping _ Tilak Polypack.jpg",
    "21": "21 - HIPAA Patient Intake & Forms Blog _ MedForward.jpg",
    "24": "24 - 1360-147055409_medium.mp4",
    "26": "26 - China’s logistics sector grows 6_2% in Q1 2026.jpg",
    "27": "27 - 878413102300172217.jpg",
    "31": "31 - Quality Packing And Shipping Solutions In Madera.jpg",
    "32": "32 - WhatsApp Business Marketing Tips for Indian SMEs.jpg",
    "33": "33 - Traveling light_ This UBeesize tripod is a….jpg",
    "34": "34 - Mobile shop #mobile accessories.jpg",
    "35": "35 - capture_tableau_de_bord_chariow.png",
    # Pixabay (licence Pixabay : usage commercial libre, sans attribution) — sources dans media/pixabay/SOURCES.json
    "PX_billets": "pixabay/px_billets_comptage.mp4",
    "PX_billets2": "pixabay/px_billets_mains.mp4",
    "PX_tel_defile": "pixabay/px_telephone_defilement.mp4",
    "PX_tel_pouce": "pixabay/px_telephone_pouce.mp4",
    "PX_tel_bois": "pixabay/px_telephone_mains_bois.mp4",
    "PX_message": "pixabay/px_message_telephone.mp4",
    "PX_tel_blanc": "pixabay/px_telephone_main_fond_blanc.mp4",
    "PX_tel_photo": "pixabay/px_telephone_ecran_photo.mp4",
    "PX_carnet_dessus": "pixabay/px_carnet_vue_dessus.mp4",
    "PX_ecriture": "pixabay/px_ecriture_carnet.mp4",
    "PX_tel_2mains": "pixabay/px_telephone_deux_mains.mp4",
    "PX_tel_manteau": "pixabay/px_telephone_manteau.mp4",
}
BLUR = {"32": [(0.27, 0.215, 0.9, 0.305)]}

KEYWORDS = ["50 dollars", "produits digitaux", "dropshipping local", "fournisseur local", "petit stock",
            "livraison", "marge", "LOCAL"]

# Plans : (mot de départ, fichier, (cx, cy, zoom), mouvement, transition, décalage dans la vidéo source en s)
# transition : "cut" (coupe franche) | "zoom" (arrivée par zoom flou, comme la référence) | "fondu"
SHOTS = [
    (0,   "PX_billets",      (0.5, 0.5, 1.0),  "in",     "cut", 1.0),   # Attends, … Congo-Kinshasa, 50 dollars
    (9,   "PX_tel_defile",   (0.55, 0.5, 1.0), "in",     "cut", 2.5),   # et tu veux aussi te lancer
    (15,  "08",              (0.48, 0.6, 1.1), "in",     "cut", 2.0),   # dans un business
    (18,  "14",              (0.5, 0.45, 1.05), "in",    "zoom", 0),    # Je ne vais pas te parler uniquement des produits digitaux
    (28,  "15",              (0.5, 0.42, 1.0), "in",     "cut", 0),     # Ce n'est pas parce que les produits digitaux…
    (39,  "24",              (0.45, 0.6, 1.0), "in",     "cut", 3.0),   # mais au contraire, ça peut très bien marcher
    (47,  "DASH",            None,             None,     "zoom", 0),    # Moi-même, j'en fais et j'ai gagné beaucoup d'argent
    (55,  "13",              (0.5, 0.5, 1.05), "in",     "cut", 0),     # Mais je ne suis pas trop dedans…
    (69,  "PX_tel_bois",     (0.4, 0.5, 1.0),  "in",     "cut", 1.0),   # Aujourd'hui, je veux te parler
    (75,  "18",              (0.5, 0.5, 1.05), "in",     "cut", 0),     # du commerce physique
    (78,  "32",              (0.5, 0.5, 1.05), "in",     "cut", 0),     # et du commerce online
    (81,  "03",              (0.5, 0.5, 1.05), "in",     "zoom", 0),    # et plus précisément du dropshipping local
    (87,  "PX_tel_pouce",    (0.5, 0.5, 1.0),  "out",    "zoom", 0.5),  # En 2023-2024 (désaturé)
    (95,  "PX_tel_manteau",  (0.42, 0.5, 1.0), "in",     "zoom", 1.0),  # Mais en 2026
    (105, "21",              (0.55, 0.45, 1.05), None,   "cut", 0),     # les commerces en ligne
    (110, "34",              (0.5, 0.45, 1.05), "gauche","cut", 0),     # et les commerces physiques
    (114, "20",              (0.55, 0.78, 1.7), "in",    "cut", 0),     # prennent de plus en plus de place
    (121, "34",              (0.5, 0.55, 1.25), "in",    "zoom", 0),    # Le dropshipping local, c'est vendre des produits disponibles
    (129, "18",              (0.5, 0.5, 1.12), "in",     "cut", 0),     # chez un fournisseur
    (132, "13",              (0.5, 0.5, 1.0),  "in",     "cut", 0),     # sans devoir acheter un gros stock au départ
    (140, "33",              (0.45, 0.5, 1.1), "in",     "cut", 0),     # Donc, tu présentes tes produits
    (146, "32",              (0.5, 0.5, 1.15), None,     "cut", 0),     # sur WhatsApp,
    (147, "16",              (0.5, 0.48, 1.2), None,     "cut", 0),     # Instagram,
    (148, "PX_tel_photo",    (0.5, 0.5, 1.0),  None,     "cut", 2.0),   # TikTok, voire même Facebook
    (152, "PX_message",      (0.5, 0.5, 1.0),  "in",     "cut", 1.0),   # Quand les clients commandent,
    (156, "34",              (0.5, 0.5, 1.15), "in",     "cut", 0),     # tu vérifies la disponibilité auprès du fournisseur
    (163, "02",              (0.5, 0.5, 1.1),  "droite", "cut", 0),     # Tu achètes des produits
    (167, "31",              (0.38, 0.66, 1.75), "in",   "cut", 0),     # et tu organises sa livraison aux clients
    (174, "20",              (0.6, 0.8, 1.9),  None,     "cut", 0),     # Selon l'accord que tu as avec les fournisseurs,
    (182, "01",              (0.48, 0.74, 1.9), "in",    "cut", 0),     # il peut aussi préparer directement le colis
    (187, "03",              (0.55, 0.6, 1.25), None,    "cut", 0),     # le colis.
    (189, "PX_ecriture",     (0.5, 0.62, 1.15), "in",    "zoom", 12.0),  # Pourquoi c'est intéressant quand on débute ?
    (195, "PX_billets2",     (0.5, 0.5, 1.0),  "in",     "cut", 1.0),   # Parce que tu peux commencer avec peu d'argent,
    (203, "PX_tel_blanc",    (0.5, 0.5, 1.0),  None,     "cut", 1.0),   # tester la demande avant d'acheter un gros stock
    (211, "PX_carnet_dessus",(0.5, 0.5, 1.0),  "in",     "cut", 8.0),   # et éviter de bloquer tout ton budget
    (218, "13",              (0.5, 0.5, 1.08), "out",    "cut", 0),     # dans un stock qui risque de ne pas être vendu
    (228, "34",              (0.5, 0.55, 1.2), "in",     "zoom", 0),    # Alors, les produits étant dans le pays,
    (235, "27",              (0.5, 0.55, 1.05), "droite","cut", 0),     # la livraison peut être plus rapide
    (241, "26",              (0.35, 0.5, 1.0), "out",    "cut", 0),     # qu'une commande à l'étranger
    (245, "13",              (0.35, 0.75, 1.8), "in",    "cut", 0),     # Tu peux aussi vérifier la qualité
    (251, "PX_message",      (0.5, 0.5, 1.1),  None,     "cut", 7.0),   # et échanger plus facilement avec ton fournisseur
    (258, "17",              (0.5, 0.5, 1.1),  "in",     "zoom", 0),    # Donc, avec 50 dollars, tu peux commencer petit
    (266, "02",              (0.5, 0.5, 1.1),  "droite", "cut", 0),     # Par exemple, avec des accessoires,
    (271, "34",              (0.5, 0.55, 1.25), "in",    "cut", 0),     # choisis le produit,
    (274, "PX_message",      (0.5, 0.5, 1.2),  "in",     "cut", 3.0),   # renseigne-toi auprès d'un fournisseur local…
    (279, "34",              (0.6, 0.35, 1.7), "in",     "cut", 0),     # sur son prix et sa disponibilité (étiquettes de prix)
    (285, "33",              (0.45, 0.42, 1.35), "in",   "cut", 0),     # Puis présente-le à tes premiers clients
    (291, "19",              (0.62, 0.5, 1.0), None,     "zoom", 0),    # Calcule bien ta marge
    (296, "PX_ecriture",     (0.5, 0.6, 1.1),  None,     "cut", 10.0),  # et prévois aussi les frais…
    (305, "PX_carnet_dessus",(0.5, 0.5, 1.1),  "in",     "zoom", 20.0), # Si tu veux te lancer dans un business à long terme,
    (316, "18",              (0.5, 0.5, 1.05), "in",     "cut", 0),     # le commerce physique
    (319, "PX_tel_manteau",  (0.42, 0.5, 1.05), "in",    "cut", 4.5),   # ou le commerce en ligne peut être une piste à explorer
    (330, "31",              (0.4, 0.62, 1.7), "in",     "zoom", 0),    # Et le dropshipping local peut t'aider…
    (339, "PX_tel_2mains",   (0.5, 0.78, 1.25), None,    "cut", 1.0),   # À apprendre à vendre
    (343, "21",              (0.55, 0.45, 1.15), "in",   "cut", 0),     # et à comprendre ce que tes clients recherchent
    (351, "13",              (0.5, 0.5, 1.08), "out",    "cut", 0),     # sans investir tout ton argent dans un gros stock
    (360, "CTA",             None,             None,     "zoom", 0),    # Alors, pour commencer, écris LOCAL…
]
GRISE = {"PX_tel_pouce"}       # plan « 2023-2024 » en couleurs passées

# Textes à l'écran : (mot de début, mot de fin exclu, type, contenu)
OVERLAYS = [
    (7, 18, "titre", ("50 $", "par où commencer ?")),
    (24, 28, "pastille", "Produits digitaux"),
    (75, 77, "pastille", "Commerce physique"),
    (78, 81, "pastille", "Commerce en ligne"),
    (84, 87, "titre", ("Dropshipping", "local")),
    (87, 95, "annee", "2023-2024"),
    (95, 104, "annee", "2026"),
    (121, 174, "etapes", None),          # Fournisseur → Présentation → Commande → Livraison
    (132, 140, "pastille", "Sans gros stock au départ"),
    (146, 152, "reseaux", None),         # WhatsApp · Instagram · TikTok · Facebook, mot par mot
    (195, 203, "pastille", "Commencer petit"),
    (203, 211, "pastille", "Tester la demande"),
    (235, 241, "pastille", "Livraison plus rapide"),
    (258, 266, "titre", ("50 $", "commencer petit")),
    (271, 291, "trois", None),           # 1 Choisir · 2 Vérifier le prix · 3 Présenter
    (291, 309, "marge", None),           # Achat · Livraison · Communication → Marge
    (330, 339, "pastille", "Étape par étape"),
    (351, 360, "pastille", "Teste. Apprends. Réinvestis."),
]
# étapes : mot où chaque étape s'allume
ETAPES = [("Fournisseur", 129), ("Présentation", 140), ("Commande", 152), ("Livraison", 167)]
TROIS = [("Choisir", 271), ("Vérifier le prix", 274), ("Présenter", 285)]
MARGE = [("Achat", 291), ("Livraison", 299), ("Communication", 302), ("Marge", 304)]
RESEAUX = [("WhatsApp", 146), ("Instagram", 147), ("TikTok", 148), ("Facebook", 151)]

# Sons : (mot, fichier, gain dB, décalage en s) — placés dans les respirations, pas sur les mots importants
SFX = [
    (9, "papier_froisse_billets", -18, -0.15),
    (15, "notification_message_pop", -20, 0.0),
    (18, "page_tournee", -16, -0.05),
    (87, "whoosh_fast_inverse", -17, -0.12),
    (95, "whoosh_air", -19, -0.1),
    (152, "clavier_telephone", -26, 0.0),
    (182, "papier_tranche_ruban", -15, 0.0),
    (241, "whoosh_fast", -18, -0.1),
    (291, "touches_calculatrice", -22, 0.0),
    (363, "clavier_telephone", -22, 0.0),
    (374, "validation_douce", -14, 0.3),
]
CTA_HOLD = 3.0
