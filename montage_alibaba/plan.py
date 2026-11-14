"""Plan de montage (source de vérité) — TikTok « Commander sur Alibaba ».

Chaque plan commence à `t` (secondes, timeline de la voix off) et se termine
au début du plan suivant. Les timings viennent de la transcription horodatée
mot à mot de la voix off (audio/voix_off_words.json).

Modes de cadrage
  fill : recadrage 9:16 plein cadre. c=(cx,cy) centre normalisé, z=zoom
         (1 = plus grand cadre 9:16 contenu dans la source). c0/c1 et z0/z1
         sont interpolés du début à la fin du plan (Ken Burns).
  fit  : capture d'écran / enregistrement d'écran : la zone `box` (normalisée
         x0,y0,x1,y1, interpolée box0->box1) est posée en carte arrondie sur un
         fond flouté de la même source. `hl` = rectangle jaune de mise en
         évidence (pixels source).
  logo : logo centré sur fond crème.
  card : fond flouté sombre + grand texte (géré par les overlays).
"""

TOTAL = 143.2  # durée totale (voix 141.82 s + respiration finale)

M = "media/"
ALI = M + "alibaba recherch produit.mp4"
LAPTOP = M + "5585988-hd_1080_1920_30fps.mp4"
CARD = M + "6633345-hd_1080_1920_25fps.mp4"
PHONE = M + "6651432-uhd_4096_2160_25fps.mp4"
HANDOFF = M + "7835286-uhd_3840_2160_25fps.mp4"
LABELV = M + "7855148-uhd_3840_2160_25fps.mp4"
WA = M + "1089871178582673740.jpg"
TRANSPORT = M + "1105844883513817896.jpg"
ALILOGO = M + "757730706103895999.jpg"
TRUCK = M + "896708975821689274.jpg"
SCALE = M + "Big Order.jpg"
LOADING = M + "Custom Canvas Totes – Ready for Your Brand.jpg"
LABEL = M + "MIL-STD-129 Labeling.jpg"
PAY = M + "Make the Last Step Feel Effortless with Free Payment UI Kits.jpg"
VERIF = M + "verified ca du fournis.png"

# carte fournisseur dans la capture « verified ca du fournis » (normalisé)
SUPPLIER_BOX = (0.072, 0.422, 0.376, 0.784)

