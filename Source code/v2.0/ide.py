import os, re, time, tkinter as tk
from tkinter import scrolledtext, messagebox

class ZNCEngine:
    def __init__(self, root_path, console_widget):
        self.root_path, self.console = root_path, console_widget
        self.modules, self.logic_map = {}, {}

    def load_resources(self):
        self.modules.clear()
        self.logic_map.clear()
        imp_p, sys_p = os.path.join(self.root_path, "Imports"), os.path.join(self.root_path, "Sys")
        if os.path.exists(imp_p):
            for f in os.listdir(imp_p):
                if f.endswith(".znm"):
                    name = f.replace(".znm", "")
                    self.modules[name] = self.parse_znm(os.path.join(imp_p, f))
        if os.path.exists(sys_p):
            for f in os.listdir(sys_p):
                if f.endswith(".znmm"):
                    with open(os.path.join(sys_p, f), 'r', encoding='utf-8') as file:
                        for line in file:
                            if "=>" in line:
                                k, v = line.strip().split("=>")
                                self.logic_map[k.strip()] = v.strip()

    def parse_znm(self, path):
        cmds = {}
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            block = re.findall(r'command\s*\((.*?)\)', content, re.DOTALL)
            if block:
                for line in block[0].strip().split('\n'):
                    if '=' in line and line.strip().startswith("-"):
                        parts = line.strip().split('=')
                        key = parts[0].replace("-", "").split('[')[0].strip()
                        cmds[key] = parts[1].strip()
        return cmds

    def log(self, text, color="#ffffff"):
        tag = f"col_{color}"
        self.console.tag_config(tag, foreground=color)
        self.console.insert(tk.END, text + "\n", tag)
        self.console.see(tk.END)

    def run(self, code):
        self.console.delete("1.0", tk.END)
        self.load_resources()
        dirs = {m[0]: m[1].strip() for m in re.findall(r'(\w+)\s+code\s*\((.*?)\)\s*(?=Sys code|$|(\w+)\s+code)', code, re.DOTALL)}
        sys_match = re.search(r'Sys code\s*\((.*?)\)', code, re.DOTALL)
        if not sys_match: return
        boot = re.findall(r'display directory\s*<(\w+)>', sys_match.group(1))
        ctx = {"self": self, "tk": tk, "time": time, "os": os, "color": "#ffffff", "code": code, "dirs": dirs}
        for target in boot:
            if target in dirs:
                self.execute_dir(dirs[target], code, ctx)

    def execute_dir(self, dir_code, full_script, ctx):
        active_imps = re.findall(r'import\s+(\w+)', full_script)
        for line in dir_code.split('\n'):
            line = line.strip()
            if not line.startswith("- "): continue
            cmd_name = line[2:].split('[')[0].strip()
            arg_m = re.search(r'\["(.*?)"\]', line)
            ctx["arg"] = arg_m.group(1) if arg_m else ""
            for imp in active_imps:
                if imp in self.modules and cmd_name in self.modules[imp]:
                    action_key = self.modules[imp][cmd_name]
                    if action_key in self.logic_map:
                        try: exec(self.logic_map[action_key], {"ctx": ctx, "self": self, "tk": tk, "time": time, "os": os}, ctx)
                        except Exception as e: self.log(f"ERR: {e}", "#ff0000")

