
-- Tạo database
CREATE DATABASE NCKH;
USE NCKH;

-- Bảng Nhân viên
CREATE TABLE Employees (
    employee_id varchar(10) PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    birthday date,
    gender char,
    department_id VARCHAR(50),
    position VARCHAR(50),
    hire_date DATE,
    status ENUM('active', 'inactive'),
    FOREIGN KEY (department_id) REFERENCES Department(department_id)
);

drop table employees;

-- Bảng Chấm công
CREATE TABLE Attendance (
    attendance_id varchar(20) PRIMARY KEY,
    employee_id varchar(10),
    work_date DATE NOT NULL,
    check_in_time datetime,
    check_out_time datetime,
    hours_worked FLOAT,
    status_atd ENUM('present', 'absent', 'leave'),
    FOREIGN KEY (employee_id) REFERENCES Employees(employee_id)
);

-- Bảng Phòng ban
CREATE TABLE Department(
    department_id VARCHAR(50) PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL
);

INSERT INTO Department (department_id, department_name) VALUES
('D001', 'Human Resources'),
('D002', 'IT Department'),
('D003', 'Finance'),
('D004', 'Marketing'),
('D005', 'Sales');

INSERT INTO Employees (employee_id, full_name, birthday, gender, department_id, position, hire_date, status) VALUES
('E001', 'Nguyễn Văn A', '1990-05-10', 'M', 'D001', 'HR Manager', '2015-06-01', 'active'),
('E002', 'Trần Thị B', '1992-08-22', 'F', 'D002', 'Software Engineer', '2018-07-15', 'active'),
('E003', 'Lê Văn C', '1988-11-30', 'M', 'D003', 'Accountant', '2016-09-25', 'active'),
('E004', 'Phạm Thị D', '1995-03-14', 'F', 'D004', 'Marketing Executive', '2019-02-10', 'active'),
('E005', 'Hoàng Văn E', '1985-07-19', 'M', 'D005', 'Sales Manager', '2014-04-20', 'inactive');

select * from employees

INSERT INTO Attendance (attendance_id, employee_id, work_date, check_in_time, check_out_time, hours_worked, status_atd) VALUES
-- Nhân viên E001
('A001', 'E001', '2024-03-01', '2024-03-01 08:00:00', '2024-03-01 17:00:00', 8.0, 'present'),
('A002', 'E001', '2024-03-02', '2024-03-02 08:30:00', '2024-03-02 16:30:00', 7.5, 'present'),
('A003', 'E001', '2024-03-03', NULL, NULL, 0, 'absent'),
('A004', 'E001', '2024-03-04', '2024-03-04 08:15:00', '2024-03-04 17:15:00', 8.5, 'present'),

-- Nhân viên E002
('A005', 'E002', '2024-03-01', '2024-03-01 09:00:00', '2024-03-01 18:00:00', 8.0, 'present'),
('A006', 'E002', '2024-03-02', '2024-03-02 08:00:00', '2024-03-02 17:00:00', 8.0, 'present'),
('A007', 'E002', '2024-03-03', NULL, NULL, 0, 'leave'),
('A008', 'E002', '2024-03-04', '2024-03-04 08:00:00', '2024-03-04 16:00:00', 7.0, 'present'),

-- Nhân viên E003
('A009', 'E003', '2024-03-01', '2024-03-01 08:00:00', '2024-03-01 17:00:00', 8.0, 'present'),
('A010', 'E003', '2024-03-02', '2024-03-02 08:30:00', '2024-03-02 16:30:00', 7.5, 'present'),
('A011', 'E003', '2024-03-03', NULL, NULL, 0, 'absent'),
('A012', 'E003', '2024-03-04', '2024-03-04 08:00:00', '2024-03-04 17:00:00', 8.0, 'present'),

-- Nhân viên E004
('A013', 'E004', '2024-03-01', '2024-03-01 09:00:00', '2024-03-01 18:00:00', 8.0, 'present'),
('A014', 'E004', '2024-03-02', NULL, NULL, 0, 'leave'),
('A015', 'E004', '2024-03-03', '2024-03-03 08:00:00', '2024-03-03 17:00:00', 8.0, 'present'),
('A016', 'E004', '2024-03-04', '2024-03-04 08:30:00', '2024-03-04 16:30:00', 7.5, 'present'),

