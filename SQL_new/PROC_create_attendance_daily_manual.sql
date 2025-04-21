-- file này chưa test cái auto đâu --

DELIMITER $$
CREATE PROCEDURE Insert_Daily_Attendance()
BEGIN
    INSERT INTO Attendance (attendance_id, employee_id, work_date, check_in_time, check_out_time, hours_worked, status_atd)
    SELECT 
        CONCAT(e.employee_id, DATE_FORMAT(CURDATE(), '%d%m%y')) AS attendance_id,
        e.employee_id,
        CURDATE(),
        NULL,  -- check_in_time
        NULL,  -- check_out_time
        0,     -- hours_worked
        NULL   -- status_atd
    FROM Employees e
    WHERE NOT EXISTS (
        SELECT 1 FROM Attendance a 
        WHERE a.employee_id = e.employee_id 
        AND a.work_date = CURDATE()
    );
END$$
DELIMITER ;




-- Bật event scheduler nếu chưa bật --Không chạy khúc dưới
SET GLOBAL event_scheduler = ON;

-- Tạo event chạy hàng ngày
CREATE EVENT Auto_Insert_Attendance_Daily
ON SCHEDULE EVERY 1 DAY
STARTS CURRENT_DATE + INTERVAL 1 DAY + INTERVAL 1 MINUTE  -- bắt đầu từ 00:01 ngày mai
DO
    CALL Insert_Daily_Attendance();

-- file này chưa test cái auto đâu --


DELIMITER $$  -- dưới này insert thủ công

CREATE PROCEDURE Insert_Attendance_If_Not_Exists (
    IN p_employee_id VARCHAR(20),
    IN p_work_date DATE,
    IN p_check_in DATETIME,
    IN p_check_out DATETIME,
    IN p_hours FLOAT,
    IN p_status BIT
)
BEGIN
    DECLARE attendance_key VARCHAR(20);

    -- Tạo attendance_id từ employee_id + ngày
    SET attendance_key = CONCAT(p_employee_id, DATE_FORMAT(p_work_date, '%d%m%y'));

    -- Kiểm tra xem đã có dữ liệu chưa
    IF NOT EXISTS (
        SELECT 1 FROM Attendance
        WHERE attendance_id = attendance_key
    ) THEN
        INSERT INTO Attendance (
            attendance_id, employee_id, work_date,
            check_in_time, check_out_time, hours_worked, status_atd
        )
        VALUES (
            attendance_key, p_employee_id, p_work_date,
            p_check_in, p_check_out, p_hours, p_status
        );
    END IF;
END$$

DELIMITER ;
