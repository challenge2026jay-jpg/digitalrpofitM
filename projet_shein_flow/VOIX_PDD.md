# Voix de Samantha — vidéo « Pinduoduo en français » (version motion, 30 s)

La vidéo `export/pinduoduo_wechat_motion_9x16.mp4` est montée sur ce texte : chaque phrase s'affiche mot à mot
dans la bulle à côté du visage. Il suffit d'ajouter la voix.

**Deux façons de l'ajouter**
1. **Ta voix clonée ElevenLabs** (« voix de samantha claude ») : il faut environ 570 crédits pour une prise
   (le compte en a 40). Dès que les crédits sont rechargés, je génère la voix et je remonte la vidéo.
2. **Ta vraie voix** : enregistre ce texte en note vocale WhatsApp ou au dictaphone, d'un ton naturel, puis
   mets le fichier dans le Drive. Je le cale sur l'image.

Dans les deux cas, le fichier va dans `audio/voix_pdd.mp3`, puis on relance `python3 build_pdd_motion.py` :
la musique baisse automatiquement sous la voix.

| Temps | Phrase |
|---|---|
| 0,0 – 2,4 s | Pinduoduo est en chinois ? |
| 2,4 – 4,6 s | Regarde, je te le mets en français avec WeChat. |
| 4,6 – 7,4 s | Ouvre WeChat, va dans « Moi », |
| 7,4 – 9,6 s | puis « Paramètres » et « Généralités ». |
| 9,6 – 12,0 s | Touche « Gérer la page Découvrir » |
| 12,0 – 14,0 s | et active les « Mini-programmes ». |
| 14,0 – 16,8 s | Dans « Découvrir », ouvre « Mini-programmes » et cherche Pinduoduo. |
| 16,8 – 19,4 s | Appuie sur « Traduction »… et voilà : c'est en français ! |
| 19,4 – 22,6 s | Tu es en RDC ? J'ai réuni la liste des transitaires et des fournisseurs dans mon groupe WhatsApp. |
| 22,6 – 25,4 s | Le lien est dans ma bio. Si tu bloques, écris-moi « PDD ». |
| 25,4 – 29,6 s | Et pour aller plus loin : mes formations. |

## Ce qu'il y a à l'écran

- **Vrais logos** : Pinduoduo (cœur rouge), WeChat (bulles blanches sur vert), WhatsApp. Ils servent
  uniquement à montrer de quelle appli on parle.
- **Visage de Samantha** dans un cercle en bas à gauche : il change d'expression selon la phrase (pensive,
  souriante, rieuse) et un anneau orange pulse quand elle « parle ». Mention « Visage généré par IA ».
- **Drapeau de la RDC** (dessiné) + « TRANSITAIRES » / « FOURNISSEURS » + « dans mon groupe WhatsApp ».
- **Capture de ta chaîne WhatsApp** + « Lien dans ma bio » + « Si tu bloques : écris « PDD » ».
- **Pages de formation** IA Motion Design (335+ apprenants) et Claude Transform (128+ apprenants).
