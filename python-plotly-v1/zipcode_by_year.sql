
select 
	date_part('year', aj."completedOn"::date) as year,
	location_customer_address_zip as zip,
	count(*) as jobs,
	count(case when invoice_total > 0 then 1 else null end) as sold_jobs,
	sum(invoice_total) as revenue
	
from servicetitan.api_jobs aj
 Where not "completedOn"::date is null
group by 1,2
order by revenue desc
