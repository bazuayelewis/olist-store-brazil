with sales as (
    select
        o.order_id
        , product_category_name
        , order_item_id
        , price
    from
        {{ ref('stg_orders') }} o
    join
        {{ ref('stg_order_items') }} oi
    on
        o.order_id = oi.order_id
    join
        {{ ref('stg_products') }} p
    on
        oi.product_id = p.product_id
)
select
    product_category_name
    , sum(price*order_item_id) as total_sales
from
    sales
group by
    product_category_name
order by 
    total_sales desc