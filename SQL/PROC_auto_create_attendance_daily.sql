DELIMITER $$

CREATE PROCEDURE Insert_Daily_Attendance()
BEGIN
    INSERT INTO Attendance (employee_id, work_date, hours_worked)
    SELECT employee_id, CURDATE(), 0
    FROM Employees;
END$$

DELIMITER ;



-- Bật event scheduler nếu chưa bật
SET GLOBAL event_scheduler = ON;

-- Tạo event chạy hàng ngày
CREATE EVENT Auto_Insert_Attendance_Daily
ON SCHEDULE EVERY 1 DAY
STARTS CURRENT_DATE + INTERVAL 1 DAY + INTERVAL 1 MINUTE  -- bắt đầu từ 00:01 ngày mai
DO
    CALL Insert_Daily_Attendance();
