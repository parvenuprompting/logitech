
{{ config(
    materialized='incremental',
    unique_key='vehicle_day_id'
) }}

with trip_segments as (

    select * from {{ ref('int_trip_segments') }}

),

daily_agg as (

    select
        vehicle_id,
        date(event_at) as date_day,
        
        -- Metrics
        count(*) as total_events,
        sum(distance_km) as total_distance_km,
        sum(duration_seconds) / 3600 as total_drive_hours,
        avg(speed_kmh) as avg_speed_kmh,
        max(speed_kmh) as max_speed_kmh,
        
        -- Fuel (Difference between max and min for the day, simplified)
        -- Real logic needs refuelling detection
        max(fuel_level_percent) - min(fuel_level_percent) as est_fuel_consumed_percent

    from trip_segments
    
    {% if is_incremental() %}
    -- Reprocess only recent data
    where event_at >= date_sub(current_date(), 3)
    {% endif %}

    group by 1, 2

)

select
    concat(vehicle_id, '_', date_day) as vehicle_day_id,
    *
from daily_agg
