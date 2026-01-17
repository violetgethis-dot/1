import tkinter as tk
from tkinter import messagebox
import hashlib
import random
import ctypes

class AggressiveLocker:
    def __init__(self, password_hash=None):
        self.root = tk.Tk()
        self.root.title("LOCKED")
        
        # Блокировка панели задач
        self.block_windows_keys()
        
        # Полноэкранный режим
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.98)
        
        # Убираем декорации
        self.root.overrideredirect(True)
        
        # Размеры экрана
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        
        # Чёрный фон для всего окна
        self.root.configure(bg='#000000')
        
        # Хеш пароля (по умолчанию "12345")
        self.password_hash = password_hash or self.hash_password("12345")
        
        # Счетчик попыток - 3
        self.failed_attempts = 0
        self.max_attempts = 3
        
        # Флаг для контроля фокуса
        self.allow_focus_steal = True
        
        # Canvas для матричного эффекта
        self.canvas = tk.Canvas(
            self.root,
            width=screen_width,
            height=screen_height,
            bg='#000000',
            highlightthickness=0
        )
        self.canvas.place(x=0, y=0)
        
        # Матричная анимация
        self.matrix_columns = []
        self.init_matrix()
        self.animate_matrix()
        
        # Настройка UI
        self.setup_ui()
        
        # Блокировка событий
        self.setup_aggressive_bindings()
        
        # Один раз установить фокус
        self.root.after(100, self.initial_focus)
        
    def block_windows_keys(self):
        """Блокировка панели задач"""
        try:
            user32 = ctypes.windll.user32
            taskbar = user32.FindWindowW("Shell_TrayWnd", None)
            if taskbar:
                user32.ShowWindow(taskbar, 0)
        except:
            pass
    
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
    
    def init_matrix(self):
        """Инициализация матричного эффекта"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Создаём колонки с падающими символами
        num_columns = screen_width // 20
        for i in range(num_columns):
            column = {
                'x': i * 20,
                'y': random.randint(-screen_height, 0),
                'speed': random.randint(2, 8),
                'chars': []
            }
            # Создаём символы для каждой колонки
            num_chars = random.randint(10, 25)
            for j in range(num_chars):
                char = random.choice('01')
                color_intensity = int(255 * (1 - j/num_chars))
                color = f'#{color_intensity//4:02x}{color_intensity:02x}{color_intensity//4:02x}'
                column['chars'].append({
                    'text': char,
                    'offset': j * 20,
                    'color': color,
                    'id': None
                })
            self.matrix_columns.append(column)
    
    def animate_matrix(self):
        """Анимация падающей матрицы"""
        screen_height = self.root.winfo_screenheight()
        
        for column in self.matrix_columns:
            # Удаляем старые символы
            for char_data in column['chars']:
                if char_data['id']:
                    self.canvas.delete(char_data['id'])
            
            # Двигаем колонку вниз
            column['y'] += column['speed']
            
            # Если колонка ушла вниз - начинаем сверху
            if column['y'] > screen_height + 500:
                column['y'] = random.randint(-200, -50)
                column['speed'] = random.randint(2, 8)
            
            # Рисуем символы
            for char_data in column['chars']:
                y_pos = column['y'] + char_data['offset']
                if -20 < y_pos < screen_height + 20:
                    # Случайно меняем символ
                    if random.random() < 0.1:
                        char_data['text'] = random.choice('01')
                    
                    char_data['id'] = self.canvas.create_text(
                        column['x'],
                        y_pos,
                        text=char_data['text'],
                        fill=char_data['color'],
                        font=('Courier', 14, 'bold')
                    )
        
        # Повторяем анимацию
        self.root.after(50, self.animate_matrix)
    
    def setup_ui(self):
        """Создание интерфейса"""
        # Полупрозрачная центральная панель
        panel_width = 600
        panel_height = 550
        
        center_x = self.root.winfo_screenwidth() // 2
        center_y = self.root.winfo_screenheight() // 2
        
        # Создаём полупрозрачный прямоугольник на canvas
        self.bg_rect = self.canvas.create_rectangle(
            center_x - panel_width//2,
            center_y - panel_height//2,
            center_x + panel_width//2,
            center_y + panel_height//2,
            fill='#0a0000',
            outline='#8B0000',
            width=3,
            stipple='gray50'  # Полупрозрачность
        )
        
        # Frame поверх canvas
        main_frame = tk.Frame(self.root, bg='#0a0000')
        main_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Череп
        skull_label = tk.Label(
            main_frame, 
            text="☠", 
            font=("Arial", 100, "bold"),
            bg='#0a0000',
            fg='#8B0000'
        )
        skull_label.pack(pady=20)
        
        # Заголовок
        self.title_label = tk.Label(
            main_frame,
            text="СИСТЕМА ЗАБЛОКИРОВАНА",
            font=("Impact", 32, "bold"),
            bg='#0a0000',
            fg='#FF0000'
        )
        self.title_label.pack(pady=10)
        
        # Подтёки
        subtitle_label = tk.Label(
            main_frame,
            text="▼ ▼ ▼",
            font=("Arial", 18),
            bg='#0a0000',
            fg='#8B0000'
        )
        subtitle_label.pack(pady=5)
        
        # Инструкция
        info_label = tk.Label(
            main_frame,
            text="ВВЕДИТЕ ПАРОЛЬ",
            font=("Arial", 13, "bold"),
            bg='#0a0000',
            fg='#DC143C'
        )
        info_label.pack(pady=15)
        
        # Поле ввода пароля
        self.password_entry = tk.Entry(
            main_frame,
            show="●",
            font=("Courier New", 18, "bold"),
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
        self.password_entry.pack(pady=20, ipady=10)
        
        # Кнопка
        self.submit_button = tk.Button(
            main_frame,
            text="⚠ РАЗБЛОКИРОВАТЬ ⚠",
            command=self.check_password,
            font=("Impact", 14, "bold"),
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
        self.submit_button.pack(pady=15)
        
        # Ошибки
        self.error_label = tk.Label(
            main_frame,
            text="",
            font=("Arial", 13, "bold"),
            bg='#0a0000',
            fg='#FF0000'
        )
        self.error_label.pack(pady=10)
        
        # Счётчик
        self.attempts_label = tk.Label(
            main_frame,
            text=f"ПОПЫТОК ОСТАЛОСЬ: {self.max_attempts}",
            font=("Courier New", 14, "bold"),
            bg='#0a0000',
            fg='#DC143C'
        )
        self.attempts_label.pack(pady=10)
        
        # Мигание заголовка
        self.blink_title()
    
    def blink_title(self, state=True):
        """Мигание заголовка"""
        if state:
            self.title_label.config(fg='#FF0000')
        else:
            self.title_label.config(fg='#8B0000')
        self.root.after(500, lambda: self.blink_title(not state))
    
    def initial_focus(self):
        """Начальная установка фокуса"""
        self.password_entry.focus_set()
        self.root.grab_set()
    
    def setup_aggressive_bindings(self):
        """Блокировка клавиш"""
        self.root.protocol("WM_DELETE_WINDOW", self.block_action)
        
        dangerous_keys = [
            '<Escape>', '<F1>', '<F2>', '<F3>', '<F4>', '<F5>', '<F6>',
            '<F7>', '<F8>', '<F9>', '<F10>', '<F11>', '<F12>',
            '<Alt-F4>', '<Alt-Tab>', '<Control-Escape>', 
            '<Control-Shift-Escape>', '<Control-Alt-Delete>',
            '<Super_L>', '<Super_R>',
            '<Control-c>', '<Control-x>', '<Control-v>',
            '<Control-a>', '<Control-s>', '<Control-z>',
            '<Print>', '<Scroll_Lock>', '<Pause>',
        ]
        
        for key in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                    'Tab', 'Escape', 'space', 'Up', 'Down', 'Left', 'Right']:
            dangerous_keys.extend([
                f'<Super-{key}>',
                f'<Alt-{key}>',
                f'<Control-Alt-{key}>',
                f'<Control-Shift-{key}>'
            ])
        
        for key in dangerous_keys:
            try:
                self.root.bind(key, self.block_action)
            except:
                pass
        
        # Enter для пароля
        self.password_entry.bind('<Return>', lambda e: self.check_password())
        
        # Правая кнопка мыши
        self.root.bind('<Button-3>', self.block_action)
    
    def block_action(self, event=None):
        """Блокировка с тряской"""
        self.shake_window()
        return "break"
    
    def shake_window(self):
        """Тряска"""
        for i in range(8):
            offset = 3 if i % 2 == 0 else -3
            self.canvas.move(self.bg_rect, offset, offset)
            self.root.update()
            self.root.after(30)
        # Возвращаем на место
        self.canvas.coords(
            self.bg_rect,
            self.root.winfo_screenwidth()//2 - 300,
            self.root.winfo_screenheight()//2 - 275,
            self.root.winfo_screenwidth()//2 + 300,
            self.root.winfo_screenheight()//2 + 275
        )
    
    def check_password(self):
        """Проверка пароля"""
        password = self.password_entry.get()
        
        if not password:
            self.show_error("⚠ ВВЕДИТЕ ПАРОЛЬ ⚠")
            self.shake_window()
            return
        
        if self.hash_password(password) == self.password_hash:
            # Правильный пароль - плавное закрытие
            self.unlock_animation()
        else:
            # Неправильный пароль
            self.failed_attempts += 1
            remaining = self.max_attempts - self.failed_attempts
            
            if remaining > 0:
                self.show_error(f"✖ НЕВЕРНЫЙ ПАРОЛЬ ✖")
                self.attempts_label.config(
                    text=f"ПОПЫТОК ОСТАЛОСЬ: {remaining}",
                    fg='#FF0000' if remaining == 1 else '#DC143C'
                )
                self.shake_window()
                self.password_entry.delete(0, tk.END)
                self.password_entry.focus_set()
            else:
                # Попытки исчерпаны
                self.show_error("✖✖✖ ДОСТУП ЗАБЛОКИРОВАН ✖✖✖")
                self.attempts_label.config(
                    text="⚠ ПОПЫТКИ ИСЧЕРПАНЫ ⚠",
                    fg='#FF0000'
                )
                self.submit_button.config(state='disabled', bg='#3a0000')
                self.password_entry.config(state='disabled')
                self.flash_screen()
    
    def unlock_animation(self):
        """Анимация разблокировки"""
        self.title_label.config(text="✓ РАЗБЛОКИРОВАНО ✓", fg='#00FF00')
        self.error_label.config(text="")
        self.attempts_label.config(text="")
        self.password_entry.config(state='disabled')
        self.submit_button.config(state='disabled')
        
        # Плавное затухание через 1 секунду
        self.root.after(1000, self.fade_out)
    
    def fade_out(self, alpha=1.0):
        """Плавное затухание"""
        if alpha > 0:
            self.root.attributes('-alpha', alpha)
            self.root.after(30, lambda: self.fade_out(alpha - 0.05))
        else:
            self.unlock()
    
    def flash_screen(self, count=0):
        """Мигание"""
        if count < 6:
            color = '#FF0000' if count % 2 == 0 else '#0a0000'
            self.canvas.itemconfig(self.bg_rect, fill=color)
            self.root.after(200, lambda: self.flash_screen(count + 1))
        else:
            self.canvas.itemconfig(self.bg_rect, fill='#0a0000')
    
    def show_error(self, message):
        """Показ ошибки"""
        self.error_label.config(text=message)
        self.root.after(2500, lambda: self.error_label.config(text=""))
    
    def unlock(self):
        """Разблокировка"""
        self.restore_taskbar()
        self.root.grab_release()
        self.root.destroy()
    
    def run(self):
        """Запуск"""
        try:
            self.root.mainloop()
        finally:
            self.restore_taskbar()


def main():
    try:
        locker = AggressiveLocker()
        locker.run()
    except Exception as e:
        print(f"Error: {e}")
        try:
            user32 = ctypes.windll.user32
            taskbar = user32.FindWindowW("Shell_TrayWnd", None)
            if taskbar:
                user32.ShowWindow(taskbar, 1)
        except:
            pass


if __name__ == "__main__":
    main()
