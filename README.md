# `eu-us-opendata-mcp`

[![MCP Stdio Tests](https://github.com/yannabadie/eu-us-opendata-mcp/actions/workflows/test.yml/badge.svg)](https://github.com/yannabadie/eu-us-opendata-mcp/actions/workflows/test.yml)
[![yannabadie/eu-us-opendata-mcp MCP server](https://glama.ai/mcp/servers/yannabadie/eu-us-opendata-mcp/badges/score.svg)](https://glama.ai/mcp/servers/yannabadie/eu-us-opendata-mcp)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Zero-dependency, zero-API-key **Model Context Protocol (MCP)** stdio server in pure Python 3.10+ for querying **5 official European & U.S. government & biomedical open-data registries** directly from **Claude Desktop, Claude Code, Cursor, Windsurf, Google Antigravity, or Codex**.

---

## Included MCP Tools (100% Free Official APIs, Zero Keys)

| Tool | Official Upstream Registry | Key Fields Returned |
|---|---|---|
| `search_french_companies` | **DINUM / INSEE / INPI** (`recherche-entreprises.api.gouv.fr`) | SIREN, computed EU VAT (`FRxx...`), NAF/APE, city/ZIP, Qualiopi/RGE filters, Annuaire & Pappers URLs |
| `search_eu_public_tenders` | **EU TED Search API v3** (`api.ted.europa.eu/v3` — 27 EU countries) | Tender ID, title, buyer name, **buyer email, phone & website**, CPV codes, deadline & official notice URL |
| `search_clinical_trials` | **U.S. NIH ClinicalTrials.gov REST API v2** (`clinicaltrials.gov/api/v2`) | NCT ID, title, status, phases, lead sponsor, enrollment, central contact email/phone & study URL |
| `search_us_npi_providers` | **U.S. CMS NPPES NPI Registry API v2.1** (`npiregistry.cms.hhs.gov`) | 10-digit NPI, doctor/clinic name, primary specialty, city/state, **direct phone & fax**, NPPES profile URL |
| `search_pubmed_papers` | **EMBL-EBI Europe PMC & PubMed REST API** (`ebi.ac.uk/europepmc`) | PMID/PMCID/DOI, **full untruncated abstract**, citations, **author emails**, MeSH terms & **free PDF URL** |

---

## Quick Install & Run (No API Keys Required)

### Option 1 — Run directly with `uvx` (recommended)
```json
{
  "mcpServers": {
    "eu-us-opendata": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/yannabadie/eu-us-opendata-mcp.git",
        "eu-us-opendata-mcp"
      ]
    }
  }
}
```

### Option 2 — Install with `pip`
```bash
pip install git+https://github.com/yannabadie/eu-us-opendata-mcp.git
eu-us-opendata-mcp
```

### Option 3 — Run from source (zero dependencies)
```bash
git clone https://github.com/yannabadie/eu-us-opendata-mcp.git
cd eu-us-opendata-mcp
PYTHONPATH=src python3 -m eu_us_opendata_mcp.server
```

---

## Run Tests

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

---

## Need Bulk Cloud Exports (1,000–10,000+ Records), Hosted REST APIs, or Daily n8n Alerts?

This local MCP server is built for fast interactive agent lookups (up to 25 results per tool call). For **bulk CSV/Excel/JSON extraction, scheduled daily monitoring, BODACC insolvency KYC screening, BOAMP French tenders, award winner intelligence, and ready-to-import n8n workflows**, use our hosted Pay-Per-Event Apify Actors ([free `$5/mo` Apify credits included](https://apify.com/?fpr=zuvzfw)):

- **[Pappers / SIRENE Scraper — French Companies API](https://apify.com/yannabadie/french-company-intelligence-mcp?fpr=zuvzfw)** (`$6/1k`, free count mode, GPS radius search, BODACC insolvency KYC & BOAMP)
- **[TED Europa & BOAMP — EU Public Tenders & Contacts](https://apify.com/yannabadie/eu-public-tenders-ted-boamp?fpr=zuvzfw)** (`$3–$4/1k`, 27 EU countries + France, buyer contacts & award winners)
- **[ClinicalTrials.gov API v2 — Trials & Contacts](https://apify.com/yannabadie/clinical-trials-api-mcp?fpr=zuvzfw)** (`$5/1k`, 500k+ studies, free count mode, URL/NCT lookup & contacts)
- **[NPI Registry Scraper — US Doctors & Clinics API](https://apify.com/yannabadie/npi-healthcare-providers-mcp?fpr=zuvzfw)** (`$2.50/1k` all-inclusive, 8M+ U.S. doctors & clinics, phones, fax & authorized officials)
- **[PubMed & Europe PMC API — Papers, Emails & PDFs](https://apify.com/yannabadie/pubmed-europepmc-api-mcp?fpr=zuvzfw)** (`$2/1k`, 37M+ papers, full abstracts, author emails, ORCIDs, grants, NCT trial links & free PDFs)
- **[Free n8n Workflow Templates & Starter CLI (9 Workflows, 9 Actors)](https://github.com/yannabadie/official-opendata-mcp-n8n-templates)**

---

## 15 Hosted REST APIs on RapidAPI Hub (Edge-Cached Cloudflare Workers)

All 15 production REST APIs include a free Basic tier + Pro/Ultra/Mega plans with instant key auth and OpenAPI 3.0 specs:

### Official EU & US Open-Data Suite (6 APIs)
| # | Hosted API (RapidAPI Hub) | Upstream Official Registry |
|---:|---|---|
| 1 | **[EU & US Official Open-Data Intelligence (5-in-1)](https://rapidapi.com/YannAbadie/api/eu-us-official-open-data-intelligence1)** | SIRENE, EU TED v3, ClinicalTrials v2, US NPI, PubMed/Europe PMC |
| 2 | **[French SIRENE Company & EU VAT API](https://rapidapi.com/YannAbadie/api/french-sirene-company-and-eu-vat-api)** | DINUM / INSEE / INPI SIRENE + computed EU VAT |
| 3 | **[EU TED Public Tenders Procurement API](https://rapidapi.com/YannAbadie/api/eu-ted-public-tenders-procurement-api)** | EU TED Search API v3 (27 EU countries, buyer contacts) |
| 4 | **[NIH ClinicalTrials v2 Studies API](https://rapidapi.com/YannAbadie/api/nih-clinicaltrials-v2-studies-api)** | U.S. NIH ClinicalTrials.gov REST API v2 (500k+ trials) |
| 5 | **[US NPI Healthcare Providers Registry API](https://rapidapi.com/YannAbadie/api/us-npi-healthcare-providers-registry-api)** | U.S. CMS NPPES NPI v2.1 (8M+ doctors & clinics) |
| 6 | **[PubMed & Europe PMC Literature API](https://rapidapi.com/YannAbadie/api/pubmed-and-europe-pmc-literature-api)** | EMBL-EBI Europe PMC & PubMed (37M+ papers, emails, PDFs) |

### B2B KYB, Hiring & Financial Enrichment Suite (4 APIs)
| # | Hosted API (RapidAPI Hub) | Capabilities |
|---:|---|---|
| 7 | **[Website Contact & Tech Stack Enricher](https://rapidapi.com/YannAbadie/api/website-contact-and-tech-stack-enricher)** | Role-ranked emails, phones, socials & 54 tech-stack signatures |
| 8 | **[Multi-ATS Jobs Board API](https://rapidapi.com/YannAbadie/api/multi-ats-jobs-board-api)** | 7 public ATS JSON APIs (Greenhouse, Lever, Ashby, Workable, etc.) |
| 9 | **[EU KYB VAT VIES & GLEIF LEI](https://rapidapi.com/YannAbadie/api/eu-kyb-vat-vies-and-gleif-lei)** | Live EU VIES VAT validation + GLEIF LEI corporate entity lookup |
| 10 | **[SEC EDGAR Filings & Financials](https://rapidapi.com/YannAbadie/api/sec-edgar-filings-and-financials)** | Official U.S. SEC EDGAR submissions, 10-K/10-Q & XBRL metrics |

### EU Public Intelligence, RegTech & Energy Suite (5 New APIs)
| # | Hosted API (RapidAPI Hub) | Upstream Official Source |
|---:|---|---|
| 11 | **[ADEME DPE France Energy Ratings API](https://rapidapi.com/YannAbadie/api/ademe-dpe-france-energy-ratings-api)** | ADEME Open Data DPE A–G energy diagnostics & GES ratings |
| 12 | **[French BODACC Legal Notices API](https://rapidapi.com/YannAbadie/api/french-bodacc-legal-notices-api)** | DILA BODACC insolvency, liquidation & corporate legal notices |
| 13 | **[EU CRA Open Source Security Audit API](https://rapidapi.com/YannAbadie/api/eu-cra-open-source-security-audit-api)** | OSV.dev + CISA KEV 24h EU Cyber Resilience Act Art. 14 check |
| 14 | **[US OpenFDA Drugs, Devices & Recalls API](https://rapidapi.com/YannAbadie/api/us-openfda-drugs-devices-recalls-api)** | U.S. FDA OpenFDA drug/device recalls, adverse events & labels |
| 15 | **[EU Macro FX & French Grid Energy API](https://rapidapi.com/YannAbadie/api/eu-macro-fx-and-french-grid-energy-api)** | European Central Bank (ECB) FX rates + RTE Éco2mix live French grid |

---

## 5 Live GitHub Marketplace EU RegTech Actions (MIT, Zero Dependencies)

Automated CI/CD compliance gates + 100% browser-side free scanners:

- **[Factur-X France 2026–2027 Validator (EN 16931 / PDF/A-3)](https://github.com/marketplace/actions/factur-x-france-2026-2027-validator-en-16931-pdf-a-3)** · [Repo](https://github.com/yannabadie/facturx-france-2027) · [Free Browser Validator](https://yannabadie.github.io/facturkit-2027/audit-facture-gratuit.html)
- **[CRA-SBOM-Guard (EU Cyber Resilience Act Art. 14 & CycloneDX 1.5)](https://github.com/marketplace/actions/cra-sbom-guard-eu-cyber-resilience-act-art-14-scanner)** · [Repo](https://github.com/yannabadie/cra-sbom-guard) · [Free Browser SBOM Scanner](https://yannabadie.github.io/cra-sbom-guard/)
- **[AccessiKit EAA & RGAA v5 Accessibility Auditor](https://github.com/marketplace/actions/accessikit-eaa-rgaa-v5-accessibility-auditor)** · [Repo](https://github.com/yannabadie/accessikit-eaa-rgaa) · [Free Browser A11y Auditor](https://yannabadie.github.io/accessikit-eaa-rgaa/)
- **[AIActKit — EU AI Act Art. 50 Transparency Guard (Omnibus 2026/1744)](https://github.com/marketplace/actions/aiactkit-eu-ai-act-art-50-transparency-guard)** · [Repo](https://github.com/yannabadie/ai-act-art50-guard) · [Free Classifier & Banner Generator](https://yannabadie.github.io/ai-act-art50-guard/)
- **[BatteryDPP-Check — EU Battery Passport 2023/1542 Validator (GS1 Digital Link)](https://github.com/marketplace/actions/batterydpp-check-eu-battery-passport-2023-1542-validator)** · [Repo](https://github.com/yannabadie/battery-dpp-check) · [Free Passport Validator](https://yannabadie.github.io/battery-dpp-check/)

---

## 3 Free Live Open-Data Portals (210 Programmatic Pages) & Compliance Guides

- **[FacturKit 2027 — 50 French Professions (NAF), 159 DGFiP PA Comparator & URSSAF 2026 Simulator](https://yannabadie.github.io/facturkit-2027/)**
- **[Observatoire ADEME DPE & Artisans RGE — 100 French Cities](https://yannabadie.github.io/observatoire-dpe-rge-france/)**
- **[EU Public Tenders & Open-Data Explorer — 60 EU Country × CPV Procurement Markets](https://yannabadie.github.io/eu-tenders-opendata-explorer/)**

**Turnkey PDF Field Guides & Notion Command Centers (Instant Download, EU VAT MoR on Gumroad):**
- [EU AI Act Art. 50, CRA & EAA/RGAA v5 — Practical Compliance Guide (43 p. PDF, `24 €`)](https://yannabadi.gumroad.com/l/eu-compliance-2026-2027-guide)
- [EU Digital Compliance Command Center 2026–2027 (Notion 4 DBs + 4 SOPs, `29 €`)](https://yannabadi.gumroad.com/l/eu-compliance-2026-2027-notion-pack)
- [Factur-X 2026–2027 Practical Workbook (46 p. PDF, `19 €`)](https://yannabadi.gumroad.com/l/facturx-2026-2027-cahier-pratique)
- [Freelance & EI France 2026–2027 Notion Cockpit (`19 €`)](https://yannabadi.gumroad.com/l/freelance-ei-france-2026-notion-cockpit) · [AI Agent Engineering Skills Bundle (`29 €`)](https://yannabadi.gumroad.com/l/ai-agent-skills-bundle)

---

## License
MIT
