# 🌀 ZNCode System (ZNC) EN

**From the Author:** This project was created purely out of boredom. I honestly didn't expect the final result to be such a "beast." It is a tool for those who need things done fast, powerfully, and without unnecessary questions.

---

## 📂 SECTION ONE: OPERATIONAL OVERVIEW

### What is it?

**ZNCode** - is a modular environment and wrapper language that allows you to turn massive chunks of code into a single simple command. It is a construction kit where you define the rules of the game.

### System Pros

* 
**Extreme Lightweight:** The system takes up minimal disk space and consumes almost zero PC resources.


* 
**Modular Repair:** If something breaks, you don't need to dig through the entire engine — just fix the specific logic module.


* 
**Direct PC Contact:** Your commands interact with the system directly through the interpreter.


* **Target Efficiency:** ZNC is designed for scenarios where standard languages are too cumbersome, allowing you to pack entire scripts into one command or build tools for highly specific tasks.

### Cons and Security

* **The Shadow Side:** The language's flexibility makes it convenient for creating "specific" or undesirable software.
* **"The Sloth" Protection:** To limit uncontrolled distribution of malicious code, there is no built-in compilation function (the author was too lazy, so it became a security feature). Code can only run if the ZNC environment is present. If you need an `.exe` — you must write the compiler yourself.

### Installation & Management

* 
**Lazy Version:** Place `ZNCodeInstaller.py` and `start installation (for the lazy).bat` in one folder and run the `.bat` file. It automatically builds the directory structure (`ZNCRoot/Code`, `Imports`, `Sys`).


* **ZNP Manager:** A graphical utility to manage modules. The **text** module is ready by default, while the **ui** module comes as a `.znp` package. To use UI, select it in the manager and click **Install**.
* **Sys Code:** This is your entry point. It uses the `display directory <name>` command to trigger specific blocks of logic.

---

# 🌀 Система ZNCode (ZNC) RU

**От автора:** Проект был создан чисто от скуки, автор сам не ожидал, что на выходе получится такая «имба». Это инструмент для тех, кому нужно быстро, мощно и без лишних вопросов.

---

## 📂 ПЕРВЫЙ РАЗДЕЛ: ПОЯСНЕНИЕ К РАБОТЕ

### Что это такое?

**ZNCode** - это модульная среда и язык-оболочка, который позволяет превращать огромные куски кода в одну простую команду. Это конструктор, где ты сам определяешь правила игры.

### Плюсы системы

* 
**Экстремальная легкость:** Система занимает минимум места на диске и практически не потребляет ресурсы ПК.


* 
**Модульный ремонт:** Если что-то сломалось, не нужно ковырять всё ядро — достаточно пофиксить один модуль логики, не трогая движок.


* 
**Прямой контакт с ПК:** Твои команды взаимодействуют с системой напрямую через интерпретатор.


* **Область применения:** Язык идеален для задач, где обычные языки слишком громоздки. Например, когда нужно упаковать целый скрипт в одну команду или создать инструмент под узкую задачу.

### Минусы и Безопасность

* **Теневая сторона:** Гибкость языка делает его удобным для создания «специфического» софта.
* **Защита «Ленивца»:** Чтобы ограничить бесконтрольное распространение кода, автор не добавил функцию компиляции (было лень). Это «фича безопасности»: запустить код можно только имея среду ZNC. Если нужен .exe — пиши компилятор сам!

### Установка и работа

* 
**Версия для ленивых:** Запустите **`start installation (for the lazy).bat`**. Он автоматически создаст структуру папок (`ZNCRoot/Code`, `Imports`, `Sys`) и базовые файлы.


* **Менеджер ZNP:** Утилита для управления пакетами. Модуль **text** готов сразу. Модуль **ui** идет в виде пакета `.znp`. Зайдите в менеджер, выберите его и нажмите **Install**, чтобы начать рисовать окна.
* **Sys code:** Точка входа в программу. Использует команду `display directory <название>` для запуска конкретных блоков кода.

---

## 🛠 ВТОРОЙ РАЗДЕЛ: ИНСТРУКЦИЯ ПО РАЗРАБОТКЕ

### Как писать на ZNC

Код делится на блоки (директории). Команды начинаются с дефиса `-`, а данные пишутся в квадратных скобках `[" "]`. `import` всегда пишется в самом верху.

