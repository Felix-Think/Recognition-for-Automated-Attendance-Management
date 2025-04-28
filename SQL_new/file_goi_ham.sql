drop database NCKH;

use nckh;

select * from Employees
select * from Department
select * from Attendance 

DELETE FROM Attendance 
-- Vào Edit > Preferences.
-- Chọn tab SQL Editor.
-- Bỏ chọn "Safe Updates (rejects UPDATEs and DELETEs with no key in WHERE clause)" ở dưới cùng
-- Nhấn OK.
-- Reconnect lại với cơ sở dữ liệu để áp dụng thay đổi.


------------------------------------------------------------------------------------------------------------------------------------
CALL sp_AddEmployee('Lý Hải Nam', '1998-02-14', 'M', 'D03', 'Kế toán', '2024-05-01', 1);
CALL sp_UpdateEmployee('E004','Lý Hải Na', '1998-02-14', 'M', 'D03', 'Kế toán', '2024-05-01', 1);
CALL sp_AddDepartment('D05','Phong CSKH')
CALL sp_UpdateDepartment('D05','Phòng CSKH')


------------------------------------------------------------------------------------------------------------------------------------
INSERT INTO Attendance (attendance_id,employee_id, work_date, check_in_time, hours_worked, status_atd)
VALUES
('E00425042025', 'E004', '2025-04-20', '2025-04-20 08:00:00', 0.0, 1);  -- có id



call sp_checkoutnow('E00425042025')
call sp_checkinnow('E00425042025')



DELETE FROM Attendance
WHERE attendance_id = ''; 

------------------------------------------------------------------------------------------------------------------------------------
 CALL Insert_Daily_Attendance()

------------------------------------------------------------------------------------------------------------------------------------
CALL Get_Employee_Monthly_Info('4','2025','E001') -- xuất lương tháng 1 nhân viên (dọc)
CALL Get_Attendance_Report_ByMonthYear_Employee('4','2025','E001')
CALL Get_Attendance_Report_ByMonthYear('4','2025') -- xuất hết nhân viên của 1 tháng (ngang)
------------------------------------------------------------------------------------------------------------------------------------
SELECT ROUTINE_NAME  
FROM INFORMATION_SCHEMA.ROUTINES  
WHERE ROUTINE_TYPE = 'PROCEDURE'  
  AND ROUTINE_SCHEMA = 'NCKH'
LIMIT 0, 1000;  -- kiem tra tat ca ham trong db
SHOW TRIGGERS LIKE 'Attendance';
SHOW TRIGGERS LIKE 'Employees';

SHOW VARIABLES LIKE 'collation%';
ALTER DATABASE `NCKH` CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;


