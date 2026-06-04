import tkinter as tk
import threading
import time
import random

# ==========================================
# 配色方案 (大地色系 & 暗色主題)
# ==========================================
BG_MAIN = "#260101"         # 深棕黑 (背景)
BG_CANVAS = "#150000"       # 極深黑 (畫布)
FG_TEXT = "#BF863F"         # 芥末金 (文字)
FG_RUNNING = "#A6633C"      # 鐵鏽橘 (狀態：執行中)
FG_DONE = "#525934"         # 橄欖綠 (狀態：完成)
FG_WINNER = "#BF863F"       # 芥末金 (結果顯示)

# ==========================================
# 字體優化 (現代簡約風格)
# ==========================================
FONT_TITLE = ("Verdana", 20, "bold")      
FONT_UI = ("Menlo", 12)                   
FONT_BOLD = ("Menlo", 12, "bold")
FONT_RESULT = ("Verdana", 14, "bold")

# 全局數據
N = 50
data_sel, data_bub, data_quick = [], [], []
algo_times = {"Selection": 0, "Bubble": 0, "Quick": 0}

# ==========================================
# 第一部分：演算法核對 (完全遵循老師講義)
# ==========================================

# 1. 選擇排序
def selection_sort(arr, canvas, status_label, time_label, color):
    start_time = time.perf_counter()
    n = len(arr)
    status_label.config(text="[RUNNING]", fg=FG_RUNNING)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        draw_mini_array(canvas, arr, color)
        time.sleep(0.015)
    elapsed = time.perf_counter() - start_time
    algo_times["Selection"] = elapsed
    status_label.config(text="[ DONE  ]", fg=FG_DONE)
    time_label.config(text=f"{elapsed:.4f} sec")

