"""Zero-dependency Python 3.10+ stdio MCP Server (JSON-RPC 2.0) for official EU & U.S. government APIs.

Tools exposed (zero API keys, zero external Python packages):
1. search_french_companies  — Official DINUM/INSEE/INPI SIRENE/RNE API (France)
2. search_eu_public_tenders — Official EU TED Search API v3 (27 EU countries + buyer contacts)
3. search_clinical_trials   — Official U.S. NIH ClinicalTrials.gov REST API v2
4. search_us_npi_providers  — Official U.S. CMS NPPES NPI Registry API v2.1 (8M+ doctors & clinics)
"""

from __future__ import annotations

import gzip
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from typing import Any

SERVER_NAME = "eu-us-opendata-mcp"
SERVER_VERSION = "1.0.0"
PROTOCOL_VERSION = "2024-11-05"
USER_AGENT = f"{SERVER_NAME}/{SERVER_VERSION} (+https://github.com/yannabadie/eu-us-opendata-mcp)"

TOOLS_SPEC: list[dict[str, Any]] = [
    {
        "name": "search_french_companies",
        "description": (
            "Search official French companies via DINUM/INSEE/INPI SIRENE/RNE Open Data API "
            "(15M+ entities: SIREN, SIRET, computed EU VAT, NAF code, revenue, labels, address & Pappers link)."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Company name, SIREN, or keyword (e.g. 'Doctolib', 'logiciel ia')."},
                "postal_code": {"type": "string", "description": "Optional 5-digit French postal code (e.g. '75008')."},
                "department": {"type": "string", "description": "Optional 2- or 3-digit department code (e.g. '75', '69')."},
                "naf_code": {"type": "string", "description": "Optional NAF/APE activity code (e.g. '62.01Z')."},
                "est_qualiopi": {"type": "boolean", "description": "Filter for Qualiopi-certified entities."},
                "est_rge": {"type": "boolean", "description": "Filter for RGE-certified entities."},
                "limit": {"type": "integer", "description": "Max results (1 to 25, default 5).", "default": 5},
            },
        },
    },
    {
        "name": "search_eu_public_tenders",
        "description": (
            "Search active European Union public procurement tenders across 27 EU countries via "
            "official EU TED Search API v3 (returns title, buyer name, buyer email/phone/website, CPV codes, deadline & official URL)."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "country": {"type": "string", "description": "ISO3 buyer country code (e.g. 'FRA', 'DEU', 'BEL', 'ESP', 'ITA')."},
                "cpv_prefix": {"type": "string", "description": "CPV sector prefix or 8-digit code (e.g. '72' for IT, '45' for construction)."},
                "keyword": {"type": "string", "description": "Optional full-text keyword."},
                "days_back": {"type": "integer", "description": "Lookback window in days (default 14).", "default": 14},
                "limit": {"type": "integer", "description": "Max notices (1 to 25, default 5).", "default": 5},
            },
        },
    },
    {
        "name": "search_clinical_trials",
        "description": (
            "Search 500,000+ clinical studies via official U.S. NIH ClinicalTrials.gov REST API v2 "
            "(returns NCT ID, title, status, phases, lead sponsor, enrollment, central contact email/phone & study URL)."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "condition": {"type": "string", "description": "Medical condition or disease (e.g. 'diabetes', 'oncology')."},
                "intervention": {"type": "string", "description": "Optional drug, biologic, or therapy name."},
                "sponsor": {"type": "string", "description": "Optional lead sponsor (e.g. 'Sanofi', 'Eli Lilly')."},
                "location": {"type": "string", "description": "Optional country or city (e.g. 'France', 'Boston')."},
                "status": {"type": "string", "description": "Optional status (e.g. 'RECRUITING', 'NOT_YET_RECRUITING').", "default": "RECRUITING"},
                "limit": {"type": "integer", "description": "Max studies (1 to 25, default 5).", "default": 5},
            },
        },
    },
    {
        "name": "search_us_npi_providers",
        "description": (
            "Search 8,000,000+ U.S. physicians, dentists, clinics, hospitals & pharmacies via official "
            "U.S. CMS NPPES NPI Registry API v2.1 (returns NPI, specialty, practice phone/fax, address & authorized official)."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "specialty": {"type": "string", "description": "Medical specialty / taxonomy (e.g. 'Cardiology', 'Dentist', 'Dermatology')."},
                "state": {"type": "string", "description": "2-letter U.S. state code (e.g. 'CA', 'NY', 'TX')."},
                "city": {"type": "string", "description": "Optional U.S. city name (e.g. 'Los Angeles', 'Austin')."},
                "organization_name": {"type": "string", "description": "Optional clinic/hospital organization name."},
                "npi_number": {"type": "string", "description": "Optional exact 10-digit NPI lookup."},
                "limit": {"type": "integer", "description": "Max providers (1 to 25, default 5).", "default": 5},
            },
        },
    },
]


