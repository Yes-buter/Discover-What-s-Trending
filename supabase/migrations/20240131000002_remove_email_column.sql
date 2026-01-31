-- 1. Truncate the table to clear all existing "bad" data
TRUNCATE TABLE public.users CASCADE;

-- 2. Drop the email column from public.users as we don't need it anymore
ALTER TABLE public.users DROP COLUMN IF EXISTS email;

-- 3. Update the trigger function to stop trying to insert email
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.users (id, username, password_hash)
  VALUES (
    NEW.id,
    COALESCE(NEW.raw_user_meta_data->>'username', 'user_' || substr(NEW.id::text, 1, 8)),
    'managed_by_supabase_auth'
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
