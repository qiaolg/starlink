

def clear(db):
    command = "MATCH (node) DETACH DELETE node"
    db.execute_query(command)

def import_all_satellites(db):
        command = "MATCH (n :Satellite) RETURN n;"
        return db.execute_and_fetch(command)

def import_all_cities(db):
        command = "MATCH (n :City) RETURN n;"
        return db.execute_and_fetch(command)
        