def _http_json(
    url: str,
    method: str = "GET",
    params: dict[str, Any] | None = None,
    json_body: dict[str, Any] | None = None,
    timeout: float = 20.0,
) -> dict[str, Any]:
    full_url = url
    if params:
        clean = {k: v for k, v in params.items() if v is not None and v != ""}
        if clean:
            sep = "&" if "?" in url else "?"
            full_url = f"{url}{sep}{urllib.parse.urlencode(clean)}"

    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "User-Agent": USER_AGENT,
    }
    body: bytes | None = None
    if json_body is not None:
        body = json.dumps(json_body).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(full_url, data=body, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read()
        if raw[:2] == b"\x1f\x8b":
            raw = gzip.decompress(raw)
        return json.loads(raw.decode("utf-8", errors="replace"))


def _compute_fr_vat(siren: str) -> str | None:
    digits = re.sub(r"\D", "", siren or "")
    if len(digits) != 9:
        return None
    key = (12 + 3 * (int(digits) % 97)) % 97
    return f"FR{key:02d}{digits}"


def _pick_localized(obj: Any) -> str | None:
    if obj is None:
        return None
    if isinstance(obj, str):
        return obj.strip() or None
    if isinstance(obj, list):
        for item in obj:
            val = _pick_localized(item)
            if val:
                return val
        return None
    if isinstance(obj, dict):
        for k in ("eng", "ENG", "fra", "FRA", "deu", "DEU"):
            if k in obj and obj[k]:
                val = _pick_localized(obj[k])
                if val:
                    return val
        for v in obj.values():
            val = _pick_localized(v)
            if val:
                return val
    return None


def tool_search_french_companies(args: dict[str, Any]) -> dict[str, Any]:
    limit = max(1, min(int(args.get("limit") or 5), 25))
    params: dict[str, Any] = {"per_page": limit, "page": 1, "etat_administratif": "A"}
    if args.get("query"):
        params["q"] = str(args["query"]).strip()
    if args.get("postal_code"):
        params["code_postal"] = str(args["postal_code"]).strip()
    if args.get("department"):
        params["departement"] = str(args["department"]).strip()
    if args.get("naf_code"):
        params["activite_principale"] = str(args["naf_code"]).strip().upper()
    if args.get("est_qualiopi"):
        params["est_qualiopi"] = "true"
    if args.get("est_rge"):
        params["est_rge"] = "true"
    if set(params.keys()) <= {"per_page", "page", "etat_administratif"}:
        params["q"] = "logiciel"

    data = _http_json("https://recherche-entreprises.api.gouv.fr/search", params=params)
    items = []
    for c in data.get("results") or []:
        siren = str(c.get("siren") or "")
        siege = c.get("siege") or {}
        raw_tva = c.get("tva")
        if isinstance(raw_tva, list):
            raw_tva = raw_tva[0] if raw_tva else None
        items.append(
            {
                "siren": siren,
                "vat_number": str(raw_tva).strip() if raw_tva else _compute_fr_vat(siren),
                "company_name": c.get("nom_complet") or c.get("nom_raison_sociale"),
                "naf_code": c.get("activite_principale"),
                "postal_code": siege.get("code_postal"),
                "city": siege.get("libelle_commune"),
                "annuaire_url": f"https://annuaire-entreprises.data.gouv.fr/entreprise/{siren}" if siren else None,
                "pappers_url": f"https://www.pappers.fr/entreprise/{siren}" if siren else None,
            }
        )
    return {
        "source": "DINUM/INSEE/INPI recherche-entreprises.api.gouv.fr",
        "total_results": int(data.get("total_results") or 0),
        "returned": len(items),
        "companies": items,
    }


def tool_search_eu_public_tenders(args: dict[str, Any]) -> dict[str, Any]:
    limit = max(1, min(int(args.get("limit") or 5), 25))
    days_back = max(1, min(int(args.get("days_back") or 14), 365))
    since = (datetime.now(timezone.utc) - timedelta(days=days_back)).strftime("%Y%m%d")
    clauses = [f"publication-date >= {since}"]
    if args.get("country"):
        c = re.sub(r"[^A-Za-z]", "", str(args["country"])).upper()[:3]
        if len(c) == 3:
            clauses.append(f"buyer-country = {c}")
    if args.get("cpv_prefix"):
        cpv = re.sub(r"[^0-9]", "", str(args["cpv_prefix"]))
        if cpv:
            clauses.append(f"classification-cpv = {cpv}*" if len(cpv) < 8 else f"classification-cpv = {cpv[:8]}")
    if args.get("keyword"):
        kw = str(args["keyword"]).replace('"', "").replace("\\", "").strip()
        if kw:
            clauses.append(f'FT ~ "{kw}"')

    query = " AND ".join(clauses)
    data = _http_json(
        "https://api.ted.europa.eu/v3/notices/search",
        method="POST",
        json_body={
            "query": query,
            "fields": [
                "publication-number",
                "publication-date",
                "notice-title",
                "notice-type",
                "buyer-name",
                "buyer-country",
                "buyer-email",
                "organisation-email-buyer",
                "organisation-tel-buyer",
                "organisation-internet-address-buyer",
                "classification-cpv",
                "deadline-receipt-tender-date-lot",
                "estimated-value-glo",
                "estimated-value-cur-glo",
            ],
            "limit": limit,
            "page": 1,
            "scope": "ACTIVE",
        },
    )
    tenders = []
    for n in data.get("notices") or []:
        pub = str(n.get("publication-number") or "")
        tenders.append(
            {
                "tenderId": pub,
                "title": _pick_localized(n.get("notice-title")) or pub,
                "buyerName": _pick_localized(n.get("buyer-name")),
                "buyerCountry": _pick_localized(n.get("buyer-country")),
                "buyerEmail": _pick_localized(n.get("buyer-email")) or _pick_localized(n.get("organisation-email-buyer")),
                "buyerPhone": _pick_localized(n.get("organisation-tel-buyer")),
                "buyerWebsite": _pick_localized(n.get("organisation-internet-address-buyer")),
                "publicationDate": str(n.get("publication-date") or "")[:10] or None,
                "deadlineDate": (_pick_localized(n.get("deadline-receipt-tender-date-lot")) or "")[:10] or None,
                "cpvCodes": list(n.get("classification-cpv") or [])[:5],
                "noticeUrl": f"https://ted.europa.eu/en/notice/-/detail/{pub}" if pub else None,
            }
        )
    return {
        "source": "EU TED Search API v3",
        "query": query,
        "total_available": int(data.get("totalNoticeCount") or 0),
        "returned": len(tenders),
        "tenders": tenders,
    }


def tool_search_clinical_trials(args: dict[str, Any]) -> dict[str, Any]:
    limit = max(1, min(int(args.get("limit") or 5), 25))
    params: dict[str, Any] = {
        "pageSize": str(limit),
        "countTotal": "true",
        "sort": "LastUpdatePostDate:desc",
    }
    if args.get("condition"):
        params["query.cond"] = str(args["condition"]).strip()
    if args.get("intervention"):
        params["query.intr"] = str(args["intervention"]).strip()
    if args.get("sponsor"):
        params["query.spons"] = str(args["sponsor"]).strip()
    if args.get("location"):
        params["query.locn"] = str(args["location"]).strip()
    if args.get("status"):
        params["filter.overallStatus"] = str(args["status"]).strip().upper()

    data = _http_json("https://clinicaltrials.gov/api/v2/studies", params=params)
    studies = []
    for st in data.get("studies") or []:
        ps = st.get("protocolSection") or {}
        ident = ps.get("identificationModule") or {}
        status = ps.get("statusModule") or {}
        design = ps.get("designModule") or {}
        sponsor = (ps.get("sponsorCollaboratorsModule") or {}).get("leadSponsor") or {}
        contacts = (ps.get("contactsLocationsModule") or {}).get("centralContacts") or []
        first_contact = contacts[0] if contacts and isinstance(contacts[0], dict) else {}
        nct = str(ident.get("nctId") or "")
        studies.append(
            {
                "nctId": nct,
                "briefTitle": ident.get("briefTitle"),
                "overallStatus": status.get("overallStatus"),
                "phases": design.get("phases") or [],
                "leadSponsor": sponsor.get("name"),
                "enrollmentCount": (design.get("enrollmentInfo") or {}).get("count"),
                "primaryContactEmail": first_contact.get("email"),
                "primaryContactPhone": first_contact.get("phone"),
                "studyUrl": f"https://clinicaltrials.gov/study/{nct}" if nct else None,
            }
        )
    return {
        "source": "NIH ClinicalTrials.gov REST API v2",
        "total_matches": int(data.get("totalCount") or 0),
        "returned": len(studies),
        "studies": studies,
    }


def tool_search_us_npi_providers(args: dict[str, Any]) -> dict[str, Any]:
    limit = max(1, min(int(args.get("limit") or 5), 25))
    params: dict[str, Any] = {"version": "2.1", "limit": limit}
    if args.get("npi_number"):
        digits = re.sub(r"\D", "", str(args["npi_number"]))
        if len(digits) == 10:
            params["number"] = digits
    else:
        if args.get("specialty"):
            params["taxonomy_description"] = str(args["specialty"]).strip()
        if args.get("state"):
            params["state"] = re.sub(r"[^A-Za-z]", "", str(args["state"])).upper()[:2]
        if args.get("city"):
            params["city"] = str(args["city"]).strip()
        if args.get("organization_name"):
            params["organization_name"] = str(args["organization_name"]).strip()
        if set(params.keys()) <= {"version", "limit", "state"}:
            params["taxonomy_description"] = "Cardiology"
            params.setdefault("state", "CA")

    data = _http_json("https://npiregistry.cms.hhs.gov/api/", params=params)
    providers = []
    for p in data.get("results") or []:
        npi = str(p.get("number") or "")
        basic = p.get("basic") or {}
        addrs = p.get("addresses") or []
        loc = next((a for a in addrs if isinstance(a, dict) and a.get("address_purpose") == "LOCATION"), None) or (addrs[0] if addrs else {})
        taxs = p.get("taxonomies") or []
        prim_tax = next((t for t in taxs if isinstance(t, dict) and t.get("primary")), None) or (taxs[0] if taxs else {})
        name = basic.get("organization_name") or " ".join(x for x in [basic.get("first_name"), basic.get("last_name")] if x)
        providers.append(
            {
                "npi": npi,
                "enumerationType": p.get("enumeration_type"),
                "providerName": name,
                "primarySpecialty": prim_tax.get("desc"),
                "city": loc.get("city"),
                "state": loc.get("state"),
                "phone": loc.get("telephone_number"),
                "fax": loc.get("fax_number"),
                "nppesUrl": f"https://npiregistry.cms.hhs.gov/provider-view/{npi}" if npi else None,
            }
        )
    return {
        "source": "U.S. CMS NPPES NPI Registry API v2.1",
        "returned": len(providers),
        "providers": providers,
    }


TOOL_DISPATCH = {
    "search_french_companies": tool_search_french_companies,
    "search_eu_public_tenders": tool_search_eu_public_tenders,
    "search_clinical_trials": tool_search_clinical_trials,
    "search_us_npi_providers": tool_search_us_npi_providers,
}


def handle_request(req: dict[str, Any]) -> dict[str, Any] | None:
    req_id = req.get("id")
    method = req.get("method", "")
    params = req.get("params") or {}

    if method == "notifications/initialized" or req_id is None and method.startswith("notifications/"):
        return None

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {"tools": {}},
                "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
            },
        }

    if method == "ping":
        return {"jsonrpc": "2.0", "id": req_id, "result": {}}

    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": TOOLS_SPEC}}

    if method == "tools/call":
        tool_name = str(params.get("name") or "")
        tool_args = params.get("arguments") or {}
        fn = TOOL_DISPATCH.get(tool_name)
        if fn is None:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"},
            }
        try:
            result = fn(tool_args)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(result, indent=2, ensure_ascii=False)}],
                    "isError": False,
                },
            }
        except Exception as err:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": f"Upstream API error: {err}"}],
                    "isError": True,
                },
            }

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32601, "message": f"Method not found: {method}"},
    }


def main() -> int:
    for line in sys.stdin:
        text = line.strip()
        if not text:
            continue
        try:
            msg = json.loads(text)
        except json.JSONDecodeError as err:
            resp = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": f"Parse error: {err}"}}
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
            continue

        reply = handle_request(msg)
        if reply is not None:
            sys.stdout.write(json.dumps(reply, ensure_ascii=False) + "\n")
            sys.stdout.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
