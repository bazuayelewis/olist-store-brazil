with delivered_orders as (
    select 
        order_id
        , (order_delivered_carrier_date - order_purchase_timestamp) as delivery_time 
    from 
        {{ ref('stg_orders') }} 
    where 
        order_delivered_carrier_date is not null and order_status = 'delivered'
    )
select 
    order_id
    , delivery_time
from 
    delivered_orders
order by 
    order_id