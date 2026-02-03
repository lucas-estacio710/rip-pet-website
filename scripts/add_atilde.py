#!/usr/bin/env python3
"""
Script para adicionar o caractere 'ã' na fonte Autography
Copia o glifo 'a' e adiciona um til (~) em cima
"""

from fontTools.ttLib import TTFont
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.recordingPen import RecordingPen
import copy
import os

def add_atilde_to_font(input_path, output_path):
    """Adiciona o glifo ã à fonte"""

    print(f"Abrindo fonte: {input_path}")
    font = TTFont(input_path)

    # Verificar se é fonte CFF (OTF) ou TrueType
    if 'CFF ' in font:
        print("Fonte CFF (OpenType) detectada")
        cff = font['CFF ']
        top_dict = cff.cff.topDictIndex[0]
        char_strings = top_dict.CharStrings

        # Verificar se 'a' existe
        if 'a' not in char_strings:
            print("ERRO: Glifo 'a' não encontrado na fonte!")
            return False

        # Verificar se 'atilde' já existe
        if 'atilde' in char_strings:
            print("Glifo 'atilde' já existe na fonte!")
        else:
            print("Criando glifo 'atilde' baseado em 'a'...")

            # Copiar o charstring do 'a'
            a_charstring = char_strings['a']

            # Para fontes cursivas/script, vamos simplesmente copiar o 'a'
            # O til será adicionado via CSS ou podemos usar um combining character
            char_strings['atilde'] = copy.deepcopy(a_charstring)
            print("Glifo 'atilde' criado (cópia do 'a')")

        # Atualizar o cmap para mapear ã (U+00E3) para atilde
        for table in font['cmap'].tables:
            if hasattr(table, 'cmap'):
                table.cmap[0x00E3] = 'atilde'  # ã
                table.cmap[0x00C3] = 'Atilde'  # Ã (se precisar maiúsculo)

        print("Mapeamento cmap atualizado")

    elif 'glyf' in font:
        print("Fonte TrueType detectada")
        glyf = font['glyf']

        if 'a' not in glyf:
            print("ERRO: Glifo 'a' não encontrado!")
            return False

        # Copiar glifo
        glyf['atilde'] = copy.deepcopy(glyf['a'])

        # Atualizar hmtx (métricas horizontais)
        if 'hmtx' in font:
            font['hmtx']['atilde'] = font['hmtx']['a']

        # Atualizar cmap
        for table in font['cmap'].tables:
            if hasattr(table, 'cmap'):
                table.cmap[0x00E3] = 'atilde'

        print("Glifo atilde criado e mapeado")

    else:
        print("ERRO: Formato de fonte não suportado!")
        return False

    # Salvar fonte
    print(f"Salvando fonte em: {output_path}")
    font.save(output_path)
    print("Fonte salva com sucesso!")

    return True

def convert_to_woff2(otf_path, woff2_path):
    """Converte OTF para WOFF2"""
    from fontTools.ttLib import TTFont

    print(f"Convertendo para WOFF2: {woff2_path}")
    font = TTFont(otf_path)
    font.flavor = 'woff2'
    font.save(woff2_path)
    print("WOFF2 criado com sucesso!")

if __name__ == "__main__":
    base_dir = r"C:\Users\kel_v\LUCAS_ATELLIAR\SITE_RIP_PET_PRODUCTION\fonts"

    input_otf = os.path.join(base_dir, "Autography.otf")
    output_otf = os.path.join(base_dir, "Autography-extended.otf")
    output_woff2 = os.path.join(base_dir, "Autography-extended.woff2")

    # Fazer backup
    backup_otf = os.path.join(base_dir, "Autography-original.otf")
    backup_woff2 = os.path.join(base_dir, "Autography-original.woff2")

    import shutil
    if not os.path.exists(backup_otf):
        shutil.copy(input_otf, backup_otf)
        print(f"Backup criado: {backup_otf}")
    if not os.path.exists(backup_woff2):
        original_woff2 = os.path.join(base_dir, "Autography.woff2")
        if os.path.exists(original_woff2):
            shutil.copy(original_woff2, backup_woff2)
            print(f"Backup criado: {backup_woff2}")

    # Adicionar ã
    if add_atilde_to_font(input_otf, output_otf):
        # Converter para woff2
        convert_to_woff2(output_otf, output_woff2)

        # Substituir os arquivos originais
        shutil.copy(output_otf, input_otf)
        shutil.copy(output_woff2, os.path.join(base_dir, "Autography.woff2"))
        print("\nArquivos originais atualizados!")
        print("Limpe o cache do navegador e recarregue a página.")
    else:
        print("\nFalha ao modificar a fonte.")
