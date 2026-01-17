import tkinter as tk
from tkinter import messagebox
import hashlib
import sys
import ctypes
from ctypes import wintypes

class AggressiveLocker:
    def __init__(self, password_hash=None):
        self.root = tk.Tk()
        self.root.title("LOCKED")
        
        # Блокировка панели задач и горячих клавиш Windows
        self.block_windows_keys()
        
        # Полноэкранный режим с максимальным приоритетом
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 1.0)
        
        # Убираем все декорации
        self.root.overrideredirect(True)
        
        # Получаем размеры экрана
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        
        # Хеш пароля (по умолчанию "12345")
        self.password_hash = password_hash or self.hash_password("12345")
        
        # Счетчик неудачных попыток - теперь 3!
        self.failed_attempts = 0
        self.max_attempts = 3
        
        # Настройка UI
        self.setup_ui()
        
        # Агрессивная блокировка событий
        self.setup_aggressive_bindings()
        
        # Постоянный захват фокуса
        self.keep_focus()
        
    def block_windows_keys(self):
        """Блокировка системных клавиш Windows через WinAPI"""
        try:
            # Константы для блокировки клавиш
            LLKHF_ALTDOWN = 0x20
            WH_KEYBOARD_LL = 13
            WM_KEYDOWN = 0x0100
            
            # Блокируемые клавиши
            blocked_keys = [
                0x5B,  # Left Windows key
                0x5C,  # Right Windows key
                0x09,  # Tab (для Alt+Tab)
                0x1B,  # Escape
                0x2C,  # Print Screen
                0x91,  # Scroll Lock
                0x13,  # Pause
                0x7A,  # F11
                0x7B,  # F12
            ]
            
            # Попытка скрыть панель задач
            try:
                user32 = ctypes.windll.user32
                # Находим панель задач
                taskbar = user32.FindWindowW("Shell_TrayWnd", None)
                if taskbar:
                    # Скрываем панель задач
                    user32.ShowWindow(taskbar, 0)
            except:
                pass
                
        except Exception as e:
            print(f"Warning: Could not block Windows keys: {e}")
    
    def restore_taskbar(self):
        """Восстановление панели задач"""
        try:
            user32 = ctypes.windll.user32
            taskbar = user32.FindWindowW("Shell_TrayWnd", None)
            if taskbar:
                user32.ShowWindow(taskbar, 1)
        except:
            pass
    
    def hash_password(self, password):
        """Хеширование пароля"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def setup_ui(self):
        """Создание кровавого интерфейса"""
        # Тёмно-красный фон
        self.root.configure(bg='#0a0000')
        
        # Главный контейнер
        main_frame = tk.Frame(self.root, bg='#0a0000')
        main_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Череп вместо замка (или кровавый замок)
        skull_label = tk.Label(
            main_frame, 
            text="☠", 
            font=("Arial", 120, "bold"),
            bg='#0a0000',
            fg='#8B0000'  # Тёмно-красный
        )
        skull_label.pack(pady=30)
        
        # Заголовок с эффектом крови
        title_label = tk.Label(
            main_frame,
            text="СИСТЕМА ЗАБЛОКИРОВАНА",
            font=("Impact", 36, "bold"),
            bg='#0a0000',
            fg='#FF0000'  # Ярко-красный
        )
        title_label.pack(pady=15)
        
        # Подзаголовок с подтёками
        subtitle_label = tk.Label(
            main_frame,
            text="▼ ▼ ▼",
            font=("Arial", 20),
            bg='#0a0000',
            fg='#8B0000'
        )
        subtitle_label.pack(pady=5)
        
        # Инструкция
        info_label = tk.Label(
            main_frame,
            text="ВВЕДИТЕ ПАРОЛЬ ИЛИ СИСТЕМА БУДЕТ УНИЧТОЖЕНА",
            font=("Arial", 14, "bold"),
            bg='#0a0000',
            fg='#DC143C'  # Малиновый
        )
        info_label.pack(pady=20)
        
        # Поле ввода пароля
        self.password_entry = tk.Entry(
            main_frame,
            show="●",
            font=("Courier New", 20, "bold"),
            width=20,
            bg='#1a0000',
            fg='#FF0000',
            insertbackground='#FF0000',
            relief='solid',
            bd=3,
            highlightthickness=2,
            highlightbackground='#8B0000',
            highlightcolor='#FF0000'
        )
        self.password_entry.pack(pady=25, ipady=12)
        self.password_entry.focus_set()
        
        # Кнопка разблокировки
        self.submit_button = tk.Button(
            main_frame,
            text="⚠ РАЗБЛОКИРОВАТЬ ⚠",
            command=self.check_password,
            font=("Impact", 16, "bold"),
            bg='#8B0000',
            fg='#FFFFFF',
            activebackground='#FF0000',
            activeforeground='#FFFFFF',
            relief='raised',
            bd=4,
            cursor='hand2',
            width=25,
            height=2
        )
        self.submit_button.pack(pady=20)
        
        # Метка для ошибок
        self.error_label = tk.Label(
            main_frame,
            text="",
            font=("Arial", 14, "bold"),
            bg='#0a0000',
            fg='#FF0000'
        )
        self.error_label.pack(pady=10)
        
        # Счётчик попыток
        self.attempts_label = tk.Label(
            main_frame,
            text=f"ПОПЫТОК ОСТАЛОСЬ: {self.max_attempts}",
            font=("Courier New", 16, "bold"),
            bg='#0a0000',
            fg='#DC143C'
        )
        self.attempts_label.pack(pady=10)
        
        # Предупреждение внизу
        warning_label = tk.Label(
            main_frame,
            text="⚠ НЕ ПЫТАЙТЕСЬ ОБОЙТИ БЛОКИРОВКУ ⚠\n⚠ ВСЕ ДЕЙСТВИЯ ЗАПИСЫВАЮТСЯ ⚠",
            font=("Arial", 11, "bold"),
            bg='#0a0000',
            fg='#8B0000',
            justify='center'
        )
        warning_label.pack(pady=20)
        
        # Мигающий эффект для заголовка
        self.blink_title(title_label)
    
    def blink_title(self, label, state=True):
        """Мигающий эффект для заголовка"""
        if state:
            label.config(fg='#FF0000')
        else:
            label.config(fg='#8B0000')
        self.root.after(500, lambda: self.blink_title(label, not state))
    
    def setup_aggressive_bindings(self):
        """Агрессивная блокировка всех комбинаций"""
        # Блокировка закрытия окна
        self.root.protocol("WM_DELETE_WINDOW", self.block_action)
        
        # Блокировка всех возможных клавиш
        dangerous_keys = [
            '<Escape>', '<F1>', '<F2>', '<F3>', '<F4>', '<F5>', '<F6>',
            '<F7>', '<F8>', '<F9>', '<F10>', '<F11>', '<F12>',
            '<Alt-F4>', '<Alt-Tab>', '<Control-Escape>', 
            '<Control-Shift-Escape>', '<Control-Alt-Delete>',
            '<Super_L>', '<Super_R>',  # Windows keys
            '<Control-c>', '<Control-x>', '<Control-v>',
            '<Control-a>', '<Control-s>', '<Control-z>',
            '<Print>', '<Scroll_Lock>', '<Pause>',
        ]
        
        # Блокировка Win комбинаций
        for key in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                    'Tab', 'Escape', 'space', 'Up', 'Down', 'Left', 'Right']:
            dangerous_keys.append(f'<Super-{key}>')
            dangerous_keys.append(f'<Alt-{key}>')
            dangerous_keys.append(f'<Control-{key}>')
            dangerous_keys.append(f'<Control-Alt-{key}>')
            dangerous_keys.append(f'<Control-Shift-{key}>')
        
        for key in dangerous_keys:
            try:
                self.root.bind(key, self.block_action)
            except:
                pass
        
        # Enter для отправки пароля
        self.password_entry.bind('<Return>', lambda e: self.check_password())
        
        # Предотвращение потери фокуса
        self.root.bind('<FocusOut>', lambda e: self.force_focus())
        
        # Блокировка правой кнопки мыши
        self.root.bind('<Button-3>', self.block_action)
    
    def block_action(self, event=None):
        """Блокировка действия с предупреждением"""
        self.shake_window()
        return "break"
    
    def shake_window(self):
        """Эффект тряски окна при попытке обойти блокировку"""
        original_geo = self.root.geometry()
        for i in range(10):
            if i % 2 == 0:
                self.root.geometry(f"+{i*2}+{i*2}")
            else:
                self.root.geometry(f"+{-i*2}+{-i*2}")
            self.root.update()
            self.root.after(20)
        self.root.geometry(original_geo)
    
    def keep_focus(self):
        """Постоянное удержание фокуса"""
        self.root.focus_force()
        self.root.grab_set()
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after(100, self.keep_focus)
    
    def force_focus(self):
        """Принудительный возврат фокуса"""
        self.root.focus_force()
        self.root.lift()
        self.root.attributes('-topmost', True)
    
    def check_password(self):
        """Проверка пароля"""
        password = self.password_entry.get()
        
        if not password:
            self.show_error("⚠ ВВЕДИТЕ ПАРОЛЬ ⚠")
            self.shake_window()
            return
        
        if self.hash_password(password) == self.password_hash:
            # Правильный пароль
            self.restore_taskbar()
            messagebox.showinfo(
                "Разблокировка", 
                "Система разблокирована!",
                parent=self.root
            )
            self.unlock()
        else:
            # Неправильный пароль
            self.failed_attempts += 1
            remaining = self.max_attempts - self.failed_attempts
            
            if remaining > 0:
                self.show_error(f"✖ НЕВЕРНЫЙ ПАРОЛЬ ✖\n⚠ СИСТЕМА БУДЕТ ПОВРЕЖДЕНА ⚠")
                self.attempts_label.config(
                    text=f"ПОПЫТОК ОСТАЛОСЬ: {remaining}",
                    fg='#FF0000' if remaining == 1 else '#DC143C'
                )
                self.shake_window()
                self.password_entry.delete(0, tk.END)
                self.password_entry.focus_set()
            else:
                # Попытки исчерпаны
                self.show_error("✖✖✖ СИСТЕМА ЗАБЛОКИРОВАНА НАВСЕГДА ✖✖✖")
                self.attempts_label.config(
                    text="⚠ ПОПЫТКИ ИСЧЕРПАНЫ ⚠",
                    fg='#FF0000'
                )
                self.submit_button.config(state='disabled', bg='#3a0000')
                self.password_entry.config(state='disabled')
                
                # Мигающее предупреждение
                self.flash_screen()
                
                messagebox.showerror(
                    "БЛОКИРОВКА",
                    "⚠⚠⚠ ДОСТУП ЗАБЛОКИРОВАН НАВСЕГДА ⚠⚠⚠\n\n"
                    "Все попытки исчерпаны.\n"
                    "Обратитесь к администратору системы.\n\n"
                    "Все действия записаны.",
                    parent=self.root
                )
    
    def flash_screen(self, count=0):
        """Мигание экрана красным"""
        if count < 6:
            if count % 2 == 0:
                self.root.configure(bg='#FF0000')
            else:
                self.root.configure(bg='#0a0000')
            self.root.after(200, lambda: self.flash_screen(count + 1))
        else:
            self.root.configure(bg='#0a0000')
    
    def show_error(self, message):
        """Показ сообщения об ошибке"""
        self.error_label.config(text=message)
        self.root.after(3000, lambda: self.error_label.config(text=""))
    
    def unlock(self):
        """Разблокировка системы"""
        self.restore_taskbar()
        self.root.grab_release()
        self.root.destroy()
    
    def run(self):
        """Запуск блокировщика"""
        try:
            self.root.mainloop()
        finally:
            self.restore_taskbar()


def main():
    """Главная функция"""
    try:
        locker = AggressiveLocker()
        locker.run()
    except Exception as e:
        print(f"Error: {e}")
        # Восстанавливаем панель задач в случае ошибки
        try:
            user32 = ctypes.windll.user32
            taskbar = user32.FindWindowW("Shell_TrayWnd", None)
            if taskbar:
                user32.ShowWindow(taskbar, 1)
        except:
            pass


if __name__ == "__main__":
    main()
