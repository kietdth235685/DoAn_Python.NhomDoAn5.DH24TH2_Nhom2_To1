import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from tkcalendar import DateEntry

# ===== HÀM KẾT NỐI DATABASE (Đã giữ nguyên) =====
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="minhkiet",  
        database="ql_benhnhan"
        #hàm này để mở kết nối đến database ql_benhnhan.
    )

# ====== TẠO CỬA SỔ CHÍNH (Đã giữ nguyên) ======
root = tk.Tk()
root.title("Quản lý bệnh nhân")
window_width = 700
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

root.geometry(f"{window_width}x{window_height}+{x}+{y}") # 👈 đặt vị trí giữa màn hình
root.config(bg="#f7f7f7")
root.resizable(False, False)

# ===== MENU VÀ BIẾN CHUNG (Đã giữ nguyên) =====
menu = tk.Menu(root) #Tạo menu để thêm submenu cho chuyển trang.
root.config(menu=menu)

frames = {} #frames dict lưu Frame cho mỗi bảng.
tables = ["benhnhan","hoso", "thuoc", "donthuoc"] #tables danh sách tên dùng để tạo frames theo vòng lặp.
titles = {
    "benhnhan": "QUẢN LÍ BỆNH NHÂN",
    "hoso": "HỒ SƠ KHÁM BỆNH",
    "thuoc": "DANH SÁCH THUỐC",
    "donthuoc": "CHI TIẾT ĐƠN THUỐC",
}
# ===== FONT CHUNG (Đã giữ nguyên) =====
title_font = ("Arial", 18, "bold")
treeviews = {} # Lưu Treeview cho mỗi frame (cần cho load_data)

# --- KHỞI TẠO CÁC HÀM TÁI SỬ DỤNG (PHẦN FORM CHUNG CỦA BẠN ĐÃ ĐƯỢC THAY THẾ BẰNG CÁC HÀM NÀY) ---

# ===== HÀM TẢI DỮ LIỆU (load_data) =====
def load_data(table_name, tree):
    for item in tree.get_children(): #xóa toàn bộ hàng hiện có trong Treeview để tránh chồng dữ liệu khi tải lại.
        tree.delete(item)
    conn = connect_db() #mở kết nối database
    cursor = conn.cursor() #tạo cursor để chạy truy vấn.

    query_map = { #là dict ánh xạ tên logical (vd "benhnhan") sang câu SQL tương ứng. Giúp hàm chung xử lý nhiều bảng.
        "benhnhan": "SELECT maBN, hoTen, ngaySinh, gioiTinh, diaChi, sdt FROM benhnhan",
        "hoso": "SELECT maHS, maBN, ngayKham, chuandoan, ghichu FROM hoso",
        "thuoc": "SELECT mathuoc, tenthuoc, donvitinh, gia FROM thuoc",
        "donthuoc": "SELECT maHS, mathuoc, soluong, huongdan FROM donthuoc",
    }
    
    header_map = {
        "benhnhan": ['Mã BN', 'Họ Tên', 'Ngày Sinh', 'Giới Tính', 'Địa Chỉ', 'SĐT'],
        "hoso": ['Mã HS', 'Mã BN', 'Ngày Khám', 'Chuẩn Đoán', 'Ghi Chú'],
        "thuoc": ['Mã Thuốc', 'Tên Thuốc', 'Đơn Vị Tính', 'Giá (VND)'],
        "donthuoc": ['Mã HS', 'Mã Thuốc', 'Số Lượng', 'Hướng Dẫn'],
    }
    
    try:
        cursor.execute(query_map[table_name])
        rows = cursor.fetchall()
        columns = header_map[table_name]
        
        tree["columns"] = columns #đặt cấu hình cột cho Treeview.
        tree["displaycolumns"] = columns
        
        width_map = {
            "benhnhan": (50, 120, 80, 50, 150, 80),
            "hoso": (50, 50, 80, 180, 180),
            "thuoc": (80, 150, 80, 80),
            "donthuoc": (50, 80, 50, 200),
        }
        
        for col in columns:
            tree.heading(col, text=col) #đặt tiêu đề hiển thị.
            col_index = columns.index(col)
            # Cài đặt độ rộng cố định và căn giữa
            tree.column(col, width=width_map[table_name][col_index], anchor="center")

        for row in rows:
            tree.insert("", "end", values=row) #thêm từng hàng vào Treeview.
            
    except Exception as e:
        messagebox.showerror("Lỗi Database", f"Không thể tải dữ liệu: {e}")
    conn.close() #đóng kết nối (rất quan trọng để giải phóng tài nguyên). 

