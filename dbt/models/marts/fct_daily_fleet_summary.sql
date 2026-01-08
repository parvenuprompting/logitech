
{{ config(
    materialized='incremental',
    unique_key='vehicle_day_id'
) }}

with daily_stats as (

    select * from {{ ref('int_daily_vehicle_stats') }}

),

final as (

    select
        vehicle_day_id,
        vehicle_id,
        date_day,
        total_events,
        total_distance_km,
        total_drive_hours,
        avg_speed_kmh,
        max_speed_kmh,
        est_fuel_consumed_percent

    from daily_stats
    
    {% if is_incremental() %}
    where date_day >= date_sub(current_date(), 3)
    {% endif %}

)

select * from final
