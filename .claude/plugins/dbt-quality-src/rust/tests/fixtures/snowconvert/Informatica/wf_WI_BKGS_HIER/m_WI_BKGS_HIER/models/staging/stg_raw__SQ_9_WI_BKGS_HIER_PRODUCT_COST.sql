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
 'PRODUCT_COST' DV_PNL_BOOK_NET_COST_TYPE,
 CASE
  WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('ERP', 'en-ci-rtrim'), COLLATE('XAAS', 'en-ci-rtrim'))
   THEN CASE
    WHEN RTRIM(UPPER(BM.CANCEL_CODE)) IN (COLLATE('LOST ORDER', 'en-ci-rtrim'))
     THEN CASE
      WHEN BM.DV_CISCO_BOOKED_DT < FY.FISCAL_MONTH_START_DATE
       THEN 'Prior Period DeBookings Cost'
                      ELSE 'Current DeBookings Cost'
     END
                  ELSE 'Current Bookings Cost'
   END
  WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('AR', 'en-ci-rtrim'))
   THEN CASE
    WHEN RTRIM(TRIM(UPPER(BM.ADJUSTMENT_CODE))) IN (COLLATE('CM', 'en-ci-rtrim'), COLLATE('CM_REVENUE', 'en-ci-rtrim'))
    AND COLLATE( TRIM(UPPER(BM.SALES_ORDER_CATEGORY_TYPE)), 'en-ci-rtrim') <> 'RETURN'
     THEN 'Bookings Credit Memos Cost'
    WHEN RTRIM(TRIM(UPPER(BM.ADJUSTMENT_CODE))) IN (COLLATE('CM', 'en-ci-rtrim'), COLLATE('CM_REVENUE', 'en-ci-rtrim'))
    AND COLLATE( TRIM(UPPER(BM.SALES_ORDER_CATEGORY_TYPE)), 'en-ci-rtrim') = 'RETURN'
     THEN 'Bookings RMA Cost'
    WHEN RTRIM(TRIM(UPPER(BM.ADJUSTMENT_CODE))) IN (COLLATE('REVENUE TRANSFER AUTO - MANUAL', 'en-ci-rtrim'))
     THEN 'Bookings Revenue Transfer Auto - Manual Cost'
    WHEN RTRIM(TRIM(UPPER(BM.ADJUSTMENT_CODE))) IN (COLLATE('REVENUE TRANSFER AUTO - SYSTEM', 'en-ci-rtrim'))
     THEN 'Bookings Revenue Transfer Auto - System Cost'
                  ELSE 'Bookings Not Mapped AR Cost'
   END
  WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('SLS_ADJ', 'en-ci-rtrim'))
   THEN CASE
    WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('RMKT1', 'en-ci-rtrim'), COLLATE('RMKT', 'en-ci-rtrim'))
     THEN 'Bookings Refurbished Orders Cost'
    WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('MITG-RES', 'en-ci-rtrim'), COLLATE('RR-RES', 'en-ci-rtrim'))
     THEN 'Bookings Reserve Cost'
    WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('MITG-REL', 'en-ci-rtrim'), COLLATE('RR-REL', 'en-ci-rtrim'))
     THEN 'Bookings Release Cost'
    WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('MGMT-RF', 'en-ci-rtrim'), COLLATE('MGMT-W', 'en-ci-rtrim'), COLLATE('MGMT-BC', 'en-ci-rtrim'), COLLATE('MGMT-AE', 'en-ci-rtrim'), COLLATE('MGMT-M', 'en-ci-rtrim'), COLLATE('NBM-M', 'en-ci-rtrim'), COLLATE('TCCV-A', 'en-ci-rtrim'), COLLATE('TCCV-T', 'en-ci-rtrim'))
     THEN 'Bookings Management Adjustment Cost'
    WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('RB', 'en-ci-rtrim'), COLLATE('VIP', 'en-ci-rtrim'), COLLATE('RB1', 'en-ci-rtrim'), COLLATE('VOLREB', 'en-ci-rtrim'))
     THEN 'Bookings Rebate Adjustment Cost'
    WHEN (COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE 'AC-%' OR RTRIM(  TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('MS-EMS', 'en-ci-rtrim'), COLLATE('MS-NS', 'en-ci-rtrim'), COLLATE('MS-PPS', 'en-ci-rtrim')))
     THEN 'Bookings Acquisition Adjustment Cost'
    WHEN ((COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE 'CLD-%') OR (COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE 'LL-%') OR (RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('LCLD-PVT', 'en-ci-rtrim'))))
     THEN 'Bookings Cloud Adjustment Cost'
    WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('FMV-%')
     THEN 'Bookings FMV Adjustment Cost'
    WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('SBP-%')
     THEN 'Bookings SBP Adjustment Cost'
    WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('MS-SMS%')
     THEN 'Bookings Managed Services Adjustment Cost'
    WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('SS-%')
     THEN 'Bookings Solution Selling Adjustment Cost'
    WHEN COLLATE(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE)), 'en-ci-rtrim') LIKE ('XAAS-%')
     THEN 'Bookings XaaS Adjustment Cost'
    WHEN RTRIM(TRIM(UPPER(BM.IDE_ADJUSTMENT_CODE))) IN (COLLATE('1C_BOOK', 'en-ci-rtrim'), COLLATE('1C_REV', 'en-ci-rtrim'), COLLATE('BKG-CR', 'en-ci-rtrim'), COLLATE('EMN', 'en-ci-rtrim'), COLLATE('MULTINAT', 'en-ci-rtrim'))
     THEN 'Bookings Other Adjustment Cost'
                  ELSE 'Bookings Not Mapped Adjustment Cost'
   END
  WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('POS', 'en-ci-rtrim'))
   THEN 'Bookings Net POS Cost'
  WHEN RTRIM(BM.BKGS_MEASURE_TRANS_TYPE_CODE) IN (COLLATE('POS_ADJ', 'en-ci-rtrim'))
   THEN 'Bookings POS Adjustments Cost'
      ELSE 'Bookings Cost Not Mapped'
 END AS DV_BOOKINGS_LINE_ITEM_NAME,
 SUM(BM.BOOKINGS_STD_COST)  BOOKINGS_AMOUNT,
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
 {{ source('raw', 'WI_BKGS_HIER_PRDT') }} BM
 INNER JOIN
  {{ source('raw', 'R_FISCAL_MONTH_TO_YEAR') }} FY
 ON BM.FISCAL_YEAR_MTH_NUMBER_INT = FY.FISCAL_YEAR_MONTH_INT
 GROUP BY 1,2,3,4,5,6,7,8,9,10,11,12,13,14,16,17,18,19,20,21,22,23,24,25,26,27