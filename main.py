import json
import os
from datetime import datetime

DATA_FILE = 'data.json'

saldo = 0
transactions = []

def muat_data():
    global saldo, transactions
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            saldo = float(data.get('saldo', 0))
            transactions = data.get('transactions', []) or []
            # pastikan angka berupa float
            for t in transactions:
                try:
                    t['amount'] = float(t.get('amount', 0))
                except (ValueError, TypeError):
                    t['amount'] = 0.0
    except (FileNotFoundError, json.JSONDecodeError, ValueError):
        saldo = 0
        transactions = []

def simpan_data():
    tmp = DATA_FILE + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump({'saldo': saldo, 'transactions': transactions}, f)
    os.replace(tmp, DATA_FILE)

def tambah_pemasukan():
    global saldo
    try:
        jumlah = float(input("Masukkan jumlah pemasukan: "))
        if jumlah <= 0:
            print("Jumlah harus lebih dari 0.")
            return
    except ValueError:
        print("Input tidak valid. Masukkan angka.")
        return

    saldo += jumlah
    txn = {'type': 'pemasukan', 'amount': jumlah, 'timestamp': datetime.now().isoformat()}
    transactions.append(txn)
    simpan_data()
    print(f"Pemasukan sebesar {jumlah:.2f} berhasil ditambahkan. Saldo sekarang: {saldo:.2f}")

def tambah_pengeluaran():
    global saldo
    try:
        jumlah = float(input("Masukkan jumlah pengeluaran: "))
        if jumlah <= 0:
            print("Jumlah harus lebih dari 0.")
            return
    except ValueError:
        print("Input tidak valid. Masukkan angka.")
        return

    if jumlah > saldo:
        print("Saldo tidak cukup.")
        return

    saldo -= jumlah
    txn = {'type': 'pengeluaran', 'amount': jumlah, 'timestamp': datetime.now().isoformat()}
    transactions.append(txn)
    simpan_data()
    print(f"Pengeluaran sebesar {jumlah:.2f} berhasil dikurangi. Saldo sekarang: {saldo:.2f}")

def format_rupiah(x):
    s = f"{x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    return s


def lihat_saldo():
    global saldo
    print("=== Saldo ===")
    print(f"Saldo saat ini: Rp{format_rupiah(saldo)}")


def laporan():
    global transactions
    total_pemasukan = sum(t['amount'] for t in transactions if t.get('type') == 'pemasukan')
    total_pengeluaran = sum(t['amount'] for t in transactions if t.get('type') == 'pengeluaran')
    print("=== Laporan Rekap ===")
    print(f"Total pemasukan: Rp{format_rupiah(total_pemasukan)}")
    print(f"Total pengeluaran: Rp{format_rupiah(total_pengeluaran)}")
    print("--- Riwayat Transaksi (terbaru) ---")
    for t in reversed(transactions[-10:]):
        ts = t.get('timestamp', '')
        try:
            dt = datetime.fromisoformat(ts)
            ts_str = dt.strftime('%Y-%m-%d %H:%M')
        except Exception:
            ts_str = ts
        tipe = 'IN' if t.get('type') == 'pemasukan' else 'OUT'
        amt = format_rupiah(t.get('amount', 0))
        print(f"{ts_str} [{tipe}] Rp{amt}")


def menu():
    print("=== Aplikasi Pengelola Uang Saku ===")
    print("1. Tambah pemasukan")
    print("2. Tambah pengeluaran")
    print("3. Lihat saldo")
    print("4. Keluar")
    print("5. Laporan")

# Muat data dari file sebelum memulai aplikasi
muat_data()

while True:
    menu()
    pilihan = input("Pilih menu: ")

    if pilihan == "1":
        tambah_pemasukan()
    elif pilihan == "2":
        tambah_pengeluaran()
    elif pilihan == "3":
        lihat_saldo()
    elif pilihan == "5":
        laporan()
    elif pilihan == "4":
        simpan_data()
        print("Terima kasih!")
        break
    else:
        print("Pilihan tidak valid")