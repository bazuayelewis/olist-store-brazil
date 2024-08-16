with source_products as (
    select 
    product_id
    , p.product_category_name
    , product_name_lenght as product_name_length
    , product_description_lenght as product_description_length
    , product_photos_qty
    , product_weight_g
    , product_length_cm
    , product_height_cm
    , product_width_cm
    , bp.product_category_name_english as product_category_name_english
    from {{ source ('olist_stores_br', 'products') }} p
    left join {{ ref('base_product_category_name_translation') }} bp 
    on p.product_category_name = bp.product_category_name
),
products as (
    select 
    product_id
    , case 
        when product_category_name_english is null 
        then product_category_name 
        else product_category_name_english 
        end as product_category_name
    , product_name_length
    , product_description_length
    , product_photos_qty
    , product_weight_g
    , product_length_cm
    , product_height_cm
    , product_width_cm
    from source_products
)

select * from products