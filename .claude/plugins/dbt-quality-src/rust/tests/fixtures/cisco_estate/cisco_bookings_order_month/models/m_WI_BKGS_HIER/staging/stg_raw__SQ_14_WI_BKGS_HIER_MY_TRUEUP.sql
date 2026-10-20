{{ config(
    tags=['m_WI_BKGS_HIER']
) }}
{{ config(materialized='table') }}
-- Self-referencing table(s): 'WI_BKGS_HIER8' used as both source and target in this mapping.
-- Materialized as TABLE to snapshot source data before the target model overwrites it.
SELECT
   FISCAL_YEAR_WEEK_NUM_INT,
   FISCAL_YEAR_MTH_NUMBER_INT,
   SALES_TERRITORY_KEY,
   PRODUCT_KEY,
   SALES_ORDER_LINE_KEY,
   BILL_TO_CUSTOMER_KEY,
   END_CUSTOMER_KEY,
   SOLD_TO_CUSTOMER_KEY,
   SHIP_TO_CUSTOMER_KEY,
   IDE_ADJUSTMENT_CODE,
   ISO_COUNTRY_CODE,
   PRODUCT_TYPE DV_PRODUCT_TYPE,
   DV_SRVC_BOOKINGS_TYPE DV_PNL_BOOK_NET_COST_TYPE,
   CASE
      WHEN COLLATE(DV_SRVC_BOOKINGS_TYPE, 'en-ci-rtrim') = 'MY_TRUEUP'
      AND RTRIM(Account_name) IN (COLLATE('AS SUBSCRIPTION', 'en-ci-rtrim'))
         THEN 'AS-S MY True-up Bookings'
      WHEN COLLATE(DV_SRVC_BOOKINGS_TYPE, 'en-ci-rtrim') = 'MY_TRUEUP'
      AND RTRIM(Account_name) IN (COLLATE('AS TRANSACTION', 'en-ci-rtrim'), COLLATE('AS ADVISORY', 'en-ci-rtrim'), COLLATE('AS FIXED', 'en-ci-rtrim'))
         THEN 'AS-T MY True-up Bookings'
      WHEN COLLATE(DV_SRVC_BOOKINGS_TYPE, 'en-ci-rtrim') = 'MY_TRUEUP'
      AND RTRIM(Account_name) IN (COLLATE('TECHNICAL SUPPORT SERVICES', 'en-ci-rtrim'), COLLATE('REMOTE OPERATIONS SERVICES', 'en-ci-rtrim'))
         THEN 'TSS MY True-up Bookings'
   END DV_BOOKINGS_LINE_ITEM_NAME,
   SUM(TRUEUP_AMT) BOOKINGS_AMOUNT,
   'BOOKINGS' DV_BOOKINGS_OR_COGS_TYPE_CD,
   DEAL_SS_CD,
   DV_DEAL_ID,
   /*BELOW 4 COLUMNS ADDED FOR Q3FY17 - RO PROJECT */
   XCAT_FLG,
   BK_OFFER_TYPE_NAME,
   RECURRING_OFFER_FLG,
   ELA_FLG,
   DV_RECURRING_OFFER_CD,
   DV_FMV_FLG,
   ADJUSTMENT_CODE,
   ACQUISITION_ORDER_ORIGIN_CD,
   ACQUISITION_ROLE
FROM
   {{ var('m_WI_BKGS_HIER_STGDB') }}.WI_BKGS_HIER_SRVC_TRUEUP
WHERE
   COLLATE(DV_SRVC_BOOKINGS_TYPE, 'en-ci-rtrim') = 'MY_TRUEUP'
GROUP BY
   1,
   2,
   3,
   4,
   5,
   6,
   7,
   8,
   9,
   10,
   11,
   12,
   13,
   14,
   16,
   17,
   18,
   19,
   20,
   21,
   22,
   23,
   24,
   25,
   26,
   27