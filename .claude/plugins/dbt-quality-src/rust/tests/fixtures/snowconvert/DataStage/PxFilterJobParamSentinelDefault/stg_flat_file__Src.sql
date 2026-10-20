SELECT
   $1 AS RecordType,
   $2 AS Data
FROM
   @public.landing_stage/dsx/sources/Src/ (FILE_FORMAT => 'Src_FILE_FORMAT')
