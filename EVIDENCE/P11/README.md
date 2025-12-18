# P11 - Dynamic Application Security Testing (DAST)

## Files in this directory:

1. **zap_baseline.html** - Full ZAP scan report (HTML format)
2. **zap_baseline.json** - Machine-readable ZAP results (JSON format)
3. **dast_summary.md** - Executive summary with risk assessment

## How to use for DS3 section:

1. **Open zap_baseline.html** in browser for detailed vulnerability analysis
2. **Review dast_summary.md** for executive overview
3. **Reference findings** in Dynamic Analysis (DS3) section of final report:
   - List identified vulnerabilities by severity
   - Document remediation actions taken
   - Note accepted risks with justification

## Scan Configuration:
- **Tool**: OWASP ZAP Baseline
- **Target**: Local FastAPI application on port 8080
- **Scan Type**: Passive and active scanning
- **Trigger**: Push to main/develop or manual workflow_dispatch

## Typical Findings:
- Missing security headers (CSP, HSTS)
- Information leakage in headers
- Cookie security attributes
- XSS and CSRF potential issues
