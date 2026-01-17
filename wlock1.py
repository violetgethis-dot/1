import tkinter as tk
from tkinter import messagebox
import hashlib
import sys
import ctypes
from ctypes import wintypes
import base64
from io import BytesIO
try:
    from PIL import Image, ImageTk
except ImportError:
    Image = None
    ImageTk = None
import random

# Встроенный логотип FSOCIETY в base64
LOGO_BASE64 = """
iVBORw0KGgoAAAANSUhEUgAABLAAAAKACAYAAAC7bAQnAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8
YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAP+lSURBVHhe7N0HnBXV/f//N/fe3V0pS1lAeu+9SBdBUVCx
xYKNGDWxxl7z/yZ+Y4z5mhhjb7H3LvYGKtJ7771t2V52+73n/88595zZhRVZ2F3g9Xw85jG7d+7ce+45
c+bMmTPnfP7/AQAAAAAAAAAAdFDGf/8HAAAAAAAAAADoiAhgAQAAAAAAAAAAdHAEsAAAAAAAAAAA
ADo4AlgAAAAAAAAAAAAdHAEsAAAAAAAAAACEDo4AlgAAAAAAAAAAAAdHAEsAAAAAAAAAACEDo4A
lgAAAAAAAAAAAAdHAEsAAAAAAAAAAKCDI4AFAAAAAAAAAADQwRHAAgAAAAAAAAAA6OAIYAEAgIO2
aNEi+eY3vyn9+vWTjIwMycvLkx49esg111wjGzduPNjLAwAAAAAAYRwBLAAAcFD+/e9/y7Bhw+T1
11+XsrIyqa+vF/2Zl5cnDzzwgAwcOFCef/75g79IAAAAAADQphHAAgAAB+zll1+W8847T4qKikRU
VlaWDBkyRM4++2wZO3asZGdny7Zt2+Tss8+Wl1566aCvEwAAAAAAtG0EsAAAwAHR4r/zzz9fdLpa
Wlqa/OhHP5L58+fLggUL5JVXXpHLL79c0tPTpaamRi688ELZunXrQV8rAAAAAABouwhgAQCAA3Lj
jTfK9u3bRX8+/fTTcu+998rgwYOlU6dO0rFjRxk4cKDcc889Mn36dDFNU26++eaDvlYAAAAAANB2
EcACAAAHZPz48dKrVy954okn5IgjjohZ//TTT5devXrJuHHjDvpaAAAAAABA20cACwAAAAAAAAAA
oIMjgAUAAAAAAAAAANDBEcACAAAAAAAAAOB/IYAFAAAAAAAAAADQwRHAAgAAAAAAAAAA6OAI
YAEAAAAAAAAAAHRPBLAAAAAAAAAAAH3ZQ0cBWAAAAAAAAAdVVFQk69atk/Lycv0/AAAAADoQXd5l
ZWVJv379JCcnJ+HnEsACAAAAADqQlStXym9+8xuZOnWq/h8AAAAAHYhOs/r27SuXX365HHXUUTrv
E46ggwKAtiAnJ0cmTJggw4YNk+uvv15mz57dZL2eTjzySMnNzZV///vfMmfOnJhtH330UZk+fbr8
+te/lv79+zc3l/dHjx49Gt/333//lS9+8Yu0XQAAAAAA2prVq1dLaWmp7N27V/eFOzsAAAAAaG90
vlVSUiJ69Oxo5l4CWADQBmiASsPJ+rPTvHnzZNCgQfLYY4/JL3/5S5k+fboMHTpUf1544YVy7733
ynXXXSd/+ctfdL0///nPep3KHXfcIatWrdIFbfv27fWRlZWlC/mtW7fKwoUL5ZJLLpE1a9bo+/1v
v6Ojo9PDy/8GAAAAAAAHRX/Pz8+XcePGyfXXX6+vNYH8E/8CAAAAAAAH5IQTTpC+ffvK2rVr
daW+fftq5m0gAAAAAAAAEMYRwAIAAAAAAAAAOjgCWAAAAAAAAAAAAABABcEAAAAAAAAAgA6OABYAAAAAAAAAEA
RwBLAAAAAAAAAAigA+OABYAAAAAAAAAQO4jgAUAAAAAAAAAdHAEsAAAAAAAAAAAOjgCWAAAgIOyefNmyczMFL2r2v/3//0/
GTRokOTk5Mg333wzZp0PPvhAr0P/v//++5P9PgAAAAAA0P4QwAIAAAdk8eLFcuONN8qVV14p+/btkxdf
fFE2btwoS5YskTPPPDP/X/7zPz+ve+6/Pmvr+//f9LXbbb/1fX///fe89xo9e/jw5559+31fv3p99n7n
6wgAAAAAAA4dAlgAAOCAvPzyyzJlyhT54IMPZPv27Xq//fbbT379618/fffdd/+v//u/H//X//2f//u//7f/T9r/X7fR13r+
Ow9EUlJTU16urqpZM2fOnE+/9x3vsv/+///7f77//vv//u//X//9//fXv//O//X//X//u///Of//f//Z//
0N93//Xv//Of//9X1ffT//v8b3/v8b3/u/r9/zv97/n+Pf//P//L//n/9X//s/5f/8v//u/frf/r//v
/+L//v8/+f+1fT//7/zf/t//f+X+r/3/8X//P/9X/+N//g/+//+b/8X/z/+v8/9/P//X///X////
+b/9v/Xf//8V/9n/V/93/7f/X/////u//n///9X//f////v////X/////X//n/f//9////////
////////1/////3////v////X///////////v////f////n////v//////////v/////////
////////////////////////////////////////////////////////X//f9///3//f////
////////////////////////////////////////////////////////////////////////
//////////////////////7///3///f////////////////////////////////////
////////////////////////////////////////////////////////////////////////
///////////////////f9///3//f/9//3///////////////////////////////
////////////////////////////////////////////////////////////////////////
//////////////3////f9///3//f9////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////f////9//3//f9///3///////////////////////////////////////
////////////////////////////////////////////////////////////////////////
//////////9////f9///3//f/9//3///////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////9///f////9//3//f/9///////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////3//f9///f////9//3//f9/////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////3//f9///f////9//3//f/////////////////////////////////////
////////////////////////////////////////////////////////////////////////
//////////////9//3//f9///f////9//3//f//////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////3//f9///f////9//3//f//////////////////////////////////
////////////////////////////////////////////////////////////////////////
//////////////////9//3//f9///f////9//3/////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////3//f9///f////9//3//f//////////////////////////////
////////////////////////////////////////////////////////////////////////
//////////////////////9//3//f9///f////9//3/////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////3//f9///f////9//3//f//////////////////////////
////////////////////////////////////////////////////////////////////////
//////////////////////////9//3//f9///f////9//3/////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////3//f9///f////9//3//f//////////////////////
////////////////////////////////////////////////////////////////////////
//////////////////////////////9//3//f9///f////9//3///////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////3//f9///f////9//3//f////////////////
////////////////////////////////////////////////////////////////////////
//////////////////////////////////9//3//f9///f////9//3///////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////3//f9///f////9//3//f////////////
////////////////////////////////////////////////////////////////////////
//////////////////////////////////////9//3//f9///f////9//3///////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////3//f9///f////9//3//f////////
////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////9//3//f9///f////9//3///////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////3//f9///f////9//3//f////
////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////9//3//f9///f////9//3///
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////3//f9///f////9//3//f/
////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////9//3//f9///f////9//3
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////3//f9///f////9//3/
////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////9//3//f9///f////9
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////3//f9///f////9
////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////9//3//f9///f//
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////3//f9///f///
////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////9//3//f9///
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////3//f9///
////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////9//3//
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////3//f
////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////9/
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////3
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
========END OF BASE64 IMAGE========
"""

