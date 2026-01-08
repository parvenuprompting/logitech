
{{ config(
    materialized='table'
) }}

with vehicle_state as (

    select * from {{ ref('stg_vehicles') }}

),

final as (

    select
        vehicle_id,
        current_status as latest_status,
        current_fuel_level as latest_fuel_level,
        last_seen_at,
        current_latitude,
        current_longitude,
        
        -- Meta
        current_timestamp() as dwh_updated_at

    from vehicle_state

)

select * from final
