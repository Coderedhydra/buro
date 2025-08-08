from __future__ import annotations
from typing import Any, Dict

SEVERITY_ORDER = ["info", "low", "medium", "high", "critical"]


def _infer_exploitability(analyzer_result: Dict[str, Any]) -> bool:
    if isinstance(analyzer_result.get("exploitable"), bool):
        return bool(analyzer_result["exploitable"])

    text = " ".join([
        " ".join(analyzer_result.get("anomalies") or []),
        str(analyzer_result.get("rationale") or ""),
    ]).lower()
    keywords = [
        "rce", "remote code execution", "sql injection", "sqli", "xss", "csrf bypass",
        "authentication bypass", "privilege escalation", "path traversal", "directory traversal",
        "arbitrary file read", "arbitrary file write", "ssrf", "template injection",
    ]
    return any(k in text for k in keywords)


def _map_confidence_to_severity(confidence: float) -> str:
    if confidence >= 0.85:
        return "high"
    if confidence >= 0.65:
        return "medium"
    if confidence >= 0.35:
        return "low"
    return "info"


def classify_finding(analyzer_result: Dict[str, Any]) -> Dict[str, Any]:
    confidence = float(analyzer_result.get("confidence") or 0.0)
    exploitable = _infer_exploitability(analyzer_result)

    if exploitable:
        severity = "critical"
    else:
        severity = _map_confidence_to_severity(confidence)

    triage = "pending" if SEVERITY_ORDER.index(severity) >= SEVERITY_ORDER.index("medium") else "info"

    return {
        "severity": severity,
        "exploitable": exploitable,
        "confidence": confidence,
        "triage": triage,
        "vuln_type": analyzer_result.get("vuln_type"),
        "cwe": analyzer_result.get("cwe"),
    }