"""
DES Cipher — Desktop GUI (Tkinter)
Hiển thị đầy đủ: 16 khóa con, trạng thái L/R từng vòng, bản mã/bản rõ.
Implement DES từ scratch theo chuẩn FIPS 46-3 — không dùng thư viện crypto.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random, os

# ═══════════════════════════════════════════════════════════════
#  DES CONSTANTS (FIPS 46-3)
# ═══════════════════════════════════════════════════════════════

IP = [58,50,42,34,26,18,10,2,60,52,44,36,28,20,12,4,
      62,54,46,38,30,22,14,6,64,56,48,40,32,24,16,8,
      57,49,41,33,25,17,9,1,59,51,43,35,27,19,11,3,
      61,53,45,37,29,21,13,5,63,55,47,39,31,23,15,7]

IP_INV = [40,8,48,16,56,24,64,32,39,7,47,15,55,23,63,31,
          38,6,46,14,54,22,62,30,37,5,45,13,53,21,61,29,
          36,4,44,12,52,20,60,28,35,3,43,11,51,19,59,27,
          34,2,42,10,50,18,58,26,33,1,41,9,49,17,57,25]

E_TABLE = [32,1,2,3,4,5,4,5,6,7,8,9,8,9,10,11,
           12,13,12,13,14,15,16,17,16,17,18,19,20,21,20,21,
           22,23,24,25,24,25,26,27,28,29,28,29,30,31,32,1]

P_TABLE = [16,7,20,21,29,12,28,17,1,15,23,26,5,18,31,10,
           2,8,24,14,32,27,3,9,19,13,30,6,22,11,4,25]

PC1 = [57,49,41,33,25,17,9,1,58,50,42,34,26,18,
       10,2,59,51,43,35,27,19,11,3,60,52,44,36,
       63,55,47,39,31,23,15,7,62,54,46,38,30,22,
       14,6,61,53,45,37,29,21,13,5,28,20,12,4]

PC2 = [14,17,11,24,1,5,3,28,15,6,21,10,
       23,19,12,4,26,8,16,7,27,20,13,2,
       41,52,31,37,47,55,30,40,51,45,33,48,
       44,49,39,56,34,53,46,42,50,36,29,32]

SHIFTS = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]

S_BOXES = [
    [[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
     [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
     [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
     [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]],
    [[15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
     [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
     [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
     [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]],
    [[10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
     [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
     [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
     [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]],
    [[7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
     [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
     [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
     [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]],
    [[2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
     [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
     [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
     [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]],
    [[12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
     [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
     [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
     [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]],
    [[4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
     [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
     [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
     [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]],
    [[13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
     [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
     [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
     [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]],
]

# ═══════════════════════════════════════════════════════════════
#  DES CORE (FIPS 46-3 từ scratch)
# ═══════════════════════════════════════════════════════════════

def _permute(block, table):
    return [block[t - 1] for t in table]

def _bytes_to_bits(b: bytes) -> list:
    bits = []
    for byte in b:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)
    return bits

def _bits_to_bytes(bits: list) -> bytes:
    out = []
    for i in range(0, len(bits), 8):
        val = 0
        for b in bits[i:i+8]:
            val = (val << 1) | b
        out.append(val)
    return bytes(out)

def _bits_to_hex(bits: list) -> str:
    val = 0
    for b in bits:
        val = (val << 1) | b
    nbytes = (len(bits) + 3) // 4
    return f"{val:0{nbytes}X}"

def _left_shift(bits, n):
    return bits[n:] + bits[:n]

def _xor(a, b):
    return [x ^ y for x, y in zip(a, b)]

def _f(r32, subkey48):
    exp = _permute(r32, E_TABLE)          # 32 → 48
    xored = _xor(exp, subkey48)
    sout = []
    for i in range(8):
        chunk = xored[i*6:(i+1)*6]
        row = (chunk[0] << 1) | chunk[5]
        col = (chunk[1]<<3)|(chunk[2]<<2)|(chunk[3]<<1)|chunk[4]
        val = S_BOXES[i][row][col]
        for j in range(3, -1, -1):
            sout.append((val >> j) & 1)
    return _permute(sout, P_TABLE)        # 32 bits

def generate_subkeys(key8: bytes) -> list:
    """Sinh 16 khóa con 48-bit từ khóa 64-bit (56-bit hiệu dụng)."""
    kb = _bytes_to_bits(key8)
    cd = _permute(kb, PC1)               # 56 bits
    c, d = cd[:28], cd[28:]
    subkeys = []
    for i in range(16):
        c = _left_shift(c, SHIFTS[i])
        d = _left_shift(d, SHIFTS[i])
        subkeys.append(_permute(c + d, PC2))   # 48 bits
    return subkeys

def des_process_block(block8: bytes, subkeys: list) -> tuple:
    """
    Mã hóa/giải mã 1 block 8 byte.
    Trả về (result_bytes, round_info_list).
    round_info[0] = sau IP, round_info[1..16] = sau mỗi vòng Feistel.
    """
    bits = _bytes_to_bits(block8)
    bits = _permute(bits, IP)
    L, R = bits[:32], bits[32:]

    info = [{'round': 0, 'label': 'Sau IP',
             'L': _bits_to_hex(L), 'R': _bits_to_hex(R),
             'K': '—'}]

    for i in range(16):
        new_L = R[:]
        new_R = _xor(L, _f(R, subkeys[i]))
        L, R = new_L, new_R
        info.append({
            'round': i + 1,
            'label': f'Vòng {i+1:02d}',
            'L': _bits_to_hex(L),
            'R': _bits_to_hex(R),
            'K': _bits_to_hex(subkeys[i]),
        })

    combined = _permute(R + L, IP_INV)
    return _bits_to_bytes(combined), info

def pad_pkcs7(data: bytes) -> bytes:
    n = 8 - (len(data) % 8)
    return data + bytes([n] * n)

def unpad_pkcs7(data: bytes) -> bytes:
    n = data[-1]
    if n < 1 or n > 8:
        raise ValueError("Padding không hợp lệ")
    return data[:-n]

def des_encrypt(plaintext_hex: str, key8: bytes):
    """Trả về (hex_ciphertext, subkeys_hex_list, all_rounds_info).
    plaintext_hex: chuỗi hex (0-9, A-F), tự động upper-case và pad nếu lẻ nibble.
    """
    subkeys = generate_subkeys(key8)
    subkeys_hex = [_bits_to_hex(sk) for sk in subkeys]

    # Chuẩn hóa hex string → bytes
    hex_clean = plaintext_hex.strip().upper()
    if len(hex_clean) % 2 != 0:
        hex_clean = hex_clean + '0'   # pad nibble lẻ (hiếm gặp trong đề thi)
    data = bytes.fromhex(hex_clean)

    data = pad_pkcs7(data)
    cipher_blocks = []
    all_rounds = []
    for i in range(0, len(data), 8):
        block = data[i:i+8]
        cb, info = des_process_block(block, subkeys)
        cipher_blocks.append(cb)
        all_rounds.append({'block': i//8 + 1,
                           'plain_hex': block.hex().upper(),
                           'rounds': info})

    cipher_hex = b''.join(cipher_blocks).hex().upper()
    return cipher_hex, subkeys_hex, all_rounds

def des_decrypt(cipher_hex: str, key8: bytes):
    """Trả về plaintext hex string."""
    subkeys = generate_subkeys(key8)
    rev_subkeys = list(reversed(subkeys))

    data = bytes.fromhex(cipher_hex)
    plain_blocks = []
    for i in range(0, len(data), 8):
        block = data[i:i+8]
        pb, _ = des_process_block(block, rev_subkeys)
        plain_blocks.append(pb)

    padded = b''.join(plain_blocks)
    return unpad_pkcs7(padded).hex().upper()

def random_des_key() -> str:
    return ''.join(random.choices('0123456789ABCDEF', k=16))

# ═══════════════════════════════════════════════════════════════
#  PALETTE & STYLE
# ═══════════════════════════════════════════════════════════════

BG      = "#0d1117"
PANEL   = "#161b22"
CARD    = "#1c2128"
BORDER  = "#30363d"
FG      = "#c9d1d9"
FG_DIM  = "#6e7681"
ACCENT  = "#f78166"       # warm red-orange — DES theme
ACCENT2 = "#79c0ff"
GREEN   = "#56d364"
YELLOW  = "#e3b341"
PURPLE  = "#d2a8ff"

F_TITLE = ("Courier New", 16, "bold")
F_HEAD  = ("Courier New", 11, "bold")
F_MONO  = ("Courier New", 10)
F_SMALL = ("Courier New", 9)
F_BTN   = ("Courier New", 10, "bold")

# ═══════════════════════════════════════════════════════════════
#  GUI
# ═══════════════════════════════════════════════════════════════

class DESApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DES Cipher — Step-by-Step Viewer")
        self.configure(bg=BG)
        self.minsize(1000, 680)

        self._last_subkeys  = []
        self._last_rounds   = []
        self._last_cipher   = ""

        self._build_styles()
        self._build_ui()

        self.update_idletasks()
        w, h = 1100, 750
        x = (self.winfo_screenwidth()  - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    # ── styles ──────────────────────────────────────────────────
    def _build_styles(self):
        st = ttk.Style()
        st.theme_use("clam")
        st.configure("Treeview",
                     background=CARD, foreground=FG,
                     fieldbackground=CARD, rowheight=22,
                     font=F_MONO)
        st.configure("Treeview.Heading",
                     background=PANEL, foreground=ACCENT,
                     font=("Courier New", 9, "bold"), relief="flat")
        st.map("Treeview",
               background=[("selected", BORDER)],
               foreground=[("selected", ACCENT2)])
        st.configure("Vertical.TScrollbar",
                     background=BORDER, troughcolor=CARD,
                     arrowcolor=FG_DIM, bordercolor=CARD)
        st.configure("TNotebook",
                     background=BG, borderwidth=0)
        st.configure("TNotebook.Tab",
                     background=PANEL, foreground=FG_DIM,
                     font=F_MONO, padding=[12, 5])
        st.map("TNotebook.Tab",
               background=[("selected", CARD)],
               foreground=[("selected", ACCENT)])

    # ── helpers ─────────────────────────────────────────────────
    def _frm(self, parent, bg=None, **kw):
        return tk.Frame(parent, bg=bg or BG, **kw)

    def _lbl(self, parent, text, fg=FG, font=None, bg=None, **kw):
        return tk.Label(parent, text=text, fg=fg,
                        font=font or F_MONO,
                        bg=bg or parent.cget("bg"), **kw)

    def _entry(self, parent, **kw):
        return tk.Entry(parent, bg=CARD, fg=FG,
                        insertbackground=FG,
                        relief="flat", font=F_MONO,
                        disabledbackground=CARD,
                        disabledforeground=FG_DIM, **kw)

    def _text(self, parent, h=4, **kw):
        t = tk.Text(parent, bg=CARD, fg=FG,
                    insertbackground=FG, relief="flat",
                    font=F_MONO, height=h,
                    selectbackground=ACCENT, selectforeground=BG,
                    wrap="word", **kw)
        return t

    def _btn(self, parent, text, cmd, color=ACCENT, width=18):
        b = tk.Button(parent, text=text, command=cmd,
                      bg=color, fg=BG,
                      activebackground=color, activeforeground=BG,
                      relief="flat", font=F_BTN,
                      cursor="hand2", width=width, pady=5)
        lighter = self._lighten(color)
        b.bind("<Enter>", lambda e: b.config(bg=lighter))
        b.bind("<Leave>", lambda e: b.config(bg=color))
        return b

    @staticmethod
    def _lighten(h, amt=25):
        h = h.lstrip('#')
        r,g,b = int(h[0:2],16),int(h[2:4],16),int(h[4:6],16)
        return f"#{min(255,r+amt):02x}{min(255,g+amt):02x}{min(255,b+amt):02x}"

    def _sep(self, parent):
        tk.Frame(parent, bg=BORDER, height=1).pack(fill="x", pady=6)

    def _set_text(self, widget, value, fg=None):
        widget.config(state="normal")
        widget.delete("1.0", "end")
        widget.insert("end", value)
        if fg:
            widget.config(fg=fg)
        widget.config(state="disabled")

    # ── main UI ─────────────────────────────────────────────────
    def _build_ui(self):
        # Header
        hdr = self._frm(self, bg=PANEL)
        hdr.pack(fill="x")
        tk.Frame(hdr, bg=ACCENT, width=4).pack(side="left", fill="y")
        self._lbl(hdr, "  ⚙  DES CIPHER — STEP-BY-STEP VIEWER",
                  fg=FG, font=F_TITLE, bg=PANEL).pack(side="left", pady=12)
        self._lbl(hdr, "  FIPS 46-3 · 64-bit block · 56-bit key · 16 Feistel rounds  ",
                  fg=FG_DIM, font=F_SMALL, bg=PANEL).pack(side="left", pady=12)

        # Body: left input + right notebook
        body = self._frm(self)
        body.pack(fill="both", expand=True, padx=12, pady=10)
        body.columnconfigure(0, weight=0, minsize=310)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)

        self._build_input_panel(body)
        self._build_output_panel(body)

    def _build_input_panel(self, parent):
        pnl = self._frm(parent, bg=PANEL)
        pnl.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # ── Message ─────────────────────────────────────────────
        self._lbl(pnl, "BẢN TIN M (plaintext hex)", fg=ACCENT,
                  font=F_HEAD, bg=PANEL).pack(anchor="w", padx=12, pady=(14, 2))
        self._lbl(pnl, "Nhập chuỗi ký tự hex (0-9, A-F), thường 16 ký tự",
                  fg=FG_DIM, font=F_SMALL, bg=PANEL).pack(anchor="w", padx=12)

        msg_frm = self._frm(pnl, bg=CARD)
        msg_frm.pack(fill="x", padx=10, pady=6)
        self._msg = self._text(msg_frm, h=5)
        self._msg.pack(fill="both", padx=6, pady=6)

        tk.Frame(pnl, bg=BORDER, height=1).pack(fill="x", padx=10, pady=4)

        # ── Key ─────────────────────────────────────────────────
        self._lbl(pnl, "KHÓA K (16 ký tự hex = 64 bit)", fg=ACCENT,
                  font=F_HEAD, bg=PANEL).pack(anchor="w", padx=12, pady=(4, 2))
        self._lbl(pnl, "16 ký tự hex (0-9, A-F) → 8 byte = 64-bit DES key",
                  fg=FG_DIM, font=F_SMALL, bg=PANEL).pack(anchor="w", padx=12)

        key_frm = self._frm(pnl, bg=CARD)
        key_frm.pack(fill="x", padx=10, pady=6)
        self._key_var = tk.StringVar()
        self._key_var.trace_add("write", self._on_key_change)
        self._key_entry = self._entry(key_frm, textvariable=self._key_var)
        self._key_entry.pack(fill="x", padx=6, ipady=7, pady=(6,2))
        self._key_hint = self._lbl(key_frm, "", fg=FG_DIM, font=F_SMALL, bg=CARD)
        self._key_hint.pack(anchor="w", padx=6, pady=(0,6))

        rnd_btn = self._btn(pnl, "🎲  Random Key", self._random_key,
                            color="#30363d", width=20)
        rnd_btn.pack(pady=(2, 8), padx=10, fill="x")

        tk.Frame(pnl, bg=BORDER, height=1).pack(fill="x", padx=10, pady=4)

        # ── Cipher hex (for decrypt) ─────────────────────────────
        self._lbl(pnl, "BẢN MÃ HEX (để giải mã)", fg=ACCENT2,
                  font=F_HEAD, bg=PANEL).pack(anchor="w", padx=12, pady=(4, 2))
        self._lbl(pnl, "Bỏ trống nếu chỉ mã hóa",
                  fg=FG_DIM, font=F_SMALL, bg=PANEL).pack(anchor="w", padx=12)
        cipher_in_frm = self._frm(pnl, bg=CARD)
        cipher_in_frm.pack(fill="x", padx=10, pady=6)
        self._cipher_input = self._text(cipher_in_frm, h=3)
        self._cipher_input.config(state="normal")
        self._cipher_input.pack(fill="both", padx=6, pady=6)

        tk.Frame(pnl, bg=BORDER, height=1).pack(fill="x", padx=10, pady=4)

        # ── Action buttons ───────────────────────────────────────
        bf = self._frm(pnl, bg=PANEL)
        bf.pack(fill="x", padx=10, pady=6)
        self._btn(bf, "🔒  MÃ HÓA", self._do_encrypt, ACCENT, 14).pack(
            side="left", padx=(0, 6))
        self._btn(bf, "🔓  GIẢI MÃ", self._do_decrypt, ACCENT2, 14).pack(
            side="left")

        self._btn(pnl, "🗑  Xóa tất cả", self._clear_all,
                  "#30363d", 20).pack(padx=10, pady=(4,10), fill="x")

        # status
        self._status_var = tk.StringVar(value="Sẵn sàng.")
        self._lbl(pnl, "", fg=GREEN, font=F_SMALL, bg=PANEL,
                  textvariable=self._status_var).pack(padx=12, pady=(0,10))

    def _build_output_panel(self, parent):
        nb = ttk.Notebook(parent)
        nb.grid(row=0, column=1, sticky="nsew")
        self._nb = nb

        # Tab 1: Kết quả
        t1 = self._frm(nb, bg=BG)
        nb.add(t1, text="  📄  Kết Quả  ")
        self._build_result_tab(t1)

        # Tab 2: Key Schedule
        t2 = self._frm(nb, bg=BG)
        nb.add(t2, text="  🔑  16 Khóa Con  ")
        self._build_keysched_tab(t2)

        # Tab 3: Vòng Feistel
        t3 = self._frm(nb, bg=BG)
        nb.add(t3, text="  🔄  Trạng Thái 16 Vòng  ")
        self._build_rounds_tab(t3)

        # Tab 4: Hướng dẫn
        t4 = self._frm(nb, bg=BG)
        nb.add(t4, text="  ℹ️  Lý Thuyết  ")
        self._build_theory_tab(t4)

    # ── Tab 1: Result ────────────────────────────────────────────
    def _build_result_tab(self, parent):
        self._lbl(parent, "KEY HEX", fg=FG_DIM, font=F_SMALL).pack(
            anchor="w", padx=12, pady=(12, 0))
        kf = self._frm(parent, bg=CARD)
        kf.pack(fill="x", padx=12, pady=(2, 8))
        self._res_keyhex = self._text(kf, h=1)
        self._res_keyhex.pack(fill="x", padx=6, pady=4)
        self._res_keyhex.config(state="disabled")

        self._lbl(parent, "PLAINTEXT", fg=FG_DIM, font=F_SMALL).pack(
            anchor="w", padx=12)
        pf = self._frm(parent, bg=CARD)
        pf.pack(fill="x", padx=12, pady=(2, 8))
        self._res_plain = self._text(pf, h=3)
        self._res_plain.pack(fill="both", padx=6, pady=4)
        self._res_plain.config(state="disabled")

        self._lbl(parent, "CIPHERTEXT (HEX)", fg=ACCENT, font=F_SMALL).pack(
            anchor="w", padx=12)
        cf = self._frm(parent, bg=CARD)
        cf.pack(fill="x", padx=12, pady=(2, 8))
        self._res_cipher = self._text(cf, h=3)
        self._res_cipher.pack(fill="both", padx=6, pady=4)
        self._res_cipher.config(fg=ACCENT, state="disabled")

        self._lbl(parent, "DECRYPTED TEXT", fg=GREEN, font=F_SMALL).pack(
            anchor="w", padx=12)
        df = self._frm(parent, bg=CARD)
        df.pack(fill="x", padx=12, pady=(2, 8))
        self._res_dec = self._text(df, h=3)
        self._res_dec.pack(fill="both", padx=6, pady=4)
        self._res_dec.config(fg=GREEN, state="disabled")

        copy_frm = self._frm(parent, bg=BG)
        copy_frm.pack(fill="x", padx=12)
        self._btn(copy_frm, "📋  Copy Cipher Hex", self._copy_cipher,
                  "#30363d", 20).pack(side="left", padx=(0,6))
        self._btn(copy_frm, "📋  Copy Decrypted", self._copy_dec,
                  "#30363d", 20).pack(side="left")

    # ── Tab 2: Key Schedule ──────────────────────────────────────
    def _build_keysched_tab(self, parent):
        info = self._lbl(
            parent,
            "Mỗi khóa con 48-bit được sinh từ khóa gốc 56-bit (sau PC-1) bằng cách dịch trái C,D rồi áp PC-2.",
            fg=FG_DIM, font=F_SMALL, wraplength=700, justify="left"
        )
        info.pack(anchor="w", padx=12, pady=(10,6))

        cols = ("round", "shift", "key_hex", "key_bin_preview")
        self._key_tree = ttk.Treeview(parent, columns=cols,
                                       show="headings", height=18)
        self._key_tree.heading("round",        text="Vòng")
        self._key_tree.heading("shift",        text="Dịch (L+R)")
        self._key_tree.heading("key_hex",      text="Khóa con Ki (hex, 48-bit)")
        self._key_tree.heading("key_bin_preview", text="6 byte hex đầy đủ")

        self._key_tree.column("round",        width=55,  anchor="center")
        self._key_tree.column("shift",        width=80,  anchor="center")
        self._key_tree.column("key_hex",      width=220, anchor="center")
        self._key_tree.column("key_bin_preview", width=300, anchor="w")

        vsb = ttk.Scrollbar(parent, orient="vertical",
                             command=self._key_tree.yview)
        self._key_tree.configure(yscrollcommand=vsb.set)

        self._key_tree.pack(side="left", fill="both", expand=True, padx=(12,0), pady=6)
        vsb.pack(side="left", fill="y", pady=6)

    # ── Tab 3: Rounds ────────────────────────────────────────────
    def _build_rounds_tab(self, parent):
        top = self._frm(parent, bg=BG)
        top.pack(fill="x", padx=12, pady=(10,4))

        self._lbl(top, "Block:", fg=FG_DIM, font=F_SMALL).pack(side="left")
        self._block_var = tk.IntVar(value=1)
        self._block_spin = tk.Spinbox(
            top, from_=1, to=1,
            textvariable=self._block_var,
            command=self._refresh_rounds,
            bg=CARD, fg=FG, insertbackground=FG,
            relief="flat", font=F_MONO, width=5,
            buttonbackground=PANEL
        )
        self._block_spin.pack(side="left", padx=6)
        self._lbl(top, "(nếu bản tin > 8 ký tự sẽ có nhiều block)",
                  fg=FG_DIM, font=F_SMALL).pack(side="left")

        cols = ("label","L","R","K")
        self._rnd_tree = ttk.Treeview(parent, columns=cols,
                                       show="headings", height=20)
        self._rnd_tree.heading("label", text="Vòng")
        self._rnd_tree.heading("L",     text="L (32-bit hex)")
        self._rnd_tree.heading("R",     text="R (32-bit hex)")
        self._rnd_tree.heading("K",     text="Khóa con Ki (48-bit hex)")

        self._rnd_tree.column("label", width=90,  anchor="center")
        self._rnd_tree.column("L",     width=140, anchor="center")
        self._rnd_tree.column("R",     width=140, anchor="center")
        self._rnd_tree.column("K",     width=220, anchor="center")

        vsb2 = ttk.Scrollbar(parent, orient="vertical",
                              command=self._rnd_tree.yview)
        self._rnd_tree.configure(yscrollcommand=vsb2.set)
        self._rnd_tree.pack(side="left", fill="both", expand=True,
                            padx=(12,0), pady=6)
        vsb2.pack(side="left", fill="y", pady=6)

        # alternating row colors
        self._rnd_tree.tag_configure("even", background=CARD)
        self._rnd_tree.tag_configure("odd",  background=PANEL)
        self._rnd_tree.tag_configure("ip",   foreground=YELLOW)
        self._key_tree.tag_configure("even", background=CARD)
        self._key_tree.tag_configure("odd",  background=PANEL)

    # ── Tab 4: Theory ────────────────────────────────────────────
    def _build_theory_tab(self, parent):
        txt = tk.Text(parent, bg=CARD, fg=FG, relief="flat",
                      font=("Courier New", 10), wrap="word",
                      padx=16, pady=12)
        vsb = ttk.Scrollbar(parent, orient="vertical", command=txt.yview)
        txt.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        txt.pack(fill="both", expand=True, padx=12, pady=10)

        txt.tag_configure("h1",  foreground=ACCENT,  font=("Courier New", 13, "bold"))
        txt.tag_configure("h2",  foreground=ACCENT2, font=("Courier New", 11, "bold"))
        txt.tag_configure("dim", foreground=FG_DIM,  font=("Courier New",  9))
        txt.tag_configure("grn", foreground=GREEN)
        txt.tag_configure("ylw", foreground=YELLOW)

        content = [
            ("h1", "DES — Data Encryption Standard (FIPS 46-3)\n\n"),
            ("h2", "Tổng quan\n"),
            ("",   "• Block size: 64 bit (8 byte)\n"
                   "• Key size:   64 bit (16 ký tự hex → 8 byte; 56 bit hiệu dụng + 8 parity bit)\n"
                   "• Rounds:     16 vòng Feistel\n"
                   "• Mode:       ECB (mỗi block độc lập) + PKCS#7 padding\n\n"),
            ("h2", "Quy trình mã hóa\n"),
            ("ylw","  1. IP  — hoán vị ban đầu (Initial Permutation)\n"),
            ("",   "         Xáo bit theo bảng IP cố định 64 phần tử.\n\n"),
            ("ylw","  2. 16 vòng Feistel:\n"),
            ("",   "         L_i = R_{i-1}\n"
                   "         R_i = L_{i-1} ⊕ f(R_{i-1}, K_i)\n"
                   "         Hàm f: Expand(32→48) → XOR K_i → 8×S-box(48→32) → P-box\n\n"),
            ("ylw","  3. Swap  — hoán đổi L₁₆ và R₁₆\n\n"),
            ("ylw","  4. IP⁻¹ — hoán vị ngược (Final Permutation)\n\n"),
            ("h2", "Key Schedule (sinh 16 khóa con)\n"),
            ("",   "  • PC-1: từ 64-bit key lấy 56 bit có nghĩa → chia C(28),D(28)\n"
                   "  • Dịch trái C,D theo SHIFTS = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]\n"
                   "  • PC-2: chọn 48 trong 56 bit → khóa con K_i\n\n"),
            ("h2", "Giải mã\n"),
            ("grn","  Hoàn toàn giống mã hóa, chỉ dùng 16 khóa con theo thứ tự NGƯỢC.\n\n"),
            ("h2", "Điểm yếu\n"),
            ("dim","  • Khóa 56-bit → 2⁵⁶ ≈ 7.2×10¹⁶ khả năng → EFF phá trong 56h (1998)\n"
                   "  • DES đã bị thay bởi AES (2001). Triple-DES (3DES) là giải pháp tạm thời.\n"),
        ]
        txt.config(state="normal")
        for tag, line in content:
            txt.insert("end", line, tag if tag else ())
        txt.config(state="disabled")

    # ── key length hint ──────────────────────────────────────────
    def _on_key_change(self, *_):
        k = self._key_var.get().strip().upper()
        n = len(k)
        invalid_chars = [c for c in k if c not in '0123456789ABCDEF']
        if invalid_chars:
            self._key_hint.config(text=f"❌ Ký tự không hợp lệ: {''.join(set(invalid_chars))}", fg=ACCENT)
        elif n == 16:
            self._key_hint.config(text=f"✅ {n}/16 ký tự hex — hợp lệ", fg=GREEN)
        elif n < 16:
            self._key_hint.config(text=f"⚠️  {n}/16 ký tự — cần thêm {16-n}", fg=YELLOW)
        else:
            self._key_hint.config(text=f"❌ {n}/16 ký tự — quá dài ({n-16} ký tự thừa)", fg=ACCENT)

    # ── actions ─────────────────────────────────────────────────
    def _validate_key(self) -> bytes | None:
        k = self._key_var.get().strip().upper()
        if len(k) != 16:
            messagebox.showerror("Khóa không hợp lệ",
                                 f"DES yêu cầu khóa đúng 16 ký tự hex (64-bit).\n"
                                 f"Khóa hiện tại: {len(k)} ký tự.")
            return None
        if not all(c in '0123456789ABCDEF' for c in k):
            messagebox.showerror("Khóa không hợp lệ",
                                 "Khóa chỉ được chứa ký tự hex (0-9, A-F).")
            return None
        return bytes.fromhex(k)

    def _do_encrypt(self):
        msg = self._msg.get("1.0", "end-1c").strip().upper()
        if not msg:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập bản tin M (hex).")
            return
        if not all(c in '0123456789ABCDEF' for c in msg):
            messagebox.showerror("Bản tin không hợp lệ",
                                 "Bản tin chỉ được chứa ký tự hex (0-9, A-F).")
            return
        key8 = self._validate_key()
        if key8 is None:
            return
        try:
            cipher_hex, subkeys_hex, all_rounds = des_encrypt(msg, key8)
            self._last_cipher   = cipher_hex
            self._last_subkeys  = subkeys_hex
            self._last_rounds   = all_rounds

            # Result tab
            self._set_text(self._res_keyhex, key8.hex().upper())
            self._set_text(self._res_plain,  msg)
            self._set_text(self._res_cipher, cipher_hex, ACCENT)
            self._set_text(self._res_dec,    "")

            self._populate_key_schedule(subkeys_hex)
            self._block_spin.config(to=len(all_rounds))
            self._block_var.set(1)
            self._refresh_rounds()

            self._nb.select(0)
            self._status_var.set(f"✅ Mã hóa OK — {len(all_rounds)} block(s) · {len(cipher_hex)//2} byte")
        except Exception as ex:
            messagebox.showerror("Lỗi", str(ex))

    def _do_decrypt(self):
        cipher_hex = self._cipher_input.get("1.0","end-1c").strip().replace(" ","")
        if not cipher_hex:
            # Try using last encryption result
            if not self._last_cipher:
                messagebox.showwarning("Thiếu dữ liệu",
                                       "Nhập bản mã hex vào ô 'BẢN MÃ HEX' hoặc mã hóa trước.")
                return
            cipher_hex = self._last_cipher
        key8 = self._validate_key()
        if key8 is None:
            return
        try:
            plain = des_decrypt(cipher_hex, key8)
            self._set_text(self._res_keyhex, key8.hex().upper())
            self._set_text(self._res_cipher, cipher_hex, ACCENT)
            self._set_text(self._res_dec, plain, GREEN)
            self._nb.select(0)
            self._status_var.set(f"✅ Giải mã OK — {len(plain)} ký tự")
        except Exception as ex:
            messagebox.showerror("Lỗi giải mã", str(ex))

    def _populate_key_schedule(self, subkeys_hex):
        for row in self._key_tree.get_children():
            self._key_tree.delete(row)
        cum = 0
        for i, kh in enumerate(subkeys_hex):
            cum += SHIFTS[i]
            tag = "even" if i % 2 == 0 else "odd"
            preview = ' '.join(kh[j:j+2] for j in range(0, len(kh), 2))
            self._key_tree.insert("", "end",
                values=(f"K{i+1:02d}", f"+{SHIFTS[i]} (Σ{cum})", kh, preview),
                tags=(tag,))

    def _refresh_rounds(self):
        for row in self._rnd_tree.get_children():
            self._rnd_tree.delete(row)
        if not self._last_rounds:
            return
        bidx = self._block_var.get() - 1
        if bidx < 0 or bidx >= len(self._last_rounds):
            return
        block_info = self._last_rounds[bidx]
        for info in block_info['rounds']:
            r = info['round']
            tag = "ip" if r == 0 else ("even" if r % 2 == 0 else "odd")
            self._rnd_tree.insert("", "end",
                values=(info['label'], info['L'], info['R'], info['K']),
                tags=(tag,))

    def _random_key(self):
        self._key_var.set(random_des_key())

    def _clear_all(self):
        self._msg.delete("1.0", "end")
        self._key_var.set("")
        self._cipher_input.config(state="normal")
        self._cipher_input.delete("1.0", "end")
        for w in [self._res_keyhex, self._res_plain,
                  self._res_cipher, self._res_dec]:
            self._set_text(w, "")
        for row in self._key_tree.get_children():
            self._key_tree.delete(row)
        for row in self._rnd_tree.get_children():
            self._rnd_tree.delete(row)
        self._last_subkeys = []
        self._last_rounds  = []
        self._last_cipher  = ""
        self._status_var.set("Đã xóa.")

    def _copy_cipher(self):
        v = self._res_cipher.get("1.0","end-1c")
        if v:
            self.clipboard_clear(); self.clipboard_append(v)
            self._status_var.set("📋 Đã copy cipher hex!")

    def _copy_dec(self):
        v = self._res_dec.get("1.0","end-1c")
        if v:
            self.clipboard_clear(); self.clipboard_append(v)
            self._status_var.set("📋 Đã copy decrypted text!")


if __name__ == "__main__":
    app = DESApp()
    app.mainloop()
