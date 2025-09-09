import osmnx as ox
import networkx as nx
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Load the map for Algeria
print("Downloading map data... (this may take a few seconds)")
graph = ox.graph_from_place("Béjaïa, Algeria", network_type="drive")

# Create main window
root = tk.Tk()
root.title("Shortest Path Finder - Algeria")
root.geometry("800x600")

# Create Matplotlib figure
fig, ax = plt.subplots(figsize=(8, 6))
ox.plot_graph(graph, show=False, close=False, edge_color="gray", node_size=0, ax=ax)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack()

selected_points = []

def onclick(event):
    x, y = event.xdata, event.ydata
    if x is None or y is None:
        return
    selected_points.append((y, x))
    print(f"Selected point: ({y}, {x})")
    ax.scatter(x, y, c='red', s=100, zorder=5)
    canvas.draw()
    if len(selected_points) == 2:
        calculate_and_plot_shortest_path(selected_points)

def calculate_and_plot_shortest_path(points):
    node1 = ox.distance.nearest_nodes(graph, points[0][1], points[0][0])  
    node2 = ox.distance.nearest_nodes(graph, points[1][1], points[1][0])  
    try:
        shortest_path = nx.astar_path(graph, node1, node2, weight="length")
    except nx.NetworkXNoPath:
        messagebox.showerror("Error", "No path found between the selected locations.")
        return
    ox.plot_graph_route(graph, shortest_path, route_color="blue", route_linewidth=3, ax=ax, show=False, close=False)
    for point in points:
        ax.scatter(point[1], point[0], c='red', s=100, zorder=5)
    canvas.draw()

def reset():
    global selected_points
    selected_points = []
    ax.clear()
    ox.plot_graph(graph, show=False, close=False, edge_color="gray", node_size=0, ax=ax)
    canvas.draw()

# Connect click event to Matplotlib
fig.canvas.mpl_connect('button_press_event', onclick)

# Reset button
reset_button = tk.Button(root, text="Reset", command=reset)
reset_button.pack()

# Run the GUI
print("Click on the map to select two locations.")
root.mainloop()