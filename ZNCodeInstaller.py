import os

IDE_CODE = r'''
import os, re, time, tkinter as tk
from tkinter import scrolledtext

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
        ctx = {"self": self, "tk": tk, "time": time, "os": os, "color": "#ffffff"}
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
    def __init__(self, root):
        self.root = root
        self.root.title("ZNCode IDE")
        self.code_path = "ZNCRoot/Code/main.znc"
        os.makedirs("ZNCRoot/Code", exist_ok=True)
        
        self.editor = scrolledtext.ScrolledText(root, bg="#1a1a1a", fg="#fff", font=("Consolas", 12), insertbackground="white", undo=True)
        self.editor.pack(expand=True, fill='both')
        
        self.editor.tag_config("keyword", foreground="#c678dd")
        self.editor.tag_config("string", foreground="#98c379")
        self.editor.tag_config("bracket", foreground="#e5c07b")
        self.editor.tag_config("sys", foreground="#61afef")

        if os.path.exists(self.code_path):
            with open(self.code_path, "r", encoding="utf-8") as f:
                self.editor.insert(tk.END, f.read())
        else:
            self.editor.insert(tk.END, 'import text\n\nmain code (\n    - print ["Hello World"]\n)\n\nSys code (\n    display directory <main>\n)')
        
        self.console = tk.Text(root, height=8, bg="#000", fg="#0f0")
        self.console.pack(fill='x')
        self.engine = ZNCEngine("ZNCRoot", self.console)
        self.editor.bind("<<Modified>>", self.on_content_changed)
        
        tk.Button(root, text="MANUAL RUN", command=self.manual_run, bg="#333", fg="#fff").pack(side=tk.LEFT, padx=5, pady=5)
        self.status_label = tk.Label(root, text="File synced", fg="#555")
        self.status_label.pack(side=tk.RIGHT, padx=10)
        self.apply_syntax()

    def apply_syntax(self):
        content = self.editor.get("1.0", tk.END)
        for tag in ["keyword", "string", "bracket", "sys"]:
            self.editor.tag_remove(tag, "1.0", tk.END)
        
        for m in re.finditer(r'\b(import|code)\b', content):
            self.editor.tag_add("keyword", f"1.0+{m.start()}c", f"1.0+{m.end()}c")
        for m in re.finditer(r'\b(Sys|display|directory)\b', content):
            self.editor.tag_add("sys", f"1.0+{m.start()}c", f"1.0+{m.end()}c")
        for m in re.finditer(r'\["(.*?)"\]', content):
            self.editor.tag_add("string", f"1.0+{m.start()}c", f"1.0+{m.end()}c")
        for m in re.finditer(r'\(|\)', content):
            self.editor.tag_add("bracket", f"1.0+{m.start()}c", f"1.0+{m.end()}c")

    def on_content_changed(self, event=None):
        if self.editor.edit_modified():
            content = self.editor.get("1.0", tk.END)
            with open(self.code_path, "w", encoding="utf-8") as f:
                f.write(content.strip())
            self.apply_syntax()
            self.editor.edit_modified(False)
            self.status_label.config(text=f"Last sync: {time.strftime('%H:%M:%S')}", fg="#0f0")

    def manual_run(self):
        self.engine.run(self.editor.get("1.0", tk.END))

if __name__ == "__main__":
    rt = tk.Tk()
    App(rt)
    rt.mainloop()
'''

MANAGER_CODE = r'''
import os, re, glob, tkinter as tk
from tkinter import messagebox, ttk

class ZNPManager:
    def __init__(self, root):
        self.root = root
        self.root.title("ZNP Manager")
        self.tree = ttk.Treeview(root, columns=("Package", "Status"), show="headings")
        self.tree.heading("Package", text="Package Name")
        self.tree.heading("Status", text="Status")
        self.tree.pack(fill="both", expand=True)
        btn_f = tk.Frame(root)
        btn_f.pack()
        tk.Button(btn_f, text="Install", command=self.install).pack(side=tk.LEFT)
        tk.Button(btn_f, text="Remove", command=self.remove).pack(side=tk.LEFT)
        self.refresh()

    def refresh(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        for f in glob.glob("*.znp"):
            try:
                with open(f, 'r', encoding='utf-8') as file: 
                    name = re.search(r'name\s*=\s*(\w+)', file.read()).group(1)
                status = "Installed" if os.path.exists(f"ZNCRoot/Imports/{name}.znm") else "Available"
                self.tree.insert("", "end", iid=f, values=(name, status))
            except: pass

    def install(self):
        sel = self.tree.selection()
        if not sel: return
        with open(sel[0], 'r', encoding='utf-8') as f: content = f.read()
        name = self.tree.item(sel[0], "values")[0]
        os.makedirs("ZNCRoot/Imports", exist_ok=True)
        os.makedirs("ZNCRoot/Sys", exist_ok=True)
        open(f"ZNCRoot/Imports/{name}.znm", "w", encoding='utf-8').write(re.search(r'\{INTERFACE\}(.*?)\{LOGIC\}', content, re.DOTALL).group(1).strip())
        open(f"ZNCRoot/Sys/{name}.znmm", "w", encoding='utf-8').write(re.search(r'\{LOGIC\}(.*)', content, re.DOTALL).group(1).strip())
        self.refresh()
        messagebox.showinfo("ZNP", f"Module {name} installed!")

    def remove(self):
        sel = self.tree.selection()
        if not sel: return
        name = self.tree.item(sel[0], "values")[0]
        for p in [f"ZNCRoot/Imports/{name}.znm", f"ZNCRoot/Sys/{name}.znmm"]:
            if os.path.exists(p): os.remove(p)
        self.refresh()
        messagebox.showinfo("ZNP", f"Module {name} removed!")

if __name__ == "__main__":
    rt = tk.Tk()
    ZNPManager(rt)
    rt.mainloop()
'''

UI_ZNP = """{INTERFACE}
name = ui
command (
- window [""] = SYS.UI.CREATE
- label [""] = SYS.UI.LABEL
)
{LOGIC}
SYS.UI.CREATE => ctx["win"] = tk.Toplevel(); ctx["win"].title(ctx["arg"]); ctx["win"].geometry("300x200")
SYS.UI.LABEL => if "win" in ctx: tk.Label(ctx["win"], text=ctx["arg"]).pack()
"""

BAT_CODE = """@echo off
start python ide.py
start python znp_manager.py
exit
"""

def run_setup():
    print("--- ZNC SYSTEM ASSEMBLY ---")
    for d in ["ZNCRoot/Imports", "ZNCRoot/Sys", "ZNCRoot/Code"]: 
        os.makedirs(d, exist_ok=True)

    with open("ide.py", "w", encoding="utf-8") as f: f.write(IDE_CODE.strip())
    with open("znp_manager.py", "w", encoding="utf-8") as f: f.write(MANAGER_CODE.strip())
    with open("ui.znp", "w", encoding="utf-8") as f: f.write(UI_ZNP.strip())
    with open("START ALL.bat", "w") as f: f.write(BAT_CODE)

    with open("ZNCRoot/Imports/text.znm", "w", encoding="utf-8") as f: 
        f.write('name = text\ncommand (\n- print [""] = terminal.log\n)')
    with open("ZNCRoot/Sys/text.znmm", "w", encoding="utf-8") as f: 
        f.write('terminal.log => self.log(f"> {ctx[\'arg\']}", ctx.get("color", "#ffffff"))')
    
    print("\n[SUCCESS] ZNCode is fully assembled!")
    print("Now just run it 'START ALL.bat'")

if __name__ == "__main__":
    run_setup()