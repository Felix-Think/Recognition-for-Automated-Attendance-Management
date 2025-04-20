SET @thang = 4;
SET @nam = 2025;
use NCKH 
SELECT 
    'Mã NV' AS 'Thông tin', e.employee_id AS 'Giá trị'
FROM Employees e
WHERE e.employee_id = 'E001'
UNION ALL
SELECT 
    'Tên NV' AS 'Thông tin', e.full_name AS 'Giá trị'
FROM Employees e
WHERE e.employee_id = 'E001'
UNION ALL
SELECT 
    'Phòng ban' AS 'Thông tin', d.department_name AS 'Giá trị'
FROM Employees e
JOIN Department d ON e.department_id = d.department_id
WHERE e.employee_id = 'E001'
UNION ALL
SELECT 
    'Vị trí' AS 'Thông tin', e.position AS 'Giá trị'
FROM Employees e
WHERE e.employee_id = 'E001'
UNION ALL
SELECT 
    'Lương 1 giờ' AS 'Thông tin', NULL AS 'Giá trị' -- (trống)
UNION ALL
SELECT 
    'Hệ số lương' AS 'Thông tin', NULL AS 'Giá trị' -- (trống)
UNION ALL
SELECT 
    'Số giờ tăng ca' AS 'Thông tin', 
    SUM(CASE WHEN a.hours_worked > 8 THEN a.hours_worked - 8 ELSE 0 END) AS 'Giá trị'
FROM Employees e
LEFT JOIN Attendance a ON e.employee_id = a.employee_id
WHERE e.employee_id = 'E001' AND MONTH(a.work_date) = @thang AND YEAR(a.work_date) = @nam
GROUP BY e.employee_id
UNION ALL
SELECT 
    'Số ngày làm' AS 'Thông tin',
    COUNT(a.work_date) AS 'Giá trị'
FROM Employees e
LEFT JOIN Attendance a ON e.employee_id = a.employee_id
WHERE e.employee_id = 'E001' AND MONTH(a.work_date) = @thang AND YEAR(a.work_date) = @nam AND a.hours_worked > 0
UNION ALL
SELECT 
    'Khoảng trừ' AS 'Thông tin', NULL AS 'Giá trị' -- (trống)
UNION ALL
SELECT 
    'Thực nhận' AS 'Thông tin', NULL AS 'Giá trị' -- (trống)
;