SHOTS = [
    # --- ACCROCHE ---
    dict(t=0.00, src=ALILOGO, mode="logo", z0=1.18, z1=1.0,
         phrase="Commander sur Alibaba n'a jamais été aussi simple"),
    dict(t=2.40, src=ALI, ss=0.0, mode="fit", box0=(0.0, 0.07, 0.44, 0.86), box1=(0.03, 0.10, 0.40, 0.70),
         phrase="qu'en 2026."),
    dict(t=4.40, src=LAPTOP, ss=0.0, speed=0.85, mode="fill", c0=(0.5, 0.40), c1=(0.5, 0.36), z0=1.0, z1=1.12,
         phrase="Si tu payes encore des formations pour apprendre ça,"),
    dict(t=6.95, src=PHONE, ss=0.0, mode="fill", c0=(0.36, 0.50), c1=(0.37, 0.48), z0=1.05, z1=1.18,
         phrase="je suis désolée pour toi."),
    dict(t=8.80, src=ALI, ss=2.6, mode="fit", box0=(0.0, 0.07, 0.44, 0.86), box1=(0.05, 0.10, 0.42, 0.62),
         phrase="Aujourd'hui, je t'explique de A à Z comment tu peux commander"),
    dict(t=12.55, src=ALI, ss=13.3, mode="fit", box0=(0.0, 0.06, 0.50, 0.97), box1=(0.0, 0.10, 0.40, 0.80),
         phrase="sur Alibaba en moins de deux minutes."),
    dict(t=15.55, src=LABELV, ss=7.0, mode="fill", c0=(0.55, 0.55), c1=(0.55, 0.52), z0=1.0, z1=1.14,
         phrase="Parce que franchement, il n'y a rien de plus simple que ça."),
    # --- ÉTAPE 1 : TRANSITAIRE ---
    dict(t=18.65, src=ALI, ss=7.9, mode="fit", box0=(0.0, 0.07, 0.44, 0.86), box1=(0.04, 0.12, 0.40, 0.72),
         phrase="La première chose avant de toucher Alibaba,"),
    dict(t=21.60, src=HANDOFF, ss=0.2, mode="fill", c0=(0.30, 0.64), c1=(0.33, 0.64), z0=1.3, z1=1.4,
         phrase="c'est de trouver un transitaire."),
    dict(t=23.85, src=TRUCK, mode="fill", c0=(0.30, 0.45), c1=(0.62, 0.55), z0=1.3, z1=1.3,
         phrase="Lui, il va t'apporter ton colis de la Chine jusqu'à ton pays."),
    dict(t=27.90, src=LOADING, mode="fill", c0=(0.55, 0.55), c1=(0.52, 0.55), z0=1.0, z1=1.12,
         phrase="Il y en a plein, ça dépend de ton pays."),
    dict(t=30.35, src=PHONE, ss=2.0, mode="fill", c0=(0.37, 0.50), c1=(0.36, 0.48), z0=1.1, z1=1.25,
         phrase="Tu les contactes, tu leur poses quatre questions précises."),
    dict(t=33.65, src=SCALE, mode="fill", c0=(0.38, 0.32), c1=(0.38, 0.28), z0=1.5, z1=2.0,
         phrase="Le prix du kilo en fonction du produit"),
    dict(t=36.40, src=TRANSPORT, mode="fill", c0=(0.60, 0.56), c1=(0.62, 0.55), z0=1.7, z1=1.95,
         phrase="et du CBM si tu veux par exemple envoyer par bateau."),
    dict(t=39.55, src=TRANSPORT, mode="fill", c0=(0.50, 0.20), c1=(0.53, 0.18), z0=1.7, z1=1.95,
         phrase="La durée d'envoi en fonction de la méthode que tu choisis."),
    dict(t=42.50, src=TRUCK, mode="fill", c0=(0.78, 0.50), c1=(0.78, 0.48), z0=1.5, z1=1.7,
         phrase="Leur adresse en Chine."),
    dict(t=43.90, src=LABEL, mode="fill", c0=(0.47, 0.55), c1=(0.47, 0.52), z0=1.0, z1=1.3,
         phrase="Et tout simplement aussi le shipping mark."),
    dict(t=46.30, src=LABELV, ss=0.0, mode="fill", c0=(0.42, 0.50), c1=(0.45, 0.50), z0=1.0, z1=1.1,
         phrase="Tu valides cette étape avant de passer à la suite."),
    dict(t=48.85, src=LABELV, ss=2.6, mode="card",
         phrase="C'est non négociable."),
    # --- ÉTAPE 2 : FOURNISSEUR ---
    dict(t=50.05, src=ALI, ss=10.4, mode="fit", box0=(0.0, 0.07, 0.50, 0.97), box1=(0.0, 0.10, 0.42, 0.85),
         phrase="Maintenant, tu vas sur Alibaba, tu cherches ton produit"),
    dict(t=52.90, src=ALI, ss=15.6, mode="fit", box0=(0.0, 0.06, 0.50, 0.97), box1=(0.02, 0.10, 0.42, 0.85),
         phrase="et là, tu ne choisis pas n'importe qui."),
    dict(t=55.30, src=ALI, ss=18.3, mode="fit", box0=(0.45, 0.06, 0.95, 0.97), box1=(0.50, 0.10, 0.90, 0.80),
         phrase="Tu filtres sur ces quatre critères seulement."),
    dict(t=58.00, src=VERIF, mode="fit", box0=SUPPLIER_BOX, box1=(0.07, 0.43, 0.30, 0.62), hl=(340, 485, 390, 514), fy=1000,
         phrase="Le fournisseur doit avoir au minimum deux ans sur la plateforme,"),
    dict(t=61.60, src=VERIF, mode="fit", box0=(0.07, 0.43, 0.378, 0.62), box1=(0.18, 0.43, 0.378, 0.56), hl=(643, 449, 711, 474), fy=1000,
         phrase="un statut vérifié,"),
    dict(t=62.90, src=VERIF, mode="fit", box0=SUPPLIER_BOX, box1=(0.12, 0.52, 0.378, 0.70), hl=(555, 581, 633, 652), fy=1000,
         phrase="des avis positifs"),
    dict(t=64.60, src=ALI, ss=19.0, mode="card",
         phrase="et le Trade Assurance."),
    dict(t=66.00, src=HANDOFF, ss=5.4, mode="fill", c0=(0.64, 0.50), c1=(0.66, 0.50), z0=1.0, z1=1.1,
         phrase="C'est la garantie d'Alibaba que si ton fournisseur te douille, Alibaba va te rembourser."),
    dict(t=71.10, src=VERIF, mode="fit", box0=(0.04, 0.0, 0.48, 0.55), box1=(0.04, 0.42, 0.48, 0.97),
         phrase="Si tu veux encore plus de sécurité, tu scrolles vers le bas de sa page"),
    dict(t=75.10, src=VERIF, mode="fit", box0=SUPPLIER_BOX, box1=(0.066, 0.55, 0.37, 0.72), hl=(155, 581, 273, 652),
         phrase="et tu regardes le montant qu'il a reçu depuis sa création."),
    dict(t=78.55, src=ALI, ss=13.3, mode="card",
         phrase="Un fournisseur avec un million de dollars de transaction, c'est bon signe."),
    dict(t=82.40, src=ALI, ss=5.0, mode="fit", box0=(0.0, 0.07, 0.44, 0.86), box1=(0.03, 0.10, 0.40, 0.70),
         phrase="Tu as trouvé ton fournisseur ? C'est parfait."),
    dict(t=85.50, src=VERIF, mode="fit", box0=SUPPLIER_BOX, box1=(0.07, 0.43, 0.37, 0.76), fy=760,
         phrase="Tu cliques maintenant tout simplement sur « Contact Supplier »."),
    # --- ÉTAPE 3 : MESSAGE + PAIEMENT ---
    dict(t=89.60, src=PHONE, ss=5.3, mode="fill", c0=(0.37, 0.50), c1=(0.37, 0.47), z0=1.15, z1=1.3,
         phrase="Tu lui envoies un message simple."),
    dict(t=91.60, src=LAPTOP, ss=0.0, speed=0.21, mode="card",
         phrase="« Hello, I hope you are well. I'm interested of your product. Could you please send me your best price for this quantity and the product specification and some picture. »"),
    dict(t=102.10, src=LAPTOP, ss=0.0, speed=0.75, mode="fill", c0=(0.5, 0.42), c1=(0.5, 0.40), z0=1.05, z1=1.15,
         phrase="Juste des trucs qui sont aussi simples que ça."),
    dict(t=105.00, src=PHONE, ss=7.0, speed=0.8, mode="fill", c0=(0.37, 0.50), c1=(0.37, 0.48), z0=1.2, z1=1.3,
         phrase="Il te répond, vous vous mettez d'accord."),
    dict(t=107.00, src=PAY, mode="fit", box0=(0.0, 0.0, 1.0, 1.0), box1=(0.05, 0.05, 0.95, 0.95), fw=760, fy=900,
         phrase="Et là, il t'envoie le lien de paiement et tu règles,"),
    dict(t=109.55, src=CARD, ss=5.8, mode="fill", c0=(0.45, 0.62), c1=(0.45, 0.60), z0=1.8, z1=1.95,
         phrase="que ce soit avec ta carte."),
    dict(t=111.30, src=CARD, ss=0.0, mode="fill", c0=(0.45, 0.62), c1=(0.44, 0.60), z0=1.6, z1=1.85,
         phrase="Moi, personnellement, j'utilise la carte virtuelle d'Orange Money."),
    dict(t=114.95, src=ALI, ss=18.6, mode="fit", box0=(0.0, 0.06, 0.50, 0.97), box1=(0.0, 0.12, 0.34, 0.62),
         phrase="Le taux de change, il est parfait."),
    # --- ÉTAPE 4 : COLIS ---
    dict(t=117.50, src=LOADING, mode="fill", c0=(0.36, 0.72), c1=(0.40, 0.70), z0=1.5, z1=1.65,
         phrase="Une fois que tu as payé, tu demandes deux choses à ton fournisseur."),
    dict(t=120.95, src=LABELV, ss=10.0, mode="fill", c0=(0.55, 0.45), c1=(0.55, 0.43), z0=1.0, z1=1.12,
         phrase="Une photo du colis avec le shipping mark bien visible"),
    dict(t=124.05, src=SCALE, mode="fill", c0=(0.50, 0.62), c1=(0.48, 0.55), z0=1.0, z1=1.25,
         phrase="et le tracking code ainsi que le poids pour que tu puisses faire tes calculs."),
    dict(t=127.95, src=LABEL, mode="fill", c0=(0.47, 0.45), c1=(0.47, 0.42), z0=1.6, z1=2.0,
         phrase="Tu prends ce tracking code ainsi que le poids,"),
    dict(t=130.60, src=TRANSPORT, mode="fill", c0=(0.50, 0.40), c1=(0.50, 0.70), z0=1.05, z1=1.05,
         phrase="tu envoies ça à ton transitaire"),
    dict(t=132.60, src=TRUCK, mode="fill", c0=(0.42, 0.50), c1=(0.48, 0.50), z0=1.0, z1=1.15,
         phrase="et là, c'est tout. Ton colis, là, il est en route."),
    dict(t=135.60, src=HANDOFF, ss=2.7, mode="fill", c0=(0.66, 0.50), c1=(0.66, 0.50), z0=1.0, z1=1.08,
         phrase="Voilà, c'est aussi simple que ça."),
    # --- CTA ---
    dict(t=137.60, src=WA, mode="logo", z0=1.15, z1=1.0,
         phrase="Pour plus d'astuces, rejoins ma chaîne WhatsApp. Le lien est dans ma bio."),
]