# Hàm các chức năng bảng bệnh nhân
def reset_benhnhan_fields(hoTen_entry, gioiTinh_entry, ngaySinh_entry, diaChi_entry, sdt_entry, tree_benhnhan):
    hoTen_entry.delete(0, tk.END)
    gioiTinh_entry.set('Nam')
    ngaySinh_entry.set_date(None) 
    diaChi_entry.delete(0, tk.END)
    sdt_entry.delete(0, tk.END)
    tree_benhnhan.selection_remove(tree_benhnhan.selection())
    
def add_benhnhan(hoTen_entry, gioiTinh_entry, ngaySinh_entry, diaChi_entry, sdt_entry, tree_benhnhan):
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""INSERT INTO benhnhan (hoten, ngaysinh, gioitinh, diachi, sdt)
                       VALUES (%s,%s,%s,%s,%s)""",
                    (hoTen_entry.get(), ngaySinh_entry.get_date(), 
                     gioiTinh_entry.get(), diaChi_entry.get(), sdt_entry.get()))
        conn.commit(); conn.close()
        messagebox.showinfo("Thành công", "Đã thêm bệnh nhân mới!")
        reset_benhnhan_fields(hoTen_entry, gioiTinh_entry, ngaySinh_entry, diaChi_entry, sdt_entry, tree_benhnhan)
        load_data("benhnhan", tree_benhnhan)
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))
        
def update_benhnhan(hoTen_entry, gioiTinh_entry, ngaySinh_entry, diaChi_entry, sdt_entry, tree_benhnhan):
    try:
        sel = tree_benhnhan.focus()
        if not sel: return
        maBN = tree_benhnhan.item(sel, "values")[0]
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""UPDATE benhnhan SET hoten=%s, ngaysinh=%s, gioitinh=%s, diachi=%s, sdt=%s WHERE maBN=%s""",
                    (hoTen_entry.get(), ngaySinh_entry.get_date(), 
                    gioiTinh_entry.get(), diaChi_entry.get(), sdt_entry.get(), maBN))
        conn.commit(); conn.close()
        messagebox.showinfo("Thành công", "Cập nhật thông tin bệnh nhân!")
        reset_benhnhan_fields(hoTen_entry, gioiTinh_entry, ngaySinh_entry, diaChi_entry, sdt_entry, tree_benhnhan)
        load_data("benhnhan", tree_benhnhan)
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

def delete_benhnhan(tree_benhnhan):
    try:
        sel = tree_benhnhan.focus()
        if not sel: return
        maBN = tree_benhnhan.item(sel, "values")[0]
        if not messagebox.askyesno("Xác nhận Xóa", "Thao tác này sẽ xóa HỒ SƠ KHÁM và ĐƠN THUỐC của bệnh nhân này. Bạn có chắc chắn?"):
            return
        
        conn = connect_db()
        cur = conn.cursor()
        
        cur.execute("DELETE FROM donthuoc WHERE maHS IN (SELECT maHS FROM hoso WHERE maBN=%s)", (maBN,))
        cur.execute("DELETE FROM hoso WHERE maBN=%s", (maBN,))
        cur.execute("DELETE FROM benhnhan WHERE maBN=%s", (maBN,))
        
        conn.commit(); conn.close()
        messagebox.showinfo("Thành công", "Đã xóa bệnh nhân!")
        tree_benhnhan.selection_remove(tree_benhnhan.selection())
        load_data("benhnhan", tree_benhnhan)
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

# Hàm các chức năng bảng hồ sơ
def reset_hoso_fields(maBN_entry, ngayKham_entry, chuandoan_entry, ghichu_entry, tree_hoso):
    maBN_entry.delete(0, tk.END)
    ngayKham_entry.set_date(None)
    chuandoan_entry.delete(0, tk.END)
    ghichu_entry.delete(0, tk.END)
    tree_hoso.selection_remove(tree_hoso.selection())

