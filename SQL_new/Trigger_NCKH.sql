DELIMITER $$

CREATE TRIGGER trg_auto_generate_employee_id
BEFORE INSERT ON Employees
FOR EACH ROW
BEGIN
    DECLARE max_num INT DEFAULT 0;
    DECLARE new_id VARCHAR(10);

    -- Tìm số lớn nhất trong employee_id hiện tại
    SELECT MAX(CAST(SUBSTRING(employee_id, 2) AS UNSIGNED))
    INTO max_num
    FROM Employees
    WHERE employee_id REGEXP '^E[0-9]{3}$';

    -- Tạo mã mới: E + 3 chữ số
    SET new_id = CONCAT('E', LPAD(max_num + 1, 3, '0'));

    -- Gán cho dòng chuẩn bị insert
    SET NEW.employee_id = new_id;
END$$

DELIMITER ;

INSERT INTO Employees (full_name, birthday, gender, department_id, position, hire_date, work_status)
VALUES ('Lý Hải Nam', '1998-02-14', 'M', 'D03', 'Kế toán', '2024-05-01', 1);

select * from Employees

DELIMITER $$

CREATE TRIGGER trg_auto_generate_attendance_id
BEFORE INSERT ON Attendance
FOR EACH ROW
BEGIN
    DECLARE max_num INT DEFAULT 0;
    DECLARE new_id VARCHAR(15);
    DECLARE emp_id_prefix VARCHAR(4);
    DECLARE current_date_str VARCHAR(8);

    -- Lấy tiền tố mã nhân viên (3 chữ số đầu trong employee_id)
    SET emp_id_prefix = SUBSTRING(NEW.employee_id, 2, 3);

    -- Lấy ngày hiện tại theo định dạng ddmmyyyy
    SET current_date_str = DATE_FORMAT(CURDATE(), '%d%m%Y');

    -- Tạo mã attendance mới: E + 3 chữ số của employee_id + ngày tháng hiện tại
    SET new_id = CONCAT('E', emp_id_prefix, current_date_str);

    -- Gán cho dòng chuẩn bị insert
    SET NEW.attendance_id = new_id;
END$$

DELIMITER ;



