CREATE DATABASE ql_benhnhan CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE ql_benhnhan;

-- Tạo bảng bệnh nhân
CREATE TABLE benhnhan(
    maBN INT AUTO_INCREMENT PRIMARY KEY,
    hoten VARCHAR(100) NOT NULL,
    ngaysinh DATE,
    gioitinh ENUM('Nam','Nữ') DEFAULT 'Nam',
    diachi VARCHAR(200),
    sdt VARCHAR(15)
);

-- Tạo bảng hồ sơ khám bệnh
CREATE TABLE hoso(
    maHS INT AUTO_INCREMENT PRIMARY KEY,
    maBN INT,
    ngaykham DATE,
    chuandoan TEXT,
    ghichu TEXT,
    FOREIGN KEY (maBN) REFERENCES benhnhan(maBN)
);

-- Tạo bảng thuốc
CREATE TABLE thuoc(
    mathuoc VARCHAR(10) PRIMARY KEY,
    tenthuoc VARCHAR(100) NOT NULL,
    donvitinh VARCHAR(20),
    gia DECIMAL(10,2)
);

-- Tạo bảng đơn thuốc
CREATE TABLE donthuoc(
    maHS INT,
    mathuoc VARCHAR(10),
    soluong INT,
    huongdan TEXT,
    PRIMARY KEY (maHS, mathuoc),
    FOREIGN KEY (maHS) REFERENCES hoso(maHS),
    FOREIGN KEY (mathuoc) REFERENCES thuoc(mathuoc)
);

-- nhập dữ liệu bảng bệnh nhân 
insert into benhnhan(hoten, ngaysinh, gioitinh, diachi,sdt) value 
 ('Võ Hoàng Yến','2005-3-2','Nữ','An Giang','0914987600'), 
 ('Trần Tuấn Anh','2004-5-8','Nam','Cần Thơ','0918283999'),
 ('Nguyễn Thị Kim Ngọc','2004-5-16','Nữ','Kiên Giang','0762773888'), 
 ('Huỳnh Nguyễn Kim Yến','2006-8-15','Nữ','Đồng Tháp','0254581258'),
 ('Lâm Chấn Khang','2000-4-19','Nam','Cà Mau','0946856856'),
 ('Đỗ Thị Thu Hà','1995-03-18', 'Nữ', 'Huế', '0945123789'), 
 ('Hoàng Văn Cường','1989-11-09','Nam','Hải Phòng','0967890123'),
 ('Ngô Thị Hường','1992-06-25','Nữ','Quảng Ninh','0933334444'),
 ('Bùi Văn Dũng','1978-10-03','Nam','Bình Dương','0911999888'),
 ('Phan Thị Khanh','2001-04-11','Nữ','Nha Trang','0955123456');
 USE ql_benhnhan;
 ALTER TABLE benhnhan AUTO_INCREMENT = 11;
-- Thêm dữ liệu bảng hồ sơ
INSERT INTO hoso(maBN, ngaykham, chuandoan, ghichu) VALUES
(1,'2025-01-10','Cảm cúm','Uống thuốc 3 ngày'),
(2,'2025-01-12','Sốt siêu vi','Nghỉ ngơi, bù nước'),
(3,'2025-02-05','Đau ngực nhẹ','Theo dõi thêm'),
(4,'2025-02-10','Viêm da','Bôi thuốc ngoài da'),
(5,'2025-03-15','Đau bụng','Siêu âm bụng'),
(6,'2025-04-01','Sâu răng','Hẹn tái khám'),
(7,'2025-04-15','Viêm họng','Uống thuốc 5 ngày'),
(8,'2025-05-05','Thai 8 tuần','Theo dõi định kỳ'),
(9,'2025-06-01','Cận thị','Kê toa kính mới'),
(10,'2025-06-10','Xét nghiệm máu','Bình thường');

-- Thêm dữ liệu bảng thuốc
INSERT INTO thuoc(mathuoc, tenthuoc, donvitinh, gia) VALUES
('T001','Paracetamol','Viên',2000),
('T002','Amoxicillin','Viên',2500),
('T003','Vitamin C','Viên',1500),
('T004','Cefalexin','Viên',3000),
('T005','Ibuprofen','Viên',2800),
('T006','Azithromycin','Viên',3500),
('T007','Efferalgan','Gói',2500),
('T008','Cotrimoxazole','Viên',2200),
('T009','Clorpheniramin','Viên',1200),
('T010','Metronidazol','Viên',2000);

-- Thêm dữ liệu bảng đơn thuốc
INSERT INTO donthuoc(maHS, mathuoc, soluong, huongdan) VALUES
(1,'T001',10,'Uống sau ăn'),
(2,'T002',15,'Ngày 2 lần'),
(3,'T003',20,'Bổ sung hàng ngày'),
(4,'T004',10,'Sáng và tối'),
(5,'T005',12,'Giảm đau khi cần'),
(6,'T006',5,'Uống trước bữa ăn'),
(7,'T007',10,'Pha với nước ấm'),
(8,'T008',8,'Ngày 2 lần'),
(9,'T009',15,'Trước khi ngủ'),
(10,'T010',6,'Sau bữa trưa');

-- Hiển thị dữ liệu kiểm tra
SELECT * FROM benhnhan; 
SELECT * FROM hoso;
SELECT * FROM thuoc;
SELECT * FROM donthuoc;