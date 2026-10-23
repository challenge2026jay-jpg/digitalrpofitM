# Sniper Entry

Compétence d'analyse de trading SMC/ICT pour XAUUSD et les principales paires Forex (EURUSD, GBPUSD, USDJPY, AUDUSD), basée sur le guide *Sniper Entry*.

## Contenu

- `SKILL.md` : la compétence elle-même (méthode, règles de risque, format du rapport, checklist).
- `scripts/polygon_trading.py` : analyse du volume et corrélation DXY/Or via l'API Polygon.
- `scripts/price_alert.py` : surveillance d'un niveau de prix.

## Utilisation

Pour l'installer comme compétence Claude, copiez le dossier `sniper-entry/` dans votre dossier de compétences (par exemple `~/.claude/skills/sniper-entry/`), ou importez-le depuis les paramètres de compétences de claude.ai.

Les scripts nécessitent Python, le paquet `polygon-api-client` (`pip install polygon-api-client`) et une clé dans la variable d'environnement `POLYGON_API_KEY`. Ne commitez jamais cette clé dans le dépôt.

## Avertissement

Cette compétence fournit une analyse, jamais une garantie de résultat. Le trading comporte un risque de perte en capital.
