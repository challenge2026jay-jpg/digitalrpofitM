#!/usr/bin/env bash
# Télécharge les ressources Mixkit utilisées par la vidéo « Dropshipping local en RDC ».
# Elles ne sont pas versionnées : les licences Mixkit interdisent de redistribuer les fichiers seuls.
# Licences vérifiées sur https://mixkit.co/license/ (Sound Effects Free License, Stock Music Free License).
# Le fichier de chaque son est celui que propose sa fenêtre de téléchargement Mixkit (WAV ou MP3 selon le son).
set -euo pipefail
UA="Mozilla/5.0"
# Mixkit refuse parfois des requêtes trop rapprochées (403) : pause et nouvelles tentatives.
get() { for n in 1 2 3 4; do curl -sSf -A "$UA" "$@" && return 0; sleep $((n * 3)); done; return 1; }

cd "$(dirname "$0")/../public" && mkdir -p mixkit && cd mixkit
for id in 1490 3120 2568 2354 1393 1530 2841 2569 2868 1112 2865 2867; do
  url=$(get "https://mixkit.co/free-sound-effects/download/$id/?context=item+grid" | grep -oE "https://assets\.mixkit\.co/active_storage/sfx/$id/[^\"]+\.(wav|mp3)" | head -1)
  ext="${url##*.}"
  get -o "sfx-$id.$ext" "$url"
  [ "$ext" = wav ] || ffmpeg -hide_banner -loglevel error -y -i "sfx-$id.$ext" "sfx-$id.wav"
  sleep 1
done
get -o "music-568.mp3" "https://assets.mixkit.co/music/568/568.mp3"
ls -la
