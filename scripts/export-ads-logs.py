#!/usr/bin/env python3
"""
Exportador de Logs do Google Ads Tracker - RIP PET
Exporta os logs de cliques do Vercel para CSV

Uso:
  python scripts/export-ads-logs.py

Requisitos:
  pip install requests

Configuração:
  1. Gere um token em: https://vercel.com/account/tokens
  2. Defina a variável de ambiente: VERCEL_TOKEN=seu_token
  3. Ou passe como argumento: python export-ads-logs.py --token=seu_token
"""

import json
import csv
import os
import sys
import argparse
from datetime import datetime, timedelta
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

# Configurações
VERCEL_API = "https://api.vercel.com"
PROJECT_NAME = "rip-pet-website"  # Nome do projeto na Vercel
OUTPUT_FILE = "ads-clicks-log.csv"


def get_logs(token, project_id=None, hours=24):
    """Busca logs da Vercel API"""

    # Primeiro, buscar o project ID se não fornecido
    if not project_id:
        print("🔍 Buscando projeto...")
        req = Request(f"{VERCEL_API}/v9/projects")
        req.add_header("Authorization", f"Bearer {token}")

        try:
            with urlopen(req) as response:
                data = json.loads(response.read().decode())
                projects = data.get("projects", [])

                # Procurar pelo projeto rip-pet
                for p in projects:
                    if "rip" in p.get("name", "").lower() or "pet" in p.get("name", "").lower():
                        project_id = p.get("id")
                        print(f"✅ Projeto encontrado: {p.get('name')} ({project_id})")
                        break

                if not project_id and projects:
                    # Usar o primeiro projeto
                    project_id = projects[0].get("id")
                    print(f"⚠️  Usando primeiro projeto: {projects[0].get('name')}")

        except HTTPError as e:
            print(f"❌ Erro ao buscar projetos: {e.code} - {e.reason}")
            return []

    if not project_id:
        print("❌ Nenhum projeto encontrado")
        return []

    # Buscar deployments recentes
    print("🔍 Buscando deployments...")
    req = Request(f"{VERCEL_API}/v6/deployments?projectId={project_id}&limit=5")
    req.add_header("Authorization", f"Bearer {token}")

    deployments = []
    try:
        with urlopen(req) as response:
            data = json.loads(response.read().decode())
            deployments = data.get("deployments", [])
            print(f"✅ {len(deployments)} deployments encontrados")
    except HTTPError as e:
        print(f"❌ Erro ao buscar deployments: {e.code}")
        return []

    # Buscar logs de cada deployment
    all_logs = []
    since = int((datetime.now() - timedelta(hours=hours)).timestamp() * 1000)

    for dep in deployments[:3]:  # Últimos 3 deployments
        dep_id = dep.get("uid")
        print(f"📋 Buscando logs do deployment {dep_id[:8]}...")

        req = Request(f"{VERCEL_API}/v2/deployments/{dep_id}/events?since={since}&limit=1000")
        req.add_header("Authorization", f"Bearer {token}")

        try:
            with urlopen(req) as response:
                events = json.loads(response.read().decode())

                for event in events:
                    # Filtrar apenas logs da função de tracking
                    text = event.get("text", "")
                    if "CLICK TRACKED" in text or "track.js" in text:
                        all_logs.append(event)

        except HTTPError as e:
            print(f"⚠️  Erro no deployment {dep_id[:8]}: {e.code}")
            continue

    return all_logs


def parse_log_entry(log_text):
    """Extrai dados de uma linha de log"""
    try:
        # O log deve ter formato JSON após "CLICK TRACKED:"
        if "CLICK TRACKED:" in log_text:
            json_str = log_text.split("CLICK TRACKED:")[1].strip()
            return json.loads(json_str)
    except:
        pass
    return None


def export_to_csv(logs, output_file):
    """Exporta logs para CSV"""

    # Parsear os logs
    parsed = []
    for log in logs:
        text = log.get("text", "")
        data = parse_log_entry(text)
        if data:
            parsed.append(data)

    if not parsed:
        print("⚠️  Nenhum log de clique encontrado")
        return 0

    # Definir colunas
    fieldnames = ["timestamp", "ip", "page", "utmSource", "utmMedium", "utmCampaign", "gclid", "userAgent", "referer"]

    # Escrever CSV
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(parsed)

    return len(parsed)


def analyze_ips(logs):
    """Analisa IPs suspeitos (muitos cliques)"""

    ip_counts = {}
    for log in logs:
        text = log.get("text", "")
        data = parse_log_entry(text)
        if data and data.get("ip"):
            ip = data["ip"]
            ip_counts[ip] = ip_counts.get(ip, 0) + 1

    if not ip_counts:
        return

    print("\n📊 Análise de IPs:")
    print("-" * 50)

    # Ordenar por quantidade de cliques
    sorted_ips = sorted(ip_counts.items(), key=lambda x: x[1], reverse=True)

    suspicious = []
    for ip, count in sorted_ips[:20]:  # Top 20
        status = "🚨 SUSPEITO" if count >= 5 else ""
        print(f"  {ip:20} → {count:3} cliques {status}")
        if count >= 5:
            suspicious.append(ip)

    if suspicious:
        print("\n⚠️  IPs para excluir no Google Ads:")
        print("-" * 50)
        for ip in suspicious:
            print(f"  {ip}")

        # Salvar lista de IPs suspeitos
        with open("ips-suspeitos.txt", "w") as f:
            f.write("\n".join(suspicious))
        print(f"\n💾 Lista salva em: ips-suspeitos.txt")


def main():
    parser = argparse.ArgumentParser(description="Exportar logs de cliques do Google Ads")
    parser.add_argument("--token", help="Token da Vercel API")
    parser.add_argument("--hours", type=int, default=24, help="Horas de logs (padrão: 24)")
    parser.add_argument("--output", default=OUTPUT_FILE, help="Arquivo de saída")
    args = parser.parse_args()

    # Obter token
    token = args.token or os.environ.get("VERCEL_TOKEN")

    if not token:
        print("❌ Token da Vercel não configurado!")
        print("\nOpções:")
        print("  1. Defina a variável: set VERCEL_TOKEN=seu_token")
        print("  2. Ou passe como argumento: python export-ads-logs.py --token=seu_token")
        print("\n📝 Gere seu token em: https://vercel.com/account/tokens")
        sys.exit(1)

    print("=" * 50)
    print("🎯 RIP PET - Exportador de Logs Google Ads")
    print("=" * 50)
    print(f"⏰ Buscando logs das últimas {args.hours} horas...\n")

    # Buscar logs
    logs = get_logs(token, hours=args.hours)

    if not logs:
        print("\n📭 Nenhum log encontrado no período")
        print("💡 Dica: Os logs aparecem após cliques em anúncios do Google Ads")
        return

    print(f"\n📥 {len(logs)} registros encontrados")

    # Exportar para CSV
    count = export_to_csv(logs, args.output)
    if count > 0:
        print(f"✅ {count} cliques exportados para: {args.output}")

    # Analisar IPs
    analyze_ips(logs)

    print("\n" + "=" * 50)
    print("✨ Concluído!")


if __name__ == "__main__":
    main()
