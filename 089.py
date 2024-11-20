import sqlite3  #Untuk database SQLite
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk  #Untuk membuat GUI

#Membuat database dan tabel
def create_database():
    conn = sqlite3.connect('nilai_siswa.db')  #Menghubungkan ke database
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  
            nama_siswa TEXT,                      
            biologi INTEGER,                      
            fisika INTEGER,                        
            inggris INTEGER,                      
            prediksi_fakultas TEXT                
        )
    ''')
    conn.commit()  #Menyimpan perubahan
    conn.close()   #Menutup koneksi

#Mengambil data dari database
def fetch_data():
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM nilai_siswa")  #Mengambil semua data dari tabel
    rows = cursor.fetchall()  #Menyimpan hasil query
    conn.close()
    return rows  #Mengembalikan data sebagai list

#Menyimpan data baru ke database
def save_to_database(nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    ''', (nama, biologi, fisika, inggris, prediksi))  
    conn.commit()
    conn.close()

#Memperbarui data berdasarkan ID
def update_database(record_id, nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE nilai_siswa
        SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ?
        WHERE id = ?
    ''', (nama, biologi, fisika, inggris, prediksi, record_id))  # Memperbarui data
    conn.commit()
    conn.close()

#Menghapus data berdasarkan ID
def delete_database(record_id):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (record_id,))  # Menghapus data
    conn.commit()
    conn.close()

#Menghitung prediksi fakultas berdasarkan nilai tertinggi
def calculate_prediction(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:
        return "Kedokteran"
    elif fisika > biologi and fisika > inggris:
        return "Teknik"
    elif inggris > biologi and inggris > fisika:
        return "Bahasa"
    else:
        return "Tidak Diketahui"  # Jika nilai sama besar

#Menyimpan data dari input form ke database
def submit():
    try:
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        if not nama:  #Validasi input nama
            raise Exception("Nama siswa tidak boleh kosong.")

        prediksi = calculate_prediction(biologi, fisika, inggris)  #Prediksi fakultas
        save_to_database(nama, biologi, fisika, inggris, prediksi)  # Menyimpan ke database

        messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}")
        clear_inputs()  #Mengosongkan input setelah menyimpan
        populate_table()  #Memperbaharui tabel
    except ValueError as e:
        messagebox.showerror("Error", f"Input tidak valid: {e}")  #Menampilkan pesan error jika data tidak vaild

#Memperbarui data yang dipilih di tabel
def update():
    try:
        if not selected_record_id.get():  # Validasi jika tidak ada data yang dipilih
            raise Exception("Pilih data dari tabel untuk di-update!")

        record_id = int(selected_record_id.get())
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        if not nama:
            raise ValueError("Nama siswa tidak boleh kosong.")

        prediksi = calculate_prediction(biologi, fisika, inggris)
        update_database(record_id, nama, biologi, fisika, inggris, prediksi)

        messagebox.showinfo("Sukses", "Data berhasil diperbarui!")
        clear_inputs()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

#Menghapus data yang dipilih
def delete():
    try:
        if not selected_record_id.get():
            raise Exception("Pilih data dari tabel untuk dihapus!")

        record_id = int(selected_record_id.get())
        delete_database(record_id)
        messagebox.showinfo("Sukses", "Data berhasil dihapus!")
        clear_inputs()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

#Mengosongkan input form
def clear_inputs():
    nama_var.set("")
    biologi_var.set("")
    fisika_var.set("")
    inggris_var.set("")
    selected_record_id.set("")

#Mengisi tabel dengan data dari database
def populate_table():
    for row in tree.get_children():  #Menghapus data lama dari tabel
        tree.delete(row)
    for row in fetch_data():  #Menambahkan data baru dari database
        tree.insert('', 'end', values=row)

#Mengisi input berdasarkan data yang dipilih di tabel
def fill_inputs_from_table(event):
    try:
        selected_item = tree.selection()[0]
        selected_row = tree.item(selected_item)['values']

        selected_record_id.set(selected_row[0])  #Mengisi ID yang dipilih
        nama_var.set(selected_row[1])
        biologi_var.set(selected_row[2])
        fisika_var.set(selected_row[3])
        inggris_var.set(selected_row[4])
    except IndexError:
        messagebox.showerror("Error", "Pilih data yang valid!")

#Inisialisasi database
create_database()

#Membuat GUI
root = Tk()
root.title("Prediksi Fakultas Siswa")

#Varaible tkinter
nama_var = StringVar()
biologi_var = StringVar()
fisika_var = StringVar()
inggris_var = StringVar()
selected_record_id = StringVar()

#Input data berupa nama siswa, nilai biologi, nilai fisika, nilai inggris
Label(root, text="Nama Siswa").grid(row=0, column=0, padx=10, pady=5)
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Nilai Biologi").grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Nilai Fisika").grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Nilai Inggris").grid(row=3, column=0, padx=10, pady=5)
Entry(root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=5)

#Membuat tombol menambahkan,memperbaharui dan menghapus data
Button(root, text="Add", command=submit).grid(row=4, column=0, pady=10)
Button(root, text="Update", command=update).grid(row=4, column=1, pady=10)
Button(root, text="Delete", command=delete).grid(row=4, column=2, pady=10)

#Membuat tabel unutk menampilkan data
columns = ("id", "nama_siswa", "biologi", "fisika", "inggris", "prediksi_fakultas")
tree = ttk.Treeview(root, columns=columns, show='headings')

#Mengatur heading dan kolom
for col in columns:
    tree.heading(col, text=col.capitalize())
    tree.column(col, anchor='center')

tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)
tree.bind('<ButtonRelease-1>', fill_inputs_from_table) #Menghubungkan event klik pada tabel untuk mengisi input form

#Mengisi tabel dengan data awal
populate_table()

#Menjalankan tkinter
root.mainloop()
