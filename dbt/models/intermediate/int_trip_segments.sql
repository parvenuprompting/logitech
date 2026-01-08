
with trips as (

    select * from {{ ref('stg_trips') }}

),

with_lag as (

    select
        *,
        lag(event_at) over (partition by vehicle_id order by event_at) as prev_event_at,
        lag(latitude) over (partition by vehicle_id order by event_at) as prev_lat,
        lag(longitude) over (partition by vehicle_id order by event_at) as prev_lon
    from trips

),

calculated as (

    select
        *,
        -- Time delta in seconds
        unix_timestamp(event_at) - unix_timestamp(prev_event_at) as duration_seconds,
        
        -- Distance delta (Approximation using speed if available, else Haversine/Euclidean)
        -- Ideally use proper Geodetic distance. Here simplified: Speed * Time
        case 
            when speed_kmh is not null and (unix_timestamp(event_at) - unix_timestamp(prev_event_at)) > 0
            then (speed_kmh / 3600.0) * (unix_timestamp(event_at) - unix_timestamp(prev_event_at))
            else 0 
        end as distance_km

    from with_lag
    where prev_event_at is not null
      and (unix_timestamp(event_at) - unix_timestamp(prev_event_at)) < 3600 -- Filter distinct trips breaks > 1h

)

select * from calculated