-- Nhân viên E005
('A017', 'E005', '2024-03-01', '2024-03-01 08:00:00', '2024-03-01 17:00:00', 8.0, 'present'),
('A018', 'E005', '2024-03-02', NULL, NULL, 0, 'absent'),
('A019', 'E005', '2024-03-03', '2024-03-03 08:00:00', '2024-03-03 17:00:00', 8.0, 'present'),
('A020', 'E005', '2024-03-04', NULL, NULL, 0, 'leave');

select * from attendance

DELIMITER //
CREATE PROCEDURE Get_Department()
BEGIN
    SELECT * FROM Department;
END //
DELIMITER ;

call Get_Department();


-- Thủ tục lấy danh sách nhân viên
DELIMITER //
CREATE PROCEDURE Get_Employees()
BEGIN
    SELECT employee_id, full_name, birthday, gender, position, department_id FROM Employees;
END //
DELIMITER ;

call Get_employees

-- Thủ tục lấy thông tin nhân viên theo ID
DELIMITER //
create PROCEDURE Get_Employees_ID(IN em_id varchar(10))
BEGIN
    SELECT * FROM Employees WHERE employee_id = em_id;
END //
DELIMITER ;

DROP PROCEDURE IF EXISTS Get_Employees_ID;

call get_employees_id('E002')

-- Thủ tục chèn nhân viên
DELIMITER //
CREATE PROCEDURE Insert_Employees(
    IN employee_id varchar(10), IN full_name VARCHAR(100), IN department VARCHAR(50),
    IN position VARCHAR(50), IN hire_date DATE)
BEGIN
    INSERT INTO Employees(employee_id, full_name, department_id, position, hire_date) 
    VALUES (employee_id, full_name, department, position, hire_date);
END //
DELIMITER ;

call insert_employees('E006','vinh pui','D003','buwin','2024-01-01')



-- Thủ tục chèn phòng ban
DELIMITER //
CREATE PROCEDURE Insert_Department(IN department_id VARCHAR(50), IN department_name VARCHAR(100))
BEGIN
    INSERT INTO Department VALUES (department_id, department_name);
END //
DELIMITER ;

INSERT INTO Department (department_id, department_name)
VALUES ('D006', 'CSKH');

-- Thủ tục xóa nhân viên theo mã nhân viên
DELIMITER //
CREATE PROCEDURE Delete_Employees(IN em_id varchar(10))
BEGIN
    DELETE FROM Employees WHERE employee_id = em_id;
END //
DELIMITER ;

call delete_employees('E006')

-- Hàm đếm số lượng nhân viên
DELIMITER //
CREATE FUNCTION CountOfEmp() RETURNS INT
READS SQL DATA
BEGIN
    DECLARE emp_count INT;
    SELECT COUNT(*) INTO emp_count FROM Employees;
    RETURN emp_count;
END //
DELIMITER ;

select CountOfEmp()

-

-- Trigger tự động cập nhật số giờ làm việc--chua xai dc
DELIMITER //
CREATE TRIGGER Update_NumOfWork
BEFORE UPDATE ON Attendance
FOR EACH ROW
BEGIN
    SET NEW.hours_worked = 
        (TIME_TO_SEC(NEW.check_out_time) - TIME_TO_SEC(NEW.check_in_time)) / 3600;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE Get_Attendance_By_Month(
    IN month_input INT,
    IN year_input INT
)
BEGIN
    SELECT 
        e.employee_id, 
        e.full_name, 
        COUNT(a.work_date) AS days_present
    FROM Employees e
    LEFT JOIN Attendance a 
        ON e.employee_id = a.employee_id
        AND MONTH(a.work_date) = month_input 
        AND YEAR(a.work_date) = year_input
        AND a.status_atd = 'present'
    GROUP BY e.employee_id, e.full_name
    ORDER BY days_present DESC;
END //

DELIMITER ;

call Get_Attendance_By_Month('03','2024')


