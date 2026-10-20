-- SnowConvert land zone: every converted flat-file read and unload binds to this stage.
CREATE STAGE IF NOT EXISTS public.landing_stage
  COMMENT = 'SnowConvert-generated land zone. Retarget URL/integration; keep the name and subfolder layout.';