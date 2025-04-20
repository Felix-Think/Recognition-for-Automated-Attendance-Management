DELIMITER $$

CREATE PROCEDURE sp_CheckInNow (
    IN p_attendance_id VARCHAR(20)
)
BEGIN
    -- Kiểm tra dòng tồn tại
    IF NOT EXISTS (
        SELECT 1 FROM Attendance WHERE attendance_id = p_attendance_id
    ) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'attendance_id không tồn tại!';
    END IF;

    -- Cập nhật check-in là thời gian hiện tại
    UPDATE Attendance
    SET check_in_time = NOW()
    WHERE attendance_id = p_attendance_id;
END$$

DELIMITER ;


DELIMITER $$

CREATE PROCEDURE sp_CheckOutNow (
    IN p_attendance_id VARCHAR(20)
)
BEGIN
    -- Kiểm tra dòng tồn tại
    IF NOT EXISTS (
        SELECT 1 FROM Attendance WHERE attendance_id = p_attendance_id
    ) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'attendance_id không tồn tại!';
    END IF;

    -- Cập nhật check-out là thời gian hiện tại
    UPDATE Attendance
    SET check_out_time = NOW()
    WHERE attendance_id = p_attendance_id;
END$$

DELIMITER ;
