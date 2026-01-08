
with source as (

    select * from {{ source('silver', 'alerts_history') }}

),

renamed as (

    select
        vehicle_id,
        alert_type,
        message,
        alert_timestamp as triggered_at,
        detection_time,
        latency_seconds

    from source

)

select * from renamed
