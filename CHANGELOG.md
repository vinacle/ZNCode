

---

# CHANGELOG

## [v2.0] - The Enterprise Leap (Current)

### EN - English Version

**Added:**

* **Patch Engine (.znce):** Introduction of the `select_engine` system. You can now load standalone patches (like `ENTERPRISE.znce`) to modify the IDE interface and logic at runtime using `exec()`.
* **Project Explorer:** Added a sidebar `Listbox` that automatically scans the `ZNCRoot/Code` folder and allows switching between scripts.
* **Intelligent Console Hints:** Pressing the `-` key now triggers a real-time hint system in the console, showing available commands based on active imports.
* **Enhanced ZNP Manager:** A dedicated tool to install or remove module packages. It automatically splits `.znp` files into `.znm` (interface) and `.znmm` (logic).
* **Advanced ZNCEngine:** The core now supports a richer `ctx` (context), including access to `tk`, `os`, `time`, and custom log colors.
* **Auto-save Logic:** The IDE now automatically saves the current file to `ZNCRoot/Code` before every execution.

---

### RU - Русская версия

**Добавлено:**

* **Движок патчей (.znce):** Внедрена система `select_engine`. Теперь можно загружать отдельные патчи (например, `ENTERPRISE.znce`) для модификации интерфейса и логики IDE на лету через `exec()`.
* **Проводник проектов:** В интерфейс добавлен сайдбар `Listbox`, который сканирует папку `ZNCRoot/Code` и позволяет быстро переключаться между скриптами.
* **Умные подсказки:** Нажатие клавиши `-` теперь вызывает систему подсказок в консоли, показывая доступные команды на основе активных импортов.
* **Улучшенный ZNP Manager:** Отдельная утилита для установки и удаления пакетов. Она сама делит `.znp` файлы на `.znm` (интерфейс) и `.znmm` (логика).
* **Продвинутый ZNCEngine:** Ядро теперь поддерживает расширенный контекст `ctx`, включая доступ к `tk`, `os`, `time` и кастомным цветам логов.
* **Логика автосохранения:** IDE теперь автоматически сохраняет текущий файл в `ZNCRoot/Code` перед каждым запуском.

---

## [v1.0] - Legacy Base

### EN

* Initial release of the ZNCode.
* Basic `.znm` and `.znmm` support.
* Standard text output to console.

### RU

* Первый релиз ZNCode.
* Базовая поддержка `.znm` и `.znmm`.
* Стандартный вывод текста в консоль.

---
