
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.animation import FuncAnimation
from IPython.display import HTML

# Set matplotlib backend for VS Code
plt.switch_backend('TkAgg')  # Or 'Qt5Agg' if you have PyQt5 installed

class Node:
    def __init__(self, value=None, node_type=None, children=None, name=""):
        self.value = value
        self.type = node_type  # 'max', 'min', or 'terminal'
        self.children = children if children else []
        self.name = name
        self.alpha = -np.inf
        self.beta = np.inf
        self.pruned = False
        self.visited = False
        self.current = False  # Is this the node being currently evaluated?

def build_sample_tree():
    """Build a balanced binary tree where each node has exactly 2 children"""
    # Terminal nodes (16 terminal nodes)
    terminals = [
        Node(value=-2, node_type='terminal', name="T1"),
        Node(value=4, node_type='terminal', name="T2"),
        Node(value=6, node_type='terminal', name="T3"),
        Node(value=-8, node_type='terminal', name="T4"),
        Node(value=-3, node_type='terminal', name="T5"),
        Node(value=-1, node_type='terminal', name="T6"),
        Node(value=7, node_type='terminal', name="T7"),
        Node(value=-5, node_type='terminal', name="T8"),
        Node(value=2, node_type='terminal', name="T9"),
        Node(value=-4, node_type='terminal', name="T10"),
        Node(value=-6, node_type='terminal', name="T11"),
        Node(value=8, node_type='terminal', name="T12"),
        Node(value=3, node_type='terminal', name="T13"),
        Node(value=1, node_type='terminal', name="T14"),
        Node(value=-7, node_type='terminal', name="T15"),
        Node(value=5, node_type='terminal', name="T16")
    ]
    
    # Third level (min nodes - 8 nodes)
    min_nodes3 = [
        Node(node_type='min', children=[terminals[0], terminals[1]], name="Min3-1"),
        Node(node_type='min', children=[terminals[2], terminals[3]], name="Min3-2"),
        Node(node_type='min', children=[terminals[4], terminals[5]], name="Min3-3"),
        Node(node_type='min', children=[terminals[6], terminals[7]], name="Min3-4"),
        Node(node_type='min', children=[terminals[8], terminals[9]], name="Min3-5"),
        Node(node_type='min', children=[terminals[10], terminals[11]], name="Min3-6"),
        Node(node_type='min', children=[terminals[12], terminals[13]], name="Min3-7"),
        Node(node_type='min', children=[terminals[14], terminals[15]], name="Min3-8")
    ]
    
    # Second level (max nodes - 4 nodes)
    max_nodes2 = [
        Node(node_type='max', children=[min_nodes3[0], min_nodes3[1]], name="Max2-1"),
        Node(node_type='max', children=[min_nodes3[2], min_nodes3[3]], name="Max2-2"),
        Node(node_type='max', children=[min_nodes3[4], min_nodes3[5]], name="Max2-3"),
        Node(node_type='max', children=[min_nodes3[6], min_nodes3[7]], name="Max2-4")
    ]
    
    # First level (min nodes - 2 nodes)
    min_nodes1 = [
        Node(node_type='min', children=[max_nodes2[0], max_nodes2[1]], name="Min1"),
        Node(node_type='min', children=[max_nodes2[2], max_nodes2[3]], name="Min2")
    ]
    
    # Root node (max)
    root = Node(node_type='max', children=min_nodes1, name="Root")
    
    return root

