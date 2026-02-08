#!/usr/bin/env python3
"""
Script para corrigir bugs em TODAS as LPs (SP, Campinas, Santos).
- Remove popups mortos (WhatsApp e Phone)
- Corrige numeros errados
- Corrige Schema areaServed do SP
- Corrige foundingDate
"""
import re
import os
import sys

# Force UTF-8 output on Windows
sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FILES = {
    'sp': os.path.join(BASE_DIR, "sao-paulo", "index.html"),
    'campinas': os.path.join(BASE_DIR, "campinas", "index.html"),
    'santos': os.path.join(BASE_DIR, "santos", "index.html"),
}

def read_file(path):
    with open(path, "r", encoding="utf-8-sig") as f:
        return f.read()

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def remove_popups(content, label):
    """Remove popup HTML blocks and their JS functions from an LP."""
    changes = []

    # 1. Remove WhatsApp popup HTML div
    pattern_wa = r'\n    <!-- WhatsApp Popup -->\n    <div class="whatsapp-popup-overlay".*?</div>\n    </div>\n    </div>'
    # More robust: find from whatsapp-popup-overlay to the closing </div> sequence
    wa_start = content.find('<div class="whatsapp-popup-overlay"')
    if wa_start == -1:
        wa_start = content.find('class="whatsapp-popup-overlay"')
        if wa_start != -1:
            # go back to find the opening tag
            wa_start = content.rfind('<div', 0, wa_start)

    if wa_start != -1:
        # Find the comment before it (if any)
        comment_start = content.rfind('<!--', max(0, wa_start - 100), wa_start)
        if comment_start != -1 and 'WhatsApp' in content[comment_start:wa_start]:
            wa_start = comment_start

        # Find matching closing: the popup has nested divs, need to count
        # Structure: <div overlay> <div popup> ... <div grid> ... </div> </div> </div>
        # Count 3 closing </div> after the grid content
        pos = content.find('</div>\n    </div>\n    </div>', wa_start)
        if pos == -1:
            pos = content.find('</div>\n        </div>\n    </div>', wa_start)
        if pos != -1:
            wa_end = content.find('\n', pos + len('</div>\n    </div>\n    </div>'))
            if wa_end == -1:
                wa_end = pos + 50
            # Also include trailing newlines
            while wa_end < len(content) and content[wa_end] in '\n\r':
                wa_end += 1
            changes.append(f"  Removed WhatsApp popup HTML ({wa_end - wa_start} chars)")
            content = content[:wa_start] + content[wa_end:]

    # 2. Remove Phone popup HTML div
    ph_start = content.find('<div class="phone-popup-overlay"')
    if ph_start == -1:
        ph_start = content.find('class="phone-popup-overlay"')
        if ph_start != -1:
            ph_start = content.rfind('<div', 0, ph_start)

    if ph_start != -1:
        comment_start = content.rfind('<!--', max(0, ph_start - 100), ph_start)
        if comment_start != -1 and 'Phone' in content[comment_start:ph_start]:
            ph_start = comment_start

        pos = content.find('</div>\n    </div>\n    </div>', ph_start)
        if pos == -1:
            pos = content.find('</div>\n        </div>\n    </div>', ph_start)
        if pos != -1:
            ph_end = content.find('\n', pos + len('</div>\n    </div>\n    </div>'))
            if ph_end == -1:
                ph_end = pos + 50
            while ph_end < len(content) and content[ph_end] in '\n\r':
                ph_end += 1
            changes.append(f"  Removed Phone popup HTML ({ph_end - ph_start} chars)")
            content = content[:ph_start] + content[ph_end:]

    # 3. Remove JS functions for popups
    for func_name in ['openWhatsAppPopup', 'closeWhatsAppPopup', 'openPhonePopup', 'closePhonePopup']:
        # Find function declaration
        pattern = f'        function {func_name}'
        func_start = content.find(pattern)
        if func_start == -1:
            # Try with comment before
            for comment in ['// WhatsApp Popup Functions', '// Phone Popup Functions']:
                cs = content.find(comment)
                if cs != -1:
                    func_start = cs
                    break
        if func_start != -1:
            # Find the closing brace
            # Count braces to find the end
            brace_count = 0
            i = content.find('{', func_start)
            if i != -1:
                for j in range(i, len(content)):
                    if content[j] == '{':
                        brace_count += 1
                    elif content[j] == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            func_end = j + 1
                            # Skip trailing newlines
                            while func_end < len(content) and content[func_end] in '\n\r ':
                                func_end += 1
                            break

    # Simpler approach: remove the entire block between markers
    # Remove "// WhatsApp Popup Functions" through end of closePhonePopup
    wa_funcs_start = content.find('        // WhatsApp Popup Functions')
    if wa_funcs_start != -1:
        # Find the end - it's the blank line before "// Historia Slider"
        historia_marker = content.find('        // Historia Slider', wa_funcs_start)
        if historia_marker == -1:
            historia_marker = content.find('        // Map Popup', wa_funcs_start)
        if historia_marker == -1:
            # Find after closePhonePopup function
            cp_end = content.find('function closePhonePopup', wa_funcs_start)
            if cp_end != -1:
                brace_count = 0
                for i in range(content.find('{', cp_end), len(content)):
                    if content[i] == '{': brace_count += 1
                    elif content[i] == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            historia_marker = i + 1
                            while historia_marker < len(content) and content[historia_marker] in '\n\r ':
                                historia_marker += 1
                            break

        if historia_marker != -1:
            changes.append(f"  Removed popup JS functions ({historia_marker - wa_funcs_start} chars)")
            content = content[:wa_funcs_start] + content[historia_marker:]

    # 4. Remove popstate handler references to popups
    # Remove the WhatsApp popstate block
    wa_popstate = content.find('            // Fecha popup WhatsApp')
    if wa_popstate != -1:
        wa_popstate_end = content.find('            }', wa_popstate + 10)
        if wa_popstate_end != -1:
            wa_popstate_end = content.find('\n', wa_popstate_end) + 1
            content = content[:wa_popstate] + content[wa_popstate_end:]

    # Remove the Phone popstate block
    ph_popstate = content.find('            // Fecha popup Phone')
    if ph_popstate != -1:
        ph_popstate_end = content.find('            }', ph_popstate + 10)
        if ph_popstate_end != -1:
            ph_popstate_end = content.find('\n', ph_popstate_end) + 1
            content = content[:ph_popstate] + content[ph_popstate_end:]

    if changes:
        print(f"  [{label}] Popup removal:")
        for c in changes:
            print(f"    {c}")
    else:
        print(f"  [{label}] No popups found to remove")

    return content


