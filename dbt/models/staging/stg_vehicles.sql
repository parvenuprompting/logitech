
with source as (

    select * from {{ source('silver', 'vehicle_state') }}

),

renamed as (

    select
        vehicle_id,
        status as current_status,
        fuel_level as current_fuel_level,
        last_seen as last_seen_at,
        current_location.lat as current_latitude,
        current_location.lon as current_longitude

    from source

)

select * from renamed
