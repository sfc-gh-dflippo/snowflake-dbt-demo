{{ config(
    tags=['m_WI_BKGS_HIER']
) }}
{{ config(materialized='table') }}
-- Self-referencing table(s): 'WI_BKGS_HIER6' used as both source and target in this mapping.
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
   'ANNUITY' DV_PNL_BOOK_NET_COST_TYPE,
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
                                 THEN 'AS-S Annuity Prior period DeBookings'
                              ELSE 'AS-S Annuity Current DeBookings'
                           END
                        ELSE 'AS-S Annuity Base Current Bookings'
                     END
                  WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('AR', 'en-ci-rtrim'))
                     THEN CASE
                        WHEN RTRIM(TRIM(UPPER(BM.ADJUSTMENT_CODE))) IN (COLLATE('CM', 'en-ci-rtrim'), COLLATE('CM_REVENUE', 'en-ci-rtrim'))
                        AND COLLATE(TRIM(UPPER(BM.SALES_ORDER_CATEGORY_TYPE)), 'en-ci-rtrim') <> 'RETURN'
                           THEN 'AS-S Annuity Bookings Credit Memos'
                        WHEN RTRIM(TRIM(UPPER(BM.ADJUSTMENT_CODE))) IN (COLLATE('CM', 'en-ci-rtrim'), COLLATE('CM_REVENUE', 'en-ci-rtrim'))
                        AND COLLATE(TRIM(UPPER(BM.SALES_ORDER_CATEGORY_TYPE)), 'en-ci-rtrim') = 'RETURN'
                           THEN 'AS-S Annuity Bookings RMA'
                        WHEN RTRIM(TRIM(UPPER(BM.ADJUSTMENT_CODE))) IN (COLLATE('REVENUE TRANSFER AUTO - MANUAL', 'en-ci-rtrim'))
                           THEN 'AS-S Annuity Bookings Revenue Transfer Auto - Manual'
                        WHEN RTRIM(TRIM(UPPER(BM.ADJUSTMENT_CODE))) IN (COLLATE('REVENUE TRANSFER AUTO - SYSTEM', 'en-ci-rtrim'))
                           THEN 'AS-S Annuity Bookings Revenue Transfer Auto - System'
                        ELSE 'AS-S Annuity Bookings Not Mapped AR'
                     END
                  WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('SLS_ADJ', 'en-ci-rtrim'))
                     THEN CASE
                        WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('RMKT1', 'en-ci-rtrim'), COLLATE('RMKT', 'en-ci-rtrim'))
                           THEN 'AS-S Annuity Bookings Refurbished Orders'
                        WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('MITG-RES', 'en-ci-rtrim'), COLLATE('RR-RES', 'en-ci-rtrim'))
                           THEN 'AS-S Annuity Bookings Reserve'
                        WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('MITG-REL', 'en-ci-rtrim'), COLLATE('RR-REL', 'en-ci-rtrim'))
                           THEN 'AS-S Annuity Bookings Release'
                        WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('MGMT-RF', 'en-ci-rtrim'), COLLATE('MGMT-W', 'en-ci-rtrim'), COLLATE('MGMT-BC', 'en-ci-rtrim'), COLLATE('MGMT-AE', 'en-ci-rtrim'), COLLATE('MGMT-M', 'en-ci-rtrim'), COLLATE('NBM-M', 'en-ci-rtrim'), COLLATE('TCCV-A', 'en-ci-rtrim'), COLLATE('TCCV-T', 'en-ci-rtrim'))
                           THEN 'AS-S Annuity Bookings Management Adjustment'
                        WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('RB', 'en-ci-rtrim'), COLLATE('VIP', 'en-ci-rtrim'), COLLATE('RB1', 'en-ci-rtrim'), COLLATE('VOLREB', 'en-ci-rtrim'))
                           THEN 'AS-S Annuity Bookings Rebate Adjustment'
                        WHEN (COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE 'AC-%'
                        OR RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('MS-EMS', 'en-ci-rtrim'), COLLATE('MS-NS', 'en-ci-rtrim'), COLLATE('MS-PPS', 'en-ci-rtrim')))
                           THEN 'AS-S Annuity Bookings Acquisition Adjustment'
                        WHEN ((COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE 'CLD-%')
                        OR (COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE 'LL-%')
                        OR (RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('LCLD-PVT', 'en-ci-rtrim'))))
                           THEN 'AS-S Annuity Bookings Cloud Adjustment'
                        WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('FMV-%')
                           THEN 'AS-S Annuity Bookings FMV Adjustment'
                        WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('SBP-%')
                           THEN 'AS-S Annuity Bookings SBP Adjustment'
                        WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('MS-SMS%')
                           THEN 'AS-S Annuity Bookings Managed Services Adjustment'
                        WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('SS-%')
                           THEN 'AS-S Annuity Bookings Solution Selling Adjustment'
                        WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('XAAS-%')
                           THEN 'AS-S Annuity Bookings Xaas Adjustment'
                        WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('1C_BOOK', 'en-ci-rtrim'), COLLATE('1C_REV', 'en-ci-rtrim'), COLLATE('BKG-CR', 'en-ci-rtrim'), COLLATE('EMN', 'en-ci-rtrim'), COLLATE('MULTINAT', 'en-ci-rtrim'))
                           THEN 'AS-S Annuity Bookings Other Adjustment'
                        ELSE 'AS-S Annuity Bookings Not Mapped Adjustment'
                     END
                  WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('POS', 'en-ci-rtrim'))
                     THEN 'AS-S Annuity Base Bookings Net POS'
                  WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('POS_ADJ', 'en-ci-rtrim'))
                     THEN 'AS-S Annuity Base Bookings POS Adjustments'
                  ELSE 'AS-S Annuity Base Not Mapped Bookings Net'
               END
            WHEN RTRIM(BM.ACCOUNT_NAME) IN (COLLATE('AS TRANSACTION', 'en-ci-rtrim'), COLLATE('AS ADVISORY', 'en-ci-rtrim'), COLLATE('AS FIXED', 'en-ci-rtrim'))
               THEN CASE
                  WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('ERP', 'en-ci-rtrim'), COLLATE('XAAS', 'en-ci-rtrim'))
                     THEN CASE
                        WHEN RTRIM(UPPER(BM.CANCEL_CODE)) IN (COLLATE('LOST ORDER', 'en-ci-rtrim'))
                           THEN CASE
                              WHEN BM.DV_CISCO_BOOKED_DT < FY.FISCAL_MONTH_START_DATE
                                 THEN 'AS-T Annuity Prior period DeBookings'
                              ELSE 'AS-T Annuity Current DeBookings'
                           END
                        ELSE 'AS-T Annuity Base Current Bookings'
                     END
                  WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('AR', 'en-ci-rtrim'))
                     THEN CASE
                        WHEN RTRIM(TRIM(UPPER(BM.ADJUSTMENT_CODE))) IN (COLLATE('CM', 'en-ci-rtrim'), COLLATE('CM_REVENUE', 'en-ci-rtrim'))
                        AND COLLATE(TRIM(UPPER(BM.SALES_ORDER_CATEGORY_TYPE)), 'en-ci-rtrim') <> 'RETURN'
                           THEN 'AS-T Annuity Bookings Credit Memos'
                        WHEN RTRIM(TRIM(UPPER(BM.ADJUSTMENT_CODE))) IN (COLLATE('CM', 'en-ci-rtrim'), COLLATE('CM_REVENUE', 'en-ci-rtrim'))
                        AND COLLATE(TRIM(UPPER(BM.SALES_ORDER_CATEGORY_TYPE)), 'en-ci-rtrim') = 'RETURN'
                           THEN 'AS-T Annuity Bookings RMA'
                        WHEN RTRIM(TRIM(UPPER(BM.ADJUSTMENT_CODE))) IN (COLLATE('REVENUE TRANSFER AUTO - MANUAL', 'en-ci-rtrim'))
                           THEN 'AS-T Annuity Bookings Revenue Transfer Auto - Manual'
                        WHEN RTRIM(TRIM(UPPER(BM.ADJUSTMENT_CODE))) IN (COLLATE('REVENUE TRANSFER AUTO - SYSTEM', 'en-ci-rtrim'))
                           THEN 'AS-T Annuity Bookings Revenue Transfer Auto - System'
                        ELSE 'AS-T Annuity Bookings Not Mapped AR'
                     END
                  WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('SLS_ADJ', 'en-ci-rtrim'))
                     THEN CASE
                        WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('RMKT1', 'en-ci-rtrim'), COLLATE('RMKT', 'en-ci-rtrim'))
                           THEN 'AS-T Annuity Bookings Refurbished Orders'
                        WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('MITG-RES', 'en-ci-rtrim'), COLLATE('RR-RES', 'en-ci-rtrim'))
                           THEN 'AS-T Annuity Bookings Reserve'
                        WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('MITG-REL', 'en-ci-rtrim'), COLLATE('RR-REL', 'en-ci-rtrim'))
                           THEN 'AS-T Annuity Bookings Release'
                        WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('MGMT-RF', 'en-ci-rtrim'), COLLATE('MGMT-W', 'en-ci-rtrim'), COLLATE('MGMT-BC', 'en-ci-rtrim'), COLLATE('MGMT-AE', 'en-ci-rtrim'), COLLATE('MGMT-M', 'en-ci-rtrim'), COLLATE('NBM-M', 'en-ci-rtrim'), COLLATE('TCCV-A', 'en-ci-rtrim'), COLLATE('TCCV-T', 'en-ci-rtrim'))
                           THEN 'AS-T Annuity Bookings Management Adjustment'
                        WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('RB', 'en-ci-rtrim'), COLLATE('VIP', 'en-ci-rtrim'), COLLATE('RB1', 'en-ci-rtrim'), COLLATE('VOLREB', 'en-ci-rtrim'))
                           THEN 'AS-T Annuity Bookings Rebate Adjustment'
                        WHEN (COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE 'AC-%'
                        OR RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('MS-EMS', 'en-ci-rtrim'), COLLATE('MS-NS', 'en-ci-rtrim'), COLLATE('MS-PPS', 'en-ci-rtrim')))
                           THEN 'AS-T Annuity Bookings Acquisition Adjustment'
                        WHEN ((COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE 'CLD-%')
                        OR (COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE 'LL-%')
                        OR (RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('LCLD-PVT', 'en-ci-rtrim'))))
                           THEN 'AS-T Annuity Bookings Cloud Adjustment'
                        WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('FMV-%')
                           THEN 'AS-T Annuity Bookings FMV Adjustment'
                        WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('SBP-%')
                           THEN 'AS-T Annuity Bookings SBP Adjustment'
                        WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('MS-SMS%')
                           THEN 'AS-T Annuity Bookings Managed Services Adjustment'
                        WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('SS-%')
                           THEN 'AS-T Annuity Bookings Solution Selling Adjustment'
                        WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('XAAS-%')
                           THEN 'AS-T Annuity Bookings Xaas Adjustment'
                        WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('1C_BOOK', 'en-ci-rtrim'), COLLATE('1C_REV', 'en-ci-rtrim'), COLLATE('BKG-CR', 'en-ci-rtrim'), COLLATE('EMN', 'en-ci-rtrim'), COLLATE('MULTINAT', 'en-ci-rtrim'))
                           THEN 'AS-T Annuity Bookings Other Adjustment'
                        ELSE 'AS-T Annuity Bookings Not Mapped Adjustment'
                     END
                  WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('POS', 'en-ci-rtrim'))
                     THEN 'AS-T Annuity Base Bookings Net POS'
                  WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('POS_ADJ', 'en-ci-rtrim'))
                     THEN 'AS-T Annuity Base Bookings POS Adjustments'
                  ELSE 'AS-T Annuity Base Not Mapped Bookings Net'
               END
            ELSE 'AS Not Mapped Annuity Bookings'
         END
      /*WHEN BM.ACCOUNT_NAME IN ('TECHNICAL SUPPORT SERVICES','REMOTE OPERATIONS SERVICES')*/
      WHEN RTRIM(BM.BK_SERVICE_CATEGORY_ID) IN (COLLATE('TECHNICAL SUPPORT SERVICES', 'en-ci-rtrim'), COLLATE('REMOTE OPERATIONS SERVICES', 'en-ci-rtrim'))
         THEN CASE
            WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('ERP', 'en-ci-rtrim'), COLLATE('XAAS', 'en-ci-rtrim'))
               THEN CASE
                  WHEN RTRIM(UPPER(BM.CANCEL_CODE)) IN (COLLATE('LOST ORDER', 'en-ci-rtrim'))
                     THEN CASE
                        WHEN BM.DV_CISCO_BOOKED_DT < FY.FISCAL_MONTH_START_DATE
                           THEN 'TSS Annuity Prior period DeBookings'
                        ELSE 'TSS Annuity Current DeBookings'
                     END
                  ELSE 'TSS Annuity Base Current Bookings'
               END
            WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('AR', 'en-ci-rtrim'))
               THEN CASE
                  WHEN RTRIM(TRIM(UPPER(BM.ADJUSTMENT_CODE))) IN (COLLATE('CM', 'en-ci-rtrim'), COLLATE('CM_REVENUE', 'en-ci-rtrim'))
                  AND COLLATE(TRIM(UPPER(BM.SALES_ORDER_CATEGORY_TYPE)), 'en-ci-rtrim') <> 'RETURN'
                     THEN 'TSS Annuity Bookings Credit Memos'
                  WHEN RTRIM(TRIM(UPPER(BM.ADJUSTMENT_CODE))) IN (COLLATE('CM', 'en-ci-rtrim'), COLLATE('CM_REVENUE', 'en-ci-rtrim'))
                  AND COLLATE(TRIM(UPPER(BM.SALES_ORDER_CATEGORY_TYPE)), 'en-ci-rtrim') = 'RETURN'
                     THEN 'TSS Annuity Bookings RMA'
                  WHEN RTRIM(TRIM(UPPER(BM.ADJUSTMENT_CODE))) IN (COLLATE('REVENUE TRANSFER AUTO - MANUAL', 'en-ci-rtrim'))
                     THEN 'TSS Annuity Bookings Revenue Transfer Auto - Manual'
                  WHEN RTRIM(TRIM(UPPER(BM.ADJUSTMENT_CODE))) IN (COLLATE('REVENUE TRANSFER AUTO - SYSTEM', 'en-ci-rtrim'))
                     THEN 'TSS Annuity Bookings Revenue Transfer Auto - System'
                  ELSE 'TSS Annuity Bookings Not Mapped AR'
               END
            WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('SLS_ADJ', 'en-ci-rtrim'))
               THEN CASE
                  WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('RMKT1', 'en-ci-rtrim'), COLLATE('RMKT', 'en-ci-rtrim'))
                     THEN 'TSS Annuity Bookings Refurbished Orders'
                  WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('MITG-RES', 'en-ci-rtrim'), COLLATE('RR-RES', 'en-ci-rtrim'))
                     THEN 'TSS Annuity Bookings Reserve'
                  WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('MITG-REL', 'en-ci-rtrim'), COLLATE('RR-REL', 'en-ci-rtrim'))
                     THEN 'TSS Annuity Bookings Release'
                  WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('MGMT-RF', 'en-ci-rtrim'), COLLATE('MGMT-W', 'en-ci-rtrim'), COLLATE('MGMT-BC', 'en-ci-rtrim'), COLLATE('MGMT-AE', 'en-ci-rtrim'), COLLATE('MGMT-M', 'en-ci-rtrim'), COLLATE('NBM-M', 'en-ci-rtrim'), COLLATE('TCCV-A', 'en-ci-rtrim'), COLLATE('TCCV-T', 'en-ci-rtrim'))
                     THEN 'TSS Annuity Bookings Management Adjustment'
                  WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('RB', 'en-ci-rtrim'), COLLATE('VIP', 'en-ci-rtrim'), COLLATE('RB1', 'en-ci-rtrim'), COLLATE('VOLREB', 'en-ci-rtrim'))
                     THEN 'TSS Annuity Bookings Rebate Adjustment'
                  WHEN (COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE 'AC-%'
                  OR RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('MS-EMS', 'en-ci-rtrim'), COLLATE('MS-NS', 'en-ci-rtrim'), COLLATE('MS-PPS', 'en-ci-rtrim')))
                     THEN 'TSS Annuity Bookings Acquisition Adjustment'
                  WHEN ((COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE 'CLD-%')
                  OR (COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE 'LL-%')
                  OR (RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('LCLD-PVT', 'en-ci-rtrim'))))
                     THEN 'TSS Annuity Bookings Cloud Adjustment'
                  WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('FMV-%')
                     THEN 'TSS Annuity Bookings FMV Adjustment'
                  WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('SBP-%')
                     THEN 'TSS Annuity Bookings SBP Adjustment'
                  WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('MS-SMS%')
                     THEN 'TSS Annuity Bookings Managed Services Adjustment'
                  WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('SS-%')
                     THEN 'TSS Annuity Bookings Solution Selling Adjustment'
                  WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('XAAS-%')
                     THEN 'TSS Annuity Bookings Xaas Adjustment'
                  WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('1C_BOOK', 'en-ci-rtrim'), COLLATE('1C_REV', 'en-ci-rtrim'), COLLATE('BKG-CR', 'en-ci-rtrim'), COLLATE('EMN', 'en-ci-rtrim'), COLLATE('MULTINAT', 'en-ci-rtrim'))
                     THEN 'TSS Annuity Bookings Other Adjustment'
                  ELSE 'TSS Annuity Bookings Not Mapped Adjustment'
               END
            WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('POS', 'en-ci-rtrim'))
               THEN 'TSS Annuity Base Bookings Net POS'
            WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('POS_ADJ', 'en-ci-rtrim'))
               THEN 'TSS Annuity Base Bookings POS Adjustments'
            ELSE 'TSS Annuity Base Not Mapped Bookings Net'
         END
      ELSE 'Service Not Mapped Annuity Bookings Net'
   END AS DV_BOOKINGS_LINE_ITEM_NAME,
   SUM(BM.ANNUITY_AMT) BOOKINGS_AMOUNT,
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
   {{ var('m_WI_BKGS_HIER_STGDB') }}.WI_BKGS_HIER_SRVC_ANTY BM
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