# Fenêtres où les sous-titres classiques sont remplacés par un texte écran synchronisé
SUB_HIDE = [(48.85, 50.05), (91.60, 102.10), (137.60, TOTAL)]

# Mots-clés en jaune (comparaison sans ponctuation, insensible à la casse)
KEYWORDS = ["alibaba", "d'alibaba", "transitaire", "prix", "cbm", "trade", "assurance",
            "shipping", "mark", "tracking", "code"]

# Effets sonores : (temps, fichier, gain dB, durée max s ou None, fondu sortie s)
SFX = [
    (0.00, "whoosh_fast", -8, None, 0),
    (0.05, "impact_deep_whoosh", -16, 1.6, 0.8),       # petit impact doux d'accroche
    (21.55, "whoosh_air", -6, None, 0),                  # « trouver un transitaire »
    (23.80, "whoosh_fast", -12, None, 0),
    (33.76, "check_box", -3, None, 0),                   # checklist transitaire
    (39.66, "check_box", -3, None, 0),
    (42.60, "check_box", -3, None, 0),
    (45.42, "check_box", -3, None, 0),
    (48.95, "impact_deep_whoosh", -15, 1.8, 1.0),       # « non négociable »
    (50.92, "mouse_double", -4, None, 0),                # recherche Alibaba
    (51.88, "typing_laptop", -12, 0.9, 0.2),
    (53.02, "mouse_clicks", -6, None, 0),
    (55.40, "mouse_double", -6, None, 0),
    (59.52, "check_box", -3, None, 0),                   # critères fournisseur
    (61.82, "check_box", -3, None, 0),
    (63.26, "check_box", -3, None, 0),
    (64.70, "check_box", -3, None, 0),
    (73.50, "whoosh_air", -14, None, 0),                 # scroll
    (87.82, "mouse_double", -2, None, 0),                # clic « Contact Supplier »
    (90.00, "typing_laptop", -14, 1.3, 0.3),             # message
    (92.00, "typing_laptop", -18, 4.0, 1.0),
    (109.20, "confirmation_tone", -16, None, 0),         # paiement
    (121.10, "camera_shutter", -5, None, 0),             # photo du colis
    (124.22, "scanner_beeps", -24, 0.7, 0.2),            # tracking code
    (125.82, "check_box", -5, None, 0),                  # poids
    (130.55, "whoosh_air", -12, None, 0),
    (132.70, "truck_steady", -22, 4.6, 1.5),             # colis en route
    (137.55, "whoosh_air", -10, None, 0),                # CTA
    (139.50, "long_pop", -5, None, 0),
]