class AlphaBetaVisualizer:
    def __init__(self, root):
        self.root = root
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        self.G = nx.DiGraph()
        self.pos = {}
        self.animation_frames = []
        self.setup_tree()
        
    def setup_tree(self):
        """Initialize the tree structure and positions"""
        self.calculate_positions(self.root, 0, 0)
        self.build_graph()
        
    def calculate_positions(self, node, x_offset, depth):
        """Calculate node positions for visualization"""
        level_height = 4
        level_spacing = 2
        
        if not node.children:
            self.pos[node.name] = (x_offset, -depth * level_height)
            return 1
        
        total_width = 0
        child_x = x_offset
        for child in node.children:
            child_width = self.calculate_positions(child, child_x, depth + 1)
            child_x += child_width * level_spacing
            total_width += child_width * level_spacing
        
        if total_width > 0:
            self.pos[node.name] = ((x_offset + child_x - level_spacing) / 2, -depth * level_height)
        else:
            self.pos[node.name] = (x_offset, -depth * level_height)
        
        return max(total_width, 1)
    
    def build_graph(self):
        """Build the NetworkX graph representation"""
        def add_nodes(node):
            self.G.add_node(node.name)
            for child in node.children:
                self.G.add_edge(node.name, child.name)
                add_nodes(child)
        add_nodes(self.root)
    
    def capture_frame(self, title=""):
        """Capture the current state of the tree as an animation frame"""
        frame_data = {
            "title": title,
            "node_states": []
        }
        
        def collect_states(node):
            frame_data["node_states"].append({
                "name": node.name,
                "value": node.value,
                "alpha": node.alpha,
                "beta": node.beta,
                "pruned": node.pruned,
                "visited": node.visited,
                "current": node.current
            })
            for child in node.children:
                collect_states(child)
                
        collect_states(self.root)
        self.animation_frames.append(frame_data)
    
    def reset_node_states(self):
        """Reset all temporary node states"""
        def reset(node):
            node.current = False
            for child in node.children:
                reset(child)
        reset(self.root)
    
    def draw_frame(self, frame_idx):
        """Draw a single frame of the animation"""
        self.ax.clear()
        frame = self.animation_frames[frame_idx]
        
        # Draw edges first
        nx.draw_networkx_edges(self.G, self.pos, ax=self.ax, arrows=True)
        
        # Draw nodes with appropriate styling
        for node_data in frame["node_states"]:
            name = node_data["name"]
            
            # Determine node appearance
            if node_data["pruned"]:
                color = "gray"
                alpha = 0.3
            elif node_data["current"]:
                color = "gold"
                alpha = 1.0
            elif node_data["visited"]:
                alpha = 1.0
                if "terminal" in name:  # Simplified check for terminal nodes
                    color = "lightgreen"
                elif "max" in name or any(n.type == "max" for n in [self.root] if n.name == name):
                    color = "lightcoral"
                else:
                    color = "lightblue"
            else:
                alpha = 0.5
                color = "lightgray"
            
            # Determine shape
            if "terminal" in name:  # Simplified check
                shape = "s"
            elif "max" in name or any(n.type == "max" for n in [self.root] if n.name == name):
                shape = "^"
            else:
                shape = "v"
            
            # Draw the node
            nx.draw_networkx_nodes(
                self.G, self.pos, nodelist=[name],
                node_color=color, node_shape=shape,
                ax=self.ax, alpha=alpha, node_size=2000
            )
            
            # Create node label
            label = name
            if node_data["value"] is not None:
                label += f"\nVal: {node_data['value']}"
            if node_data["alpha"] != -np.inf:
                label += f"\nα: {node_data['alpha']}"
            if node_data["beta"] != np.inf:
                label += f"\nβ: {node_data['beta']}"
            
            # Draw label
            self.ax.text(
                self.pos[name][0], self.pos[name][1],
                label, ha='center', va='center',
                fontsize=8, bbox=dict(facecolor='white', alpha=0.7, edgecolor='none')
            )
        
        self.ax.set_title(frame["title"])
        self.ax.axis('off')
        self.fig.tight_layout()
    
    def animate(self):
        """Create and return the animation"""
        self.capture_frame("Initial Tree")
        
        # Run alpha-beta pruning while capturing frames
        self.alphabeta(self.root, visualize=True)
        
        # Create animation
        anim = FuncAnimation(
            self.fig, self.draw_frame,
            frames=len(self.animation_frames),
            interval=1000, repeat=False
        )
        
        # Display in VS Code
        plt.show()
        
        # Optionally save to file
        # anim.save('alphabeta.mp4', writer='ffmpeg', fps=1)
        
        return anim
    
    def alphabeta(self, node, depth=0, alpha=-np.inf, beta=np.inf, visualize=False):
        """Minimax with alpha-beta pruning that captures animation frames"""
        if visualize:
            self.reset_node_states()
            node.current = True
            title = f"Evaluating {node.name}"
            if node.type != 'terminal':
                title += f"\nα: {alpha if alpha != -np.inf else '-∞'}, β: {beta if beta != np.inf else '∞'}"
            self.capture_frame(title)
        
        if node.type == 'terminal':
            node.visited = True
            if visualize:
                self.reset_node_states()
                node.current = True
                self.capture_frame(f"Terminal {node.name}\nValue: {node.value}")
            return node.value
        
        if node.type == 'max':
            node.alpha = alpha
            node.beta = beta
            value = -np.inf
            for child in node.children:
                child_value = self.alphabeta(child, depth+1, alpha, beta, visualize)
                value = max(value, child_value)
                alpha = max(alpha, value)
                node.value = value
                node.alpha = alpha
                node.beta = beta
                node.visited = True
                
                if visualize:
                    self.reset_node_states()
                    node.current = True
                    self.capture_frame(
                        f"Updated {node.name}\n"
                        f"Value: {value}, α: {alpha if alpha != -np.inf else '-∞'}, "
                        f"β: {beta if beta != np.inf else '∞'}"
                    )
                
                if beta <= alpha:
                    for remaining_child in node.children[node.children.index(child)+1:]:
                        remaining_child.pruned = True
                        if visualize:
                            self.reset_node_states()
                            node.current = True
                            remaining_child.pruned = True
                            self.capture_frame(
                                f"Pruned {remaining_child.name}\n"
                                f"α: {alpha if alpha != -np.inf else '-∞'} ≥ "
                                f"β: {beta if beta != np.inf else '∞'}"
                            )
                    break  # Beta cutoff
            return value
        else:  # min node
            node.alpha = alpha
            node.beta = beta
            value = np.inf
            for child in node.children:
                child_value = self.alphabeta(child, depth+1, alpha, beta, visualize)
                value = min(value, child_value)
                beta = min(beta, value)
                node.value = value
                node.alpha = alpha
                node.beta = beta
                node.visited = True
                
                if visualize:
                    self.reset_node_states()
                    node.current = True
                    self.capture_frame(
                        f"Updated {node.name}\n"
                        f"Value: {value}, α: {alpha if alpha != -np.inf else '-∞'}, "
                        f"β: {beta if beta != np.inf else '∞'}"
                    )
                
                if beta <= alpha:
                    for remaining_child in node.children[node.children.index(child)+1:]:
                        remaining_child.pruned = True
                        if visualize:
                            self.reset_node_states()
                            node.current = True
                            remaining_child.pruned = True
                            self.capture_frame(
                                f"Pruned {remaining_child.name}\n"
                                f"β: {beta if beta != np.inf else '∞'} ≤ "
                                f"α: {alpha if alpha != -np.inf else '-∞'}"
                            )
                    break  
            return value

if __name__ == "__main__":
    print("Building game tree...")
    root = build_sample_tree()
    
    print("Creating visualizer...")
    visualizer = AlphaBetaVisualizer(root)
    
    print("Running alpha-beta pruning with animation...")
    animation = visualizer.animate()
    
    print("Animation complete! Close the window to exit.")