class App:
    def __init__(self, root, patch_code=None):
        self.root = root
        self.root.title("ZNCode IDE Pro")
        self.root.geometry("1000x700")
        
        self.sidebar = tk.Frame(root, width=200, bg="#252526")
        self.sidebar.pack(side=tk.LEFT, fill='y')
        tk.Label(self.sidebar, text="PROJECT FILES", bg="#252526", fg="#aaa", font=("Arial", 10, "bold")).pack(pady=5)
        
        # Исправленный tk.Listbox
        self.file_list = tk.Listbox(self.sidebar, bg="#252526", fg="#fff", bd=0, highlightthickness=0, font=("Consolas", 10))
        self.file_list.pack(expand=True, fill='both', padx=5)
        self.file_list.bind("<<ListboxSelect>>", self.load_selected_file)

        self.main_area = tk.Frame(root)
        self.main_area.pack(side=tk.RIGHT, expand=True, fill='both')
        
        self.toolbar = tk.Frame(self.main_area, bg="#333")
        self.toolbar.pack(fill='x')
        tk.Button(self.toolbar, text="RUN", command=self.manual_run, bg="#4CAF50", fg="white", font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=5, pady=2)
        tk.Button(self.toolbar, text="REFRESH", command=self.refresh_file_list).pack(side=tk.LEFT, padx=2)
        
        self.editor = scrolledtext.ScrolledText(self.main_area, bg="#1a1a1a", fg="#fff", font=("Consolas", 12), insertbackground="white", undo=True)
        self.editor.pack(expand=True, fill='both')
        
        self.console = tk.Text(self.main_area, height=10, bg="#000", fg="#0f0", font=("Consolas", 10))
        self.console.pack(fill='x')
        
        self.engine = ZNCEngine("ZNCRoot", self.console)
        self.current_file = "ZNCRoot/Code/main.znc"
        
        self.editor.bind("<KeyRelease-minus>", self.show_suggestions)
        
        self.refresh_file_list()
        if os.path.exists(self.current_file): self.load_file(self.current_file)

        if patch_code:
            try:
                exec(patch_code, {"self": self, "root": self.root, "tk": tk, "engine": self.engine})
            except Exception as e:
                messagebox.showerror("Patch Error", f"Patch failed: {e}")

    def show_suggestions(self, event):
        content = self.editor.get("1.0", tk.END)
        imports = re.findall(r'import\s+(\w+)', content)
        self.engine.load_resources()
        hints = []
        for imp in imports:
            if imp in self.engine.modules:
                hints.extend([f"- {cmd}" for cmd in self.engine.modules[imp].keys()])
        if hints:
            self.console.delete("1.0", tk.END)
            self.engine.log("Hints: " + ", ".join(hints[:10]), "#888888")

    def refresh_file_list(self):
        self.file_list.delete(0, tk.END)
        path = "ZNCRoot/Code"
        if not os.path.exists(path): os.makedirs(path)
        for f in os.listdir(path):
            if f.endswith(".znc"): self.file_list.insert(tk.END, f)

    def load_selected_file(self, event):
        if not self.file_list.curselection(): return
        name = self.file_list.get(self.file_list.curselection())
        self.load_file(f"ZNCRoot/Code/{name}")

    def load_file(self, path):
        self.current_file = path
        with open(path, "r", encoding="utf-8") as f:
            self.editor.delete("1.0", tk.END)
            self.editor.insert(tk.END, f.read())

    def manual_run(self):
        content = self.editor.get("1.0", tk.END).strip()
        with open(self.current_file, "w", encoding="utf-8") as f:
            f.write(content)
        self.engine.run(content)

def select_engine():
    sel = tk.Tk()
    sel.title("ZNCEngine Selector")
    sel.geometry("300x350")
    tk.Label(sel, text="Choose Mode:", font=("Arial", 10, "bold")).pack(pady=10)
    
    selected_patch = [None]
    def start(p):
        selected_patch[0] = p
        sel.destroy()

    tk.Button(sel, text="Stock (Standard)", command=lambda: start(None), width=25).pack(pady=5)
    
    for f in os.listdir("."):
        if f.endswith(".znce"):
            with open(f, "r", encoding="utf-8") as pf:
                code = pf.read()
                tk.Button(sel, text=f"Patch: {f}", command=lambda c=code: start(c), width=25, bg="#d1e7ff").pack(pady=2)
                
    sel.mainloop()
    return selected_patch[0]

if __name__ == "__main__":
    patch = select_engine()
    rt = tk.Tk()
    App(rt, patch)
    rt.mainloop()