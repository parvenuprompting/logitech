-- Custom data quality test
-- Ensures that calculated trip distance is never negative
-- Strategies: 
-- 1. Error if count > 0

select
    event_id,
    distance_km
from {{ ref('fct_trip_analysis') }}
where distance_km < 0