MUSIC_GAIN_DB = -23
MUSIC_DUCK = (48.80, 50.15, 0.12)   # baisse de la musique sur « non négociable »

# ------------------------------------------------------------------ version 3
# L'intro est réenregistrée avec une formulation sans promesse (même voix clonée) :
#   « Commander sur Alibaba n'a jamais été aussi simple qu'en 2026. Pas besoin de te
#     compliquer la vie avec ça. Aujourd'hui, je t'explique de A à Z comment tu peux
#     commander sur Alibaba, étape par étape. Parce que franchement, il n'y a rien de
#     plus simple que ça. »
# Elle remplace la voix d'origine de 0 à ORIG_RESUME (« La première chose… »), le reste
# de la voix d'origine est conservé tel quel et décalé de DELTA.
INTRO_VOICE = "audio/intro_v3.mp3"
INTRO_WORDS = "audio/intro_v3_words.json"
INTRO_DUR = 443 / 30          # fin de l'intro réenregistrée (+ respiration)
ORIG_RESUME = 561 / 30        # reprise de la voix d'origine (18,70 s, dans le silence)
DELTA = INTRO_DUR - ORIG_RESUME
FIRST_KEPT = 7                # index dans SHOTS du premier plan d'origine conservé (18,65 s)

INTRO_SHOTS = [
    dict(t=0.00, src=ALILOGO, mode="logo", z0=1.18, z1=1.0,
         phrase="Commander sur Alibaba n'a jamais été aussi simple"),
    dict(t=2.90, src=ALI, ss=0.0, mode="fit", box0=(0.0, 0.07, 0.44, 0.86), box1=(0.03, 0.10, 0.40, 0.70),
         phrase="qu'en 2026."),
    dict(t=4.35, src=LAPTOP, ss=0.0, speed=0.85, mode="fill", c0=(0.5, 0.40), c1=(0.5, 0.36), z0=1.0, z1=1.12,
         phrase="Pas besoin de te compliquer la vie avec ça."),
    dict(t=6.70, src=ALI, ss=2.6, mode="fit", box0=(0.0, 0.07, 0.44, 0.86), box1=(0.05, 0.10, 0.42, 0.62),
         phrase="Aujourd'hui, je t'explique de A à Z comment tu peux commander"),
    dict(t=9.92, src=ALI, ss=13.3, mode="fit", box0=(0.0, 0.06, 0.50, 0.97), box1=(0.0, 0.10, 0.40, 0.80),
         phrase="sur Alibaba, étape par étape."),
    dict(t=11.95, src=LABELV, ss=7.0, mode="fill", c0=(0.55, 0.55), c1=(0.55, 0.52), z0=1.0, z1=1.14,
         phrase="Parce que franchement, il n'y a rien de plus simple que ça."),
]

def to_new(t):
    """Temps de la timeline d'origine -> temps de la vidéo v3 (partie conservée)."""
    return t + DELTA if t >= SHOTS[FIRST_KEPT]["t"] else t

NEW_TOTAL = TOTAL + DELTA

def timeline():
    """Liste (plan, début, fin, décalage) dans le temps de la v3 ; décalage = DELTA pour les plans d'origine."""
    items = [(s, s["t"], 0.0) for s in INTRO_SHOTS] + [(s, s["t"] + DELTA, DELTA) for s in SHOTS[FIRST_KEPT:]]
    out = []
    for i, (s, t0, off) in enumerate(items):
        t1 = items[i + 1][1] if i + 1 < len(items) else NEW_TOTAL
        out.append((s, t0, t1, off))
    return out

def sfx_new(t):
    """Effets de l'accroche gardés tels quels, les autres suivent la voix d'origine."""
    return t if t < 1.0 else t + DELTA
