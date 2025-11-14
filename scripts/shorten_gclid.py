#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script para encurtar GCLID no WhatsApp"""

# Ler o arquivo
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Modificar função para usar apenas primeiros 12 caracteres
old_code = """                    const message = encodeURIComponent(`Olá, estava no site da R.I.P. Pet e preciso de mais informações. (Protocolo: ${gclid})`);"""

new_code = """                    // Usar apenas primeiros 12 caracteres do GCLID (mais discreto)
                    const shortGclid = gclid.substring(0, 12);
                    const message = encodeURIComponent(`Olá, estava no site da R.I.P. Pet e preciso de mais informações. (Protocolo: ${shortGclid})`);"""

content = content.replace(old_code, new_code)

# Salvar arquivo
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("GCLID encurtado com sucesso!")
print("Agora mostra apenas os primeiros 12 caracteres")
print("Exemplo: Cj0KCQiAiKzI ao inves de Cj0KCQiAiKzIBhCOARIsAKpKLANkh2F0Dw...")
