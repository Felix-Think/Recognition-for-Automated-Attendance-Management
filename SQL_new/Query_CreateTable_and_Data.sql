create database NCKH;
use nckh;


CREATE TABLE Department(
    department_id VARCHAR(10) PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL
);

CREATE TABLE Employees (
    employee_id VARCHAR(20) PRIMARY KEY,       -- 1. Mã nhân viên (PK luôn đặt đầu)
    full_name VARCHAR(100) NOT NULL,           -- 2. Tên nhân viên
    gender CHAR(1),                             -- 3. Giới tính
    birthday DATE,                              -- 4. Ngày sinh
    department_id VARCHAR(10),                  -- 5. Mã phòng ban (FK)
    position VARCHAR(50),                       -- 6. Chức vụ
    hire_date DATE,                             -- 7. Ngày vào làm
    work_status BIT,                            -- 8. Trạng thái làm việc (0 nghỉ, 1 làm)
    profile_pic  VARCHAR(255),                  -- 9. Đường dẫn ảnh 
    FOREIGN KEY (department_id) REFERENCES Department(department_id)
);



CREATE TABLE Attendance (
    attendance_id varchar(20) PRIMARY KEY,  -- manv+ngaythangnam
    employee_id varchar(20),
    work_date DATE NOT NULL,
    check_in_time datetime, -- luc dau null
    check_out_time datetime, -- luc dau null
    hours_worked FLOAT, -- -------!!!!!-------
    status_atd bit,  -- luc dau null,1 la dang o trong cong ty, 0 la dang o ngoai
    FOREIGN KEY (employee_id) REFERENCES Employees(employee_id)
);

INSERT INTO Department (department_id, department_name)
VALUES
('D01', 'Phòng Nhân sự'),
('D02', 'Phòng Kỹ thuật'),
('D03', 'Phòng Kế toán');

INSERT INTO Employees (employee_id, full_name, birthday, gender, department_id, position, hire_date, work_status)
VALUES
('E001', 'Nguyễn Văn A', '1990-01-15', 'M', 'D01', 'Trưởng phòng', '2015-06-01', 1),
('E002', 'Trần Thị B', '1992-05-20', 'F', 'D02', 'Kỹ sư', '2018-03-10', 1),
('E003', 'Lê Văn C', '1995-09-25', 'M', 'D03', 'Kế toán viên', '2020-11-05', 1);

-- Thêm dữ liệu cho các ngày trong tháng 4, 2025

INSERT INTO Attendance (attendance_id, employee_id, work_date, check_in_time, check_out_time, hours_worked, status_atd)
VALUES
('E001120425', 'E001', '2025-04-12', '2025-04-12 08:00:00', '2025-04-12 17:00:00', 9.0, 0),
('E002120425', 'E002', '2025-04-12', '2025-04-12 08:00:00', '2025-04-12 17:00:00', 9.0, 0),
('E003120425', 'E003', '2025-04-12', '2025-04-12 08:00:00', '2025-04-12 17:00:00', 9.0, 0),

('E001130425', 'E001', '2025-04-13', '2025-04-13 08:00:00', '2025-04-13 17:00:00', 9.0, 0),
('E002130425', 'E002', '2025-04-13', '2025-04-13 08:00:00', '2025-04-13 17:00:00', 9.0, 0),
('E003130425', 'E003', '2025-04-13', '2025-04-13 08:00:00', '2025-04-13 17:00:00', 9.0, 0),

('E001140425', 'E001', '2025-04-14', '2025-04-14 08:00:00', '2025-04-14 17:30:00', 9.5, 0), -- tăng ca 1.5 giờ
('E002140425', 'E002', '2025-04-14', '2025-04-14 08:00:00', '2025-04-14 17:00:00', 9.0, 0),
('E003140425', 'E003', '2025-04-14', '2025-04-14 08:00:00', '2025-04-14 17:00:00', 9.0, 0),

('E001150425', 'E001', '2025-04-15', '2025-04-15 08:00:00', '2025-04-15 18:00:00', 10.0, 0), -- tăng ca 2 giờ
('E002150425', 'E002', '2025-04-15', '2025-04-15 08:00:00', '2025-04-15 17:00:00', 9.0, 0),
('E003150425', 'E003', '2025-04-15', '2025-04-15 08:00:00', '2025-04-15 17:00:00', 9.0, 0),

('E001160425', 'E001', '2025-04-16', '2025-04-16 08:00:00', '2025-04-16 17:00:00', 9.0, 0),
('E002160425', 'E002', '2025-04-16', '2025-04-16 08:00:00', '2025-04-16 17:00:00', 9.0, 0),
('E003160425', 'E003', '2025-04-16', '2025-04-16 08:00:00', '2025-04-16 17:00:00', 9.0, 0),

('E001170425', 'E001', '2025-04-17', '2025-04-17 08:00:00', '2025-04-17 17:00:00', 9.0, 0),
('E002170425', 'E002', '2025-04-17', '2025-04-17 08:00:00', '2025-04-17 17:00:00', 9.0, 0),
('E003170425', 'E003', '2025-04-17', '2025-04-17 08:00:00', '2025-04-17 17:00:00', 9.0, 0),

('E001180425', 'E001', '2025-04-18', '2025-04-18 08:00:00', '2025-04-18 17:00:00', 9.0, 0),
('E002180425', 'E002', '2025-04-18', '2025-04-18 08:00:00', '2025-04-18 17:00:00', 9.0, 0),
('E003180425', 'E003', '2025-04-18', '2025-04-18 08:00:00', '2025-04-18 17:00:00', 9.0, 0);




