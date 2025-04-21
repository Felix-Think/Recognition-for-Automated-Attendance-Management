DELIMITER $$

CREATE PROCEDURE Get_Employee_Monthly_Info(
    IN p_thang INT,
    IN p_nam INT,
    IN p_employee_id VARCHAR(20)
)
BEGIN
    SELECT 
        'Mã NV' AS 'Thông tin', e.employee_id AS 'Giá trị'
    FROM Employees e
    WHERE e.employee_id = p_employee_id

    UNION ALL

    SELECT 
        'Tên NV' AS 'Thông tin', e.full_name AS 'Giá trị'
    FROM Employees e
    WHERE e.employee_id = p_employee_id

    UNION ALL

    SELECT 
        'Phòng ban' AS 'Thông tin', d.department_name AS 'Giá trị'
    FROM Employees e
    JOIN Department d ON e.department_id = d.department_id
    WHERE e.employee_id = p_employee_id

    UNION ALL

    SELECT 
        'Vị trí' AS 'Thông tin', e.position AS 'Giá trị'
    FROM Employees e
    WHERE e.employee_id = p_employee_id

    UNION ALL

    SELECT 
        'Lương 1 giờ' AS 'Thông tin', NULL AS 'Giá trị'

    UNION ALL

    SELECT 
        'Hệ số lương' AS 'Thông tin', NULL AS 'Giá trị'

    UNION ALL

    SELECT 
        'Số giờ tăng ca' AS 'Thông tin', 
        CAST(SUM(CASE WHEN a.hours_worked > 8 THEN a.hours_worked - 8 ELSE 0 END) AS CHAR) AS 'Giá trị'
    FROM Employees e
    LEFT JOIN Attendance a ON e.employee_id = a.employee_id
    WHERE e.employee_id = p_employee_id 
      AND MONTH(a.work_date) = p_thang 
      AND YEAR(a.work_date) = p_nam
    GROUP BY e.employee_id

    UNION ALL

    SELECT 
        'Số ngày làm' AS 'Thông tin',
        CAST(COUNT(a.work_date) AS CHAR) AS 'Giá trị'
    FROM Employees e
    LEFT JOIN Attendance a ON e.employee_id = a.employee_id
    WHERE e.employee_id = p_employee_id 
      AND MONTH(a.work_date) = p_thang 
      AND YEAR(a.work_date) = p_nam 
      AND a.hours_worked > 0

    UNION ALL

    SELECT 
        'Khoảng trừ' AS 'Thông tin', NULL AS 'Giá trị'

    UNION ALL

    SELECT 
        'Thực nhận' AS 'Thông tin', NULL AS 'Giá trị';
END$$

DELIMITER ;
