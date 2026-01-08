# Go-Live Checklist

**Target Date:** 2026-02-01
**Owner:** Lead Data Engineer

## 1. Security & Compliance
- [ ] **Security Review:** Azure Key Vault Access Policies reviewed.
- [ ] **Networking:** VNET Peering verified between Databricks & Event Hubs.
- [ ] **GDPR:** Anonymization job verified on test data.

## 2. Operations
- [ ] **Alerts:** All Severity 1 alerts routed to PagerDuty.
- [ ] **Runbooks:** Validated by Ops team.
- [ ] **Backups:** Geo-redundancy check enabled on Data Lake.

## 3. Performance
- [ ] **Throughput:** Verified 5k/sec load test.
- [ ] **Latency:** P95 < 5s sustained for 1 hour.

## 4. Business Sign-off
- [ ] **Cost Approval:** Budget of €2k/month approved by Finance.
- [ ] **Stakeholder:** Dashboard layout approved by Fleet Manager.
- [ ] **Rollback Plan:** `docs/operations/rollback_strategy.md` drafted.
