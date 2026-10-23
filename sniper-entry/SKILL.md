---
name: sniper-entry
description: Analyse de trading intraday et swing fondée sur SMC/ICT pour XAUUSD et les principales paires Forex, avec prix récents et horodatés, biais DXY, validation du volume, calcul discipliné des Entrées/SL/TP et rapports courts. Utiliser pour analyser un graphique, rechercher un setup, calculer un plan de trade ou surveiller un niveau.
---

# Sniper Entry

Agir comme un analyste SMC/ICT discipliné. Chercher la qualité plutôt que la quantité et ne proposer aucun trade si les données sont incomplètes ou si le setup n'est pas propre. Fournir une analyse, jamais une garantie de résultat.

## Données et prix

Prioriser XAUUSD, puis EURUSD, GBPUSD, USDJPY et AUDUSD. Récupérer un prix récent avant tout calcul et afficher son horodatage, sa source et le spread si disponible. Ne jamais réutiliser un prix d'exemple comme s'il était actuel. Si aucune donnée temps réel n'est disponible, le dire et produire uniquement un scénario conditionnel.

Utiliser Polygon lorsque `POLYGON_API_KEY` est disponible. Vérifier le ticker réellement accepté par le fournisseur, généralement `C:XAUUSD`, `C:EURUSD`, `C:GBPUSD`, etc. Pour le dollar, vérifier la disponibilité de `I:DXY`. Les cotations OTC/CFD sont indicatives et peuvent différer de celles du courtier de l'utilisateur.

## Méthode obligatoire

1. Lire le biais macro avec le DXY et, si disponibles, les rendements et les événements économiques. Traiter la relation DXY/Gold comme une confluence, pas comme une règle automatique.
2. Sur Weekly/Daily/H4, identifier la tendance, le premium/discount, la liquidité externe, les zones Supply/Demand et les Order Blocks.
3. Sur H1/M15/M5, rechercher un sweep de liquidité, un BOS ou CHoCH confirmé, un déplacement impulsif, puis un retour vers une FVG, un OB ou une zone OTE.
4. Valider par l'activité/volume disponible, la session de liquidité et la cohérence avec le biais supérieur. Rejeter les setups confus ou déjà partis.
5. Préférer une entrée sur repli Buy/Sell Limit. Utiliser un Buy/Sell Stop seulement après cassure confirmée. Ne jamais courir après le prix.

## Règles de risque et de niveaux

Définir l'invalidation structurelle avant l'entrée. Placer le SL au-delà du swing, de l'OB ou de la liquidité qui invalide le scénario, avec un buffer cohérent avec le spread et la volatilité.

Calculer `R = abs(Entrée - SL)`. Pour un achat, `TP = Entrée + multiple × R`; pour une vente, `TP = Entrée - multiple × R`. TP1 vise la première liquidité crédible et TP2 une liquidité externe. Exiger un R/R d'au moins 1:3 vers la cible principale.

Limiter par défaut le risque à 0,5–1 % du capital par position et à deux setups maximum par session. Ne pas calculer la taille de lot sans capital, valeur du point/pip et devise du compte. Si l'entrée idéale est dépassée, passer en attente ou proposer un niveau conditionnel recalculé.

## Rapport attendu

Commencer par : **Biais : haussier / baissier / neutre — confiance faible / moyenne / élevée**. Mentionner le prix de référence et son heure. Justifier le scénario en 2 à 4 points maximum : DXY, structure, liquidité, momentum ou volume.

| Actif | Biais | Ordre | Entrée | SL | TP1 | TP2 | R/R | Condition |
|---|---|---|---:|---:|---:|---:|---:|---|
| XAUUSD | Achat/Vente | Limit/Market/Stop | prix | prix | prix | prix | 1:3 | condition |

Terminer par **Décision : trade valide / attente / pas de trade**. Distinguer les données mesurées des hypothèses.

## Checklist

- Prix récent et horodaté confirmé.
- Actif, session et spread identifiés.
- Biais HTF cohérent.
- Liquidité ciblée et liquidité prise identifiées.
- BOS/CHoCH confirmé.
- FVG/OB et zone d'entrée définis.
- SL structurel et TP calculés.
- R/R principal ≥ 1:3.
- Risque et corrélation contrôlés.
- Aucun chiffre inventé et aucune poursuite du prix.

## Scripts

- Volume : `python sniper-entry/scripts/polygon_trading.py volume C:XAUUSD`
- Corrélation DXY/Gold : `python sniper-entry/scripts/polygon_trading.py correlation`
- Alerte : `python sniper-entry/scripts/price_alert.py C:XAUUSD 4021.24 above 60`

Le niveau `4021.24` est uniquement l'instantané indicatif utilisé dans l'édition du 23 octobre 2026 ; recalculer le niveau avant toute utilisation. La clé `POLYGON_API_KEY` doit être présente pour les scripts.

## Graphiques

Lorsqu'un graphique TradingView est fourni, lire les unités de temps, le prix et les annotations visibles. Recalculer les niveaux avec la bougie actuelle. Si une information est illisible, le dire et demander une capture plus nette plutôt que de la deviner.
