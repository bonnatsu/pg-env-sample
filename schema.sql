CREATE TABLE IF NOT EXISTS users (
	id SERIAL PRIMARY KEY,
	name TEXT NOT NULL,
	email TEXT UNIQUE NOT NULL,
	create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS products (
	id SERIAL PRIMARY KEY,
	product_code VARCHAR(50) UNIQUE NOT NULL,
	product_name VARCHAR(100) NOT NULL,
	unit         VARCHAR(10),
	created_at   TIMESTAMP DEFAULT now()
);


CREATE TABLE IF NOT EXISTS locations (
	location_id SERIAL primary key,
	location_code VARCHAR(50) UNIQUE NOT NULL,
	location_name VARCHAR(100),
	create_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS stocks (
	stock_id        SERIAL PRIMARY KEY,
	product_id      INT NOT NULL REFERENCES products(id),
	quantity        INT NOT NULL DEFAULT 0,

	-- 将来拡張用
	location_id     INT,
	lot_no          VARCHAR(50),
	expiration_date DATE,
	received_at     TIMESTAMP,

	created_at      TIMESTAMP DEFAULT now(),
	updated_at      TIMESTAMP DEFAULT now(),

	UNIQUE (product_id, location_id, lot_no, expiration_date)
);


CREATE TABLE IF NOT EXISTS stock_transactions (
	transaction_id SERIAL PRIMARY KEY,
	stock_id        INTEGER NOT NULL REFERENCES stocks(stock_id),
	txn_type        VARCHAR(10) NOT NULL CHECK (txn_type IN ('IN','OUT','ADJUST')),
	qty             INTEGER NOT NULL,
	reason          VARCHAR(20),
	ref_no          VARCHAR(50),
	created_at      TIMESTAMP DEFAULT now()
);


CREATE TABLE IF NOT EXISTS stock_movements (
	id SERIAL PRIMARY KEY,
	product_id INT NOT NULL,
	movement_type VARCHAR(20) NOT NULL, -- IN/OUT
	quantity INT NOT NULL,
	before_qty INT NOT NULL,
	after_qty INT NOT NULL,
	reason VARCHAR(50), --入出庫理由
	create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);