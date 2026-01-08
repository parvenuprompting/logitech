# Change Governance Enforcement

Om de integriteit van de Silver Layer en productieomgeving te waarborgen, worden de volgende technische maatregelen afgedwongen.

## 1. GitHub Branch Protection Rules
Ingeschakeld op `main` branch:

- **Require Pull Request Reviews**: Minimaal 1 reviewer. Voor `databricks/silver/*` wijzigingen is Code Owner approval vereist.
- **Require Status Checks**:
  - `terraform-validate`: Infrastructure check.
  - `pytest`: Unit tests moeten slagen.
  - `impact-analysis`: Het `generate_graph.py` script moet succesvol draaien (geen broken references).
- **Require Signed Commits**: Verplicht voor traceerbaarheid.

## 2. Architect Review Policy
Voor wijzigingen gemarkeerd als **High Impact** (zie `silver_layer_policy.md`) of **Critical**:

- Label PR met `impact:high`.
- GitHub Action blokkeert merge totdat `CODEOWNERS` (Architect team) approved.

## 3. Performance Regression Testing
In CI/CD pipeline (Staging):

- **Job**: `tests/performance/benchmark_silver.py`
- **Check**: Vergelijk run-time van `validate_deduplicate` en `enrich_telemetry` met baseline.
- **Fail**: Indien >10% regressie.

## 4. Audit Logging
Alle schema wijzigingen en feature flag toggles worden gelogd in:
- `docs/silver_change_log.md` (Git text-based)
- Azure Monitor Logs (Automated)
