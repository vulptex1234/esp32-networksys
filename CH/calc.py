import math

def sim_score(current_head, node, battery_weight=1.0, comm_weight=1.0, battery_penalty_factor=2, comm_penalty_factor=2):
    battery_current, comm_nodes_current = current_head
    battery_node, comm_nodes_node = node

    #calculate diff battery
    if battery_node < battery_current:
        battery_diff = (battery_current - battery_node) * battery_penalty_factor
    else:
        battery_diff = battery_current - battery_node

    #calculate diff communicatable nodes
    if comm_nodes_node < comm_nodes_current:
        comm_nodes_diff = (comm_nodes_current - comm_nodes_node) * comm_penalty_factor
    else:
        comm_nodes_diff = comm_nodes_current - comm_nodes_node

    #euclidian distance
    weighted_distance = math.sqrt((battery_diff * battery_weight)**2 + (comm_nodes_diff * comm_weight)**2)
    return weighted_distance