def fix_sp(content):
    """Fix bugs specific to the SP LP."""
    print("\n=== FIXING SAO PAULO LP ===")
    changes = 0

    # 1. Fix mobile thumb CTA: Pinda landline -> SP number
    old = 'tel:+551236441766'
    new = 'tel:+5511991603041'
    if old in content:
        content = content.replace(old, new)
        print(f"  Fixed mobile thumb CTA: {old} -> {new}")
        changes += 1

    # 2. Fix floating phone button title
    old = 'title="Ligar Agora (13) 99806-8262" aria-label="Ligar para R.I.P. Pet São Paulo"'
    new = 'title="Ligar Agora (11) 99160-3041" aria-label="Ligar para R.I.P. Pet São Paulo"'
    if old in content:
        content = content.replace(old, new)
        print(f"  Fixed floating phone title")
        changes += 1

    # 3. Fix floating WhatsApp button title
    old = 'title="WhatsApp 24h (13) 99806-8262" aria-label="Falar no WhatsApp São Paulo"'
    new = 'title="WhatsApp 24h (11) 99160-3041" aria-label="Falar no WhatsApp São Paulo"'
    if old in content:
        content = content.replace(old, new)
        print(f"  Fixed floating WhatsApp title")
        changes += 1

    # 4. Fix Schema areaServed (has Santos cities instead of Grande SP)
    old_area = """      "areaServed": [
        {"@type": "City", "name": "S\u00e3o Paulo"},
        {"@type": "City", "name": "Guaruj\u00e1"},
        {"@type": "City", "name": "S\u00e3o Vicente"},
        {"@type": "City", "name": "Santo Andr\u00e9"},
        {"@type": "City", "name": "Cubat\u00e3o"},
        {"@type": "City", "name": "S\u00e3o Caetano do Sul"},
        {"@type": "City", "name": "Mongagu\u00e1"},
        {"@type": "City", "name": "Itanha\u00e9m"},
        {"@type": "City", "name": "Peru\u00edbe"}
      ]"""
    new_area = """      "areaServed": [
        {"@type": "City", "name": "S\u00e3o Paulo"},
        {"@type": "City", "name": "Guarulhos"},
        {"@type": "City", "name": "Osasco"},
        {"@type": "City", "name": "Santo Andr\u00e9"},
        {"@type": "City", "name": "S\u00e3o Bernardo do Campo"},
        {"@type": "City", "name": "S\u00e3o Caetano do Sul"},
        {"@type": "City", "name": "Diadema"},
        {"@type": "City", "name": "Mau\u00e1"},
        {"@type": "City", "name": "Tabo\u00e3o da Serra"}
      ]"""
    if old_area in content:
        content = content.replace(old_area, new_area)
        print("  Fixed Schema areaServed (Santos cities -> Grande SP cities)")
        changes += 1
    else:
        # Try with corrupted encoding
        old_area_corrupt = old_area.replace("Santo Andr\u00e9", "Santo Andr\ufffd")
        if old_area_corrupt in content:
            content = content.replace(old_area_corrupt, new_area)
            print("  Fixed Schema areaServed (corrupted encoding + wrong cities)")
            changes += 1
        else:
            print("  WARNING: Could not find areaServed to fix (may need manual fix)")

    # 5. Fix foundingDate: 2012 -> 2018 (SP unit opened in 2018)
    old = '"foundingDate": "2012"'
    new = '"foundingDate": "2018"'
    if old in content:
        content = content.replace(old, new)
        print(f"  Fixed foundingDate: 2012 -> 2018")
        changes += 1

    print(f"  Total SP fixes: {changes}")
    return content


