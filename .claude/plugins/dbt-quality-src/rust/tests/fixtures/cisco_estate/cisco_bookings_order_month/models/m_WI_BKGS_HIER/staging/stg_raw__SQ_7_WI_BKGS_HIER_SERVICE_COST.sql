{{ config(
    tags=['m_WI_BKGS_HIER']
) }}
{{ config(materialized='table') }}
-- Self-referencing table(s): 'WI_BKGS_HIER' used as both source and target in this mapping.
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
   'SERVICE_COST' AS DV_PNL_BOOK_NET_COST_TYPE,
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
                                 THEN 'AS-S Prior Period DeBookings Cost'
                              ELSE 'AS-S Current DeBookings Cost'
                           END
                        ELSE 'AS-S Current Bookings Cost'
                     END
                  WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('AR', 'en-ci-rtrim'))
                     THEN CASE
                        WHEN RTRIM(TRIM(UPPER(BM.ADJUSTMENT_CODE))) IN (COLLATE('CM', 'en-ci-rtrim'), COLLATE('CM_REVENUE', 'en-ci-rtrim'))
                        AND COLLATE(TRIM(UPPER(BM.SALES_ORDER_CATEGORY_TYPE)), 'en-ci-rtrim') <> 'RETURN'
                           THEN 'AS-S Bookings Credit Memos Cost'
                        WHEN RTRIM(TRIM(UPPER(BM.ADJUSTMENT_CODE))) IN (COLLATE('CM', 'en-ci-rtrim'), COLLATE('CM_REVENUE', 'en-ci-rtrim'))
                        AND COLLATE(TRIM(UPPER(BM.SALES_ORDER_CATEGORY_TYPE)), 'en-ci-rtrim') = 'RETURN'
                           THEN 'AS-S Bookings RMA Cost'
                        WHEN RTRIM(TRIM(UPPER(BM.ADJUSTMENT_CODE))) IN (COLLATE('REVENUE TRANSFER AUTO - MANUAL', 'en-ci-rtrim'))
                           THEN 'AS-S Bookings Revenue Transfer Auto - Manual Cost'
                        WHEN RTRIM(TRIM(UPPER(BM.ADJUSTMENT_CODE))) IN (COLLATE('REVENUE TRANSFER AUTO - SYSTEM', 'en-ci-rtrim'))
                           THEN 'AS-S Bookings Revenue Transfer Auto - System Cost'
                        ELSE 'AS-S Bookings Not Mapped AR Cost'
                     END
                  WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('SLS_ADJ', 'en-ci-rtrim'))
                     THEN CASE
                        WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('RMKT1', 'en-ci-rtrim'), COLLATE('RMKT', 'en-ci-rtrim'))
                           THEN 'AS-S Bookings Refurbished Orders Cost'
                        WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('MITG-RES', 'en-ci-rtrim'), COLLATE('RR-RES', 'en-ci-rtrim'))
                           THEN 'AS-S Bookings Reserve Cost'
                        WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('MITG-REL', 'en-ci-rtrim'), COLLATE('RR-REL', 'en-ci-rtrim'))
                           THEN 'AS-S Bookings Release Cost'
                        WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('MGMT-RF', 'en-ci-rtrim'), COLLATE('MGMT-W', 'en-ci-rtrim'), COLLATE('MGMT-BC', 'en-ci-rtrim'), COLLATE('MGMT-AE', 'en-ci-rtrim'), COLLATE('MGMT-M', 'en-ci-rtrim'), COLLATE('NBM-M', 'en-ci-rtrim'), COLLATE('TCCV-A', 'en-ci-rtrim'), COLLATE('TCCV-T', 'en-ci-rtrim'))
                           THEN 'AS-S Bookings Management Adjustment Cost'
                        WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('RB', 'en-ci-rtrim'), COLLATE('VIP', 'en-ci-rtrim'), COLLATE('RB1', 'en-ci-rtrim'), COLLATE('VOLREB', 'en-ci-rtrim'))
                           THEN 'AS-S Bookings Rebate Adjustment Cost'
                        WHEN (COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE 'AC-%'
                        OR RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('MS-EMS', 'en-ci-rtrim'), COLLATE('MS-NS', 'en-ci-rtrim'), COLLATE('MS-PPS', 'en-ci-rtrim')))
                           THEN 'AS-S Bookings Acquisition Adjustment Cost'
                        WHEN ((COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE 'CLD-%')
                        OR (COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE 'LL-%')
                        OR (RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('LCLD-PVT', 'en-ci-rtrim'))))
                           THEN 'AS-S Bookings Cloud Adjustment Cost'
                        WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('FMV-%')
                           THEN 'AS-S Bookings FMV Adjustment Cost'
                        WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('SBP-%')
                           THEN 'AS-S Bookings SBP Adjustment Cost'
                        WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('MS-SMS%')
                           THEN 'AS-S Bookings Managed Services Adjustment Cost'
                        WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('SS-%')
                           THEN 'AS-S Bookings Solution Selling Adjustment Cost'
                        WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('XAAS-%')
                           THEN 'AS-S Bookings XaaS Adjustment Cost'
                        WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('1C_BOOK', 'en-ci-rtrim'), COLLATE('1C_REV', 'en-ci-rtrim'), COLLATE('BKG-CR', 'en-ci-rtrim'), COLLATE('EMN', 'en-ci-rtrim'), COLLATE('MULTINAT', 'en-ci-rtrim'))
                           THEN 'AS-S Bookings Other Adjustment Cost'
                        ELSE 'AS-S Bookings Not Mapped Adjustment Cost'
                     END
                  WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('POS', 'en-ci-rtrim'))
                     THEN 'AS-S Bookings Net POS Cost'
                  WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('POS_ADJ', 'en-ci-rtrim'))
                     THEN 'AS-S Bookings POS Adjustments Cost'
                  ELSE 'AS-S Not Mapped Bookings Cost'
               END
            WHEN RTRIM(BM.ACCOUNT_NAME) IN (COLLATE('AS TRANSACTION', 'en-ci-rtrim'), COLLATE('AS ADVISORY', 'en-ci-rtrim'), COLLATE('AS FIXED', 'en-ci-rtrim'))
               THEN CASE
                  WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('ERP', 'en-ci-rtrim'), COLLATE('XAAS', 'en-ci-rtrim'))
                     THEN CASE
                        WHEN RTRIM(UPPER(BM.CANCEL_CODE)) IN (COLLATE('LOST ORDER', 'en-ci-rtrim'))
                           THEN CASE
                              WHEN BM.DV_CISCO_BOOKED_DT < FY.FISCAL_MONTH_START_DATE
                                 THEN 'AS-T Prior Period DeBookings Cost'
                              ELSE 'AS-T Current DeBookings Cost'
                           END
                        ELSE 'AS-T Current Bookings Cost'
                     END
                  WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('AR', 'en-ci-rtrim'))
                     THEN CASE
                        WHEN RTRIM(TRIM(UPPER(BM.ADJUSTMENT_CODE))) IN (COLLATE('CM', 'en-ci-rtrim'), COLLATE('CM_REVENUE', 'en-ci-rtrim'))
                        AND COLLATE(TRIM(UPPER(BM.SALES_ORDER_CATEGORY_TYPE)), 'en-ci-rtrim') <> 'RETURN'
                           THEN 'AS-T Bookings Credit Memos Cost'
                        WHEN RTRIM(TRIM(UPPER(BM.ADJUSTMENT_CODE))) IN (COLLATE('CM', 'en-ci-rtrim'), COLLATE('CM_REVENUE', 'en-ci-rtrim'))
                        AND COLLATE(TRIM(UPPER(BM.SALES_ORDER_CATEGORY_TYPE)), 'en-ci-rtrim') = 'RETURN'
                           THEN 'AS-T Bookings RMA Cost'
                        WHEN RTRIM(TRIM(UPPER(BM.ADJUSTMENT_CODE))) IN (COLLATE('REVENUE TRANSFER AUTO - MANUAL', 'en-ci-rtrim'))
                           THEN 'AS-T Bookings Revenue Transfer Auto - Manual Cost'
                        WHEN RTRIM(TRIM(UPPER(BM.ADJUSTMENT_CODE))) IN (COLLATE('REVENUE TRANSFER AUTO - SYSTEM', 'en-ci-rtrim'))
                           THEN 'AS-T Bookings Revenue Transfer Auto - System Cost'
                        ELSE 'AS-T Bookings Not Mapped AR Cost'
                     END
                  WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('SLS_ADJ', 'en-ci-rtrim'))
                     THEN CASE
                        WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('RMKT1', 'en-ci-rtrim'), COLLATE('RMKT', 'en-ci-rtrim'))
                           THEN 'AS-T Bookings Refurbished Orders Cost'
                        WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('MITG-RES', 'en-ci-rtrim'), COLLATE('RR-RES', 'en-ci-rtrim'))
                           THEN 'AS-T Bookings Reserve Cost'
                        WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('MITG-REL', 'en-ci-rtrim'), COLLATE('RR-REL', 'en-ci-rtrim'))
                           THEN 'AS-T Bookings Release Cost'
                        WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('MGMT-RF', 'en-ci-rtrim'), COLLATE('MGMT-W', 'en-ci-rtrim'), COLLATE('MGMT-BC', 'en-ci-rtrim'), COLLATE('MGMT-AE', 'en-ci-rtrim'), COLLATE('MGMT-M', 'en-ci-rtrim'), COLLATE('NBM-M', 'en-ci-rtrim'), COLLATE('TCCV-A', 'en-ci-rtrim'), COLLATE('TCCV-T', 'en-ci-rtrim'))
                           THEN 'AS-T Bookings Management Adjustment Cost'
                        WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('RB', 'en-ci-rtrim'), COLLATE('VIP', 'en-ci-rtrim'), COLLATE('RB1', 'en-ci-rtrim'), COLLATE('VOLREB', 'en-ci-rtrim'))
                           THEN 'AS-T Bookings Rebate Adjustment Cost'
                        WHEN (COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE 'AC-%'
                        OR RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('MS-EMS', 'en-ci-rtrim'), COLLATE('MS-NS', 'en-ci-rtrim'), COLLATE('MS-PPS', 'en-ci-rtrim')))
                           THEN 'AS-T Bookings Acquisition Adjustment Cost'
                        WHEN ((COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE 'CLD-%')
                        OR (COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE 'LL-%')
                        OR (RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('LCLD-PVT', 'en-ci-rtrim'))))
                           THEN 'AS-T Bookings Cloud Adjustment Cost'
                        WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('FMV-%')
                           THEN 'AS-T Bookings FMV Adjustment Cost'
                        WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('SBP-%')
                           THEN 'AS-T Bookings SBP Adjustment Cost'
                        WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('MS-SMS%')
                           THEN 'AS-T Bookings Managed Services Adjustment Cost'
                        WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('SS-%')
                           THEN 'AS-T Bookings Solution Selling Adjustment Cost'
                        WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('XAAS-%')
                           THEN 'AS-T Bookings XaaS Adjustment Cost'
                        WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('1C_BOOK', 'en-ci-rtrim'), COLLATE('1C_REV', 'en-ci-rtrim'), COLLATE('BKG-CR', 'en-ci-rtrim'), COLLATE('EMN', 'en-ci-rtrim'), COLLATE('MULTINAT', 'en-ci-rtrim'))
                           THEN 'AS-T Bookings Other Adjustment Cost'
                        ELSE 'AS-T Bookings Not Mapped Adjustment Cost'
                     END
                  WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('POS', 'en-ci-rtrim'))
                     THEN 'AS-T Bookings Net POS Cost'
                  WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('POS_ADJ', 'en-ci-rtrim'))
                     THEN 'AS-T Bookings POS Adjustments Cost'
                  ELSE 'AS-T Not Mapped Bookings Cost'
               END
            ELSE 'AS Not Mapped Bookings Cost'
         END
      /* WHEN BM.ACCOUNT_NAME IN ('TECHNICAL SUPPORT SERVICES','REMOTE OPERATIONS SERVICES')*/
      WHEN RTRIM(BM.BK_SERVICE_CATEGORY_ID) IN (COLLATE('TECHNICAL SUPPORT SERVICES', 'en-ci-rtrim'), COLLATE('REMOTE OPERATIONS SERVICES', 'en-ci-rtrim'))
         THEN CASE
            WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('ERP', 'en-ci-rtrim'), COLLATE('XAAS', 'en-ci-rtrim'))
               THEN CASE
                  WHEN RTRIM(UPPER(BM.CANCEL_CODE)) IN (COLLATE('LOST ORDER', 'en-ci-rtrim'))
                     THEN CASE
                        WHEN BM.DV_CISCO_BOOKED_DT < FY.FISCAL_MONTH_START_DATE
                           THEN 'TSS Prior Period DeBookings Cost'
                        ELSE 'TSS Current DeBookings Cost'
                     END
                  ELSE 'TSS Current Bookings Cost'
               END
            WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('AR', 'en-ci-rtrim'))
               THEN CASE
                  WHEN RTRIM(TRIM(UPPER(BM.ADJUSTMENT_CODE))) IN (COLLATE('CM', 'en-ci-rtrim'), COLLATE('CM_REVENUE', 'en-ci-rtrim'))
                  AND COLLATE(TRIM(UPPER(BM.SALES_ORDER_CATEGORY_TYPE)), 'en-ci-rtrim') <> 'RETURN'
                     THEN 'TSS Bookings Credit Memos Cost'
                  WHEN RTRIM(TRIM(UPPER(BM.ADJUSTMENT_CODE))) IN (COLLATE('CM', 'en-ci-rtrim'), COLLATE('CM_REVENUE', 'en-ci-rtrim'))
                  AND COLLATE(TRIM(UPPER(BM.SALES_ORDER_CATEGORY_TYPE)), 'en-ci-rtrim') = 'RETURN'
                     THEN 'TSS Bookings RMA Cost'
                  WHEN RTRIM(TRIM(UPPER(BM.ADJUSTMENT_CODE))) IN (COLLATE('REVENUE TRANSFER AUTO - MANUAL', 'en-ci-rtrim'))
                     THEN 'TSS Bookings Revenue Transfer Auto - Manual Cost'
                  WHEN RTRIM(TRIM(UPPER(BM.ADJUSTMENT_CODE))) IN (COLLATE('REVENUE TRANSFER AUTO - SYSTEM', 'en-ci-rtrim'))
                     THEN 'TSS Bookings Revenue Transfer Auto - System Cost'
                  ELSE 'TSS Bookings Not Mapped AR Cost'
               END
            WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('SLS_ADJ', 'en-ci-rtrim'))
               THEN CASE
                  WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('RMKT1', 'en-ci-rtrim'), COLLATE('RMKT', 'en-ci-rtrim'))
                     THEN 'TSS Bookings Refurbished Orders Cost'
                  WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('MITG-RES', 'en-ci-rtrim'), COLLATE('RR-RES', 'en-ci-rtrim'))
                     THEN 'TSS Bookings Reserve Cost'
                  WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('MITG-REL', 'en-ci-rtrim'), COLLATE('RR-REL', 'en-ci-rtrim'))
                     THEN 'TSS Bookings Release Cost'
                  WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('MGMT-RF', 'en-ci-rtrim'), COLLATE('MGMT-W', 'en-ci-rtrim'), COLLATE('MGMT-BC', 'en-ci-rtrim'), COLLATE('MGMT-AE', 'en-ci-rtrim'), COLLATE('MGMT-M', 'en-ci-rtrim'), COLLATE('NBM-M', 'en-ci-rtrim'), COLLATE('TCCV-A', 'en-ci-rtrim'), COLLATE('TCCV-T', 'en-ci-rtrim'))
                     THEN 'TSS Bookings Management Adjustment Cost'
                  WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('RB', 'en-ci-rtrim'), COLLATE('VIP', 'en-ci-rtrim'), COLLATE('RB1', 'en-ci-rtrim'), COLLATE('VOLREB', 'en-ci-rtrim'))
                     THEN 'TSS Bookings Rebate Adjustment Cost'
                  WHEN (COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE 'AC-%'
                  OR RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('MS-EMS', 'en-ci-rtrim'), COLLATE('MS-NS', 'en-ci-rtrim'), COLLATE('MS-PPS', 'en-ci-rtrim')))
                     THEN 'TSS Bookings Acquisition Adjustment Cost'
                  WHEN ((COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE 'CLD-%')
                  OR (COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE 'LL-%')
                  OR (RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('LCLD-PVT', 'en-ci-rtrim'))))
                     THEN 'TSS Bookings Cloud Adjustment Cost'
                  WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('FMV-%')
                     THEN 'TSS Bookings FMV Adjustment Cost'
                  WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('SBP-%')
                     THEN 'TSS Bookings SBP Adjustment Cost'
                  WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('MS-SMS%')
                     THEN 'TSS Bookings Managed Services Adjustment Cost'
                  WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('SS-%')
                     THEN 'TSS Bookings Solution Selling Adjustment Cost'
                  WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('XAAS-%')
                     THEN 'TSS Bookings XaaS Adjustment Cost'
                  WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('1C_BOOK', 'en-ci-rtrim'), COLLATE('1C_REV', 'en-ci-rtrim'), COLLATE('BKG-CR', 'en-ci-rtrim'), COLLATE('EMN', 'en-ci-rtrim'), COLLATE('MULTINAT', 'en-ci-rtrim'))
                     THEN 'TSS Bookings Other Adjustment Cost'
                  ELSE 'TSS Bookings Not Mapped Adjustment Cost'
               END
            WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('POS', 'en-ci-rtrim'))
               THEN 'TSS Bookings Net POS Cost'
            WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('POS_ADJ', 'en-ci-rtrim'))
               THEN 'TSS Bookings POS Adjustments Cost'
            ELSE 'TSS Not Mapped Bookings Cost'
         END
      ELSE 'Service Bookings Cost Not Mapped'
   END AS DV_BOOKINGS_LINE_ITEM_NAME,
   SUM(BM.BOOKINGS_STD_COST) BOOKINGS_AMOUNT,
   'COGS' DV_BOOKINGS_OR_COGS_TYPE_CD,
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
   {{ var('m_WI_BKGS_HIER_STGDB') }}.WI_BKGS_HIER_SRVC_COST BM
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