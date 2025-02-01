
-- Use the `ref` function to select from other models

{{config(materialized = "table")}}

with filterd_data as (
    select * from {{source('public','stg_medical_data')}}
    
)

select 
    concat(channel, '_', message_id) as message_id,  -- Concatenate channel and message_id,
    date,
    extract(year from date) as year,
    extract(month from date) as month,
    extract(day from date) as day,  
    sender,
    channel,
    text  
from filterd_data
