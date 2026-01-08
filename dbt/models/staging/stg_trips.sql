
with source as (

    select * from {{ source('silver', 'enriched_trip_events') }}

),

renamed as (

    select
        event_id,
        vehicle_id,
        timestamp as event_at,
        event_type,
        latitude,
        longitude,
        speed_kmh,
        heading,
        fuel_level_percent,
        weather_condition,
        region,
        processed_at

    from source

)

select * from renamed
