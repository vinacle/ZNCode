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