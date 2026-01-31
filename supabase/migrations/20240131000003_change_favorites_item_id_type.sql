-- Change item_id from UUID to TEXT to support both UUIDs (Papers) and Integers/Strings (GitHub Projects)
ALTER TABLE public.favorites ALTER COLUMN item_id TYPE TEXT;
