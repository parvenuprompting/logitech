
{{ config(
    materialized='incremental',
    unique_key='event_id',
    partition_by={'field': 'event_at', 'data_type': 'date'}
) }}

with segments as (

    select * from {{ ref('int_trip_segments') }}

),

final as (

    select
        event_id,
        vehicle_id,
        event_at,
        event_type,
        
        -- Locatie
        latitude,
        longitude,
        region,
        
        -- Metrieken
        speed_kmh,
        duration_seconds,
        distance_km,
        fuel_level_percent,
        weather_condition,
        
        -- Derived
        date(event_at) as date_day

    from segments
    
    {% if is_incremental() %}
    where event_at >= date_sub(current_date(), 3)
    {% endif %}

)

select * from final
