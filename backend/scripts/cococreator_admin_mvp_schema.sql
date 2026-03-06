-- =========================================================
-- CocoCreator Admin MVP - PostgreSQL Final Schema
-- =========================================================

-- =========================================================
-- 1. USERS / AUTH
-- =========================================================

CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'admin', -- super_admin, admin, operator, finance
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    last_login_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_is_active ON users(is_active);

CREATE TABLE user_sessions (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    refresh_token_hash VARCHAR(255) NOT NULL,
    ip_address VARCHAR(100),
    user_agent TEXT,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_user_sessions_user_id ON user_sessions(user_id);
CREATE INDEX idx_user_sessions_expires_at ON user_sessions(expires_at);

-- =========================================================
-- 2. CREATORS
-- =========================================================

CREATE TABLE creators (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    display_name VARCHAR(150),
    email VARCHAR(255),
    phone VARCHAR(50),
    country_code VARCHAR(10),
    platform VARCHAR(50), -- youtube, tiktok, instagram
    channel_name VARCHAR(150),
    channel_url TEXT,
    subscribers_count BIGINT NOT NULL DEFAULT 0,
    avg_views BIGINT NOT NULL DEFAULT 0,
    category VARCHAR(100), -- mukbang, food, beauty, fitness
    status VARCHAR(50) NOT NULL DEFAULT 'lead', -- lead, contacted, negotiating, partner, inactive
    audience_summary TEXT,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_creators_status ON creators(status);
CREATE INDEX idx_creators_country_code ON creators(country_code);
CREATE INDEX idx_creators_category ON creators(category);
CREATE INDEX idx_creators_platform ON creators(platform);

CREATE TABLE creator_contacts (
    id BIGSERIAL PRIMARY KEY,
    creator_id BIGINT NOT NULL REFERENCES creators(id) ON DELETE CASCADE,
    contact_type VARCHAR(50) NOT NULL, -- email, instagram, whatsapp, manager
    contact_value VARCHAR(255) NOT NULL,
    is_primary BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_creator_contacts_creator_id ON creator_contacts(creator_id);

-- =========================================================
-- 3. BRANDS
-- =========================================================

CREATE TABLE brands (
    id BIGSERIAL PRIMARY KEY,
    creator_id BIGINT NOT NULL REFERENCES creators(id) ON DELETE RESTRICT,
    name VARCHAR(150) NOT NULL,
    slug VARCHAR(150) UNIQUE,
    description TEXT,
    status VARCHAR(50) NOT NULL DEFAULT 'planning', -- planning, active, paused, archived
    launch_date DATE,
    logo_url TEXT,
    brand_story TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_brands_creator_id ON brands(creator_id);
CREATE INDEX idx_brands_status ON brands(status);

-- =========================================================
-- 4. PRODUCT TEMPLATES
-- =========================================================

CREATE TABLE product_templates (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    category VARCHAR(100) NOT NULL, -- sauce, ramen_sauce, snack
    description TEXT,
    base_cost NUMERIC(12,2) NOT NULL DEFAULT 0,
    suggested_price NUMERIC(12,2) NOT NULL DEFAULT 0,
    currency VARCHAR(10) NOT NULL DEFAULT 'USD',
    halal_supported BOOLEAN NOT NULL DEFAULT FALSE,
    status VARCHAR(50) NOT NULL DEFAULT 'active', -- active, inactive
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_product_templates_category ON product_templates(category);
CREATE INDEX idx_product_templates_status ON product_templates(status);

CREATE TABLE template_flavors (
    id BIGSERIAL PRIMARY KEY,
    product_template_id BIGINT NOT NULL REFERENCES product_templates(id) ON DELETE CASCADE,
    flavor_name VARCHAR(100) NOT NULL,
    spice_level VARCHAR(50), -- mild, medium, hot, extreme
    description TEXT,
    additional_cost NUMERIC(12,2) NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_template_flavors_template_id ON template_flavors(product_template_id);

-- =========================================================
-- 5. FACTORIES / OEM
-- =========================================================

CREATE TABLE factories (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    country_code VARCHAR(10),
    website_url TEXT,
    contact_name VARCHAR(100),
    contact_email VARCHAR(255),
    contact_phone VARCHAR(50),
    halal_certified BOOLEAN NOT NULL DEFAULT FALSE,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_factories_country_code ON factories(country_code);

CREATE TABLE factory_capabilities (
    id BIGSERIAL PRIMARY KEY,
    factory_id BIGINT NOT NULL REFERENCES factories(id) ON DELETE CASCADE,
    category VARCHAR(100) NOT NULL, -- sauce, snack, ramen_sauce
    moq INTEGER,
    lead_time_days INTEGER,
    estimated_unit_cost NUMERIC(12,2),
    currency VARCHAR(10) NOT NULL DEFAULT 'USD',
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_factory_capabilities_factory_id ON factory_capabilities(factory_id);
CREATE INDEX idx_factory_capabilities_category ON factory_capabilities(category);

-- =========================================================
-- 6. PRODUCTS
-- =========================================================

CREATE TABLE products (
    id BIGSERIAL PRIMARY KEY,
    brand_id BIGINT NOT NULL REFERENCES brands(id) ON DELETE CASCADE,
    product_template_id BIGINT REFERENCES product_templates(id) ON DELETE SET NULL,
    template_flavor_id BIGINT REFERENCES template_flavors(id) ON DELETE SET NULL,
    factory_id BIGINT REFERENCES factories(id) ON DELETE SET NULL,
    name VARCHAR(150) NOT NULL,
    sku VARCHAR(100) UNIQUE,
    category VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'idea', -- idea, research, sampling, negotiation, production, launch, active, paused
    cogs NUMERIC(12,2) NOT NULL DEFAULT 0,
    shipping_cost NUMERIC(12,2) NOT NULL DEFAULT 0,
    platform_fee_rate NUMERIC(5,2) NOT NULL DEFAULT 0,
    retail_price NUMERIC(12,2) NOT NULL DEFAULT 0,
    currency VARCHAR(10) NOT NULL DEFAULT 'USD',
    halal_required BOOLEAN NOT NULL DEFAULT FALSE,
    halal_status VARCHAR(50) DEFAULT 'not_started', -- not_started, in_progress, approved, not_required
    package_type VARCHAR(100),
    package_size VARCHAR(100),
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_products_brand_id ON products(brand_id);
CREATE INDEX idx_products_template_id ON products(product_template_id);
CREATE INDEX idx_products_factory_id ON products(factory_id);
CREATE INDEX idx_products_status ON products(status);
CREATE INDEX idx_products_category ON products(category);

CREATE TABLE product_pipeline_logs (
    id BIGSERIAL PRIMARY KEY,
    product_id BIGINT NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    stage VARCHAR(50) NOT NULL, -- idea, research, sampling, oem_negotiation, production, launch
    note TEXT,
    changed_by_user_id BIGINT REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_product_pipeline_logs_product_id ON product_pipeline_logs(product_id);
CREATE INDEX idx_product_pipeline_logs_stage ON product_pipeline_logs(stage);
CREATE INDEX idx_product_pipeline_logs_changed_by_user_id ON product_pipeline_logs(changed_by_user_id);

-- =========================================================
-- 7. SALES CHANNELS / LISTINGS
-- =========================================================

CREATE TABLE sales_channels (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL, -- shopee, tiktok_shop, shopify
    country_code VARCHAR(10),
    status VARCHAR(50) NOT NULL DEFAULT 'active',
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE product_listings (
    id BIGSERIAL PRIMARY KEY,
    product_id BIGINT NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    sales_channel_id BIGINT NOT NULL REFERENCES sales_channels(id) ON DELETE RESTRICT,
    listing_name VARCHAR(150) NOT NULL,
    listing_url TEXT,
    listing_price NUMERIC(12,2) NOT NULL,
    currency VARCHAR(10) NOT NULL DEFAULT 'USD',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX uq_product_listings_product_channel
ON product_listings(product_id, sales_channel_id);

-- =========================================================
-- 8. ORDERS
-- =========================================================

CREATE TABLE orders (
    id BIGSERIAL PRIMARY KEY,
    product_id BIGINT NOT NULL REFERENCES products(id) ON DELETE RESTRICT,
    sales_channel_id BIGINT REFERENCES sales_channels(id) ON DELETE SET NULL,
    order_number VARCHAR(100) UNIQUE,
    order_date TIMESTAMP NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    gross_revenue NUMERIC(12,2) NOT NULL DEFAULT 0,
    platform_fee_amount NUMERIC(12,2) NOT NULL DEFAULT 0,
    shipping_fee_amount NUMERIC(12,2) NOT NULL DEFAULT 0,
    net_revenue NUMERIC(12,2) NOT NULL DEFAULT 0,
    currency VARCHAR(10) NOT NULL DEFAULT 'USD',
    order_status VARCHAR(50) NOT NULL DEFAULT 'paid', -- paid, shipped, delivered, canceled, refunded
    customer_country_code VARCHAR(10),
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_orders_product_id ON orders(product_id);
CREATE INDEX idx_orders_order_date ON orders(order_date);
CREATE INDEX idx_orders_status ON orders(order_status);

-- =========================================================
-- 9. CREATOR DEALS / REVENUE SHARE
-- =========================================================

CREATE TABLE creator_deals (
    id BIGSERIAL PRIMARY KEY,
    creator_id BIGINT NOT NULL REFERENCES creators(id) ON DELETE CASCADE,
    brand_id BIGINT REFERENCES brands(id) ON DELETE CASCADE,
    revenue_share_type VARCHAR(50) NOT NULL DEFAULT 'profit_share', -- profit_share, revenue_share, fixed_fee
    creator_share_rate NUMERIC(5,2) NOT NULL DEFAULT 0,
    platform_share_rate NUMERIC(5,2) NOT NULL DEFAULT 0,
    contract_start_date DATE,
    contract_end_date DATE,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_creator_deals_creator_id ON creator_deals(creator_id);
CREATE INDEX idx_creator_deals_brand_id ON creator_deals(brand_id);

-- =========================================================
-- 10. PAYOUTS
-- =========================================================

CREATE TABLE payouts (
    id BIGSERIAL PRIMARY KEY,
    creator_id BIGINT NOT NULL REFERENCES creators(id) ON DELETE RESTRICT,
    brand_id BIGINT REFERENCES brands(id) ON DELETE SET NULL,
    product_id BIGINT REFERENCES products(id) ON DELETE SET NULL,
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    total_revenue NUMERIC(12,2) NOT NULL DEFAULT 0,
    creator_share_amount NUMERIC(12,2) NOT NULL DEFAULT 0,
    currency VARCHAR(10) NOT NULL DEFAULT 'USD',
    payment_status VARCHAR(50) NOT NULL DEFAULT 'pending', -- pending, paid, failed
    paid_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_payouts_creator_id ON payouts(creator_id);
CREATE INDEX idx_payouts_payment_status ON payouts(payment_status);

-- =========================================================
-- 11. NOTES
-- =========================================================

CREATE TABLE notes (
    id BIGSERIAL PRIMARY KEY,
    entity_type VARCHAR(50) NOT NULL, -- creator, brand, product, factory
    entity_id BIGINT NOT NULL,
    content TEXT NOT NULL,
    created_by_user_id BIGINT REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_notes_entity ON notes(entity_type, entity_id);
CREATE INDEX idx_notes_created_by_user_id ON notes(created_by_user_id);
