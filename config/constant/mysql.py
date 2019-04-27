class MySQLConstant:
    INSERT_ORDER = """INSERT INTO history (identifier, currency_pair, direction, timestamp, status,  
                      initial_price, filled_price, initial_volume, filled_volume, description, tags) 
                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