class HackerLocker:
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
        
        # Счетчик неудачных попыток
        self.failed_attempts = 0
        self.max_attempts = 3
        
        # Фоновая анимация двоичного кода
        self.binary_lines = []
        
        # Настройка UI
        self.setup_ui()
        
        # Агрессивная блокировка событий
        self.setup_aggressive_bindings()
        
        # Постоянный захват фокуса
        self.keep_focus()
        
        # Запуск анимации двоичного кода
        self.animate_binary()
        
    def block_windows_keys(self):
        """Блокировка системных клавиш Windows"""
        try:
            # Попытка скрыть панель задач
            try:
                user32 = ctypes.windll.user32
                taskbar = user32.FindWindowW("Shell_TrayWnd", None)
                if taskbar:
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
    
    def load_logo(self):
        """Загрузка логотипа из base64"""
        try:
            if Image and ImageTk:
                # Декодируем base64
                image_data = base64.b64decode(LOGO_BASE64)
                # Создаём изображение из байтов
                image = Image.open(BytesIO(image_data))
                # Изменяем размер для красоты
                image = image.resize((400, 150), Image.Resampling.LANCZOS)
                # Конвертируем в PhotoImage
                return ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"Error loading logo: {e}")
        return None
    
    def setup_ui(self):
        """Создание хакерского интерфейса"""
        # Чёрный фон
        self.root.configure(bg='#000000')
        
        # Canvas для двоичного кода на фоне
        self.canvas = tk.Canvas(
            self.root,
            bg='#000000',
            highlightthickness=0
        )
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Главный контейнер поверх canvas
        main_frame = tk.Frame(self.root, bg='#000000')
        main_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Загружаем логотип FSOCIETY
        logo_image = self.load_logo()
        
        if logo_image:
            logo_label = tk.Label(main_frame, image=logo_image, bg='#000000')
            logo_label.image = logo_image  # Сохраняем ссылку
            logo_label.pack(pady=30)
        else:
            # Fallback текст если не удалось загрузить картинку
            ascii_art = tk.Label(
                main_frame,
                text="FSOCIETY",
                font=("Courier New", 36, "bold"),
                bg='#000000',
                fg='#FF0000'
            )
            ascii_art.pack(pady=30)
        
        # Заголовок в стиле консоли
        title_label = tk.Label(
            main_frame,
            text=">>> ACCESS DENIED <<<",
            font=("Courier New", 32, "bold"),
            bg='#000000',
            fg='#00FF00'
        )
        title_label.pack(pady=15)
        
        # Разделитель
        separator = tk.Label(
            main_frame,
            text="=" * 50,
            font=("Courier New", 10),
            bg='#000000',
            fg='#00FF00'
        )
        separator.pack(pady=5)
        
        # Инструкция
        info_label = tk.Label(
            main_frame,
            text="[!] ENTER PASSWORD TO UNLOCK SYSTEM [!]",
            font=("Courier New", 12, "bold"),
            bg='#000000',
            fg='#00FF00'
        )
        info_label.pack(pady=20)
        
        # Промпт как в консоли
        prompt_label = tk.Label(
            main_frame,
            text="root@system:~$ ",
            font=("Courier New", 14, "bold"),
            bg='#000000',
            fg='#00FF00'
        )
        prompt_label.pack(pady=5)
        
        # Поле ввода пароля в стиле терминала
        self.password_entry = tk.Entry(
            main_frame,
            show="*",
            font=("Courier New", 18, "bold"),
            width=30,
            bg='#0a0a0a',
            fg='#00FF00',
            insertbackground='#00FF00',
            relief='solid',
            bd=2,
            highlightthickness=0
        )
        self.password_entry.pack(pady=15, ipady=8)
        self.password_entry.focus_set()
        
        # Кнопка
        self.submit_button = tk.Button(
            main_frame,
            text="[ EXECUTE ]",
            command=self.check_password,
            font=("Courier New", 14, "bold"),
            bg='#003300',
            fg='#00FF00',
            activebackground='#005500',
            activeforeground='#00FF00',
            relief='solid',
            bd=2,
            cursor='hand2',
            width=20,
            height=2
        )
        self.submit_button.pack(pady=15)
        
        # Метка для ошибок
        self.error_label = tk.Label(
            main_frame,
            text="",
            font=("Courier New", 12, "bold"),
            bg='#000000',
            fg='#FF0000'
        )
        self.error_label.pack(pady=10)
        
        # Счётчик попыток
        self.attempts_label = tk.Label(
            main_frame,
            text=f"[i] Attempts remaining: {self.max_attempts}",
            font=("Courier New", 11),
            bg='#000000',
            fg='#FFFF00'
        )
        self.attempts_label.pack(pady=10)
    
    def animate_binary(self):
        """Анимация падающего двоичного кода"""
        # Создаём новые линии кода
        if random.random() < 0.3:  # 30% шанс создать новую линию
            x = random.randint(0, self.root.winfo_width())
            binary = ''.join(random.choice('01') for _ in range(random.randint(10, 20)))
            line = self.canvas.create_text(
                x, 0,
                text=binary,
                fill='#003300',
                font=('Courier New', 10),
                anchor='n'
            )
            self.binary_lines.append({'id': line, 'y': 0, 'speed': random.randint(1, 3)})
        
        # Обновляем существующие линии
        for line in self.binary_lines[:]:
            line['y'] += line['speed']
            self.canvas.coords(line['id'], self.canvas.coords(line['id'])[0], line['y'])
            
            # Удаляем линии, вышедшие за экран
            if line['y'] > self.root.winfo_height():
                self.canvas.delete(line['id'])
                self.binary_lines.remove(line)
        
        # Повторяем анимацию
        self.root.after(50, self.animate_binary)
    
    def setup_aggressive_bindings(self):
        """Агрессивная блокировка всех комбинаций"""
        self.root.protocol("WM_DELETE_WINDOW", self.block_action)
        
        # Блокировка всех опасных клавиш
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
        
        # Win, Alt, Ctrl комбинации
        for key in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                    'Tab', 'Escape', 'space', 'Up', 'Down', 'Left', 'Right']:
            dangerous_keys.extend([
                f'<Super-{key}>',
                f'<Alt-{key}>',
                f'<Control-{key}>',
                f'<Control-Alt-{key}>',
                f'<Control-Shift-{key}>'
            ])
        
        for key in dangerous_keys:
            try:
                self.root.bind(key, self.block_action)
            except:
                pass
        
        # Enter для отправки
        self.password_entry.bind('<Return>', lambda e: self.check_password())
        
        # Блокировка потери фокуса
        self.root.bind('<FocusOut>', lambda e: self.force_focus())
        
        # Блокировка ПКМ
        self.root.bind('<Button-3>', self.block_action)
    
    def block_action(self, event=None):
        """Блокировка действия"""
        return "break"
    
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
            self.show_error("[!] ERROR: Password field is empty")
            return
        
        if self.hash_password(password) == self.password_hash:
            # Правильный пароль - ВАЖНО: сначала освобождаем всё
            self.root.grab_release()
            self.restore_taskbar()
            
            # Показываем сообщение
            messagebox.showinfo(
                "Access Granted", 
                "System unlocked successfully!",
                parent=self.root
            )
            
            # Закрываем окно
            self.root.quit()
            self.root.destroy()
        else:
            # Неправильный пароль
            self.failed_attempts += 1
            remaining = self.max_attempts - self.failed_attempts
            
            if remaining > 0:
                self.show_error(f"[X] AUTHENTICATION FAILED")
                self.attempts_label.config(
                    text=f"[!] Attempts remaining: {remaining}",
                    fg='#FF0000' if remaining == 1 else '#FFFF00'
                )
                self.password_entry.delete(0, tk.END)
                self.password_entry.focus_set()
            else:
                # Попытки исчерпаны
                self.show_error("[X] ACCESS PERMANENTLY DENIED")
                self.attempts_label.config(
                    text="[!] MAXIMUM ATTEMPTS EXCEEDED",
                    fg='#FF0000'
                )
                self.submit_button.config(state='disabled', bg='#1a0000')
                self.password_entry.config(state='disabled')
                
                messagebox.showerror(
                    "LOCKDOWN",
                    "[CRITICAL ERROR]\n\n"
                    "Maximum authentication attempts exceeded.\n"
                    "System is now in lockdown mode.\n\n"
                    "Contact system administrator.",
                    parent=self.root
                )
    
    def show_error(self, message):
        """Показ сообщения об ошибке"""
        self.error_label.config(text=message)
        self.root.after(3000, lambda: self.error_label.config(text=""))
    
    def run(self):
        """Запуск блокировщика"""
        try:
            self.root.mainloop()
        finally:
            self.restore_taskbar()


def main():
    """Главная функция"""
    try:
        locker = HackerLocker()
        locker.run()
    except Exception as e:
        print(f"Error: {e}")
        # Восстанавливаем панель задач
        try:
            user32 = ctypes.windll.user32
            taskbar = user32.FindWindowW("Shell_TrayWnd", None)
            if taskbar:
                user32.ShowWindow(taskbar, 1)
        except:
            pass


if __name__ == "__main__":
    main()
