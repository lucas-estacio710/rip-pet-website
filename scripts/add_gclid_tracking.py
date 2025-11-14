#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script para adicionar captura de GCLID e modificar link do WhatsApp de Santos"""

# Ler o arquivo
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Adicionar código de captura de GCLID logo após <script>
gclid_capture_code = """    <script>
        // ========== CAPTURA DE GCLID PARA GOOGLE ADS ==========
        // Captura GCLID da URL e salva em cookie por 90 dias
        function captureGCLID() {
            const urlParams = new URLSearchParams(window.location.search);
            const gclid = urlParams.get('gclid');

            if (gclid) {
                // Salva GCLID em cookie por 90 dias
                const expiryDate = new Date();
                expiryDate.setDate(expiryDate.getDate() + 90);
                document.cookie = `gclid=${gclid}; expires=${expiryDate.toUTCString()}; path=/`;
                console.log('GCLID capturado:', gclid);
            }
        }

        // Função para recuperar GCLID do cookie
        function getGCLID() {
            const name = 'gclid=';
            const decodedCookie = decodeURIComponent(document.cookie);
            const cookieArray = decodedCookie.split(';');

            for(let i = 0; i < cookieArray.length; i++) {
                let cookie = cookieArray[i].trim();
                if (cookie.indexOf(name) === 0) {
                    return cookie.substring(name.length, cookie.length);
                }
            }
            return null;
        }

        // Executa captura imediatamente
        captureGCLID();

        // Loading Screen"""

content = content.replace('    <script>\n        // Loading Screen', gclid_capture_code)

# 2. Modificar o link do WhatsApp de Santos no POPUP para incluir GCLID
# Encontrar o link de Santos no popup de WhatsApp
old_santos_whatsapp = 'href="https://wa.me/5513998068262?text=Olá, estava no site da R.I.P. Pet e preciso de mais informações."'
new_santos_whatsapp = 'href="https://wa.me/5513998068262?text=Olá, estava no site da R.I.P. Pet e preciso de mais informações." id="santos-whatsapp-link"'

content = content.replace(old_santos_whatsapp, new_santos_whatsapp)

# 3. Adicionar script para modificar link dinamicamente com GCLID
# Procurar onde adicionar (antes do fechamento do script principal)
script_addition = """
        // ========== ADICIONAR GCLID NO WHATSAPP DE SANTOS ==========
        function updateSantosWhatsAppLink() {
            const santosLink = document.getElementById('santos-whatsapp-link');
            if (santosLink) {
                const gclid = getGCLID();
                if (gclid) {
                    const baseUrl = 'https://wa.me/5513998068262';
                    const message = encodeURIComponent(`Olá, estava no site da R.I.P. Pet e preciso de mais informações. (Protocolo: ${gclid})`);
                    santosLink.href = `${baseUrl}?text=${message}`;
                    console.log('Link de Santos atualizado com GCLID:', gclid);
                }
            }
        }

        // Atualizar link quando página carregar
        window.addEventListener('load', updateSantosWhatsAppLink);

        // Atualizar link quando popup de WhatsApp abrir
        function openWhatsAppPopup() {
            updateSantosWhatsAppLink();
            const popup = document.getElementById('whatsappPopupOverlay');
            if (popup) {
                popup.style.display = 'flex';
                setTimeout(() => popup.classList.add('active'), 10);
            }
            return false;
        }
"""

# Adicionar antes do fechamento do script (antes de </script>)
# Procurar uma boa localização - antes do último </script> no arquivo
last_script_close = content.rfind('</script>')
if last_script_close != -1:
    # Inserir antes do último </script>
    content = content[:last_script_close] + script_addition + '\n    ' + content[last_script_close:]

# Salvar arquivo
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Implementacao concluida com sucesso!")
print("1. Codigo de captura de GCLID adicionado")
print("2. Link do WhatsApp de Santos modificado para incluir protocolo")
print("3. Funcao de atualizacao dinamica adicionada")
