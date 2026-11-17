-- Incremental PostgreSQL migration for v2 order idempotency.
-- Review existing legacy rows before making request_hash NOT NULL.

ALTER TABLE order_requests
  ADD COLUMN IF NOT EXISTS request_hash VARCHAR(64);

COMMENT ON COLUMN order_requests.request_hash IS
  'SHA-256 of the canonical checkout payload; NULL is allowed only for legacy rows.';

-- The idempotency key constraint is created by the original schema/model:
-- uq_order_requests_idempotency_key. Do not drop or recreate it here.
