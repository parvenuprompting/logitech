# Alert Rollout Strategy

## Phases

### Phase 1: Canary (Week 1)
- **Target**: 2-5 trucks (specifieke IDs)
- **Metric**: Validation of false positive rate
- **Action**: Monitor `monitoring.alert_dead_letter_queue`

### Phase 2: Pilot (Week 2)
- **Target**: 10% of fleet
- **Config**: Update `canary_vehicle_ids` in `config.alert_feature_flags`

### Phase 3: General Availability (Week 3)
- **Target**: 100% of fleet
- **Config**: Set `canary_vehicle_ids` to `["ALL"]` or empty list means all (logic dependent)

## Emergency Rollback

To disable an alert type instantly:

```sql
UPDATE config.alert_feature_flags 
SET enabled = false 
WHERE alert_type = 'idle_detection';
```

No redeploy required. Streaming job picks up change automatically on next micro-batch trigger (if reading config per batch) or needs restart (if cached).
*Implementation Note*: The streaming job re-reads config every micro-batch to ensure instant kill-switch capability.
