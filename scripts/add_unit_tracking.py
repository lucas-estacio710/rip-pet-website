#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script para adicionar tracking de cliques por unidade no GA4"""

# Ler o arquivo
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Adicionar onclick nos links de TELEFONE no popup
phone_units = [
    ('5512997996543', 'Matriz - Vale do Paraíba'),
    ('5511991603041', 'São Paulo'),
    ('5513998068262', 'Santos'),
    ('5519999161977', 'Campinas'),
    ('5524998379825', 'Resende'),
    ('553599042223', 'Pouso Alegre')
]

for phone, unit_name in phone_units:
    # Encontrar link de telefone e adicionar onclick
    old_phone = f'<a href="tel:+{phone}" class="region-compose"'
    new_phone = f'<a href="tel:+{phone}" onclick="trackPhoneClick(\'{unit_name}\')" class="region-compose"'
    content = content.replace(old_phone, new_phone)

# 2. Adicionar onclick nos links de WHATSAPP no popup
whatsapp_units = [
    ('5512997996543', 'Matriz - Vale do Paraíba'),
    ('5511991603041', 'São Paulo'),
    ('5513998068262', 'Santos'),
    ('5519999161977', 'Campinas'),
    ('5524998379825', 'Resende'),
    ('553599042223', 'Pouso Alegre')
]

for phone, unit_name in whatsapp_units:
    # Encontrar links de WhatsApp e adicionar onclick
    old_whatsapp = f'href="https://wa.me/{phone}'
    # Precisamos adicionar onclick mantendo o id santos-whatsapp-link se for Santos
    if phone == '5513998068262':
        # Santos tem ID especial
        old_santos = f'href="https://wa.me/{phone}?text=Olá, estava no site da R.I.P. Pet e preciso de mais informações." id="santos-whatsapp-link"'
        new_santos = f'href="https://wa.me/{phone}?text=Olá, estava no site da R.I.P. Pet e preciso de mais informações." onclick="trackWhatsAppClick(\'{unit_name}\')" id="santos-whatsapp-link"'
        content = content.replace(old_santos, new_santos)
    else:
        # Outras unidades
        old_wa = f'href="https://wa.me/{phone}?text=Olá, estava no site da R.I.P. Pet e preciso de mais informações." class="region-compose"'
        new_wa = f'href="https://wa.me/{phone}?text=Olá, estava no site da R.I.P. Pet e preciso de mais informações." onclick="trackWhatsAppClick(\'{unit_name}\')" class="region-compose"'
        content = content.replace(old_wa, new_wa)

# 3. Adicionar funções de tracking antes do fechamento do script
tracking_functions = """
        // ========== TRACKING GA4 - CLIQUES POR UNIDADE ==========
        function trackPhoneClick(unidade) {
            if (typeof gtag !== 'undefined') {
                gtag('event', 'phone_click', {
                    'event_category': 'Contact',
                    'event_label': unidade,
                    'unidade': unidade,
                    'contact_type': 'phone'
                });
                console.log('GA4 Event: phone_click -', unidade);
            }
        }

        function trackWhatsAppClick(unidade) {
            if (typeof gtag !== 'undefined') {
                gtag('event', 'whatsapp_click', {
                    'event_category': 'Contact',
                    'event_label': unidade,
                    'unidade': unidade,
                    'contact_type': 'whatsapp'
                });
                console.log('GA4 Event: whatsapp_click -', unidade);
            }
        }
"""

# Adicionar as funções antes do último </script>
last_script = content.rfind('</script>')
if last_script != -1:
    content = content[:last_script] + tracking_functions + '\n    ' + content[last_script:]

# Salvar arquivo
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Tracking de unidades adicionado com sucesso!")
print("")
print("Eventos GA4 configurados:")
print("- phone_click (com parametro 'unidade')")
print("- whatsapp_click (com parametro 'unidade')")
print("")
print("Unidades rastreadas:")
for phone, unit in phone_units:
    print(f"  - {unit}")
