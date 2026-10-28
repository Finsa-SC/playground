BEGIN;

-- Generic updated_at maintenance.
CREATE FUNCTION set_updated_at()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_categories_updated_at
BEFORE UPDATE ON categories
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_products_updated_at
BEFORE UPDATE ON products
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_orders_updated_at
BEFORE UPDATE ON orders
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_shipments_updated_at
BEFORE UPDATE ON shipments
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_disputes_updated_at
BEFORE UPDATE ON disputes
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_reviews_updated_at
BEFORE UPDATE ON reviews
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_reports_updated_at
BEFORE UPDATE ON reports
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- Feed: approved products ordered by publication time.
CREATE INDEX idx_products_public_feed
    ON products (published_at DESC, id DESC)
    WHERE status = 'approved';

-- Seller dashboard.
CREATE INDEX idx_products_seller_created
    ON products (seller_id, created_at DESC);

CREATE INDEX idx_products_moderation_queue
    ON products (submitted_at ASC, id ASC)
    WHERE status = 'pending';

CREATE INDEX idx_products_category_feed
    ON products (category_id, published_at DESC)
    WHERE status = 'approved';

CREATE INDEX idx_product_media_product_position
    ON product_media (product_id, position, id);

CREATE INDEX idx_product_moderation_product_created
    ON product_moderation_events (product_id, created_at DESC);

CREATE INDEX idx_product_moderation_actor_created
    ON product_moderation_events (moderator_id, created_at DESC);

-- Users and security audit.
CREATE INDEX idx_user_roles_role
    ON user_roles (role_id, user_id);

CREATE INDEX idx_security_events_user_created
    ON user_security_events (user_id, created_at DESC);

-- Orders.
CREATE INDEX idx_orders_buyer_created
    ON orders (buyer_id, created_at DESC);

CREATE INDEX idx_orders_seller_created
    ON orders (seller_id, created_at DESC);

CREATE INDEX idx_orders_status_created
    ON orders (status, created_at DESC);

CREATE INDEX idx_order_items_order
    ON order_items (order_id);

CREATE INDEX idx_shipments_order_created
    ON shipments (order_id, created_at DESC);

CREATE INDEX idx_order_evidence_order_created
    ON order_evidence (order_id, uploaded_at DESC);

CREATE INDEX idx_order_evidence_shipment
    ON order_evidence (shipment_id);

-- Ledger.
CREATE INDEX idx_ledger_transactions_order_created
    ON ledger_transactions (order_id, created_at DESC);

CREATE INDEX idx_ledger_entries_account_created
    ON ledger_entries (account_id, created_at DESC, id);

CREATE INDEX idx_ledger_entries_transaction
    ON ledger_entries (transaction_id);

-- Reviews, reports, and disputes.
CREATE INDEX idx_reviews_target_user_created
    ON reviews (target_user_id, created_at DESC)
    WHERE target_user_id IS NOT NULL;

CREATE INDEX idx_reviews_product_created
    ON reviews (product_id, created_at DESC)
    WHERE product_id IS NOT NULL;

CREATE INDEX idx_disputes_status_created
    ON disputes (status, created_at ASC);

CREATE INDEX idx_dispute_events_dispute_created
    ON dispute_events (dispute_id, created_at ASC);

CREATE INDEX idx_reports_status_created
    ON reports (status, created_at ASC);

CREATE INDEX idx_reports_operator_status
    ON reports (assigned_operator_id, status);

-- Prevent updates and deletes on append-only records.
CREATE FUNCTION prevent_record_mutation()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    RAISE EXCEPTION
        'Records in table % are append-only; % is not allowed',
        TG_TABLE_NAME,
        TG_OP;
END;
$$;

CREATE TRIGGER trg_ledger_transactions_immutable
BEFORE UPDATE OR DELETE ON ledger_transactions
FOR EACH ROW EXECUTE FUNCTION prevent_record_mutation();

CREATE TRIGGER trg_ledger_entries_immutable
BEFORE UPDATE OR DELETE ON ledger_entries
FOR EACH ROW EXECUTE FUNCTION prevent_record_mutation();

CREATE TRIGGER trg_product_moderation_events_immutable
BEFORE UPDATE OR DELETE ON product_moderation_events
FOR EACH ROW EXECUTE FUNCTION prevent_record_mutation();

CREATE TRIGGER trg_dispute_events_immutable
BEFORE UPDATE OR DELETE ON dispute_events
FOR EACH ROW EXECUTE FUNCTION prevent_record_mutation();

COMMIT;