-- Crear tabla products en Supabase
-- Ejecutar esto en Supabase → SQL Editor

CREATE TABLE IF NOT EXISTS products (
  id BIGSERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  cat TEXT NOT NULL,
  score INTEGER NOT NULL,
  change TEXT,
  change_num INTEGER,
  plts JSONB DEFAULT '[]',
  margin INTEGER,
  margin_str TEXT,
  hot BOOLEAN DEFAULT false,
  regions JSONB DEFAULT '[]',
  comp TEXT,
  price_min INTEGER,
  price_str TEXT,
  history JSONB DEFAULT '[]',
  rank INTEGER,
  suppliers JSONB DEFAULT '[]',
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Habilitar acceso público de lectura
ALTER TABLE products ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Public read" ON products
  FOR SELECT USING (true);

CREATE POLICY "Service write" ON products
  FOR ALL USING (auth.role() = 'service_role');
