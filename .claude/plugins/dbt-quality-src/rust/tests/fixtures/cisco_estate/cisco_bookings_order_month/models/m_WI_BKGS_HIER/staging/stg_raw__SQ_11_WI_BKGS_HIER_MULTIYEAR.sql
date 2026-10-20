{{ config(
    tags=['m_WI_BKGS_HIER']
) }}
{{ config(materialized='table') }}
-- Self-referencing table(s): 'WI_BKGS_HIER3' used as both source and target in this mapping.
-- Materialized as TABLE to snapshot source data before the target model overwrites it.
SELECT
   BM.FISCAL_YEAR_WEEK_NUM_INT,
   BM.FISCAL_YEAR_MTH_NUMBER_INT,
   BM.SALES_TERRITORY_KEY,
   BM.PRODUCT_KEY,
   BM.SALES_ORDER_LINE_KEY,
   BM.BILL_TO_CUSTOMER_KEY,
   BM.END_CUSTOMER_KEY,
   BM.SOLD_TO_CUSTOMER_KEY,
   BM.SHIP_TO_CUSTOMER_KEY,
   BM.IDE_ADJUSTMENT_CODE,
   BM.ISO_COUNTRY_CODE,
   BM.PRODUCT_TYPE DV_PRODUCT_TYPE,
   'MULTIYEAR' DV_PNL_BOOK_NET_COST_TYPE,
   CASE
      WHEN RTRIM(BM.BK_SERVICE_CATEGORY_ID) IN (COLLATE('ADVANCED SERVICES', 'en-ci-rtrim'))
         THEN CASE
            WHEN RTRIM(BM.ACCOUNT_NAME) IN (COLLATE('AS SUBSCRIPTION', 'en-ci-rtrim'))
               THEN CASE
                  WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('ERP', 'en-ci-rtrim'), COLLATE('XAAS', 'en-ci-rtrim'))
                     THEN CASE
                        WHEN RTRIM(UPPER(BM.CANCEL_CODE)) IN (COLLATE('LOST ORDER', 'en-ci-rtrim'))
                           THEN CASE
                              WHEN BM.DV_CISCO_BOOKED_DT < FY.FISCAL_MONTH_START_DATE
                                 THEN 'AS-S MY Prior period DeBookings'
                              ELSE 'AS-S MY Current DeBookings'
                           END
                        ELSE 'AS-S MY Base Current Bookings'
                     END
                  WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('AR', 'en-ci-rtrim'))
                     THEN CASE
                        WHEN RTRIM(TRIM(UPPER(BM.ADJUSTMENT_CODE))) IN (COLLATE('CM', 'en-ci-rtrim'), COLLATE('CM_REVENUE', 'en-ci-rtrim'))
                        AND COLLATE(TRIM(UPPER(BM.SALES_ORDER_CATEGORY_TYPE)), 'en-ci-rtrim') <> 'RETURN'
                           THEN 'AS-S MY Bookings Credit Memos'
                        WHEN RTRIM(TRIM(UPPER(BM.ADJUSTMENT_CODE))) IN (COLLATE('CM', 'en-ci-rtrim'), COLLATE('CM_REVENUE', 'en-ci-rtrim'))
                        AND COLLATE(TRIM(UPPER(BM.SALES_ORDER_CATEGORY_TYPE)), 'en-ci-rtrim') = 'RETURN'
                           THEN 'AS-S MY Bookings RMA'
                        WHEN RTRIM(TRIM(UPPER(BM.ADJUSTMENT_CODE))) IN (COLLATE('REVENUE TRANSFER AUTO - MANUAL', 'en-ci-rtrim'))
                           THEN 'AS-S MY Bookings Revenue Transfer Auto - Manual'
                        WHEN RTRIM(TRIM(UPPER(BM.ADJUSTMENT_CODE))) IN (COLLATE('REVENUE TRANSFER AUTO - SYSTEM', 'en-ci-rtrim'))
                           THEN 'AS-S MY Bookings Revenue Transfer Auto - System'
                        ELSE 'AS-S MY Bookings Not Mapped AR'
                     END
                  WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('SLS_ADJ', 'en-ci-rtrim'))
                     THEN CASE
                        WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('RMKT1', 'en-ci-rtrim'), COLLATE('RMKT', 'en-ci-rtrim'))
                           THEN 'AS-S MY Bookings Refurbished Orders'
                        WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('MITG-RES', 'en-ci-rtrim'), COLLATE('RR-RES', 'en-ci-rtrim'))
                           THEN 'AS-S MY Bookings Reserve'
                        WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('MITG-REL', 'en-ci-rtrim'), COLLATE('RR-REL', 'en-ci-rtrim'))
                           THEN 'AS-S MY Bookings Release'
                        WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('MGMT-RF', 'en-ci-rtrim'), COLLATE('MGMT-W', 'en-ci-rtrim'), COLLATE('MGMT-BC', 'en-ci-rtrim'), COLLATE('MGMT-AE', 'en-ci-rtrim'), COLLATE('MGMT-M', 'en-ci-rtrim'), COLLATE('NBM-M', 'en-ci-rtrim'), COLLATE('TCCV-A', 'en-ci-rtrim'), COLLATE('TCCV-T', 'en-ci-rtrim'))
                           THEN 'AS-S MY Bookings Management Adjustment'
                        WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('RB', 'en-ci-rtrim'), COLLATE('VIP', 'en-ci-rtrim'), COLLATE('RB1', 'en-ci-rtrim'), COLLATE('VOLREB', 'en-ci-rtrim'))
                           THEN 'AS-S MY Bookings Rebate Adjustment'
                        WHEN (COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE 'AC-%'
                        OR RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('MS-EMS', 'en-ci-rtrim'), COLLATE('MS-NS', 'en-ci-rtrim'), COLLATE('MS-PPS', 'en-ci-rtrim')))
                           THEN 'AS-S MY Bookings Acquisition Adjustment'
                        WHEN ((COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE 'CLD-%')
                        OR (COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE 'LL-%')
                        OR (RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('LCLD-PVT', 'en-ci-rtrim'))))
                           THEN 'AS-S MY Bookings Cloud Adjustment'
                        WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('FMV-%')
                           THEN 'AS-S MY Bookings FMV Adjustment'
                        WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('SBP-%')
                           THEN 'AS-S MY Bookings SBP Adjustment'
                        WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('MS-SMS%')
                           THEN 'AS-S MY Bookings Managed Services Adjustment'
                        WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('SS-%')
                           THEN 'AS-S MY Bookings Solution Selling Adjustment'
                        WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('XAAS-%')
                           THEN 'AS-S MY Bookings Xaas Adjustment'
                        WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('1C_BOOK', 'en-ci-rtrim'), COLLATE('1C_REV', 'en-ci-rtrim'), COLLATE('BKG-CR', 'en-ci-rtrim'), COLLATE('EMN', 'en-ci-rtrim'), COLLATE('MULTINAT', 'en-ci-rtrim'))
                           THEN 'AS-S MY Bookings Other Adjustment'
                        ELSE 'AS-S MY Bookings Not Mapped Adjustment'
                     END
                  WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('POS', 'en-ci-rtrim'))
                     THEN 'AS-S MY Base Bookings Net POS'
                  WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('POS_ADJ', 'en-ci-rtrim'))
                     THEN 'AS-S MY Base Bookings POS Adjustments'
                  ELSE 'AS-S MY Base Not Mapped Bookings Net'
               END
            WHEN RTRIM(BM.ACCOUNT_NAME) IN (COLLATE('AS TRANSACTION', 'en-ci-rtrim'), COLLATE('AS ADVISORY', 'en-ci-rtrim'), COLLATE('AS FIXED', 'en-ci-rtrim'))
               THEN CASE
                  WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('ERP', 'en-ci-rtrim'), COLLATE('XAAS', 'en-ci-rtrim'))
                     THEN CASE
                        WHEN RTRIM(UPPER(BM.CANCEL_CODE)) IN (COLLATE('LOST ORDER', 'en-ci-rtrim'))
                           THEN CASE
                              WHEN BM.DV_CISCO_BOOKED_DT < FY.FISCAL_MONTH_START_DATE
                                 THEN 'AS-T MY Prior period DeBookings'
                              ELSE 'AS-T MY Current DeBookings'
                           END
                        ELSE 'AS-T MY Base Current Bookings'
                     END
                  WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('AR', 'en-ci-rtrim'))
                     THEN CASE
                        WHEN RTRIM(TRIM(UPPER(BM.ADJUSTMENT_CODE))) IN (COLLATE('CM', 'en-ci-rtrim'), COLLATE('CM_REVENUE', 'en-ci-rtrim'))
                        AND COLLATE(TRIM(UPPER(BM.SALES_ORDER_CATEGORY_TYPE)), 'en-ci-rtrim') <> 'RETURN'
                           THEN 'AS-T MY Bookings Credit Memos'
                        WHEN RTRIM(TRIM(UPPER(BM.ADJUSTMENT_CODE))) IN (COLLATE('CM', 'en-ci-rtrim'), COLLATE('CM_REVENUE', 'en-ci-rtrim'))
                        AND COLLATE(TRIM(UPPER(BM.SALES_ORDER_CATEGORY_TYPE)), 'en-ci-rtrim') = 'RETURN'
                           THEN 'AS-T MY Bookings RMA'
                        WHEN RTRIM(TRIM(UPPER(BM.ADJUSTMENT_CODE))) IN (COLLATE('REVENUE TRANSFER AUTO - MANUAL', 'en-ci-rtrim'))
                           THEN 'AS-T MY Bookings Revenue Transfer Auto - Manual'
                        WHEN RTRIM(TRIM(UPPER(BM.ADJUSTMENT_CODE))) IN (COLLATE('REVENUE TRANSFER AUTO - SYSTEM', 'en-ci-rtrim'))
                           THEN 'AS-T MY Bookings Revenue Transfer Auto - System'
                        ELSE 'AS-T MY Bookings Not Mapped AR'
                     END
                  WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('SLS_ADJ', 'en-ci-rtrim'))
                     THEN CASE
                        WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('RMKT1', 'en-ci-rtrim'), COLLATE('RMKT', 'en-ci-rtrim'))
                           THEN 'AS-T MY Bookings Refurbished Orders'
                        WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('MITG-RES', 'en-ci-rtrim'), COLLATE('RR-RES', 'en-ci-rtrim'))
                           THEN 'AS-T MY Bookings Reserve'
                        WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('MITG-REL', 'en-ci-rtrim'), COLLATE('RR-REL', 'en-ci-rtrim'))
                           THEN 'AS-T MY Bookings Release'
                        WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('MGMT-RF', 'en-ci-rtrim'), COLLATE('MGMT-W', 'en-ci-rtrim'), COLLATE('MGMT-BC', 'en-ci-rtrim'), COLLATE('MGMT-AE', 'en-ci-rtrim'), COLLATE('MGMT-M', 'en-ci-rtrim'), COLLATE('NBM-M', 'en-ci-rtrim'), COLLATE('TCCV-A', 'en-ci-rtrim'), COLLATE('TCCV-T', 'en-ci-rtrim'))
                           THEN 'AS-T MY Bookings Management Adjustment'
                        WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('RB', 'en-ci-rtrim'), COLLATE('VIP', 'en-ci-rtrim'), COLLATE('RB1', 'en-ci-rtrim'), COLLATE('VOLREB', 'en-ci-rtrim'))
                           THEN 'AS-T MY Bookings Rebate Adjustment'
                        WHEN (COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE 'AC-%'
                        OR RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('MS-EMS', 'en-ci-rtrim'), COLLATE('MS-NS', 'en-ci-rtrim'), COLLATE('MS-PPS', 'en-ci-rtrim')))
                           THEN 'AS-T MY Bookings Acquisition Adjustment'
                        WHEN ((COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE 'CLD-%')
                        OR (COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE 'LL-%')
                        OR (RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('LCLD-PVT', 'en-ci-rtrim'))))
                           THEN 'AS-T MY Bookings Cloud Adjustment'
                        WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('FMV-%')
                           THEN 'AS-T MY Bookings FMV Adjustment'
                        WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('SBP-%')
                           THEN 'AS-T MY Bookings SBP Adjustment'
                        WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('MS-SMS%')
                           THEN 'AS-T MY Bookings Managed Services Adjustment'
                        WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('SS-%')
                           THEN 'AS-T MY Bookings Solution Selling Adjustment'
                        WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('XAAS-%')
                           THEN 'AS-T MY Bookings Xaas Adjustment'
                        WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('1C_BOOK', 'en-ci-rtrim'), COLLATE('1C_REV', 'en-ci-rtrim'), COLLATE('BKG-CR', 'en-ci-rtrim'), COLLATE('EMN', 'en-ci-rtrim'), COLLATE('MULTINAT', 'en-ci-rtrim'))
                           THEN 'AS-T MY Bookings Other Adjustment'
                        ELSE 'AS-T MY Bookings Not Mapped Adjustment'
                     END
                  WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('POS', 'en-ci-rtrim'))
                     THEN 'AS-T MY Base Bookings Net POS'
                  WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('POS_ADJ', 'en-ci-rtrim'))
                     THEN 'AS-T MY Base Bookings POS Adjustments'
                  ELSE 'AS-T MY Base Not Mapped Bookings Net'
               END
            ELSE 'AS Not Mapped MY Bookings'
         END
      /*WHEN BM.ACCOUNT_NAME IN ('TECHNICAL SUPPORT SERVICES','REMOTE OPERATIONS SERVICES')*/
      WHEN RTRIM(BM.BK_SERVICE_CATEGORY_ID) IN (COLLATE('TECHNICAL SUPPORT SERVICES', 'en-ci-rtrim'), COLLATE('REMOTE OPERATIONS SERVICES', 'en-ci-rtrim'))
         THEN CASE
            WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('ERP', 'en-ci-rtrim'), COLLATE('XAAS', 'en-ci-rtrim'))
               THEN CASE
                  WHEN RTRIM(UPPER(BM.CANCEL_CODE)) IN (COLLATE('LOST ORDER', 'en-ci-rtrim'))
                     THEN CASE
                        WHEN BM.DV_CISCO_BOOKED_DT < FY.FISCAL_MONTH_START_DATE
                           THEN 'TSS MY Prior period DeBookings'
                        ELSE 'TSS MY Current DeBookings'
                     END
                  ELSE 'TSS MY Base Current Bookings'
               END
            WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('AR', 'en-ci-rtrim'))
               THEN CASE
                  WHEN RTRIM(TRIM(UPPER(BM.ADJUSTMENT_CODE))) IN (COLLATE('CM', 'en-ci-rtrim'), COLLATE('CM_REVENUE', 'en-ci-rtrim'))
                  AND COLLATE(TRIM(UPPER(BM.SALES_ORDER_CATEGORY_TYPE)), 'en-ci-rtrim') <> 'RETURN'
                     THEN 'TSS MY Bookings Credit Memos'
                  WHEN RTRIM(TRIM(UPPER(BM.ADJUSTMENT_CODE))) IN (COLLATE('CM', 'en-ci-rtrim'), COLLATE('CM_REVENUE', 'en-ci-rtrim'))
                  AND COLLATE(TRIM(UPPER(BM.SALES_ORDER_CATEGORY_TYPE)), 'en-ci-rtrim') = 'RETURN'
                     THEN 'TSS MY Bookings RMA'
                  WHEN RTRIM(TRIM(UPPER(BM.ADJUSTMENT_CODE))) IN (COLLATE('REVENUE TRANSFER AUTO - MANUAL', 'en-ci-rtrim'))
                     THEN 'TSS MY Bookings Revenue Transfer Auto - Manual'
                  WHEN RTRIM(TRIM(UPPER(BM.ADJUSTMENT_CODE))) IN (COLLATE('REVENUE TRANSFER AUTO - SYSTEM', 'en-ci-rtrim'))
                     THEN 'TSS MY Bookings Revenue Transfer Auto - System'
                  ELSE 'TSS MY Bookings Not Mapped AR'
               END
            WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('SLS_ADJ', 'en-ci-rtrim'))
               THEN CASE
                  WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('RMKT1', 'en-ci-rtrim'), COLLATE('RMKT', 'en-ci-rtrim'))
                     THEN 'TSS MY Bookings Refurbished Orders'
                  WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('MITG-RES', 'en-ci-rtrim'), COLLATE('RR-RES', 'en-ci-rtrim'))
                     THEN 'TSS MY Bookings Reserve'
                  WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('MITG-REL', 'en-ci-rtrim'), COLLATE('RR-REL', 'en-ci-rtrim'))
                     THEN 'TSS MY Bookings Release'
                  WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('MGMT-RF', 'en-ci-rtrim'), COLLATE('MGMT-W', 'en-ci-rtrim'), COLLATE('MGMT-BC', 'en-ci-rtrim'), COLLATE('MGMT-AE', 'en-ci-rtrim'), COLLATE('MGMT-M', 'en-ci-rtrim'), COLLATE('NBM-M', 'en-ci-rtrim'), COLLATE('TCCV-A', 'en-ci-rtrim'), COLLATE('TCCV-T', 'en-ci-rtrim'))
                     THEN 'TSS MY Bookings Management Adjustment'
                  WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('RB', 'en-ci-rtrim'), COLLATE('VIP', 'en-ci-rtrim'), COLLATE('RB1', 'en-ci-rtrim'), COLLATE('VOLREB', 'en-ci-rtrim'))
                     THEN 'TSS MY Bookings Rebate Adjustment'
                  WHEN (COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE 'AC-%'
                  OR RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('MS-EMS', 'en-ci-rtrim'), COLLATE('MS-NS', 'en-ci-rtrim'), COLLATE('MS-PPS', 'en-ci-rtrim')))
                     THEN 'TSS MY Bookings Acquisition Adjustment'
                  WHEN ((COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE 'CLD-%')
                  OR (COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE 'LL-%')
                  OR (RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('LCLD-PVT', 'en-ci-rtrim'))))
                     THEN 'TSS MY Bookings Cloud Adjustment'
                  WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('FMV-%')
                     THEN 'TSS MY Bookings FMV Adjustment'
                  WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('SBP-%')
                     THEN 'TSS MY Bookings SBP Adjustment'
                  WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('MS-SMS%')
                     THEN 'TSS MY Bookings Managed Services Adjustment'
                  WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('SS-%')
                     THEN 'TSS MY Bookings Solution Selling Adjustment'
                  WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('XAAS-%')
                     THEN 'TSS MY Bookings Xaas Adjustment'
                  WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('1C_BOOK', 'en-ci-rtrim'), COLLATE('1C_REV', 'en-ci-rtrim'), COLLATE('BKG-CR', 'en-ci-rtrim'), COLLATE('EMN', 'en-ci-rtrim'), COLLATE('MULTINAT', 'en-ci-rtrim'))
                     THEN 'TSS MY Bookings Other Adjustment'
                  ELSE 'TSS MY Bookings Not Mapped Adjustment'
               END
            WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('POS', 'en-ci-rtrim'))
               THEN 'TSS MY Base Bookings Net POS'
            WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('POS_ADJ', 'en-ci-rtrim'))
               THEN 'TSS MY Base Bookings POS Adjustments'
            ELSE 'TSS MY Base Not Mapped Bookings Net'
         END
      ELSE 'Service Not Mapped MY Bookings Net'
   END AS DV_BOOKINGS_LINE_ITEM_NAME,
   SUM(BM.MULTIYEAR_AMT) BOOKINGS_AMOUNT,
   'BOOKINGS' DV_BOOKINGS_OR_COGS_TYPE_CD,
   BM.DEAL_SS_CD,
   BM.DV_DEAL_ID,
   /*BELOW 3 COLUMNS ADDED FOR Q3FY17 - RO PROJECT */
   BM.XCAT_FLG,
   BM.BK_OFFER_TYPE_NAME,
   BM.RECURRING_OFFER_FLG,
   BM.ELA_FLG,
   BM.DV_RECURRING_OFFER_CD,
   BM.DV_FMV_FLG,
   BM.ADJUSTMENT_CODE,
   BM.ACQUISITION_ORDER_ORIGIN_CD,
   BM.ACQUISITION_ROLE
FROM
   {{ var('m_WI_BKGS_HIER_STGDB') }}.WI_BKGS_HIER_SRVC_MY BM
   INNER JOIN
      {{ var('m_WI_BKGS_HIER_COMREFVWDB') }}.R_FISCAL_MONTH_TO_YEAR FY
      ON BM.FISCAL_YEAR_MTH_NUMBER_INT = FY.FISCAL_YEAR_MONTH_INT
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