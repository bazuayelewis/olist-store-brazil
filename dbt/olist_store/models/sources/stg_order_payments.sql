with order_payments as (
    select 
    order_id
    , payment_sequential
    , payment_type
    , payment_installments
    , payment_value
    from {{ source ('olist_stores_br', 'order_payments') }}
)

select * from order_payments