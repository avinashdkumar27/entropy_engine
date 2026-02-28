import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from core.strength_logic import analyze_password
from core.attack_models import ATTACK_MODELS

class EntropyEngineApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Entropy Engine")
        self.geometry("600x700")
        self.configure(bg="#1E1E1E")
        
        self.style = ttk.Style(self)
        try:
            self.style.theme_use("clam")
        except:
            pass
            
        self.style.configure("TLabel", background="#1E1E1E", foreground="#FFFFFF", font=("Segoe UI", 11))
        self.style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground="#00BFFF")
        self.style.configure("TButton", font=("Segoe UI", 11, "bold"), background="#333333", foreground="#FFFFFF")
        self.style.map("TButton", background=[("active", "#444444")])
        
        self.create_widgets()
        
    def create_widgets(self):
        main_frame = tk.Frame(self, bg="#1E1E1E", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        ttk.Label(main_frame, text="Entropy Engine", style="Header.TLabel").pack(pady=(0, 20))
        
        # input frame
        input_frame = tk.Frame(main_frame, bg="#1E1E1E")
        input_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(input_frame, text="Password:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(input_frame, textvariable=self.password_var, show="*", font=("Segoe UI", 12), width=30)
        self.password_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        self.show_pw_var = tk.BooleanVar(value=False)
        self.show_cb = tk.Checkbutton(input_frame, text="Show", variable=self.show_pw_var, command=self.toggle_password, bg="#1E1E1E", fg="#FFFFFF", selectcolor="#333")
        self.show_cb.pack(side=tk.LEFT, padx=10)
        
        # Attack model
        model_frame = tk.Frame(main_frame, bg="#1E1E1E")
        model_frame.pack(fill=tk.X, pady=10)
        ttk.Label(model_frame, text="Attack Model:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.model_var = tk.StringVar(value="CPU (basic)")
        self.model_dropdown = ttk.Combobox(model_frame, textvariable=self.model_var, values=list(ATTACK_MODELS.keys()), state="readonly", font=("Segoe UI", 11))
        self.model_dropdown.pack(side=tk.LEFT, expand=True, fill=tk.X)
        self.model_dropdown.bind("<<ComboboxSelected>>", lambda e: self.analyze())
        
        # Buttons
        btn_frame = tk.Frame(main_frame, bg="#1E1E1E")
        btn_frame.pack(fill=tk.X, pady=15)
        ttk.Button(btn_frame, text="Analyze", command=self.analyze).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        self.graph_btn = ttk.Button(btn_frame, text="Crack Graph (Log scale)", command=self.show_graph, state=tk.DISABLED)
        self.graph_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        
        # Results
        results_frame = tk.Frame(main_frame, bg="#2D2D2D", padx=15, pady=15)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Strength Meter
        self.meter_canvas = tk.Canvas(results_frame, height=20, bg="#444444", highlightthickness=0)
        self.meter_canvas.pack(fill=tk.X, pady=(0, 15))
        self.meter_rect = self.meter_canvas.create_rectangle(0, 0, 0, 20, fill="gray")
        
        self.meter_lbl = tk.Label(results_frame, text="Strength: N/A", bg="#2D2D2D", fg="white", font=("Segoe UI", 12, "bold"))
        self.meter_lbl.pack(pady=(0, 15))
        
        self.entropy_lbl = ttk.Label(results_frame, text="Entropy: 0 bits", background="#2D2D2D")
        self.entropy_lbl.pack(anchor=tk.W, pady=2)
        
        self.time_lbl = ttk.Label(results_frame, text="Time to crack: 0", background="#2D2D2D")
        self.time_lbl.pack(anchor=tk.W, pady=2)
        
        self.zxcvbn_lbl = ttk.Label(results_frame, text="zxcvbn Score: 0/4", background="#2D2D2D")
        self.zxcvbn_lbl.pack(anchor=tk.W, pady=2)
        
        self.breach_lbl = ttk.Label(results_frame, text="Breach Status: Not Checked", background="#2D2D2D")
        self.breach_lbl.pack(anchor=tk.W, pady=2)
        
        self.warnings_lbl = tk.Label(results_frame, text="", bg="#2D2D2D", fg="#FF4C4C", font=("Segoe UI", 10), justify=tk.LEFT, wraplength=500)
        self.warnings_lbl.pack(anchor=tk.W, pady=(10, 0))
        
        # Track last analysis 
        self.last_results = None
        
        # Bind enter key
        self.password_entry.bind("<Return>", lambda e: self.analyze())
        
        # Initial Meter
        self.update_meter(-1, "gray")

    def toggle_password(self):
        if self.show_pw_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")
            
    def analyze(self):
        password = self.password_var.get()
        model = self.model_var.get()
        
        if not password:
            return
            
        res = analyze_password(password, model)
        self.last_results = res
        
        # Update Labels
        self.entropy_lbl.config(text=f"Entropy: {res['entropy']} bits")
        self.time_lbl.config(text=f"Time to crack ({model}): {res['crack_time_display']}")
        self.zxcvbn_lbl.config(text=f"zxcvbn Score: {res['zxcvbn_score']}/4")
        
        if res['pwned_count'] > 0:
            self.breach_lbl.config(text=f"Breach Status: Found in {res['pwned_count']} breaches!", foreground="#FF4C4C")
            self.style.configure("Breach.TLabel", foreground="#FF4C4C", background="#2D2D2D")
            self.breach_lbl.configure(style="Breach.TLabel")
        else:
            self.breach_lbl.config(text="Breach Status: Not found in known breaches")
            self.style.configure("Safe.TLabel", foreground="#32CD32", background="#2D2D2D")
            self.breach_lbl.configure(style="Safe.TLabel")
            
        self.warnings_lbl.config(text=res['warnings'] if res['warnings'] else "")
        self.meter_lbl.config(text=f"Strength: {res['meter_label']}", fg=res['meter_color'])
        
        self.update_meter(res['final_score'], res['meter_color'])
        self.graph_btn.config(state=tk.NORMAL)
        
    def update_meter(self, score, color):
        self.update() # Update UI to get correct width
        width = self.meter_canvas.winfo_width()
        if width <= 1:
            width = 500 # Default fallback
            
        fill_width = width * ((score + 1) / 5)
        self.meter_canvas.coords(self.meter_rect, 0, 0, fill_width, 20)
        self.meter_canvas.itemconfig(self.meter_rect, fill=color)

    def show_graph(self):
        if not self.last_results:
            return
            
        crack_times = self.last_results["crack_times_all"]
        models = list(crack_times.keys())
        times = [max(1e-5, crack_times[m]) for m in models] # Avoid log(0)
        
        plt.figure("Entropy Engine - Attack Simulator", figsize=(8, 5))
        plt.bar(models, times, color=['#FF4C4C', '#FFA500', '#FFD700', '#32CD32'])
        plt.yscale("log")
        plt.ylabel("Time to Crack (Seconds) - Log Scale")
        plt.xlabel("Attack Models")
        plt.title("Estimated Crack Time by Attack Model")
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    app = EntropyEngineApp()
    app.mainloop()
