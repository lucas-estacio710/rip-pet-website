#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script para corrigir ícones de telefone - trocar gradiente azul por branco sólido"""

# Ler o arquivo
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Substituir todos os ícones de telefone com gradiente azul por ícones brancos
content = content.replace(
    'style="font-size: 1.2rem; background: linear-gradient(135deg, #3b82f6, #1e40af); background-clip: text; -webkit-background-clip: text; color: transparent; transition: all 0.3s ease;"',
    'style="font-size: 1.2rem; color: white; transition: all 0.3s ease;"'
)

# Salvar arquivo
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Icones de telefone corrigidos - agora estao brancos!")