def add_hoso(maBN_entry, ngayKham_entry, chuandoan_entry, ghichu_entry, tree_hoso):
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT maBN FROM benhnhan WHERE maBN = %s", (maBN_entry.get(),))
        if not cur.fetchone():
            messagebox.showerror("Lỗi", "Mã Bệnh Nhân không tồn tại!")
            conn.close()
            return
        cur.execute("""INSERT INTO hoso (maBN, ngaykham, chuandoan, ghichu)
                       VALUES (%s,%s,%s,%s)""",
                    (maBN_entry.get(), ngayKham_entry.get_date(), 
                     chuandoan_entry.get(), ghichu_entry.get()))
        conn.commit(); conn.close()
        messagebox.showinfo("Thành công", "Đã thêm Hồ sơ khám bệnh!")
        reset_hoso_fields(maBN_entry, ngayKham_entry, chuandoan_entry, ghichu_entry, tree_hoso)
        load_data("hoso", tree_hoso)
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

def update_hoso(maBN_entry, ngayKham_entry, chuandoan_entry, ghichu_entry, tree_hoso):
    try:
        sel = tree_hoso.focus()
        if not sel: return
        maHS = tree_hoso.item(sel, "values")[0]
        
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT maBN FROM benhnhan WHERE maBN = %s", (maBN_entry.get(),))
        if not cur.fetchone():
            messagebox.showerror("Lỗi", "Mã Bệnh Nhân không tồn tại!")
            conn.close()
            return
            
        cur.execute("""UPDATE hoso SET maBN=%s, ngaykham=%s, chuandoan=%s, ghichu=%s WHERE maHS=%s""",
                    (maBN_entry.get(), ngayKham_entry.get_date(), 
                    chuandoan_entry.get(), ghichu_entry.get(), maHS))
        conn.commit(); conn.close()
        messagebox.showinfo("Thành công", "Cập nhật Hồ sơ thành công!")
        reset_hoso_fields(maBN_entry, ngayKham_entry, chuandoan_entry, ghichu_entry, tree_hoso)
        load_data("hoso", tree_hoso)
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

def delete_hoso(tree_hoso):
    try:
        sel = tree_hoso.focus()
        if not sel: return
        maHS = tree_hoso.item(sel, "values")[0]
        if not messagebox.askyesno("Xác nhận Xóa", "Thao tác này sẽ xóa ĐƠN THUỐC liên quan. Bạn có chắc chắn?"):
            return
        
        conn = connect_db()
        cur = conn.cursor()
        
        cur.execute("DELETE FROM donthuoc WHERE maHS=%s", (maHS,))
        cur.execute("DELETE FROM hoso WHERE maHS=%s", (maHS,))
        
        conn.commit(); conn.close()
        messagebox.showinfo("Thành công", "Đã xóa Hồ sơ!")
        tree_hoso.selection_remove(tree_hoso.selection())
        load_data("hoso", tree_hoso)
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

# Hàm các chức năng bảng thuốc
def reset_thuoc_fields(maThuoc_entry, tenThuoc_entry, donViTinh_entry, gia_entry, tree_thuoc):
    maThuoc_entry.config(state=tk.NORMAL) 
    maThuoc_entry.delete(0, tk.END)
    tenThuoc_entry.delete(0, tk.END)
    donViTinh_entry.delete(0, tk.END)
    gia_entry.delete(0, tk.END)
    tree_thuoc.selection_remove(tree_thuoc.selection())

def add_thuoc(maThuoc_entry, tenThuoc_entry, donViTinh_entry, gia_entry, tree_thuoc):
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""INSERT INTO thuoc (mathuoc, tenthuoc, donvitinh, gia)
                       VALUES (%s,%s,%s,%s)""",
                    (maThuoc_entry.get(), tenThuoc_entry.get(), 
                     donViTinh_entry.get(), gia_entry.get()))
        conn.commit(); conn.close()
        messagebox.showinfo("Thành công", "Đã thêm Thuốc mới!")
        reset_thuoc_fields(maThuoc_entry, tenThuoc_entry, donViTinh_entry, gia_entry, tree_thuoc)
        load_data("thuoc", tree_thuoc)
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))
        
def update_thuoc(tenThuoc_entry, donViTinh_entry, gia_entry, tree_thuoc):
    try:
        sel = tree_thuoc.focus()
        if not sel: return
        maThuoc = tree_thuoc.item(sel, "values")[0]
        
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""UPDATE thuoc SET tenthuoc=%s, donvitinh=%s, gia=%s WHERE mathuoc=%s""",
                    (tenThuoc_entry.get(), donViTinh_entry.get(), 
                    gia_entry.get(), maThuoc))
        conn.commit(); conn.close()
        messagebox.showinfo("Thành công", "Cập nhật Thuốc thành công!")
        tree_thuoc.selection_remove(tree_thuoc.selection())
        load_data("thuoc", tree_thuoc)
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

