
{{ config(materialized='table') }}

select * 
from public.telegram_data