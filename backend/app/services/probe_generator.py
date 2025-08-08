from __future__ import annotations
from typing import Any, Dict, List
from urllib.parse import urlencode, urlparse, parse_qs, urlunparse


def build_query_url_with_params(base_url: str, params: Dict[str, Any]) -> str:
    parsed = urlparse(base_url)
    existing = parse_qs(parsed.query)
    existing.update({k: [str(v)] for k, v in params.items()})
    new_query = urlencode(existing, doseq=True)
    return urlunparse(parsed._replace(query=new_query))


def generate_probe_requests(*, method: str, url: str, params: List[Dict[str, Any]], plan: Dict[str, Any]) -> List[Dict[str, Any]]:
    requests: List[Dict[str, Any]] = []

    families = plan.get("test_families") or []
    for family in families:
        examples = family.get("examples") or []
        for example in examples:
            # Expect example: { "param": "q", "value": "...", "location": "query" }
            param_name = example.get("param")
            value = example.get("value")
            location = (example.get("location") or "query").lower()
            headers: Dict[str, str] = {"X-Probe-Family": str(family.get("name", "unknown"))}

            if location == "query":
                target_url = build_query_url_with_params(url, {param_name: value})
                requests.append({
                    "method": method,
                    "url": target_url,
                    "headers": headers,
                    "body": None,
                })
            elif location == "header":
                hdrs = {**headers, param_name: str(value)}
                requests.append({
                    "method": method,
                    "url": url,
                    "headers": hdrs,
                    "body": None,
                })
            elif location == "body":
                # Non-destructive: send JSON body with only the tested param
                body = {param_name: value}
                requests.append({
                    "method": method,
                    "url": url,
                    "headers": {**headers, "Content-Type": "application/json"},
                    "body": body,
                })
            # ignore other locations for MVP

    return requests