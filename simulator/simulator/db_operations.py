from simulator import utils


def create_data(tx, moving_objects_dict_by_id, cities):
    tx.run("BEGIN")

    for moving_object_id in moving_objects_dict_by_id.keys():
        moving_object = moving_objects_dict_by_id[moving_object_id]
        command = "CREATE (n:Satellite {id:'" + str(moving_object.id) + \
            "', x:" + str(moving_object.x) + \
            ", y:" + str(moving_object.y) + \
            ", z:" + str(moving_object.z) + "})"
        tx.run(command)

    for city in cities:
        command = "CREATE (n:City {id:'" + str(city.id) + \
            "', name:'" + str(city.name) + \
            "', x:" + str(city.x) + \
            ", y:" + str(city.y) + "})"
        tx.run(command)

    for city in cities:
        for key in city.moving_objects_tt_dict:
            command = "MATCH (a:City { id:'" + str(city.id) + \
                "'}),(b:Satellite) WHERE b.id = '" + str(key) + \
                "' CREATE (b)-[r:VISIBLE_FROM { transmission_time: " + \
                str(city.moving_objects_tt_dict[key]) + " }]->(a)"
            tx.run(command)

    for moving_object_id in moving_objects_dict_by_id.keys():
        moving_object = moving_objects_dict_by_id[moving_object_id]
        command = "MATCH (a:Satellite),(b:Satellite) WHERE b.id = '" + str(moving_object.laser_left_id) + "' AND a.id = '" + str(moving_object.id) + \
            "' CREATE (a)-[r:CONNECTED_TO { transmission_time: " + \
            str(moving_object.laser_left_transmission_time) + " }]->(b)"
        tx.run(command)

        command = "MATCH (a:Satellite),(b:Satellite) WHERE b.id = '" + str(moving_object.laser_right_id) + "' AND a.id = '" + str(moving_object.id) + \
            "' CREATE (a)-[r:CONNECTED_TO { transmission_time: " + \
            str(moving_object.laser_right_transmission_time) + " }]->(b)"
        tx.run(command)

        if hasattr(moving_object, 'laser_up_id'):
            command = "MATCH (a:Satellite),(b:Satellite) WHERE b.id = '" + str(moving_object.laser_up_id) + "' AND a.id = '" + str(moving_object.id) + \
                "' CREATE (a)-[r:CONNECTED_TO { transmission_time: " + \
                str(moving_object.laser_up_transmission_time) + " }]->(b)"
            tx.run(command)

        if hasattr(moving_object, 'laser_down_id'):
            command = "MATCH (a:Satellite),(b:Satellite) WHERE b.id = '" + str(moving_object.laser_down_id) + "' AND a.id = '" + str(moving_object.id) + \
                "' CREATE (a)-[r:CONNECTED_TO { transmission_time: " + \
                str(moving_object.laser_down_transmission_time) + " }]->(b)"
            tx.run(command)

    tx.run("COMMIT")


def update_data(tx, moving_objects_dict_by_id, cities):
    tx.run("BEGIN")

    for city in cities:
        command = "MATCH (b:Satellite)-[r]->(a:City {id:'" + \
            str(city.id) + "'}) DELETE r"
        tx.run(command)
        for key in city.moving_objects_tt_dict:
            command = "MATCH (a:City { id:'" + str(city.id) + \
                "'}),(b:Satellite) WHERE b.id = '" + str(key) + \
                "' CREATE (b)-[r:VISIBLE_FROM { transmission_time: " + \
                str(city.moving_objects_tt_dict[key]) + " }]->(a)"
            tx.run(command)

    for moving_object_id in moving_objects_dict_by_id.keys():
        moving_object = moving_objects_dict_by_id[moving_object_id]
        command = "MATCH (a:Satellite { id:'" + str(moving_object.id) + \
            "'}) SET a.x=" + str(moving_object.x) + \
            ", a.y=" + str(moving_object.y) + \
            ", a.z=" + str(moving_object.z)
        tx.run(command)

        command = "MATCH (a:Satellite {id:'" + str(moving_object.id) + "'})-[r]-(b:Satellite {id:'" + str(moving_object.laser_left_id) + "'})" + \
            " SET r.transmission_time=" + \
            str(moving_object.laser_left_transmission_time)
        tx.run(command)

        command = "MATCH (a:Satellite {id:'" + str(moving_object.id) + "'})-[r]-(b:Satellite {id:'" + str(moving_object.laser_right_id) + "'})" + \
            " SET r.transmission_time=" + \
            str(moving_object.laser_right_transmission_time)
        tx.run(command)

        if hasattr(moving_object, 'laser_up_id'):
            command = "MATCH (a:Satellite {id:'" + str(moving_object.id) + "'})-[r]-(b:Satellite {id:'" + str(moving_object.laser_up_id) + "'})" + \
                " SET r.transmission_time=" + \
                str(moving_object.laser_up_transmission_time)
            tx.run(command)

        if hasattr(moving_object, 'laser_down_id'):
            command = "MATCH (a:Satellite {id:'" + str(moving_object.id) + "'})-[r]-(b:Satellite {id:'" + str(moving_object.laser_down_id) + "'})" + \
                " SET r.transmission_time=" + \
                str(moving_object.laser_down_transmission_time)
            tx.run(command)

    tx.run("COMMIT")


def clear(db):
    command = "MATCH (node) DETACH DELETE node"
    db.execute_query(command)