def delete_thuoc(tree_thuoc):
    try:
        sel = tree_thuoc.focus()
        if not sel: return
        maThuoc = tree_thuoc.item(sel, "values")[0]
        if not messagebox.askyesno("Xác nhận Xóa", "Bạn có chắc chắn muốn xóa thuốc này?"):
            return
        
        conn = connect_db()
        cur = conn.cursor()
        
        cur.execute("SELECT COUNT(*) FROM donthuoc WHERE mathuoc=%s", (maThuoc,))
        if cur.fetchone()[0] > 0:
            messagebox.showerror("Lỗi", "Không thể xóa. Thuốc này đang được sử dụng trong Đơn Thuốc.")
            conn.close()
            return
            
        cur.execute("DELETE FROM thuoc WHERE mathuoc=%s", (maThuoc,))
        
        conn.commit(); conn.close()
        messagebox.showinfo("Thành công", "Đã xóa Thuốc!")
        tree_thuoc.selection_remove(tree_thuoc.selection())
        load_data("thuoc", tree_thuoc)
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

# Hàm các chức năng bảng đơn thuốc
def reset_donthuoc_fields(maHS_entry, maThuoc_dt_entry, soLuong_entry, huongDan_entry, tree_donthuoc):
    maHS_entry.config(state=tk.NORMAL)
    maThuoc_dt_entry.config(state=tk.NORMAL)
    maHS_entry.delete(0, tk.END)
    maThuoc_dt_entry.delete(0, tk.END)
    soLuong_entry.delete(0, tk.END)
    huongDan_entry.delete(0, tk.END)
    tree_donthuoc.selection_remove(tree_donthuoc.selection())

def add_donthuoc(maHS_entry, maThuoc_dt_entry, soLuong_entry, huongDan_entry, tree_donthuoc):
    try:
        conn = connect_db()
        cur = conn.cursor()

        cur.execute("SELECT maHS FROM hoso WHERE maHS = %s", (maHS_entry.get(),))
        if not cur.fetchone():
            messagebox.showerror("Lỗi", "Mã Hồ Sơ không tồn tại!")
            conn.close()
            return
        cur.execute("SELECT mathuoc FROM thuoc WHERE mathuoc = %s", (maThuoc_dt_entry.get(),))
        if not cur.fetchone():
            messagebox.showerror("Lỗi", "Mã Thuốc không tồn tại!")
            conn.close()
            return
        
        cur.execute("""INSERT INTO donthuoc (maHS, mathuoc, soluong, huongdan)
                       VALUES (%s,%s,%s,%s)""",
                    (maHS_entry.get(), maThuoc_dt_entry.get(), 
                     soLuong_entry.get(), huongDan_entry.get()))
        conn.commit(); conn.close()
        messagebox.showinfo("Thành công", "Đã thêm Chi tiết Đơn Thuốc!")
        reset_donthuoc_fields(maHS_entry, maThuoc_dt_entry, soLuong_entry, huongDan_entry, tree_donthuoc)
        load_data("donthuoc", tree_donthuoc)
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))
        
