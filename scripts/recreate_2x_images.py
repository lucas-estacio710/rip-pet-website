#!/usr/bin/env python3
"""
Recriar imagens @2x corretamente mantendo proporções originais
"""

from PIL import Image
import os

# Processar cada imagem mantendo aspect ratio original
images = [
    'images/matriz_pinda.jpg',
    'images/matriz_pinda2.jpg',
    'images/matriz_pinda3.jpg'
]

for img_path in images:
    print(f"\nProcessando {img_path}...")

    # Abrir imagem original
    img = Image.open(img_path)
    print(f"   Original: {img.size}")

    # Calcular nova largura máxima (1200px) mantendo aspect ratio
    max_width = 1200
    ratio = img.height / img.width
    new_width = max_width
    new_height = int(new_width * ratio)

    print(f"   Redimensionando para: {new_width}x{new_height}")

    # Redimensionar mantendo proporções
    img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Salvar como WebP @2x
    output_name = img_path.replace('.jpg', '_opt@2x.webp')
    img_resized.save(output_name, 'WEBP', quality=85, method=6)

    size = os.path.getsize(output_name) / 1024
    print(f"   Criado: {output_name} - {size:.1f} KB")

print("\nImagens @2x recriadas corretamente!")
