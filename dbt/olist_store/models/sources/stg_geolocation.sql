with geolocation as (
    select 
    geolocation_zip_code_prefix
    , geolocation_lat
    , geolocation_lng
    , geolocation_city
    , geolocation_state
    from {{ source ('olist_stores_br', 'geolocation') }}
)

select * from geolocation