def fix_santos(content):
    """Fix bugs specific to the Santos LP."""
    print("\n=== FIXING SANTOS LP ===")
    changes = 0

    # 1. Fix mobile thumb CTA: Pinda landline -> Santos number
    old = 'tel:+551236441766'
    new = 'tel:+5513998068262'
    if old in content:
        content = content.replace(old, new)
        print(f"  Fixed mobile thumb CTA: {old} -> {new}")
        changes += 1

    # 2. Fix foundingDate: 2012 -> 2023 (Santos unit opened in 2023)
    old = '"foundingDate": "2012"'
    new = '"foundingDate": "2023"'
    if old in content:
        content = content.replace(old, new)
        print(f"  Fixed foundingDate: 2012 -> 2023")
        changes += 1

    print(f"  Total Santos fixes: {changes}")
    return content


def fix_campinas(content):
    """Fix bugs specific to the Campinas LP (most already fixed during creation)."""
    print("\n=== FIXING CAMPINAS LP ===")
    changes = 0
    # Campinas was created from the fixed SP, so most bugs are already fixed
    # Just verify mobile thumb CTA
    if 'tel:+551236441766' in content:
        content = content.replace('tel:+551236441766', 'tel:+5519999161977')
        print("  Fixed mobile thumb CTA")
        changes += 1

    print(f"  Total Campinas fixes: {changes}")
    return content


def main():
    for label, path in FILES.items():
        if not os.path.exists(path):
            print(f"\n[{label}] File not found: {path}")
            continue

        print(f"\n{'='*60}")
        print(f"Processing: {label} ({os.path.basename(os.path.dirname(path))})")
        print(f"{'='*60}")

        content = read_file(path)
        original_len = len(content)

        # Remove popups from all LPs
        content = remove_popups(content, label)

        # Apply LP-specific fixes
        if label == 'sp':
            content = fix_sp(content)
        elif label == 'santos':
            content = fix_santos(content)
        elif label == 'campinas':
            content = fix_campinas(content)

        write_file(path, content)
        new_len = len(content)
        print(f"\n  Size: {original_len:,} -> {new_len:,} ({new_len - original_len:+,} bytes)")

    # Final verification
    print(f"\n{'='*60}")
    print("FINAL VERIFICATION")
    print(f"{'='*60}")

    for label, path in FILES.items():
        if not os.path.exists(path):
            continue
        content = read_file(path)
        print(f"\n  [{label}]")

        # Check for Pinda landline
        count = content.count('551236441766')
        print(f"    551236441766 (Pinda landline): {count} {'OK' if count == 0 else 'FOUND!'}")

        # Check for popup functions
        count = content.count('openWhatsAppPopup')
        print(f"    openWhatsAppPopup: {count} {'OK' if count == 0 else 'FOUND!'}")

        count = content.count('openPhonePopup')
        print(f"    openPhonePopup: {count} {'OK' if count == 0 else 'FOUND!'}")

        count = content.count('whatsappPopupOverlay')
        print(f"    whatsappPopupOverlay: {count} {'OK' if count == 0 else 'FOUND!'}")

        count = content.count('phonePopupOverlay')
        print(f"    phonePopupOverlay: {count} {'OK' if count == 0 else 'FOUND!'}")


if __name__ == "__main__":
    main()
