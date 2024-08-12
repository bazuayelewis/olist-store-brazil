with states_orders as (
    select 
        c.customer_id
        , customer_state 
    from 
        {{ ref('stg_orders') }} o
    join 
        {{ ref('stg_customers') }} c 
    on 
        c.customer_id = o.customer_id 
)
select 
    customer_state
    , count(customer_id) as total_orders 
from 
    states_orders 
group by 
    customer_state
order by 
    total_orders desc