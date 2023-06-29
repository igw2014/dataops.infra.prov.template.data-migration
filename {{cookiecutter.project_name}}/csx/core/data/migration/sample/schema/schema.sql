CREATE TABLE jcbdevschema.country (
	country_id int4 NOT NULL,
	country_name varchar NULL,
	country_code varchar NULL,
	nat_lang_code int4 NULL,
	currency_code varchar NULL,
	CONSTRAINT country_pkey PRIMARY KEY (country_id)
);
CREATE TABLE jcbdevschema.employment_jobs (
	hr_job_id int primary KEY,
	countries_country_id int,
	country_name varchar NULL,
	country_code varchar NULL,
	nat_lang_code int NULL,
	currency_code varchar null,
	FOREIGN KEY (countries_country_id)
    REFERENCES jcbdevschema.country(country_id)
);