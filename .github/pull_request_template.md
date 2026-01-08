# Silver Layer Change Request

## Description
<!-- Beschrijf wat er verandert en waarom -->

## Change Type
- [ ] **Low Impact** (New enrichment, no break)
- [ ] **Medium Impact** (Logic change, data value change)
- [ ] **High Impact** (Alert logic change, operational impact)
- [ ] **Critical** (Schema breaking change)

## Impact Checklis (VERPLICHT voor Silver Layer)
<!-- Vink af en vul in waar van toepassing -->

- [ ] **Streaming Jobs Affected**:
  - [ ] `detect_idle`
  - [ ] `detect_route_deviation`
  - [ ] `ingest_telemetry` (Schema changes!)
  - *Lijst hier:* 

- [ ] **Batch Jobs / Gold Models Affected**:
  - [ ] `stg_trips` (dbt)
  - [ ] `fct_trip_analysis` (dbt)
  - *Lijst hier:*

- [ ] **Backwards Compatibility**:
  - [ ] Is deze wijziging compatible met historische data?
  - [ ] Is een schema migratie nodig?
  - *Toelichting:*

- [ ] **Rollback Plan**:
  - [ ] Feature Flag aanwezig? (Naam: `...`)
  - [ ] Is data herstel nodig bij fout?

## Verification
- [ ] Unit tests toegevoegd/geupdate
- [ ] Getest op dev dataset
- [ ] Performance impact ingeschat (Shuffle/Join?)
