select 
    order_id
    , delivery_time
from
    {{ ref('int_avg_delivery_time') }}