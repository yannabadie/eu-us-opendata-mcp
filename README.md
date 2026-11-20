# `eu-us-opendata-mcp`

Zero-dependency, zero-API-key **Model Context Protocol (MCP)** stdio server in pure Python 3.10+ for querying **4 official European & U.S. government open-data registries** directly from **Claude Desktop, Claude Code, Cursor, Windsurf, Google Antigravity, or Codex**.

---

## Included MCP Tools (100% Free Official APIs, Zero Keys)

| Tool | Official Upstream Registry | Key Fields Returned |
|---|---|---|
| `search_french_companies` | **DINUM / INSEE / INPI** (`recherche-entreprises.api.gouv.fr`) | SIREN, computed EU VAT (`FRxx...`), NAF/APE, city/ZIP, Qualiopi/RGE filters, Annuaire & Pappers URLs |
| `search_eu_public_tenders` | **EU TED Search API v3** (`api.ted.europa.eu/v3` — 27 EU countries) | Tender ID, title, buyer name, **buyer email, phone & website**, CPV codes, deadline & official notice URL |
| `search_clinical_trials` | **U.S. NIH ClinicalTrials.gov REST API v2** (`clinicaltrials.gov/api/v2`) | NCT ID, title, status, phases, lead sponsor, enrollment, central contact email/phone & study URL |
| `search_us_npi_providers` | **U.S. CMS NPPES NPI Registry API v2.1** (`npiregistry.cms.hhs.gov`) | 10-digit NPI, doctor/clinic name, primary specialty, city/state, **direct phone & fax**, NPPES profile URL |

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

## Need Bulk Cloud Exports (1,000–10,000+ Records), Daily n8n Alerts, or Hosted Remote MCP?

This local MCP server is built for fast interactive agent lookups (up to 25 results per tool call). For **bulk CSV/Excel/JSON extraction, scheduled daily monitoring, BODACC insolvency KYC screening, BOAMP French tenders, award winner intelligence, and ready-to-import n8n workflows**, use our hosted Pay-Per-Event Apify Actors (free `$5/mo` Apify credits included):

- **[Pappers / SIRENE Scraper — French Companies API](https://apify.com/yannabadie/french-company-intelligence-mcp)** (`$6/1k`, free count mode, GPS radius search, BODACC insolvency KYC & BOAMP)
- **[TED Europa & BOAMP — EU Public Tenders & Contacts](https://apify.com/yannabadie/eu-public-tenders-ted-boamp)** (`$3–$4/1k`, 27 EU countries + France, buyer contacts & award winners)
- **[ClinicalTrials.gov API v2 — Trials & Contacts](https://apify.com/yannabadie/clinical-trials-api-mcp)** (`$5/1k`, 500k+ studies, free count mode, URL/NCT lookup & contacts)
- **[NPI Registry Scraper — US Doctors & Clinics API](https://apify.com/yannabadie/npi-healthcare-providers-mcp)** (`$2.50/1k` all-inclusive, 8M+ U.S. doctors & clinics, phones, fax & authorized officials)
- **[Free n8n Workflow Templates & Starter CLI](https://github.com/yannabadie/official-opendata-mcp-n8n-templates)**

---

## License
MIT
