#!/usr/bin/env python3
"""
RIP PET - Script de Otimização de Imagens
Converte para WebP, redimensiona e cria versões @2x para retina.

USO:
    python scripts/optimize_image.py imagem.jpg              # Otimiza com padrões
    python scripts/optimize_image.py imagem.jpg -w 800       # Define largura máxima
    python scripts/optimize_image.py imagem.jpg -q 90        # Define qualidade
    python scripts/optimize_image.py images/*.jpg            # Múltiplas imagens

REQUISITOS:
    pip install Pillow
"""

import os
import sys
import argparse
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("ERRO: Pillow não instalado. Execute: pip install Pillow")
    sys.exit(1)


def optimize_image(input_path, output_dir=None, target_width=None, quality=85, create_2x=True):
    """
    Otimiza uma imagem: redimensiona, converte para WebP e cria versão @2x.

    Args:
        input_path: Caminho da imagem original
        output_dir: Diretório de saída (None = mesmo diretório)
        target_width: Largura máxima (None = mantém original)
        quality: Qualidade WebP (1-100)
        create_2x: Criar versão @2x para telas retina

    Returns:
        dict com informações da otimização
    """
    input_path = Path(input_path)

    if not input_path.exists():
        print(f"  ERRO: {input_path} não encontrado")
        return None

    # Definir diretório de saída
    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    else:
        output_dir = input_path.parent

    # Nome base para saída
    stem = input_path.stem
    if stem.endswith('_opt'):
        stem = stem[:-4]  # Remove _opt se já existir

    print(f"\n{'='*50}")
    print(f"Processando: {input_path.name}")
    print(f"{'='*50}")

    # Abrir imagem
    img = Image.open(input_path)
    original_size = input_path.stat().st_size

    print(f"  Original: {img.size[0]}x{img.size[1]} | {original_size / 1024:.1f} KB")

    # Redimensionar se necessário
    if target_width and img.width > target_width:
        ratio = target_width / img.width
        new_height = int(img.height * ratio)
        img_1x = img.resize((target_width, new_height), Image.Resampling.LANCZOS)
        print(f"  Redimensionado: {img_1x.size[0]}x{img_1x.size[1]}")
    else:
        img_1x = img.copy()
        target_width = img.width

    # Criar versão @2x
    if create_2x and img.width >= target_width * 2:
        new_height_2x = int(img.height * (target_width * 2) / img.width)
        img_2x = img.resize((target_width * 2, new_height_2x), Image.Resampling.LANCZOS)
    else:
        img_2x = None

    # Converter RGBA para RGB se necessário
    def convert_to_rgb(image):
        if image.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'P':
                image = image.convert('RGBA')
            if image.mode in ('RGBA', 'LA'):
                background.paste(image, mask=image.split()[-1])
            return background
        elif image.mode != 'RGB':
            return image.convert('RGB')
        return image

    img_1x = convert_to_rgb(img_1x)
    if img_2x:
        img_2x = convert_to_rgb(img_2x)

    results = {'original_size': original_size, 'files': []}

    # Salvar WebP 1x
    webp_path = output_dir / f"{stem}_opt.webp"
    img_1x.save(webp_path, 'WEBP', quality=quality, method=6)
    webp_size = webp_path.stat().st_size
    results['files'].append(str(webp_path))
    print(f"  WebP: {webp_size / 1024:.1f} KB")

    # Salvar WebP 2x
    if img_2x:
        webp_2x_path = output_dir / f"{stem}_opt@2x.webp"
        img_2x.save(webp_2x_path, 'WEBP', quality=quality, method=6)
        results['files'].append(str(webp_2x_path))
        print(f"  WebP @2x: {webp_2x_path.stat().st_size / 1024:.1f} KB")

    # Salvar JPG como fallback
    jpg_path = output_dir / f"{stem}_opt.jpg"
    img_1x.save(jpg_path, 'JPEG', quality=quality, optimize=True)
    jpg_size = jpg_path.stat().st_size
    results['files'].append(str(jpg_path))
    print(f"  JPG fallback: {jpg_size / 1024:.1f} KB")

    # Calcular economia
    economia = (1 - webp_size / original_size) * 100
    results['webp_size'] = webp_size
    results['economia'] = economia

    print(f"  Economia: {economia:.1f}%")

    return results


def main():
    parser = argparse.ArgumentParser(
        description='Otimiza imagens para web (WebP + JPG fallback)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python optimize_image.py foto.jpg
  python optimize_image.py foto.jpg -w 800 -q 90
  python optimize_image.py images/*.jpg -o images/optimized
        """
    )
    parser.add_argument('images', nargs='+', help='Imagem(ns) para otimizar')
    parser.add_argument('-w', '--width', type=int, help='Largura máxima (px)')
    parser.add_argument('-q', '--quality', type=int, default=85, help='Qualidade (1-100, padrão: 85)')
    parser.add_argument('-o', '--output', help='Diretório de saída')
    parser.add_argument('--no-2x', action='store_true', help='Não criar versão @2x')

    args = parser.parse_args()

    print("\n" + "="*50)
    print("RIP PET - OTIMIZADOR DE IMAGENS")
    print("="*50)

    total_original = 0
    total_optimized = 0
    count = 0

    for image_path in args.images:
        result = optimize_image(
            image_path,
            output_dir=args.output,
            target_width=args.width,
            quality=args.quality,
            create_2x=not args.no_2x
        )

        if result:
            total_original += result['original_size']
            total_optimized += result['webp_size']
            count += 1

    if count > 0:
        print("\n" + "="*50)
        print("RESUMO")
        print("="*50)
        print(f"  Imagens processadas: {count}")
        print(f"  Tamanho original: {total_original / 1024:.1f} KB")
        print(f"  Tamanho otimizado: {total_optimized / 1024:.1f} KB")
        print(f"  Economia total: {(1 - total_optimized / total_original) * 100:.1f}%")
        print("\nDica: Use <picture> no HTML para WebP com fallback JPG")
    else:
        print("\nNenhuma imagem processada.")


if __name__ == "__main__":
    main()
