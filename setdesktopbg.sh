#!/bin/bash
#
#
new=$(find /home/alexandre/Imagens/wallpapers/*.jpg -type f -printf "%f\n" | shuf | sed -n 1p)

feh --bg-fill /home/alexandre/Imagens/wallpapers/$new --bg-fill /home/alexandre/Imagens/wallpapers/mirror/$new

echo $new
