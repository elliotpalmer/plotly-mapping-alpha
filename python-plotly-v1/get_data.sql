select 
	aj."id",
	aj.status,
	aj."noCharge",
	aj."completedOn",
	aj.invoice_total,
	location_customer_address_longitude as lon,
	location_customer_address_latitude as lat

from servicetitan.api_jobs aj