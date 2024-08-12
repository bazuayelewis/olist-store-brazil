with sellers as (
    select 
    seller_id
    , seller_zip_code_prefix
    , seller_city
    , seller_state
    from {{ source ('olist_stores_br', 'sellers') }}
)

select * from sellers