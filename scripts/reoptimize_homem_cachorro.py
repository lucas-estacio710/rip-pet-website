#!/usr/bin/env python3
"""
Reotimizar homem-cachorro.png (nova versão)
"""

from PIL import Image
import os

input_path = 'images/homem-cachorro.png'
output_webp = 'images/homem-cachorro.webp'

print(f"Otimizando {input_path}...")

# Abrir imagem
img = Image.open(input_path)
original_size = os.path.getsize(input_path) / 1024
print(f"   Tamanho original: {img.size} - {original_size:.1f} KB")

# Converter para WebP com qualidade 85
img.save(output_webp, 'WEBP', quality=85, method=6)

# Verificar tamanhos
webp_size = os.path.getsize(output_webp) / 1024
reduction = ((original_size - webp_size) / original_size) * 100

print(f"WebP criado: {output_webp}")
print(f"   PNG: {original_size:.1f} KB")
print(f"   WebP: {webp_size:.1f} KB")
print(f"   Reducao: {reduction:.1f}%")