def update_donthuoc(soLuong_entry, huongDan_entry, tree_donthuoc):
    try:
        sel = tree_donthuoc.focus()
        if not sel: return
        maHS_key = tree_donthuoc.item(sel, "values")[0]
        maThuoc_key = tree_donthuoc.item(sel, "values")[1]
        
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""UPDATE donthuoc SET soluong=%s, huongdan=%s WHERE maHS=%s AND mathuoc=%s""",
                    (soLuong_entry.get(), huongDan_entry.get(), maHS_key, maThuoc_key))
        conn.commit(); conn.close()
        messagebox.showinfo("Thành công", "Cập nhật Đơn Thuốc thành công!")
        tree_donthuoc.selection_remove(tree_donthuoc.selection())
        load_data("donthuoc", tree_donthuoc)
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

def delete_donthuoc(tree_donthuoc):
    try:
        sel = tree_donthuoc.focus()
        if not sel: return
        maHS_key = tree_donthuoc.item(sel, "values")[0]
        maThuoc_key = tree_donthuoc.item(sel, "values")[1]
        
        if not messagebox.askyesno("Xác nhận Xóa", f"Bạn có chắc chắn muốn xóa thuốc {maThuoc_key} khỏi Hồ sơ {maHS_key}?"):
            return
        
        conn = connect_db()
        cur = conn.cursor()
        
        cur.execute("DELETE FROM donthuoc WHERE maHS=%s AND mathuoc=%s", (maHS_key, maThuoc_key))
        
        conn.commit(); conn.close()
        messagebox.showinfo("Thành công", "Đã xóa chi tiết Đơn Thuốc!")
        tree_donthuoc.selection_remove(tree_donthuoc.selection())
        load_data("donthuoc", tree_donthuoc)
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

# ===== HÀM CHUYỂN FRAME (Đã giữ nguyên) =====
def show_frame(name):
    for f in frames.values():
        f.pack_forget() 
    frames[name].pack(fill="both", expand=True) #làm frame giãn đầy vùng chứa.


# ===== TẠO FRAME VÀ CHỨC NĂNG (Đã giữ nguyên cấu trúc vòng lặp) =====
for t in tables: #Vòng lặp tạo frame cho từng bảng
    frames[t] = tk.Frame(root, bg="#f7f7f7")
    
    # ===== TIÊU ĐỀ =====
    title_label = tk.Label(
        frames[t],
        text=titles[t],
        font=title_font,
        fg="#333",
        # Sử dụng bg="#f7f7f7" thay vì "#fff" để đồng nhất với root
        bg="#f7f7f7"
    )
    title_label.pack(pady=(20, 10))
    
    # ====================================================================
    #                               TRANG BỆNH NHÂN
    # ====================================================================
    if t == "benhnhan":
        # --- FORM NHẬP LIỆU ---
        form = tk.Frame(frames[t], bg="#f7f7f7")
        form.pack(pady=5, padx=100, fill="x") 
        
        # Các Entry và Label
        tk.Label(form, text="Họ và tên:", bg="#f7f7f7").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        hoTen_entry = tk.Entry(form, width=20)
        hoTen_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        tk.Label(form, text="Ngày sinh:", bg="#f7f7f7").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        ngaySinh_entry = DateEntry(form, width=18, date_pattern='yyyy-mm-dd')
        ngaySinh_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(form, text="Giới tính:", bg="#f7f7f7").grid(row=0, column=2, padx=10, pady=5, sticky="w")
        gioiTinh_entry = ttk.Combobox(form, values=["Nam", "Nữ"], state="readonly", width=17)
        gioiTinh_entry.grid(row=0, column=3, padx=5, pady=5)
        gioiTinh_entry.current(0)

        tk.Label(form, text="Địa chỉ:", bg="#f7f7f7").grid(row=1, column=2, padx=10, pady=5, sticky="w")
        diaChi_entry = tk.Entry(form, width=20)
        diaChi_entry.grid(row=1, column=3, padx=5, pady=5)

        tk.Label(form, text="Số điện thoại:", bg="#f7f7f7").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        sdt_entry = tk.Entry(form, width=20)
        sdt_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # --- BẢNG DỮ LIỆU ---
        tree_benhnhan = ttk.Treeview(frames[t], show="headings") 
        tree_benhnhan.pack(fill="both", expand=True, padx=10, pady=10)
        treeviews[t] = tree_benhnhan # Lưu Treeview

        def select_benhnhan_item(event):
            reset_benhnhan_fields(hoTen_entry, gioiTinh_entry, ngaySinh_entry, diaChi_entry, sdt_entry, tree_benhnhan)
            sel = tree_benhnhan.focus()
            if not sel: return
            vals = tree_benhnhan.item(sel, "values")
            if vals:
                hoTen_entry.insert(0, vals[1])
                ngaySinh_entry.set_date(vals[2])
                gioiTinh_entry.set(vals[3])
                diaChi_entry.insert(0, vals[4])
                sdt_entry.insert(0, vals[5])

        tree_benhnhan.bind("<ButtonRelease-1>", select_benhnhan_item)

        # --- NÚT CHỨC NĂNG (Đã cập nhật command) ---
        btn_frame = tk.Frame(frames[t], bg="#f7f7f7")
        btn_frame.pack(pady=2)

        ttk.Button(btn_frame, text="Thêm", width=15, command=lambda: add_benhnhan
                   (hoTen_entry, gioiTinh_entry, ngaySinh_entry, diaChi_entry, sdt_entry, tree_benhnhan)).grid(row=0, column=0, padx=8, pady=8)
        ttk.Button(btn_frame, text="Sửa", width=15, command=lambda: update_benhnhan
                   (hoTen_entry, gioiTinh_entry, ngaySinh_entry, diaChi_entry, sdt_entry, tree_benhnhan)).grid(row=0, column=1, padx=8, pady=8)
        ttk.Button(btn_frame, text="Xóa", width=15, command=lambda: delete_benhnhan
                   (tree_benhnhan)).grid(row=0, column=2, padx=8, pady=8)
        
        ttk.Button(btn_frame, text="Tải danh sách", width=15, command=lambda: load_data("benhnhan", tree_benhnhan)).grid(row=0, column=3, padx=8, pady=8)
        
        btn_frame2 = tk.Frame(frames[t], bg="#f7f7f7")
        btn_frame2.pack(pady=2)
            
        ttk.Button(btn_frame2, text="Reset", width=18, command=lambda: reset_benhnhan_fields(hoTen_entry, gioiTinh_entry, ngaySinh_entry, diaChi_entry, sdt_entry, tree_benhnhan)).pack(side="left", padx=10, pady=5)
        ttk.Button(btn_frame2, text="Thoát", width=18, style="Accent.TButton", command=root.destroy).pack(side="left", padx=10 ,pady=5)
                
    # ====================================================================
    #                            TRANG HỒ SƠ KHÁM BỆNH
    # ====================================================================
    elif t == "hoso":
        # --- FORM NHẬP LIỆU HỒ SƠ ---
        form = tk.Frame(frames[t], bg="#f7f7f7")
        form.pack(pady=5, padx=100, fill="x") 

        tk.Label(form, text="Mã Bệnh Nhân:", bg="#f7f7f7").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        maBN_entry = tk.Entry(form, width=20)
        maBN_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        tk.Label(form, text="Ngày Khám:", bg="#f7f7f7").grid(row=0, column=2, padx=10, pady=5, sticky="w")
        ngayKham_entry = DateEntry(form, width=20, date_pattern='yyyy-mm-dd')
        ngayKham_entry.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        tk.Label(form, text="Chuẩn Đoán:", bg="#f7f7f7").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        chuandoan_entry = tk.Entry(form, width=50)
        chuandoan_entry.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky="w")

        tk.Label(form, text="Ghi Chú:", bg="#f7f7f7").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        ghichu_entry = tk.Entry(form, width=50)
        ghichu_entry.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky="w")
        
        # --- BẢNG DỮ LIỆU ---
        tree_hoso = ttk.Treeview(frames[t], show="headings")
        tree_hoso.pack(fill="both", expand=True, padx=10, pady=10)
        treeviews[t] = tree_hoso
        
        def select_hoso_item(event):
            reset_hoso_fields(maBN_entry, ngayKham_entry, chuandoan_entry, ghichu_entry, tree_hoso)
            sel = tree_hoso.focus()
            if not sel: return
            vals = tree_hoso.item(sel, "values")
            if vals:
                maBN_entry.insert(0, vals[1])
                ngayKham_entry.set_date(vals[2])
                chuandoan_entry.insert(0, vals[3])
                ghichu_entry.insert(0, vals[4])

        tree_hoso.bind("<ButtonRelease-1>", select_hoso_item)
        
        # --- NÚT CHỨC NĂNG (Đã cập nhật command) ---
        btn_frame = tk.Frame(frames[t], bg="#f7f7f7")
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="Thêm", width=15, command=lambda: add_hoso
                   (maBN_entry, ngayKham_entry, chuandoan_entry, ghichu_entry, tree_hoso)).grid(row=0, column=0, padx=8, pady=8)
        ttk.Button(btn_frame, text="Sửa", width=15, command=lambda: update_hoso
                   (maBN_entry, ngayKham_entry, chuandoan_entry, ghichu_entry, tree_hoso)).grid(row=0, column=1, padx=8, pady=8)
        ttk.Button(btn_frame, text="Xóa", width=15, command=lambda: delete_hoso
                   (tree_hoso)).grid(row=0, column=2, padx=8, pady=8)
        ttk.Button(btn_frame, text="Tải danh sách", width=15, command=lambda: load_data("hoso", tree_hoso)).grid(row=0, column=3, padx=8, pady=8)
        
        btn_frame2 = tk.Frame(frames[t], bg="#f7f7f7")
        btn_frame2.pack(pady=2)
            
        ttk.Button(btn_frame2, text="Reset", width=18, command=lambda: reset_hoso_fields
                   (maBN_entry, ngayKham_entry, chuandoan_entry, ghichu_entry, tree_hoso)).pack(side="left", padx=10, pady=5)
        ttk.Button(btn_frame2, text="Thoát", width=18, style="Accent.TButton", command=root.destroy).pack(side="left", padx=10 ,pady=5)
   
   
    # ====================================================================
    #                            TRANG DANH SÁCH THUỐC
    # ====================================================================
    elif t == "thuoc":
        # --- FORM NHẬP LIỆU THUỐC ---
        form = tk.Frame(frames[t], bg="#f7f7f7")
        form.pack(pady=5, padx=100, fill="x") 

        tk.Label(form, text="Mã Thuốc:", bg="#f7f7f7").grid(row=0, column=0, padx=  10, pady=5, sticky="w")
        maThuoc_entry = tk.Entry(form, width=15)
        maThuoc_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        tk.Label(form, text="Tên Thuốc:", bg="#f7f7f7").grid(row=0, column=2, padx=10, pady=5, sticky="w")
        tenThuoc_entry = tk.Entry(form, width=30)
        tenThuoc_entry.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        tk.Label(form, text="Đơn Vị Tính:", bg="#f7f7f7").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        donViTinh_entry = tk.Entry(form, width=15)
        donViTinh_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(form, text="Giá (VND):", bg="#f7f7f7").grid(row=1, column=2, padx=10, pady=5, sticky="w")
        gia_entry = tk.Entry(form, width=30)
        gia_entry.grid(row=1, column=3, padx=5, pady=5, sticky="w")
        
        # --- BẢNG DỮ LIỆU ---
        tree_thuoc = ttk.Treeview(frames[t], show="headings")
        tree_thuoc.pack(fill="both", expand=True, padx=10, pady=10)
        treeviews[t] = tree_thuoc
        
        def select_thuoc_item(event):
            reset_thuoc_fields(maThuoc_entry, tenThuoc_entry, donViTinh_entry, gia_entry, tree_thuoc)
            sel = tree_thuoc.focus()
            if not sel: return
            vals = tree_thuoc.item(sel, "values")
            if vals:
                maThuoc_entry.insert(0, vals[0])
                tenThuoc_entry.insert(0, vals[1])
                donViTinh_entry.insert(0, vals[2])
                gia_entry.insert(0, vals[3])
                maThuoc_entry.config(state=tk.DISABLED) 

        tree_thuoc.bind("<ButtonRelease-1>", select_thuoc_item)
        
        # --- NÚT CHỨC NĂNG (Đã cập nhật command) ---
        btn_frame = tk.Frame(frames[t], bg="#f7f7f7")
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="Thêm", width=15, command=lambda: add_thuoc
                   (maThuoc_entry, tenThuoc_entry, donViTinh_entry, gia_entry, tree_thuoc)).grid(row=0, column=0, padx=8, pady=8)
        ttk.Button(btn_frame, text="Sửa", width=15, command=lambda: update_thuoc
                   (tenThuoc_entry, donViTinh_entry, gia_entry, tree_thuoc)).grid(row=0, column=1, padx=8, pady=8)
        ttk.Button(btn_frame, text="Xóa", width=15, command=lambda: delete_thuoc
                   (tree_thuoc)).grid(row=0, column=2, padx=8, pady=8)
        ttk.Button(btn_frame, text="Tải danh sách", width=15, command=lambda: load_data("thuoc", tree_thuoc)).grid(row=0, column=3, padx=8, pady=8)
        
        btn_frame2 = tk.Frame(frames[t], bg="#f7f7f7")
        btn_frame2.pack(pady=2)
            
        ttk.Button(btn_frame2, text="Reset", width=18, command=lambda: reset_thuoc_fields
                   (maThuoc_entry, tenThuoc_entry, donViTinh_entry, gia_entry, tree_thuoc)).pack(side="left", padx=10, pady=5)
        ttk.Button(btn_frame2, text="Thoát", width=18, style="Accent.TButton", command=root.destroy).pack(side="left", padx=10 ,pady=5)
    
    
    # ====================================================================
    #                         TRANG CHI TIẾT ĐƠN THUỐC
    # ====================================================================
    elif t == "donthuoc":
        # --- FORM NHẬP LIỆU ĐƠN THUỐC ---
        form = tk.Frame(frames[t], bg="#f7f7f7")
        form.pack(pady=5, padx=100, fill="x") 

        tk.Label(form, text="Mã Hồ Sơ (maHS):", bg="#f7f7f7").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        maHS_entry = tk.Entry(form, width=15)
        maHS_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        tk.Label(form, text="Mã Thuốc (mathuoc):", bg="#f7f7f7").grid(row=0, column=2, padx=10, pady=5, sticky="w")
        maThuoc_dt_entry = tk.Entry(form, width=30)
        maThuoc_dt_entry.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        tk.Label(form, text="Số Lượng:", bg="#f7f7f7").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        soLuong_entry = tk.Entry(form, width=15)
        soLuong_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(form, text="Hướng Dẫn Dùng:", bg="#f7f7f7").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        huongDan_entry = tk.Entry(form, width=50)
        huongDan_entry.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky="w")
        
        # --- BẢNG DỮ LIỆU ---
        tree_donthuoc = ttk.Treeview(frames[t], show="headings")
        tree_donthuoc.pack(fill="both", expand=True, padx=10, pady=10)
        treeviews[t] = tree_donthuoc
        
        def select_donthuoc_item(event):
            reset_donthuoc_fields(maHS_entry, maThuoc_dt_entry, soLuong_entry, huongDan_entry, tree_donthuoc)
            sel = tree_donthuoc.focus()
            if not sel: return
            vals = tree_donthuoc.item(sel, "values")
            if vals:
                maHS_entry.insert(0, vals[0])
                maThuoc_dt_entry.insert(0, vals[1])
                soLuong_entry.insert(0, vals[2])
                huongDan_entry.insert(0, vals[3])
                # Khóa Mã HS và Mã Thuốc khi Sửa/Xóa vì chúng là Khóa Chính Kép
                maHS_entry.config(state=tk.DISABLED)
                maThuoc_dt_entry.config(state=tk.DISABLED)

        tree_donthuoc.bind("<ButtonRelease-1>", select_donthuoc_item)
        
        # --- NÚT CHỨC NĂNG (Đã cập nhật command) ---
        btn_frame = tk.Frame(frames[t], bg="#f7f7f7")
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="Thêm", width=15, command=lambda: add_donthuoc
                   (maHS_entry, maThuoc_dt_entry, soLuong_entry, huongDan_entry, tree_donthuoc)).grid(row=0, column=0, padx=8, pady=8)
        ttk.Button(btn_frame, text="Sửa", width=15, command=lambda: update_donthuoc
                   (soLuong_entry, huongDan_entry, tree_donthuoc)).grid(row=0, column=1, padx=8, pady=8)
        ttk.Button(btn_frame, text="Xóa", width=15, command=lambda: delete_donthuoc
                   (tree_donthuoc)).grid(row=0, column=2, padx=8, pady=8)
        ttk.Button(btn_frame, text="Tải danh sách", width=15, command=lambda: load_data("donthuoc", tree_donthuoc)).grid(row=0, column=3, padx=8, pady=8)
        
        btn_frame2 = tk.Frame(frames[t], bg="#f7f7f7")
        btn_frame2.pack(pady=2)
            
        ttk.Button(btn_frame2, text="Reset", width=18, command=lambda: reset_donthuoc_fields
                   (maHS_entry, maThuoc_dt_entry, soLuong_entry, huongDan_entry, tree_donthuoc)).pack(side="left", padx=10, pady=5)
        ttk.Button(btn_frame2, text="Thoát", width=18, style="Accent.TButton", command=root.destroy).pack(side="left", padx=10 ,pady=5)

# ===== MENU CHUYỂN TRANG (Đã giữ nguyên) =====
submenu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label=" Trang chính", menu=submenu)
for t in tables:
    submenu.add_command(label=titles[t], command=lambda n=t: show_frame(n))

root.update()
root.minsize(root.winfo_width(), root.winfo_height())
show_frame("benhnhan") 
root.mainloop()