import os, re, time, sys, inspect
import tkinter as tk
from tkinter import messagebox

class ZNCEngine:
    def __init__(self, root_path, console_widget):
        self.root_path = root_path
        self.console = console_widget
        self.modules = {}
        self.logic_map = {}
        self.active_win = None

    def load_resources(self):
        self.modules.clear()
        self.logic_map.clear()
        for folder in ["Imports", "Sys"]:
            path = os.path.join(self.root_path, folder)
            if not os.path.exists(path):
                path = os.path.join(self.root_path, "ZNCRoot", folder)
            
            if os.path.exists(path):
                for f in os.listdir(path):
                    if f.endswith((".znm", ".znp", ".znmm")):
                        self.parse_module(os.path.join(path, f))

    def parse_module(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        name_m = re.search(r'name\s*=\s*(\w+)', content)
        name = name_m.group(1) if name_m else os.path.basename(path).split('.')[0]
        if name not in self.modules: self.modules[name] = {}
        
        cmds = re.findall(r'-\s*([\w_]+)\s*\[.*?\]\s*=\s*([\w\.]+)', content)
        for k, v in cmds: self.modules[name][k] = v
        
        logic_lines = re.findall(r'([\w\.]+)\s*=>\s*(.*)', content)
        for k, v in logic_lines: self.logic_map[k.strip()] = v.strip()

    def log(self, text, color="#ffffff"):
        if hasattr(self.console, 'insert'):
            self.console.insert(tk.END, str(text) + "\n")
            self.console.see(tk.END)
        else: print(text)

    def run(self, code):
        self.load_resources()
        
        is_ide = hasattr(self.console, 'tag_config')
        
        if self.active_win and self.active_win.winfo_exists():
            self.active_win.destroy()
            
        self.active_win = tk.Toplevel() if is_ide else tk.Tk()
        self.active_win.title("ZNC Runner")
 
        dirs = {m[0]: m[1].strip() for m in re.findall(r'(\w+)\s+code\s*\((.*?)\)\s*(?=Sys code|$|(\w+)\s+code)', code, re.DOTALL)}
        sys_match = re.search(r'Sys code\s*\((.*?)\)', code, re.DOTALL)
        if not sys_match: return
        
        boot = re.findall(r'display directory\s*<(\w+)>', sys_match.group(1))
        
        ctx = {
            "self": self, "tk": tk, "os": os, "time": time,
            "win": self.active_win, "root": self.active_win,
            "dirs": dirs, "code": code, "arg": ""
        }
        
        for target in boot:
            if target in dirs:
                self.execute_dir(dirs[target], code, ctx)
        
        if not is_ide: self.active_win.mainloop()

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
                        try:
                            exec(self.logic_map[action_key], {}, {"ctx": ctx, "self": self, "tk": tk, "os": os, "time": time})
                        except Exception as e:
                            self.log(f"ERR {cmd_name}: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        class FakeConsole:
            def insert(self, *a): print(a[1] if len(a)>1 else a[0])
            def see(self, *a): pass
        eng = ZNCEngine(".", FakeConsole())
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            eng.run(f.read())