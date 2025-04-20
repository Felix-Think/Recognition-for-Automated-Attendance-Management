DELIMITER $$

CREATE PROCEDURE Generate_Pivot_Report()
BEGIN
    DECLARE i INT DEFAULT 1;
    DECLARE max_day INT;
    DECLARE sql_query TEXT DEFAULT '';

    -- Lấy ngày hiện tại trong tháng
    SET max_day = DAY(CURDATE());

    -- Bắt đầu xây chuỗi SELECT
    SET sql_query = CONCAT('SELECT e.employee_id AS "Mã NV", ');

    -- Duyệt từ ngày 1 đến ngày hiện tại
    WHILE i <= max_day DO
        SET sql_query = CONCAT(
            sql_query,
            'SUM(CASE WHEN DAY(a.work_date) = ', i, ' THEN a.hours_worked ELSE NULL END) AS `', i, '`, '
        );
        SET i = i + 1;
    END WHILE;

    -- Loại bỏ dấu phẩy cuối cùng sau cột ngày
    SET sql_query = LEFT(sql_query, LENGTH(sql_query) - 2);

    -- Thêm phần số ngày nghỉ và tăng ca
    SET sql_query = CONCAT(
        sql_query,
        ', ',  -- Chèn dấu phẩy trước phần tiếp theo
        'COUNT(DISTINCT a.work_date) AS so_ngay_nghi, ',
        'SUM(CASE WHEN a.hours_worked > 8 THEN a.hours_worked - 8 ELSE 0 END) AS `Số giờ tăng ca` ',
        'FROM Employees e ',
        'LEFT JOIN Attendance a ON e.employee_id = a.employee_id ',
        'WHERE MONTH(a.work_date) = MONTH(CURDATE()) ',
        'AND YEAR(a.work_date) = YEAR(CURDATE()) ',
        'AND DAY(a.work_date) <= ', max_day, ' ',
        'GROUP BY e.employee_id'
    );

    -- Thực thi câu lệnh động
    PREPARE stmt FROM sql_query;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;

END$$

DELIMITER ;


