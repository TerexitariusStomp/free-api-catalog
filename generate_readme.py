#!/usr/bin/env python3
"""Generate clean README with service pattern classification."""
import json, os
from collections import Counter

with open('/home/terexitarius/free-api-catalog/apis.json') as f:
    catalog = json.load(f)

apis = catalog['apis']
counts = Counter(api.get('service_pattern', 'Reference') for api in apis)
no_auth = [a for a in apis if a.get('auth') == 'No']
needs_auth = [a for a in apis if a.get('auth') not in ('No', '')]

# Regenerate README
lines = [
    "# Free API Catalog",
    "",
    f"A curated collection of **{len(apis)} free and open APIs** across **52 topic categories**, classified into **11 functional patterns** based on what they do.",
    "",
    "## Quick Stats",
    "",
    f"- **Total APIs:** {len(apis)}",
    f"- **No auth required:** {len(no_auth)} ({int(len(no_auth)/len(apis)*100)}%)",
    f"- **Free key / registration:** {len(needs_auth)} ({int(len(needs_auth)/len(apis)*100)}%)",
    f"- **Topic categories:** 52",
    f"- **Functional patterns:** 11",
    "",
    "---",
    "",
    "## Functional Patterns",
    "",
    "Each API is classified by **what it DOES** (functional pattern) AND **its domain** (topic category).",
    "",
    "| Pattern | Count | Description |",
    "|---------|-------|-------------|",
    f"| 📚 [Reference Data](#reference-data) | {counts.get('Reference', 0)} | Static data — books, movies, recipes, quotes, facts, species, dictionaries |",
    f"| 🔧 [Service](#service) | {counts.get('Service', 0)} | Generates or transforms — QR codes, URL shortening, conversion, color palettes |",
    f"| 📡 [Dynamic Data](#dynamic-data) | {counts.get('Dynamic Data', 0)} | Real-time/updated — weather, markets, news, sports, air quality |",
    f"| 🗺️ [Geospatial](#geospatial) | {counts.get('Geospatial', 0)} | Location-based — maps, geocoding, routing, public transit |",
    f"| 💬 [Communication](#communication) | {counts.get('Communication', 0)} | Messaging — email, social, notifications, webhooks, publishing |",
    f"| 🏛️ [Government](#government) | {counts.get('Government', 0)} | Official data — census, legislation, patents, compliance |",
    f"| 📊 [Analytics](#analytics) | {counts.get('Analytics', 0)} | Monitoring — metrics, security scanning, threat detection |",
    f"| 🤖 [AI/ML](#aiml) | {counts.get('AI/ML', 0)} | Intelligence — NLP, text analysis, classification, translation |",
    f"| 🖥️ [Platform](#platform) | {counts.get('Platform', 0)} | Integration — CMS, CRM, PM, e-commerce CRUD APIs |",
    f"| 🧪 [Testing](#testing) | {counts.get('Testing', 0)} | Mock data — fake endpoints, echo servers, sandboxes |",
    f"| 🔐 [Identity](#identity) | {counts.get('Identity', 0)} | Authentication — OAuth, OTP, identity verification |",
    "",
    "---",
    "",
]

# Detailed pattern sections
for pattern in sorted(counts.keys(), key=lambda x: -counts[x]):
    pattern_apis = sorted(
        [a for a in apis if a.get('service_pattern', 'Reference') == pattern],
        key=lambda x: (x.get('category', ''), x.get('name', '').lower())
    )
    
    descs = {
        'Reference': 'Static or semi-static reference data: books, movies, music, recipes, quotes, facts, species databases, dictionaries, holiday calendars.',
        'Service': 'APIs that generate, transform, or process content: QR code generators, URL shorteners, file converters, color palette generators, lorem ipsum.',
        'Dynamic Data': 'Real-time or regularly updated data: weather forecasts, market prices, news feeds, sports scores, air quality, transit schedules.',
        'Geospatial': 'Location-based services: maps, geocoding, routing, public transit, elevation, GPS.',
        'Communication': 'Messaging and communication: email, social media, notifications, webhooks, publishing.',
        'Government': 'Official government and public data: census, legislation, patents, transparency, compliance, law enforcement.',
        'Analytics': 'Monitoring and analysis: metrics, security scanning, threat detection, health checks, abuse detection.',
        'AI/ML': 'Machine learning and AI: NLP, text analysis, translation, classification, image recognition.',
        'Platform': 'Platform integration APIs: CMS, CRM, project management, e-commerce.',
        'Testing': 'Testing and mock APIs: fake endpoints, echo servers, mock data.',
        'Identity': 'Authentication and identity: OAuth, OTP, identity verification, KYC.',
    }
    
    lines.append(f"## {pattern} ({len(pattern_apis)})")
    lines.append("")
    lines.append(descs.get(pattern, ''))
    lines.append("")
    lines.append("| API | Category | Auth | Description |")
    lines.append("|-----|----------|------|-------------|")
    
    for a in pattern_apis:
        auth_badge = "🔑" if a.get('auth', 'No') != 'No' else "🆓"
        cat = a.get('category', 'Other')
        desc_text = (a.get('description', '') or '—')[:100]
        lines.append(f"| [{a['name']}]({a['url']}) | {cat} | {auth_badge} | {desc_text} |")
    lines.append("")

lines.append("---")
lines.append("")
lines.append("## File Structure")
lines.append("")
lines.append("```")
lines.append("apis.json              # Full catalog with service_pattern field")
lines.append("no-auth-apis.json      # 1,159 APIs requiring zero authentication")
lines.append("categories/            # 52 files organized by topic category")
lines.append("patterns/              # 11 files organized by functional pattern")
lines.append("classify_service_patterns.py  # Classification script")
lines.append("```")

lines.append("")
lines.append("## Classification Methodology")
lines.append("")
lines.append("Each API is assigned exactly one **functional pattern** based on what the API does.")
lines.append("Additionally, each API belongs to a **topic category** describing its domain.")
lines.append("")
lines.append("For example:")
lines.append("- **CoinGecko API**: `Dynamic Data` (real-time prices) in `Cryptocurrency` category")
lines.append("- **QR code Generator**: `Service` (generates QR codes) in `Development` category")
lines.append("- **eBird**: `Reference Data` (species observations) in `Animals` category")
lines.append("")
lines.append("---")
lines.append("")
lines.append("## Sources")
lines.append("")
lines.append("Aggregated, deduplicated, and merged from:")
lines.append("1. [public-apis/public-apis](https://github.com/marcelscruz/public-apis)")
lines.append("2. [public-api-lists/public-api-lists](https://github.com/public-api-lists/public-api-lists)")
lines.append("3. [FreePublicAPIs.com](https://www.freepublicapis.com)")
lines.append("4. APIs.guru OpenAPI directory")
lines.append("5. Honcho Agent context (research-verified)")
lines.append("6. Manual curation of free/zero-key services")
lines.append("")

readme_path = '/home/terexitarius/free-api-catalog/README.md'
with open(readme_path, 'w') as f:
    f.write('\n'.join(lines))

print(f"README.md written: {os.path.getsize(readme_path):,} bytes")
print(f"Generated {len(lines)} lines")