# 2. 泡泡排序
def bubble_sort(arr, canvas, status_label, time_label, color):
    start_time = time.perf_counter()
    n = len(arr)
    status_label.config(text="[RUNNING]", fg=FG_RUNNING)
    for i in range(n - 1, 0, -1):
        for j in range(0, i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                draw_mini_array(canvas, arr, color)
                time.sleep(0.01)
    elapsed = time.perf_counter() - start_time
    algo_times["Bubble"] = elapsed
    status_label.config(text="[ DONE  ]", fg=FG_DONE)
    time_label.config(text=f"{elapsed:.4f} sec")

# 3. 快速排序
def quick_sort_logic(arr, start, end, canvas, color):
    if start >= end: return
    pivot_val = arr[start] 
    left, right = start + 1, end
    while True:
        while left <= right and arr[right] >= pivot_val: right -= 1
        while left <= right and arr[left] <= pivot_val: left += 1
        if left < right:
            arr[left], arr[right] = arr[right], arr[left]
            draw_mini_array(canvas, arr, color)
            time.sleep(0.04)
        else: break
    arr[start], arr[right] = arr[right], arr[start] 
    draw_mini_array(canvas, arr, color)
    time.sleep(0.04)
    quick_sort_logic(arr, start, right - 1, canvas, color)
    quick_sort_logic(arr, right + 1, end, canvas, color)

def run_quick_sort(arr, canvas, status_label, time_label, color):
    start_time = time.perf_counter()
    status_label.config(text="[RUNNING]", fg=FG_RUNNING)
    quick_sort_logic(arr, 0, len(arr)-1, canvas, color)
    elapsed = time.perf_counter() - start_time
    algo_times["Quick"] = elapsed
    status_label.config(text="[ DONE  ]", fg=FG_DONE)
    time_label.config(text=f"{elapsed:.4f} sec")

# ==========================================
# 第二部分：GUI 輔助功能
# ==========================================

def draw_mini_array(canvas, arr, color):
    canvas.delete("all")
    w, h = 300, 40
    bw = w / len(arr)
    mv = max(arr) if arr else 1
    for i, v in enumerate(arr):
        x0, y0 = i * bw, h - (v / mv * h)
        canvas.create_rectangle(x0, y0, (i+1)*bw, h, fill=color, outline=BG_CANVAS)
    canvas.update_idletasks()

def reset_sims():
    global data_sel, data_bub, data_quick, algo_times
    base = random.sample(range(1, N + 1), N)
    data_sel, data_bub, data_quick = base.copy(), base.copy(), base.copy()
    algo_times = {"Selection": 0, "Bubble": 0, "Quick": 0}
    draw_mini_array(canvas_sel, data_sel, "#525934")
    draw_mini_array(canvas_bub, data_bub, "#A6633C")
    draw_mini_array(canvas_quick, data_quick, "#731E0A")
    lbl_status.config(text="> SYS: Data initialized.", fg=FG_TEXT)
    lbl_win.config(text="")
    for s in [st_sel, st_bub, st_quick]: s.config(text="[WAITING]", fg=FG_TEXT)
    for t in [tm_sel, tm_bub, tm_quick]: t.config(text="0.0000 sec")
    btn_run.config(state="normal"); btn_rst.config(state="disabled")

def start_sims():
    btn_run.config(state="disabled"); btn_rst.config(state="disabled")
    lbl_status.config(text="> SYS: Sorting in progress...", fg=FG_RUNNING)
    threads = [
        threading.Thread(target=selection_sort, args=(data_sel, canvas_sel, st_sel, tm_sel, "#525934")),
        threading.Thread(target=bubble_sort, args=(data_bub, canvas_bub, st_bub, tm_bub, "#A6633C")),
        threading.Thread(target=run_quick_sort, args=(data_quick, canvas_quick, st_quick, tm_quick, "#731E0A"))
    ]
    for t in threads: t.start()
    def monitor():
        for t in threads: t.join()
        lbl_status.config(text="> SYS: All tasks finished.", fg=FG_DONE)
        fastest = min(algo_times, key=algo_times.get)
        lbl_win.config(text=f"★ Winner: {fastest} Sort ({algo_times[fastest]:.4f} sec)")
        btn_rst.config(state="normal")
    threading.Thread(target=monitor).start()

# ==========================================
# 第三部分：主佈局
# ==========================================

root = tk.Tk()
root.title("Performance Analytics")
root.configure(bg=BG_MAIN, padx=30, pady=30)

# Title (修正：將 pb=20 改為 pady=(0, 20))
tk.Label(root, text="SORTING ANALYSIS", font=FONT_TITLE, bg=BG_MAIN, fg=FG_TEXT).pack(anchor="w", pady=(0, 20))

# Create Rows
def add_row(txt):
    f = tk.Frame(root, bg=BG_MAIN, pady=10)
    f.pack(fill="x")
    tk.Label(f, text=txt, font=FONT_UI, bg=BG_MAIN, fg=FG_TEXT, width=15, anchor="w").pack(side="left")
    c = tk.Canvas(f, width=300, height=40, bg=BG_CANVAS, highlightthickness=1, highlightbackground=FG_TEXT)
    c.pack(side="left", padx=20)
    s = tk.Label(f, text="[WAITING]", font=FONT_UI, bg=BG_MAIN, fg=FG_TEXT, width=10)
    s.pack(side="left")
    return c, s

canvas_sel, st_sel = add_row("Selection:")
canvas_bub, st_bub = add_row("Bubble:")
canvas_quick, st_quick = add_row("Quick:")

# Divider
tk.Frame(root, height=1, bg=FG_TEXT).pack(fill="x", pady=20)

# Runtime Labels
def add_time(txt):
    f = tk.Frame(root, bg=BG_MAIN)
    f.pack(fill="x")
    tk.Label(f, text=txt, font=FONT_UI, bg=BG_MAIN, fg=FG_TEXT, width=15, anchor="w").pack(side="left")
    l = tk.Label(f, text="0.0000 sec", font=FONT_UI, bg=BG_MAIN, fg=FG_TEXT)
    l.pack(side="left")
    return l

lbl_status = tk.Label(root, text="> SYS: Ready.", font=FONT_UI, bg=BG_MAIN, fg=FG_TEXT); lbl_status.pack(anchor="w")
tm_sel = add_time("Selection:"); tm_bub = add_time("Bubble:"); tm_quick = add_time("Quick:")
lbl_win = tk.Label(root, text="", font=FONT_RESULT, bg=BG_MAIN, fg=FG_WINNER); lbl_win.pack(pady=15, anchor="w")

# Buttons (修正：將 pt=10 改為 pady=(10, 0))
bf = tk.Frame(root, bg=BG_MAIN)
bf.pack(fill="x", pady=(10, 0)) 
btn_run = tk.Button(bf, text="RUN", command=start_sims, font=FONT_BOLD, width=8)
btn_run.pack(side="left")
btn_rst = tk.Button(bf, text="RESET", command=reset_sims, font=FONT_BOLD, width=8)
btn_rst.pack(side="left", padx=20)
tk.Button(bf, text="QUIT", command=root.destroy, font=FONT_BOLD, width=8).pack(side="right")

reset_sims()
root.mainloop()