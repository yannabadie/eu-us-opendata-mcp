# Security Policy

## Supported Versions

Only the latest minor release series receives security updates:

| Version | Supported |
| ------- | --------- |
| 1.1.x   | Yes       |
| < 1.1.0 | No        |

## Reporting a Vulnerability

Please report suspected security vulnerabilities privately through GitHub Security Advisories rather than opening a public issue:

- **Private disclosure URL**: https://github.com/yannabadie/eu-us-opendata-mcp/security/advisories/new

Include reproduction steps, affected version/commit SHA, and potential impact. Maintainer acknowledgement is targeted within 72 hours, with coordinated disclosure once a fix is released.

## Security Architecture & Threat Model

`eu-us-opendata-mcp` is designed with a minimal attack surface:

- **Read-only, zero-key architecture**: All 5 MCP tools (`search_french_companies`, `search_eu_public_tenders`, `search_clinical_trials`, `search_us_npi_providers`, `search_pubmed_papers`) perform strictly read-only HTTPS requests to official EU and U.S. public government/scientific APIs.
- **No credential or PII storage**: The server requires no API keys, stores no user secrets, writes no persistent local state, and logs no query credentials.
- **No dynamic code or shell execution**: No `eval`, `exec`, or subprocess invocations are executed from tool inputs; all query parameters are validated and clamped before outbound requests with bounded HTTP timeouts.
- **Upstream boundaries**: Data availability, rate limits, and transport security of upstream public registries (`recherche-entreprises.api.gouv.fr`, `api.ted.europa.eu`, `clinicaltrials.gov`, `npiregistry.cms.hhs.gov`, `www.ebi.ac.uk`) are governed by their respective operators.
