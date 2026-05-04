import matplotlib.pyplot as plt
from collections import deque
import matplotlib.colors as mcolors
from collections import defaultdict
from matplotlib.animation import FuncAnimation

def animate_heatmap_then_path(distance, path, n=8):
    fig, ax = plt.subplots()

    max_depth = max(distance.values())

    for x in range(n):
        for y in range(n):
            base_color = "white" if (x + y) % 2 == 0 else "lightgray"
            ax.add_patch(plt.Rectangle((x, y), 1, 1, color=base_color))

    ax.set_xlim(0, n)
    ax.set_ylim(0, n)   # correct chess orientation
    ax.set_aspect('equal')
    ax.axis('off')

    def draw_board(upto):

        # draw heat map in animation
        for x in range(n):
            for y in range(n):
                d = distance.get((x, y), None)

                if d is not None and d <= upto:

                    if d == 0:
                        color = "darkgreen"
                    elif d == 1:
                        color = "green"
                    elif d == 2:
                        color = "yellowgreen"
                    elif d == 3:
                        color = "yellow"
                    elif d == 4:
                        color = "orange"
                    elif d == 5:
                        color = "darkorange"
                    else:
                        color = "red"

                    ax.add_patch(plt.Rectangle((x, y), 1, 1, color=color, alpha=0.6))

                    ax.text(
                    x + 0.5, y + 0.5,
                    str(d),
                    ha='center',
                    va='center',
                    fontsize=10
                    )

        # draw knights path when heat map is completed
        if upto == max_depth:
            xs = [p[0] + 0.5 for p in path]
            ys = [p[1] + 0.5 for p in path]

            ax.plot(xs, ys, color="blue", linewidth=2, marker='o')

            # knight start/end
            sx, sy = path[0]
            ex, ey = path[-1]

            ax.text(sx + 0.5, sy + 0.5, "♞", fontsize=20, ha='center', va='center')
            ax.text(ex + 0.5, ey + 0.5, "♞", fontsize=20, ha='center', va='center')


    # animation of BFS
    ani = FuncAnimation(
        fig,
        draw_board,
        frames=range(max_depth + 1),
        interval=1200,
        repeat=False
    )

    plt.show()

def visualize_heatmap_with_path(distance, path, n=8):
    fig, ax = plt.subplots()

    # draw heat map layers
    for x in range(n):
        for y in range(n):
            d = distance.get((x, y), None)

            if d is None:
                color = "black"
            elif d == 0:
                color = "darkgreen"
            elif d == 1:
                color = "green"
            elif d == 2:
                color = "yellowgreen"
            elif d == 3:
                color = "yellow"
            else:
                color = "orange"

            ax.add_patch(plt.Rectangle((x, y), 1, 1, color=color))

            # labels
            if d is not None:
                ax.text(x + 0.5, y + 0.5, str(d),
                        ha='center', va='center', fontsize=8)

    # draw shortest path for the knight
    xs = [p[0] + 0.5 for p in path]
    ys = [p[1] + 0.5 for p in path]

    ax.plot(xs, ys, color="blue", linewidth=2, marker='o')

    # mark start and end of the knight with knight picture
    sx, sy = path[0]
    ex, ey = path[-1]

    ax.text(sx + 0.5, sy + 0.5, "♞", fontsize=20, ha='center', va='center')
    ax.text(ex + 0.5, ey + 0.5, "♞", fontsize=20, ha='center', va='center')

    # formatting
    ax.set_xlim(0, n)
    ax.set_ylim(n, 0)
    ax.set_aspect('equal')
    ax.axis('off')

    plt.show()




def chess_to_coords(pos):
    col = ord(pos[0].lower()) - ord('a')
    row = int(pos[1]) - 1
    return (col, row)

user_start = chess_to_coords(input("Start position(ex: A1): "))
user_end = chess_to_coords(input("End posistion(ex: H8): "))

def knight_moves_BFS(start, end, n = 8):
    possible_moves = [ (2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1)]

    # queue in order to have first in first out in order to make sure that the first path that finds the end in the path that we return
    queue = deque([start])
    
    # a set to insure that we do not visit squares that we already visited and prevent loops
    visited = set([start])

    # a parent dicionary so we can store the previos squares visited in the path when we inevitably hit the end square we are looking for
    parent = {start: None}

    # in order to show the heat map for the BFS steps we will need a distance variable connected to each move. This will help visualize the algorithm
    distance = {start: 0}
    
    #loop in order to run through all the possible possitions of the knight
    while queue:
        x, y = queue.popleft()
        
        # stop early if we reach target possition
        if (x, y) == end:
            break
        
        #loop to make all possible next moves from the current queue possition and store the new possition, previous possition, and distance from the starting possition
        for dx, dy in possible_moves:
            nx, ny = x + dx, y + dy
            
            # constraint to make sure we do not leave the size of the chess board
            if 0 <= nx < n and 0 <= ny < n:
                next_node = (nx, ny)
                
                # checking to make sure we are not revisiting previously visited squares
                if next_node not in visited:
                    visited.add(next_node)
                    queue.append(next_node)
                    
                    # store BFS tree info
                    parent[next_node] = (x, y)
                    distance[next_node] = distance[(x, y)] + 1
    
    # Return parent in order to show the shortest path with visualize_knight_path(path, n=8), and distance to use in visualize_heatmap
    return parent, distance

# running BFS with the user inputs
shortest_path_map, heat_map_distances = knight_moves_BFS(user_start, user_end)

def reconstruct_path(parent, start, end):
    path = []
    current = end
    
    while current is not None:
        path.append(current)
        current = parent[current]
    
    return path[::-1]

# reconstructing the final path and reversing it in order to visualize it from start to finish not in reverse becuase popping the path from the dictionary will be end to start
final_path = reconstruct_path(shortest_path_map, user_start, user_end)

# visualize_heatmap_with_path(heat_map_distances, final_path)
animate_heatmap_then_path(heat_map_distances, final_path)



