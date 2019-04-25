CREATE TABLE IF NOT EXISTS history (
  identifier varchar(30) NOT NULL,
  currency_pair varchar(20) NOT NULL,
  direction varchar(10) NOT NULL,
  timestamp varchar(30) NOT NULL,
  status varchar(30) NOT NULL,
  initial_price decimal(20,5) NOT NULL,
  initial_volume decimal(20,8) NOT NULL,
  filled_price decimal(20,5) NOT NULL,
  filled_volume decimal(20,8) NOT NULL,
  description text NOT NULL,
  tags varchar(255) NOT NULL,
  PRIMARY KEY (identifier,status)
);