{{ config(
    tags=['m_WI_BKGS_HIER']
) }}
{{ config(materialized='table') }}
-- Self-referencing table(s): 'WI_BKGS_HIER4' used as both source and target in this mapping.
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
   'ANNUAL' DV_PNL_BOOK_NET_COST_TYPE,
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
                                 THEN 'AS-S Annual Prior period DeBookings'
                              ELSE 'AS-S Annual Current DeBookings'
                           END
                        ELSE 'AS-S Annual Base Current Bookings'
                     END
                  WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('AR', 'en-ci-rtrim'))
                     THEN CASE
                        WHEN RTRIM(TRIM(UPPER(BM.ADJUSTMENT_CODE))) IN (COLLATE('CM', 'en-ci-rtrim'), COLLATE('CM_REVENUE', 'en-ci-rtrim'))
                        AND COLLATE(TRIM(UPPER(BM.SALES_ORDER_CATEGORY_TYPE)), 'en-ci-rtrim') <> 'RETURN'
                           THEN 'AS-S Annual Bookings Credit Memos'
                        WHEN RTRIM(TRIM(UPPER(BM.ADJUSTMENT_CODE))) IN (COLLATE('CM', 'en-ci-rtrim'), COLLATE('CM_REVENUE', 'en-ci-rtrim'))
                        AND COLLATE(TRIM(UPPER(BM.SALES_ORDER_CATEGORY_TYPE)), 'en-ci-rtrim') = 'RETURN'
                           THEN 'AS-S Annual Bookings RMA'
                        WHEN RTRIM(TRIM(UPPER(BM.ADJUSTMENT_CODE))) IN (COLLATE('REVENUE TRANSFER AUTO - MANUAL', 'en-ci-rtrim'))
                           THEN 'AS-S Annual Bookings Revenue Transfer Auto - Manual'
                        WHEN RTRIM(TRIM(UPPER(BM.ADJUSTMENT_CODE))) IN (COLLATE('REVENUE TRANSFER AUTO - SYSTEM', 'en-ci-rtrim'))
                           THEN 'AS-S Annual Bookings Revenue Transfer Auto - System'
                        ELSE 'AS-S Annual Bookings Not Mapped AR'
                     END
                  WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('SLS_ADJ', 'en-ci-rtrim'))
                     THEN CASE
                        WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('RMKT1', 'en-ci-rtrim'), COLLATE('RMKT', 'en-ci-rtrim'))
                           THEN 'AS-S Annual Bookings Refurbished Orders'
                        WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('MITG-RES', 'en-ci-rtrim'), COLLATE('RR-RES', 'en-ci-rtrim'))
                           THEN 'AS-S Annual Bookings Reserve'
                        WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('MITG-REL', 'en-ci-rtrim'), COLLATE('RR-REL', 'en-ci-rtrim'))
                           THEN 'AS-S Annual Bookings Release'
                        WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('MGMT-RF', 'en-ci-rtrim'), COLLATE('MGMT-W', 'en-ci-rtrim'), COLLATE('MGMT-BC', 'en-ci-rtrim'), COLLATE('MGMT-AE', 'en-ci-rtrim'), COLLATE('MGMT-M', 'en-ci-rtrim'), COLLATE('NBM-M', 'en-ci-rtrim'), COLLATE('TCCV-A', 'en-ci-rtrim'), COLLATE('TCCV-T', 'en-ci-rtrim'))
                           THEN 'AS-S Annual Bookings Management Adjustment'
                        WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('RB', 'en-ci-rtrim'), COLLATE('VIP', 'en-ci-rtrim'), COLLATE('RB1', 'en-ci-rtrim'), COLLATE('VOLREB', 'en-ci-rtrim'))
                           THEN 'AS-S Annual Bookings Rebate Adjustment'
                        WHEN (COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE 'AC-%'
                        OR RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('MS-EMS', 'en-ci-rtrim'), COLLATE('MS-NS', 'en-ci-rtrim'), COLLATE('MS-PPS', 'en-ci-rtrim')))
                           THEN 'AS-S Annual Bookings Acquisition Adjustment'
                        WHEN ((COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE 'CLD-%')
                        OR (COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE 'LL-%')
                        OR (RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('LCLD-PVT', 'en-ci-rtrim'))))
                           THEN 'AS-S Annual Bookings Cloud Adjustment'
                        WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('FMV-%')
                           THEN 'AS-S Annual Bookings FMV Adjustment'
                        WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('SBP-%')
                           THEN 'AS-S Annual Bookings SBP Adjustment'
                        WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('MS-SMS%')
                           THEN 'AS-S Annual Bookings Managed Services Adjustment'
                        WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('SS-%')
                           THEN 'AS-S Annual Bookings Solution Selling Adjustment'
                        WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('XAAS-%')
                           THEN 'AS-S Annual Bookings Xaas Adjustment'
                        WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('1C_BOOK', 'en-ci-rtrim'), COLLATE('1C_REV', 'en-ci-rtrim'), COLLATE('BKG-CR', 'en-ci-rtrim'), COLLATE('EMN', 'en-ci-rtrim'), COLLATE('MULTINAT', 'en-ci-rtrim'))
                           THEN 'AS-S Annual Bookings Other Adjustment'
                        ELSE 'AS-S Annual Bookings Not Mapped Adjustment'
                     END
                  WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('POS', 'en-ci-rtrim'))
                     THEN 'AS-S Annual Base Bookings Net POS'
                  WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('POS_ADJ', 'en-ci-rtrim'))
                     THEN 'AS-S Annual Base Bookings POS Adjustments'
                  ELSE 'AS-S Annual Base Not Mapped Bookings Net'
               END
            WHEN RTRIM(BM.ACCOUNT_NAME) IN (COLLATE('AS TRANSACTION', 'en-ci-rtrim'), COLLATE('AS ADVISORY', 'en-ci-rtrim'), COLLATE('AS FIXED', 'en-ci-rtrim'))
               THEN CASE
                  WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('ERP', 'en-ci-rtrim'), COLLATE('XAAS', 'en-ci-rtrim'))
                     THEN CASE
                        WHEN RTRIM(UPPER(BM.CANCEL_CODE)) IN (COLLATE('LOST ORDER', 'en-ci-rtrim'))
                           THEN CASE
                              WHEN BM.DV_CISCO_BOOKED_DT < FY.FISCAL_MONTH_START_DATE
                                 THEN 'AS-T Annual Prior period DeBookings'
                              ELSE 'AS-T Annual Current DeBookings'
                           END
                        ELSE 'AS-T Annual Base Current Bookings'
                     END
                  WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('AR', 'en-ci-rtrim'))
                     THEN CASE
                        WHEN RTRIM(TRIM(UPPER(BM.ADJUSTMENT_CODE))) IN (COLLATE('CM', 'en-ci-rtrim'), COLLATE('CM_REVENUE', 'en-ci-rtrim'))
                        AND COLLATE(TRIM(UPPER(BM.SALES_ORDER_CATEGORY_TYPE)), 'en-ci-rtrim') <> 'RETURN'
                           THEN 'AS-T Annual Bookings Credit Memos'
                        WHEN RTRIM(TRIM(UPPER(BM.ADJUSTMENT_CODE))) IN (COLLATE('CM', 'en-ci-rtrim'), COLLATE('CM_REVENUE', 'en-ci-rtrim'))
                        AND COLLATE(TRIM(UPPER(BM.SALES_ORDER_CATEGORY_TYPE)), 'en-ci-rtrim') = 'RETURN'
                           THEN 'AS-T Annual Bookings RMA'
                        WHEN RTRIM(TRIM(UPPER(BM.ADJUSTMENT_CODE))) IN (COLLATE('REVENUE TRANSFER AUTO - MANUAL', 'en-ci-rtrim'))
                           THEN 'AS-T Annual Bookings Revenue Transfer Auto - Manual'
                        WHEN RTRIM(TRIM(UPPER(BM.ADJUSTMENT_CODE))) IN (COLLATE('REVENUE TRANSFER AUTO - SYSTEM', 'en-ci-rtrim'))
                           THEN 'AS-T Annual Bookings Revenue Transfer Auto - System'
                        ELSE 'AS-T Annual Bookings Not Mapped AR'
                     END
                  WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('SLS_ADJ', 'en-ci-rtrim'))
                     THEN CASE
                        WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('RMKT1', 'en-ci-rtrim'), COLLATE('RMKT', 'en-ci-rtrim'))
                           THEN 'AS-T Annual Bookings Refurbished Orders'
                        WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('MITG-RES', 'en-ci-rtrim'), COLLATE('RR-RES', 'en-ci-rtrim'))
                           THEN 'AS-T Annual Bookings Reserve'
                        WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('MITG-REL', 'en-ci-rtrim'), COLLATE('RR-REL', 'en-ci-rtrim'))
                           THEN 'AS-T Annual Bookings Release'
                        WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('MGMT-RF', 'en-ci-rtrim'), COLLATE('MGMT-W', 'en-ci-rtrim'), COLLATE('MGMT-BC', 'en-ci-rtrim'), COLLATE('MGMT-AE', 'en-ci-rtrim'), COLLATE('MGMT-M', 'en-ci-rtrim'), COLLATE('NBM-M', 'en-ci-rtrim'), COLLATE('TCCV-A', 'en-ci-rtrim'), COLLATE('TCCV-T', 'en-ci-rtrim'))
                           THEN 'AS-T Annual Bookings Management Adjustment'
                        WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('RB', 'en-ci-rtrim'), COLLATE('VIP', 'en-ci-rtrim'), COLLATE('RB1', 'en-ci-rtrim'), COLLATE('VOLREB', 'en-ci-rtrim'))
                           THEN 'AS-T Annual Bookings Rebate Adjustment'
                        WHEN (COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE 'AC-%'
                        OR RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('MS-EMS', 'en-ci-rtrim'), COLLATE('MS-NS', 'en-ci-rtrim'), COLLATE('MS-PPS', 'en-ci-rtrim')))
                           THEN 'AS-T Annual Bookings Acquisition Adjustment'
                        WHEN ((COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE 'CLD-%')
                        OR (COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE 'LL-%')
                        OR (RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('LCLD-PVT', 'en-ci-rtrim'))))
                           THEN 'AS-T Annual Bookings Cloud Adjustment'
                        WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('FMV-%')
                           THEN 'AS-T Annual Bookings FMV Adjustment'
                        WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('SBP-%')
                           THEN 'AS-T Annual Bookings SBP Adjustment'
                        WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('MS-SMS%')
                           THEN 'AS-T Annual Bookings Managed Services Adjustment'
                        WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('SS-%')
                           THEN 'AS-T Annual Bookings Solution Selling Adjustment'
                        WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('XAAS-%')
                           THEN 'AS-T Annual Bookings Xaas Adjustment'
                        WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('1C_BOOK', 'en-ci-rtrim'), COLLATE('1C_REV', 'en-ci-rtrim'), COLLATE('BKG-CR', 'en-ci-rtrim'), COLLATE('EMN', 'en-ci-rtrim'), COLLATE('MULTINAT', 'en-ci-rtrim'))
                           THEN 'AS-T Annual Bookings Other Adjustment'
                        ELSE 'AS-T Annual Bookings Not Mapped Adjustment'
                     END
                  WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('POS', 'en-ci-rtrim'))
                     THEN 'AS-T Annual Base Bookings Net POS'
                  WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('POS_ADJ', 'en-ci-rtrim'))
                     THEN 'AS-T Annual Base Bookings POS Adjustments'
                  ELSE 'AS-T Annual Base Not Mapped Bookings Net'
               END
            ELSE 'AS Not Mapped Base Bookings'
         END
      /*WHEN BM.ACCOUNT_NAME IN ('TECHNICAL SUPPORT SERVICES','REMOTE OPERATIONS SERVICES')*/
      WHEN (RTRIM(BM.BK_SERVICE_CATEGORY_ID) IN (COLLATE('TECHNICAL SUPPORT SERVICES', 'en-ci-rtrim'), COLLATE('REMOTE OPERATIONS SERVICES', 'en-ci-rtrim'))
      AND RTRIM(BM.BK_ALLOCATED_SERVC_GROUP_ID) NOT IN (COLLATE('TRAINING', 'en-ci-rtrim')))
         THEN CASE
            WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('ERP', 'en-ci-rtrim'), COLLATE('XAAS', 'en-ci-rtrim'))
               THEN CASE
                  WHEN RTRIM(UPPER(BM.CANCEL_CODE)) IN (COLLATE('LOST ORDER', 'en-ci-rtrim'))
                     THEN CASE
                        WHEN BM.DV_CISCO_BOOKED_DT < FY.FISCAL_MONTH_START_DATE
                           THEN 'TSS Annual Prior period DeBookings'
                        ELSE 'TSS Annual Current DeBookings'
                     END
                  ELSE 'TSS Annual Base Current Bookings'
               END
            WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('AR', 'en-ci-rtrim'))
               THEN CASE
                  WHEN RTRIM(TRIM(UPPER(BM.ADJUSTMENT_CODE))) IN (COLLATE('CM', 'en-ci-rtrim'), COLLATE('CM_REVENUE', 'en-ci-rtrim'))
                  AND COLLATE(TRIM(UPPER(BM.SALES_ORDER_CATEGORY_TYPE)), 'en-ci-rtrim') <> 'RETURN'
                     THEN 'TSS Annual Bookings Credit Memos'
                  WHEN RTRIM(TRIM(UPPER(BM.ADJUSTMENT_CODE))) IN (COLLATE('CM', 'en-ci-rtrim'), COLLATE('CM_REVENUE', 'en-ci-rtrim'))
                  AND COLLATE(TRIM(UPPER(BM.SALES_ORDER_CATEGORY_TYPE)), 'en-ci-rtrim') = 'RETURN'
                     THEN 'TSS Annual Bookings RMA'
                  WHEN RTRIM(TRIM(UPPER(BM.ADJUSTMENT_CODE))) IN (COLLATE('REVENUE TRANSFER AUTO - MANUAL', 'en-ci-rtrim'))
                     THEN 'TSS Annual Bookings Revenue Transfer Auto - Manual'
                  WHEN RTRIM(TRIM(UPPER(BM.ADJUSTMENT_CODE))) IN (COLLATE('REVENUE TRANSFER AUTO - SYSTEM', 'en-ci-rtrim'))
                     THEN 'TSS Annual Bookings Revenue Transfer Auto - System'
                  ELSE 'TSS Annual Bookings Not Mapped AR'
               END
            WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('SLS_ADJ', 'en-ci-rtrim'))
               THEN CASE
                  WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('RMKT1', 'en-ci-rtrim'), COLLATE('RMKT', 'en-ci-rtrim'))
                     THEN 'TSS Annual Bookings Refurbished Orders'
                  WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('MITG-RES', 'en-ci-rtrim'), COLLATE('RR-RES', 'en-ci-rtrim'))
                     THEN 'TSS Annual Bookings Reserve'
                  WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('MITG-REL', 'en-ci-rtrim'), COLLATE('RR-REL', 'en-ci-rtrim'))
                     THEN 'TSS Annual Bookings Release'
                  WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('MGMT-RF', 'en-ci-rtrim'), COLLATE('MGMT-W', 'en-ci-rtrim'), COLLATE('MGMT-BC', 'en-ci-rtrim'), COLLATE('MGMT-AE', 'en-ci-rtrim'), COLLATE('MGMT-M', 'en-ci-rtrim'), COLLATE('NBM-M', 'en-ci-rtrim'), COLLATE('TCCV-A', 'en-ci-rtrim'), COLLATE('TCCV-T', 'en-ci-rtrim'))
                     THEN 'TSS Annual Bookings Management Adjustment'
                  WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('RB', 'en-ci-rtrim'), COLLATE('VIP', 'en-ci-rtrim'), COLLATE('RB1', 'en-ci-rtrim'), COLLATE('VOLREB', 'en-ci-rtrim'))
                     THEN 'TSS Annual Bookings Rebate Adjustment'
                  WHEN (COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE 'AC-%'
                  OR RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('MS-EMS', 'en-ci-rtrim'), COLLATE('MS-NS', 'en-ci-rtrim'), COLLATE('MS-PPS', 'en-ci-rtrim')))
                     THEN 'TSS Annual Bookings Acquisition Adjustment'
                  WHEN ((COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE 'CLD-%')
                  OR (COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE 'LL-%')
                  OR (RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('LCLD-PVT', 'en-ci-rtrim'))))
                     THEN 'TSS Annual Bookings Cloud Adjustment'
                  WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('FMV-%')
                     THEN 'TSS Annual Bookings FMV Adjustment'
                  WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('SBP-%')
                     THEN 'TSS Annual Bookings SBP Adjustment'
                  WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('MS-SMS%')
                     THEN 'TSS Annual Bookings Managed Services Adjustment'
                  WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('SS-%')
                     THEN 'TSS Annual Bookings Solution Selling Adjustment'
                  WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('XAAS-%')
                     THEN 'TSS Annual Bookings Xaas Adjustment'
                  WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('1C_BOOK', 'en-ci-rtrim'), COLLATE('1C_REV', 'en-ci-rtrim'), COLLATE('BKG-CR', 'en-ci-rtrim'), COLLATE('EMN', 'en-ci-rtrim'), COLLATE('MULTINAT', 'en-ci-rtrim'))
                     THEN 'TSS Annual Bookings Other Adjustment'
                  ELSE 'TSS Annual Bookings Not Mapped Adjustment'
               END
            WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('POS', 'en-ci-rtrim'))
               THEN 'TSS Annual Base Bookings Net POS'
            WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('POS_ADJ', 'en-ci-rtrim'))
               THEN 'TSS Annual Base Bookings POS Adjustments'
            ELSE 'TSS Annual Base Not Mapped Bookings Net'
         END
      WHEN (RTRIM(BM.BK_SERVICE_CATEGORY_ID) IN (COLLATE('TECHNICAL SUPPORT SERVICES', 'en-ci-rtrim'))
      AND COLLATE(BM.BK_ALLOCATED_SERVC_GROUP_ID, 'en-ci-rtrim') = 'TRAINING')
         THEN 'Training Bookings'
      ELSE 'Service Not Mapped Annual Bookings Net'
   END AS DV_BOOKINGS_LINE_ITEM_NAME,
   SUM(BM.ANNUALIZED_AMT) BOOKINGS_AMOUNT,
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
   {{ var('m_WI_BKGS_HIER_STGDB') }}.WI_BKGS_HIER_SRVC_ANNUAL BM
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