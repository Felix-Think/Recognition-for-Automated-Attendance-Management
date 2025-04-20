DELIMITER $$

CREATE PROCEDURE sp_AddEmployee (
    IN p_full_name nVARCHAR(100),
    IN p_birthday DATE,
    IN p_gender CHAR(1),
    IN p_department_id VARCHAR(10),
    IN p_position VARCHAR(50),
    IN p_hire_date DATE,
    IN p_work_status BIT
)
BEGIN
    -- Kiểm tra phòng ban tồn tại
    IF NOT EXISTS (
        SELECT 1 FROM Department WHERE department_id = p_department_id
    ) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Phòng ban không tồn tại!';
    END IF;

    -- Kiểm tra trùng họ tên + ngày sinh
    IF EXISTS (
        SELECT 1 FROM Employees 
        WHERE full_name = p_full_name AND birthday = p_birthday
    ) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Nhân viên đã tồn tại (trùng tên và ngày sinh)!';
    END IF;

    -- Thêm nhân viên (ID sẽ được trigger tự sinh)
    INSERT INTO Employees (
        full_name, birthday, gender, department_id, position, hire_date, work_status
    )
    VALUES (
        p_full_name, p_birthday, p_gender, p_department_id, p_position, p_hire_date, p_work_status
    );
END$$

DELIMITER ;

CALL sp_AddEmployee('Lý Hải Nam', '1998-02-14', 'M', 'D03', 'Kế toán', '2024-05-01', 1);

DELIMITER $$

CREATE PROCEDURE sp_UpdateEmployee (
    IN p_employee_id VARCHAR(20),
    IN p_full_name nVARCHAR(100),
    IN p_birthday DATE,
    IN p_gender CHAR(1),
    IN p_department_id VARCHAR(10),
    IN p_position VARCHAR(50),
    IN p_hire_date DATE,
    IN p_work_status BIT
)
BEGIN
    -- Kiểm tra nhân viên tồn tại
    IF NOT EXISTS (
        SELECT 1 FROM Employees WHERE employee_id = p_employee_id
    ) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Mã nhân viên không tồn tại!';
    END IF;

    -- Cập nhật thông tin
    UPDATE Employees
    SET full_name = p_full_name,
        birthday = p_birthday,
        gender = p_gender,
        department_id = p_department_id,
        position = p_position,
        hire_date = p_hire_date,
        work_status = p_work_status
    WHERE employee_id = p_employee_id;
END$$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE sp_DeleteEmployee (
    IN p_employee_id VARCHAR(20)
)
BEGIN
    -- Kiểm tra tồn tại
    IF NOT EXISTS (
        SELECT 1 FROM Employees WHERE employee_id = p_employee_id
    ) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Mã nhân viên không tồn tại!';
    END IF;

    -- Xóa nhân viên
    DELETE FROM Employees WHERE employee_id = p_employee_id;
END$$

DELIMITER ;

DELIMITER $$
-- ---------------------------------------------------------- --

DELIMITER $$

CREATE PROCEDURE sp_AddDepartment (
    IN p_department_id VARCHAR(10),
    IN p_department_name nVARCHAR(100)
)
BEGIN
    -- Kiểm tra phòng ban đã tồn tại hay chưa
    IF EXISTS (
        SELECT 1 FROM Department WHERE department_id = p_department_id
    ) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Mã phòng ban đã tồn tại!';
    END IF;

    -- Thêm phòng ban
    INSERT INTO Department (department_id, department_name)
    VALUES (p_department_id, p_department_name);
END$$

DELIMITER ;


DELIMITER $$

CREATE PROCEDURE sp_UpdateDepartment (
    IN p_department_id VARCHAR(10),
    IN p_department_name nVARCHAR(100)
)
BEGIN
    -- Kiểm tra mã phòng ban tồn tại
    IF NOT EXISTS (
        SELECT 1 FROM Department WHERE department_id = p_department_id
    ) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Phòng ban không tồn tại!';
    END IF;
    
    -- Cập nhật thông tin phòng ban
    UPDATE Department
    SET department_name = p_department_name
    WHERE department_id = p_department_id;
END$$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE sp_DeleteDepartment (
    IN p_department_id VARCHAR(10)
)
BEGIN
    -- Kiểm tra mã phòng ban tồn tại
    IF NOT EXISTS (
        SELECT 1 FROM Department WHERE department_id = p_department_id
    ) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Phòng ban không tồn tại!';
    END IF;
    
    -- Xóa phòng ban
    DELETE FROM Department
    WHERE department_id = p_department_id;
END$$

DELIMITER ;





	




