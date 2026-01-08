# Weekly Cost Review Template

**Date:** [YYYY-MM-DD]
**Reviewer:** [Name]
**Participants:** [List]

---

## 1. Budget Status
| Environment | Budget | Actual Spend (MTD) | Forecast (EOM) | Status |
|-------------|--------|--------------------|----------------|--------|
| Development | €2,000 | €...               | €...           | 🟢 / 🔴 |
| PoC         | €5,000 | €...               | €...           | 🟢 / 🔴 |
| Production  | €15,000| €...               | €...           | 🟢 / 🔴 |

## 2. Top 5 Cost Drivers (Jobs/Clusters)
*Identifying the most expensive workloads this week.*

1.  **Job Name**: [Name] - €[Amount]
    *   *Analysis*: [Why is it high? Normal growth or issue?]
2.  **Job Name**: [Name] - €[Amount]
3.  ...

## 3. Anomalies Detected
*Any unexpected spikes > 20% compared to average?*

*   [ ] No anomalies detected.
*   [ ] Anomaly: [Description] (e.g., streaming job loop, huge backfill).
    *   *Action Taken*: [Mitigation]

## 4. Optimization Actions
*   [ ] **Action**: Downsize cluster [X] from DS4 to DS3. (Estimated saving: €...)
*   [ ] **Action**: Enable spot instances for job [Y].
*   [ ] **Action**: Review retention policy for [Table Z].

## 5. Next Week Forecast
*   Expected significant changes? (e.g., new onboarding, marketing campaign event volume spike).

---
**Sign-off:** [Manager Name]
