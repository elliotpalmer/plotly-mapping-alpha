select 
	aj."id",
	aj.status,
	aj."noCharge",
	aj."completedOn"::date,
	aj.type_name,
	aj.invoice_total,
	location_customer_address_longitude as lon,
	location_customer_address_latitude as lat,
	location_customer_address_zip as zip

from servicetitan.api_jobs aj;