CREATE TABLE homeequipments.country (
	country_id int4 NOT NULL,
	country_name varchar NULL,
	country_code varchar NULL,
	nat_lang_code int4 NULL,
	currency_code varchar NULL,
	CONSTRAINT country_pkey PRIMARY KEY (country_id)
);
CREATE TABLE homeequipments.warehouse (
	warehouse_id int primary KEY,
	countries_country_id int,
	country_name varchar NULL,
	country_code varchar NULL,
	warehouse_code int NULL,
	warehouse_location_code varchar null,
	item_code varchar null,
	item_qty_remaining int4 NULL,
	item_qty_consumed int4 NULL,
	item_qty_threshold int4 NULL,
	transaction_date varchar null,
	transaction_type varchar null,
	FOREIGN KEY (countries_country_id)
    REFERENCES homeequipments.country(country_id)
);