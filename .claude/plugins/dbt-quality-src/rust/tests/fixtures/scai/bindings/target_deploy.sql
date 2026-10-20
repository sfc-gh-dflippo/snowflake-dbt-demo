-- =============================================================================
-- Target Deploy Script (Snowflake)
-- Database: ${E2E_TARGET_DATABASE}
-- Schema: TEST
-- =============================================================================

CREATE DATABASE IF NOT EXISTS ${E2E_TARGET_DATABASE};
CREATE SCHEMA IF NOT EXISTS ${E2E_TARGET_DATABASE}.${E2E_TARGET_SCHEMA};
USE DATABASE ${E2E_TARGET_DATABASE};

-- -----------------------------------------------------------------------------
-- 1. Table: ${E2E_TARGET_DATABASE}.${E2E_TARGET_SCHEMA}.customer_reviews
-- -----------------------------------------------------------------------------

/* <sc-table> ${E2E_TARGET_DATABASE}.${E2E_TARGET_SCHEMA}.customer_reviews </sc-table> */

CREATE OR REPLACE TABLE ${E2E_TARGET_DATABASE}.${E2E_TARGET_SCHEMA}.customer_reviews
(
	review_id INTEGER
	,customer_id INTEGER NOT NULL
	,product_id INTEGER NOT NULL
	,rating INTEGER NOT NULL
	,review_text VARCHAR(1000)
	,review_date TIMESTAMP_NTZ DEFAULT GETDATE()
	,is_verified BOOLEAN  DEFAULT false
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/18/2026",  "domain": "no-domain-provided",  "migrationid": "1gKdAR6vwXGWVHtsq6gukg==" }}'
;

INSERT INTO ${E2E_TARGET_DATABASE}.${E2E_TARGET_SCHEMA}.customer_reviews (review_id, customer_id, product_id, rating, review_text, review_date, is_verified) VALUES
(1, 101, 501, 5, 'Excellent product, highly recommend!', '2026-01-15 10:30:00', TRUE),
(2, 102, 502, 5, 'Changed my mind, this is perfect!', '2026-01-20 14:45:00', TRUE),
(3, 103, 501, 4, 'Updated: better than I initially thought.', '2026-02-01 09:15:00', FALSE),
(4, 104, 503, 5, 'Best purchase I have made this year!', '2026-02-10 16:00:00', TRUE),
(5, 105, 504, 3, 'Replacement arrived, updating my review.', '2026-02-14 11:20:00', TRUE),
(8, 108, 503, 5, 'Amazing quality, would buy again.', '2026-03-05 17:45:00', TRUE),
(10, 110, 505, 4, 'Pretty good overall, minor issues.', '2026-03-15 12:30:00', TRUE),
(55, 111, 506, 5, 'Fantastic product, exceeded expectations!', '2026-03-18 21:09:30', FALSE),
(56, 112, 507, 3, 'Average quality, nothing special.', '2026-03-18 21:09:31', FALSE),
(57, 113, 508, 4, 'Great value for money.', '2026-03-18 21:09:33', FALSE),
(61, 111, 506, 5, 'Fantastic product, exceeded expectations!', '2026-03-18 21:19:34', FALSE),
(62, 112, 507, 3, 'Average quality, nothing special.', '2026-03-18 21:19:35', FALSE),
(63, 113, 508, 4, 'Great value for money.', '2026-03-18 21:19:37', FALSE);

-- -----------------------------------------------------------------------------
-- 2. Procedure: ${E2E_TARGET_DATABASE}.${E2E_TARGET_SCHEMA}.insert_customer_review
-- -----------------------------------------------------------------------------

/* <sc-procedure> ${E2E_TARGET_DATABASE}.${E2E_TARGET_SCHEMA}.insert_customer_review </sc-procedure> */

CREATE OR REPLACE PROCEDURE ${E2E_TARGET_DATABASE}.${E2E_TARGET_SCHEMA}.insert_customer_review (
p_customer_id integer
,p_product_id integer
,p_rating integer
,p_review_text VARCHAR)
RETURNS TABLE(ROWS_AFFECTED INTEGER)
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/18/2026",  "domain": "no-domain-provided",  "migrationid": "1gKdAR6vwXGWVHtsq6gukg==" }}'
EXECUTE AS CALLER
AS $$
DECLARE
    res RESULTSET;
    affected INTEGER;
BEGIN
    INSERT INTO ${E2E_TARGET_SCHEMA}.customer_reviews (customer_id, product_id, rating, review_text, review_date, is_verified)
    VALUES (:p_customer_id, : p_product_id, : p_rating, : p_review_text, GETDATE(), FALSE);
    affected := SQLROWCOUNT;
    res := (SELECT :affected AS ROWS_AFFECTED);
    RETURN TABLE(res);
END;
$$;

-- -----------------------------------------------------------------------------
-- 3. Procedure: ${E2E_TARGET_DATABASE}.${E2E_TARGET_SCHEMA}.update_customer_review
-- -----------------------------------------------------------------------------

/* <sc-procedure> ${E2E_TARGET_DATABASE}.${E2E_TARGET_SCHEMA}.update_customer_review </sc-procedure> */

CREATE OR REPLACE PROCEDURE ${E2E_TARGET_DATABASE}.${E2E_TARGET_SCHEMA}.update_customer_review (
p_review_id integer
,p_rating integer
,p_review_text VARCHAR)
RETURNS TABLE(ROWS_AFFECTED INTEGER)
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/18/2026",  "domain": "no-domain-provided",  "migrationid": "1gKdAR6vwXGWVHtsq6gukg==" }}'
EXECUTE AS CALLER
AS $$
DECLARE
    res RESULTSET;
    affected INTEGER;
BEGIN
    UPDATE ${E2E_TARGET_SCHEMA}.customer_reviews
     SET rating = : p_rating,
        review_text = : p_review_text
    WHERE review_id = : p_review_id;
    affected := SQLROWCOUNT;
    res := (SELECT :affected AS ROWS_AFFECTED);
    RETURN TABLE(res);
END;
$$;

-- -----------------------------------------------------------------------------
-- 4. Procedure: ${E2E_TARGET_DATABASE}.${E2E_TARGET_SCHEMA}.delete_customer_review
-- -----------------------------------------------------------------------------

/* <sc-procedure> ${E2E_TARGET_DATABASE}.${E2E_TARGET_SCHEMA}.delete_customer_review </sc-procedure> */

-- RETURNS VARCHAR (NOT TABLE) — Snowflake SQL Script always emits a 1-row,
-- 1-column status payload {DELETE_CUSTOMER_REVIEW: NULL} from CALL on
-- non-RETURNS-TABLE procs.  Pairs with the silent SQL Server source proc to
-- exercise the implicit-return short-circuit in InMemoryResultComparator on
-- a non-Teradata source dialect (Teradata exercises it naturally; Redshift
-- forces validate=false on CALL so the path is unreachable there).
CREATE OR REPLACE PROCEDURE ${E2E_TARGET_DATABASE}.${E2E_TARGET_SCHEMA}.delete_customer_review (
p_review_id integer)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/18/2026",  "domain": "no-domain-provided",  "migrationid": "1gKdAR6vwXGWVHtsq6gukg==" }}'
EXECUTE AS CALLER
AS $$
BEGIN
    DELETE FROM ${E2E_TARGET_SCHEMA}.customer_reviews
    WHERE review_id = :p_review_id;
END;
$$;
