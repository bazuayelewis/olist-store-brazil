with orders as (
    select 
    order_id
    , customer_id
    , order_status
    , cast (order_purchase_datetime as datetime) as order_purchase_datetime
    , cast (order_approved_at as datetime) as order_approved_at
    , cast (order_delivered_carrier_date as datetime) as order_delivered_carrier_date
    , cast (order_delivered_customer_date as datetime) as order_delivered_customer_date
    , cast (order_estimated_delivery_date as datetime) as order_estimated_delivery_date
    from {{ source ('olist_stores_br', 'orders') }}
)

select * from orders