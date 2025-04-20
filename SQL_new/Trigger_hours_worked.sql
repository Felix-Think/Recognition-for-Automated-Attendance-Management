DELIMITER $$

CREATE TRIGGER trg_UpdateHoursWorked
BEFORE UPDATE ON Attendance
FOR EACH ROW
BEGIN
    -- Chỉ xử lý khi check_out_time thay đổi
    IF NEW.check_out_time IS NOT NULL AND 
       (OLD.check_out_time IS NULL OR NEW.check_out_time <> OLD.check_out_time) THEN
        
        -- Nếu đang ở trong công ty (status_atd = 1)
        IF OLD.status_atd = 1 THEN
            -- Tính số giờ làm = checkout - checkin (theo giây, chia 3600 để ra giờ thập phân)
            SET NEW.hours_worked = TIMESTAMPDIFF(SECOND, OLD.check_in_time, NEW.check_out_time) / 3600.0;

            -- Đặt trạng thái về 0
            SET NEW.status_atd = 0;
        END IF;

    END IF;
END$$

DELIMITER ;


drop trigger trg_UpdateHoursWorked
SHOW TRIGGERS LIKE 'Attendance';



INSERT INTO Attendance (attendance_id, employee_id, work_date, check_in_time, hours_worked, status_atd)
VALUES
('E00318042025_2', 'E004', '2025-04-18', '2025-04-18 08:00:00', 0.0, 1);

UPDATE Attendance
SET check_out_time = NOW()
WHERE attendance_id = 'E00318042025_2';

DELETE FROM Attendance
WHERE attendance_id = 'E00318042025_2';


select * from attendance
