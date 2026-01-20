from tkinter import *
from tkinter import messagebox
from collections import deque
import time

root = Tk()
root.title("8-Puzzle Solver")
root.geometry("920x560")
root.configure(bg="#0f1116")
root.resizable(False, False)

# GLOBAL
solution_path = []
step_index = 0
animating = False

def is_valid_state(state):
    return sorted(state) == list("012345678")

def is_solvable(state, goal):
    def inversions(s):
        arr = [int(x) for x in s if x != "0"]
        return sum(arr[i] > arr[j] for i in range(len(arr)) for j in range(i+1, len(arr)))
    return inversions(state) % 2 == inversions(goal) % 2

def get_neighbors(state):
    neighbors = []
    idx = state.index("0")
    r, c = divmod(idx, 3)
    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        nr, nc = r+dr, c+dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            ni = nr*3 + nc
            s = list(state)
            s[idx], s[ni] = s[ni], s[idx]
            neighbors.append("".join(s))
    return neighbors

def bfs(start, goal):
    start_time = time.time()
    q = deque([(start, [start])])
    visited = {start}
    nodes = 0
    while q:
        state, path = q.popleft()
        nodes += 1
        if state == goal:
            return path, nodes, time.time() - start_time
        for n in get_neighbors(state):
            if n not in visited:
                visited.add(n)
                q.append((n, path + [n]))
    return None, nodes, time.time() - start_time

def draw_board(state):
    for i, v in enumerate(state):
        tile = tiles[i]
        if v == "0":
            tile.config(text="", bg="#0f1116")
        else:
            tile.config(text=v, bg="#2196f3")

def animate_solution():
    global step_index, animating
    if step_index >= len(solution_path):
        animating = False
        return
    draw_board(solution_path[step_index])
    step_label.config(text=f"Step {step_index}/{len(solution_path)-1}")
    step_index += 1
    root.after(550, animate_solution)

def solve():
    global solution_path, step_index, animating
    if animating:
        return
    start = initial_entry.get().strip()
    goal = goal_entry.get().strip()
    if len(start) != 9 or len(goal) != 9:
        messagebox.showerror("Error", "State must contain exactly 9 digits")
        return
    if not is_valid_state(start) or not is_valid_state(goal):
        messagebox.showerror("Error", "State must contain digits 0-8 exactly once")
        return
    if not is_solvable(start, goal):
        messagebox.showerror("Unsolvable", "This puzzle cannot be solved to the given goal")
        return
    solution_path, nodes, runtime = bfs(start, goal)
    step_index = 0
    animating = True
    result_label.config(
        text=f"Runtime: {runtime:.3f}s\n"
             f"Nodes Expanded: {nodes}\n"
             f"Search Depth: {len(solution_path)-1}\n"
             f"Path Cost: {len(solution_path)-1}"
    )
    animate_solution()

left = Frame(root, bg="#0f1116")
left.pack(side=LEFT, padx=20, pady=20)

Label(left, text="Initial State", fg="white", bg="#0f1116").pack(anchor="w")
initial_entry = Entry(left, width=25)
initial_entry.insert(0, "410263758")
initial_entry.pack(pady=5)

Label(left, text="Goal State", fg="white", bg="#0f1116").pack(anchor="w")
goal_entry = Entry(left, width=25)
goal_entry.insert(0, "012345678")
goal_entry.pack(pady=5)

Button(left, text="Solve Puzzle", width=20, command=solve).pack(pady=25)

center = Frame(root, bg="#0f1116")
center.pack(side=LEFT, padx=50)

Label(center, text="8-Puzzle Solver", fg="white", bg="#0f1116",
      font=("Arial", 22, "bold")).pack(pady=20)

board = Frame(center, bg="#0f1116")
board.pack()

tiles = []
for i in range(9):
    lbl = Label(
        board,
        text="",
        width=6,
        height=3,
        font=("Arial", 22, "bold"),
        fg="white",
        bg="#2196f3"
    )
    lbl.grid(row=i//3, column=i%3, padx=6, pady=6)
    tiles.append(lbl)

step_label = Label(center, text="Step 0/0", fg="white", bg="#0f1116")
step_label.pack(pady=10)

right = Frame(root, bg="#0f1116")
right.pack(side=RIGHT, padx=20)

Label(right, text="Results", fg="#4fa3ff", bg="#0f1116",
      font=("Arial", 18, "bold")).pack(pady=10)

result_label = Label(
    right,
    text="Pending user input...",
    fg="white",
    bg="#0f1116",
    justify="left"
)
result_label.pack(anchor="w")

draw_board("410263758")
root.mainloop()