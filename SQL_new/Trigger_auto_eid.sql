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