**Пример `main.znc`:**

```text
import text
import ui

main code (
    - print ["Запуск системы..."]
    - window ["Моя Программа"]
)

Sys code (
    display directory <main>
)

```

### Как писать ZNP (Пакеты)

Пакет — это один файл, объединяющий интерфейс (**ZNM**) и логику (**ZNMM**).

* **{INTERFACE} (ZNM):** Описывает связь команды с ключом логики.
* **{LOGIC} (ZNMM):** Содержит реальный машинный код исполнения.

**Пример `ui.znp`:**

```text
{INTERFACE}
name = ui
command (
- window [""] = SYS.UI.CREATE
- label [""] = SYS.UI.LABEL
)

{LOGIC}
SYS.UI.CREATE => ctx["win"] = tk.Toplevel(); ctx["win"].title(ctx["arg"]); ctx["win"].geometry("300x200")
SYS.UI.LABEL => if "win" in ctx: tk.Label(ctx["win"], text=ctx["arg"]).pack()

```

---

## 💎 ПОЛЕЗНОЕ

### Как это работает внутри?

1. **import:** Подключает «словарь» команд.
2. **Связь:** Система ищет команду в `.znm` и находит её ключ.
3. **Исполнение:** Система находит этот ключ в файле логики `.znmm` и выполняет скрытый за ним код.

### Команды для логики (ZNMM)

* `self.log(ctx["arg"])` - вывод в консоль.
* `ctx["arg"]` - получение данных из скобок `[" "]`.
* **Важно:** Команд бесконечное множество. Вы можете вставить любые системные вызовы Windows или команды других языков, установленных на ПК (например, Java). Автору просто было лень выписывать всё!

### Расшифровка:

* **ZNC** - ZNCode (Твой код).
* **ZNP** - ZNPackage (Пакет/Архив модуля).
* **ZNM** - ZNModule (Файл интерфейса).
* **ZNMM** - ZNModuleManager (Файл машинной логики).

---

## 🎁 ДЛЯ ТЕХ, КТО ПРОЧИТАЛ: BUILDER (Подарок)

Это инструмент для создания «чистой» сборки. Он копирует нужные модули и создает готовый `run_app.bat` для запуска вашего кода без IDE.

**Код модуля `builder.znp`:**

```python
{INTERFACE}
name = zn_builder
command (
- build [""] = B.FULL_RUN
)

{LOGIC}
B.FULL_RUN => import os, shutil, re; name = ctx.get("arg", "App"); dist = f"Dist_{name}"; assets = f"{dist}/assets"; os.makedirs(assets, exist_ok=True); [os.makedirs(f"{assets}/{d}", exist_ok=True) for d in ["Code", "Imports", "Sys"]]; [[shutil.copy(f"ZNCRoot/{f}/{i}", f"{assets}/{f}/{i}") for i in os.listdir(f"ZNCRoot/{f}") if "builder" not in i.lower()] for f in ["Code", "Imports", "Sys"] if os.path.exists(f"ZNCRoot/{f}")]; main_p = f"{assets}/Code/main.znc"; c = open(main_p, "r", encoding="utf-8").read() if os.path.exists(main_p) else ""; clean = re.sub(r'import\s+zn_builder|-\s+build\s*\[".*?"\]', '', c); open(main_p, "w", encoding="utf-8").write(clean.strip()) if main_p else None; shutil.copy("ide.py", f"{dist}/ide.py") if os.path.exists("ide.py") else None; f = open(f"{dist}/Runner.py", "w", encoding="utf-8"); f.write("import os, tkinter as tk\nfrom ide import ZNCEngine\nroot = tk.Tk()\nroot.withdraw()\nengine = ZNCEngine('assets', tk.Text(root))\nengine.log = lambda t, c=None: print(f'[LOG]: {t}')\nif __name__ == '__main__':\n    with open('assets/Code/main.znc', 'r', encoding='utf-8') as z:\n        engine.run(z.read())\n    input('\\nDone.')"); f.close(); b = open(f"{dist}/run_app.bat", "w"); b.write(f"@echo off\ntitle {name}\npython Runner.py\npause"); b.close(); self.log(f"Чистая сборка {name} готова!", "#00ff00")

```
