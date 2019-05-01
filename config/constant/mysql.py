INSERT_ORDER = """INSERT IGNORE INTO history (identifier, currency_pair, direction, status, timestamp,  
                  initial_price, filled_price, initial_volume, filled_volume, description, tags) 
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
