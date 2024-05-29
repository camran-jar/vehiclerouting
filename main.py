import utility as utility
import loader as loader
import numpy as np

from utility import calculate_euclidean_distance

def main():
    # Paths to the data and solution files.
    #vrp_file = "n32-k5.vrp"  # "data/n80-k10.vrp"
    #sol_file = "n32-k5.sol"  # "data/n80-k10.sol"

    vrp_file = "n80-k10.vrp"
    sol_file = "n80-k10.sol"

    # Loading the VRP data file.
    px, py, demand, capacity, depot = loader.load_data(vrp_file)

    # Displaying to console the distance and visualizing the optimal VRP solution.
    vrp_best_sol = loader.load_solution(sol_file)
    best_distance = utility.calculate_total_distance(vrp_best_sol, px, py, depot)
    print("Best VRP Distance:", best_distance)
    utility.visualise_solution(vrp_best_sol, px, py, depot, "Optimal Solution")

    # Executing and visualizing the nearest neighbour VRP heuristic.
    nnh_solution = nearest_neighbour_heuristic(px, py, demand, capacity, depot)
    nnh_distance = utility.calculate_total_distance(nnh_solution, px, py, depot)
    print("Nearest Neighbour VRP Heuristic Distance:", nnh_distance)
    utility.visualise_solution(nnh_solution, px, py, depot, "Nearest Neighbour Heuristic")

    # Executing and visualizing the saving VRP heuristic.
    sh_solution = savings_heuristic(px, py, demand, capacity, depot)
    sh_distance = utility.calculate_total_distance(sh_solution, px, py, depot)
    print("Saving VRP Heuristic Distance:", sh_distance)
    utility.visualise_solution(sh_solution, px, py, depot, "Savings Heuristic")


def nearest_neighbour_heuristic(px, py, demand, capacity, depot):
    """
    Algorithm for the nearest neighbour heuristic to generate VRP solutions.

    :param px: List of X coordinates for each node.
    :param py: List of Y coordinates for each node.
    :param demand: List of each node's demand.
    :param capacity: Vehicle carrying capacity.
    :param depot: Depot.
    :return: List of vehicle routes (tours).
    """
    num_customers = len(px) - 1  # exclude the depot
    visited = [False] * (num_customers + 1)
    routes = []

    while True:
        current_route = [depot]
        current_load = 0
        current_node = depot

        while True:
            visited[current_node] = True
            nearest_node = -1
            nearest_distance = float('inf')

            for next_node in range(1, len(px)):
                if not visited[next_node] and demand[next_node] + current_load <= capacity:
                    distance = calculate_euclidean_distance(px, py, current_node, next_node)
                    if distance < nearest_distance:
                        nearest_distance = distance
                        nearest_node = next_node
            
            if nearest_node == -1:
                break

            current_route.append(nearest_node)
            current_load += demand[nearest_node]
            current_node = nearest_node

        current_route.append(depot)
        routes.append(current_route)

        if all(visited[1:]):
            break
    
    return routes

def savings_heuristic(px, py, demand, capacity, depot):
    """
    Algorithm for implementing the savings heuristic to generate VRP solutions.

    :param px: List of X coordinates for each node.
    :param py: List of Y coordinates for each node.
    :param demand: List of each node's demand.
    :param capacity: Vehicle carrying capacity.
    :param depot: Depot.
    :return: List of vehicle routes (tours).
    """
    num_customers = len(px) - 1  # exclude the depot

    #Calculate initial savings
    savings = []
    for i in range(1, num_customers + 1):
        for j in range(i + 1, num_customers + 1):
            savings_ij = calculate_euclidean_distance(px, py, depot, i) + \
                         calculate_euclidean_distance(px, py, depot, j) - \
                         calculate_euclidean_distance(px, py, i, j)
            savings.append((savings_ij, i, j))
    
    savings.sort(reverse=True, key=lambda x: x[0])
    
    # Initialise each customer with its own route
    routes = [[i] for i in range(1, num_customers + 1)]
    current_loads = {i: demand[i] for i in range(1, num_customers + 1)}
    
    def find_route(node, routes):
        for route in routes:
            if node in route:
                return route

    # Apply savings to merge routes
    for saving, i, j in savings:
        route_i = find_route(i, routes)
        route_j = find_route(j, routes)
        
        if route_i != route_j:
            load_i = sum(demand[node] for node in route_i)
            load_j = sum(demand[node] for node in route_j)
            if load_i + load_j <= capacity:
                routes.remove(route_i)
                routes.remove(route_j)
                new_route = route_i + route_j
                routes.append(new_route)
    
    final_routes = [[depot] + route + [depot] for route in routes]
    
    return final_routes

if __name__ == '__main__':
    main()