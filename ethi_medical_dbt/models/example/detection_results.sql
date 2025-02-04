
{{ config(materialized='table') }}

select * 
from public.detection_results