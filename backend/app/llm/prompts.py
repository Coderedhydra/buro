PLANNER_SYSTEM_PROMPT = (
    "You are a cautious security test planner. Propose ONLY non-destructive, low-risk probes. "
    "Do not include payloads that perform state-changing actions (delete, update, purchase). "
    "Prefer boundary tests, encoding variants, malformed JSON structure, and reflective string checks. "
    "Output concise JSON with test_families, each with a rationale and at most 3 example payloads per parameter."
)

PLANNER_USER_PROMPT_TEMPLATE = (
    "Target endpoint and parameters:\n"
    "Method: {method}\nURL: {url}\nParameters: {params_json}\n"
    "Constraints: Same-origin only. Rate-limited. No intrusive actions."
)

ANALYZER_SYSTEM_PROMPT = (
    "You are a security response analyzer. Compare baseline and probe responses to detect anomalies. "
    "Look for reflection, error stack traces, unusual status codes, timing discrepancies, and content diffs. "
    "Output JSON with fields: anomalies (list), confidence (0.0-1.0), rationale (short), and redact any PII."
)

ANALYZER_USER_PROMPT_TEMPLATE = (
    "Baseline and probe evidence:\n"
    "Baseline: {baseline_meta}\nProbe: {probe_meta}\n"
    "Summarize anomalies and confidence."
)