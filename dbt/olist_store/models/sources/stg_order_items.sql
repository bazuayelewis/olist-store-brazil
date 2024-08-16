with order_items as (
    select 
    order_id
    , order_item_id
    , product_id
    , seller_id
    , cast (shipping_limit_date as datetime) as shipping_limit_date
    , price
    , freight_value
    from {{ source ('olist_stores_br', 'order_items') }}
)

select * from order_items