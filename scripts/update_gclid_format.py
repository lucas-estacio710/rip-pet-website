#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script para adicionar quebra de linha antes do protocolo e voltar GCLID completo"""

# Ler o arquivo
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remover o código de encurtamento e adicionar quebra de linha
old_code = """                    // Usar apenas primeiros 12 caracteres do GCLID (mais discreto)
                    const shortGclid = gclid.substring(0, 12);
                    const message = encodeURIComponent(`Olá, estava no site da R.I.P. Pet e preciso de mais informações. (Protocolo: ${shortGclid})`);"""

new_code = """                    const message = encodeURIComponent(`Olá, estava no site da R.I.P. Pet e preciso de mais informações.

(Protocolo: ${gclid})`);"""

content = content.replace(old_code, new_code)

# Salvar arquivo
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Formato atualizado com sucesso!")
print("Agora tem quebra de linha antes do protocolo")
print("")
print("Formato da mensagem:")
print("Ola, estava no site da R.I.P. Pet e preciso de mais informacoes.")
print("")
print("(Protocolo: Cj0KCQiAiKzIBhCOARIsAKp...)")
