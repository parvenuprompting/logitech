-- Custom data quality test
-- Fuel percentage should be between 0 and 100

select
    vehicle_id,
    latest_fuel_level
from {{ ref('dim_vehicles') }}
where latest_fuel_level < 0 OR latest_fuel_level > 100
