#!/usr/bin/env python3
"""
Script para criar versão da logo com fundo transparente
"""
from PIL import Image
import os

def remove_white_background(input_path, output_path, threshold=240):
    """Remove fundo branco/claro da imagem e salva com transparência"""
    # Abrir imagem
    img = Image.open(input_path)

    # Converter para RGBA se necessário
    img = img.convert("RGBA")

    # Pegar dados dos pixels
    datas = img.getdata()

    new_data = []
    for item in datas:
        # Trocar pixels brancos/claros por transparente
        # Se R, G e B forem maiores que threshold, tornar transparente
        if item[0] > threshold and item[1] > threshold and item[2] > threshold:
            new_data.append((255, 255, 255, 0))  # Transparente
        else:
            new_data.append(item)

    # Atualizar dados da imagem
    img.putdata(new_data)

    # Salvar
    img.save(output_path, "PNG")
    print(f"✓ Logo transparente criada: {output_path}")

    # Também criar versão WebP otimizada
    webp_path = output_path.replace('.png', '.webp')
    img.save(webp_path, "WEBP", quality=90, method=6)
    print(f"✓ Logo WebP criada: {webp_path}")

if __name__ == "__main__":
    # Usar a logo com melhor transparência como base
    input_file = "assets/rippet_logo_horizontal_fundo_clarot.png"
    output_file = "assets/rippet_logo_transparent.png"

    print("Criando logo com fundo transparente...")
    remove_white_background(input_file, output_file, threshold=240)
    print("\nPronto! Logos criadas com sucesso.")
