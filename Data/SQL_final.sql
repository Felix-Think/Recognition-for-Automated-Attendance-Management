----Định nghĩa bảng Nhân viên
CREATE TABLE Employees (
    employee_id INT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
	birthday DATETIME,
	gender bit,
    department_id VARCHAR(50),
    position VARCHAR(50),
    hire_date DATE,
    status NVARCHAR(20) CHECK (status IN ('active', 'inactive')),
	FOREIGN KEY (department_id) REFERENCES Department(department_id)
)

----Định nghĩa bảng Chấm công
CREATE TABLE Attendance (
    attendance_id INT PRIMARY KEY,
    employee_id INT,
    work_date DATE NOT NULL,
    check_in_time TIME,
    check_out_time TIME,
    hours_worked FLOAT,
    status NVARCHAR(20) CHECK (status IN ('present', 'absent', 'leave')),
    FOREIGN KEY (employee_id) REFERENCES Employees(employee_id)
)

----Định nghĩa bảng Phòng ban
CREATE TABLE Department(
	department_id VARCHAR(50) PRIMARY KEY,
	department_name VARCHAR(100) NOT NULL
)


----------THỦ TỤC----------

----Thủ tục lấy danh sách tất cả nhân viên
CREATE PROC Get_Employees
AS
SELECT employee_id, full_name, birthday, gender, position, department_id FROM Employees

----Thủ tục lấy về tất cả các phòng ban
CREATE PROC Get_Department
AS
SELECT * FROM Department

----Thủ tục lấy thông tin nhân viên dựa vào mã nhân viên
CREATE PROC Get_Employees_ID(@em_id INT)
AS
	SELECT * FROM Employees WHERE employee_id = @em_id

----Thủ tục chèn nhân viên
create proc Insert_Employees(@employee_id int, @full_name varchar(100),@department varchar(50),
@position VARCHAR(50),@hire_date DATE)
as
  insert into Employees(employee_id,full_name,department_id,position,hire_date) 
  values(@employee_id,@full_name,@department,@position,@hire_date)

----Thủ tục chèn phòng ban
create proc Insert_Department(@department_id varchar(50), @department_name nvarchar(100))
as
	insert into Department values(@department_id,@department_name)

----Thủ tục xóa nhân viên theo mã nhân viên
CREATE PROC Delete_Employees(@em_id int)
AS
	DELETE FROM Employees WHERE  @em_id = employee_id

----Thủ tục cập nhật thông tin nhân viên
create proc Process_Employees(@employee_id int, @full_name nvarchar(50), @birthday date, @gender nvarchar(10), @link_image nvarchar(100),@department nvarchar(50),@position nvarchar(10))
as
	if  exists (select * from department where @department = department_id)
		if not exists (select * from Employees where @employee_id=employee_id)
			insert into Employees(department_id,employee_id,full_name,position,birthday,gender,link_image)
			values(@department, @employee_id,@full_name,@position,@birthday,@gender,@link_image)
		else
			update Employees set department_id=@department,full_name=@full_name,position=@position,birthday=@birthday,gender=@gender,link_image=@link_image
						where employee_id=@employee_id

----Thủ tục LẤY DANH SÁCH CHẤM CÔNG THEO THÁNG
create proc Take_Attendance_MonthEmployee(@month int, @employee_id int)
as
begin
	declare @cols AS NVARCHAR(MAX), --Chuỗi danh sách ngày làm việc
			@query  AS NVARCHAR(MAX), --Chuỗi chứa truy vấn động
			@year as int --Năm hiện tại
	set @year = cast(year(getdate()) as int)
	select @cols = STRING_AGG(QUOTENAME(CONVERT(VARCHAR, work_date, 111)), ', ')
	from (SELECT DISTINCT work_date from Attendance 
			where cast(MONTH(work_date)as int) = @month and year(work_date) = @year 
					and employee_id=@employee_id) AS DateList;

	--Câu truy vấn động với PIVOT tạo ra bảng chấm công số giờ làm việc của nhân viên cụ thể trong một tháng
	SET @query = '
	SELECT employee_id, ' + @cols + '
	FROM (
		SELECT employee_id, 
			   CONVERT(VARCHAR,work_date , 111) AS work_date, 
			   hours_worked
		FROM Attendance
	) AS SourceTable
	PIVOT (
		SUM(hours_worked)
		FOR work_date IN (' + @cols + ')
	) AS PivotTable'

	--Thực thi truy vấn động
	exec sp_executesql @query
end
----Giải thích:
--STRING_AGG: Hàm này được sử dụng để tạo chuỗi các ngày trong định dạng cột. QUOTENAME được sử dụng để đảm bảo rằng tên cột được định dạng đúng.


----------FUNCTION----------

----Hàm đếm số lượng nhân viên
create function CountOfEmp()
returns int
as
	begin
		declare @count int
		select @count=count(*) from Employees
		return @count
	end

----Hàm tạo mã nhân viên tự động 
create function Get_Employee_id()
returns int
as
	begin
		declare @Number int
		select @Number=COUNT(*) from Employees
		return @Number+1
	end
	
----Định nghĩa hàm kiểm tra chấm công
--Trả về 0 nếu mã nhân viên chưa tồn tại
--Trả về 1 nếu trong ngày đó đã check in và check out
--Trả vè 2 nếu thực hiện check out thành công
--Trả về 3 nếu thực hiên check in thành công
CREATE FUNCTION Check_attendaces(@employee_id INT, @work_date DATE, @time TIME)
RETURNS INT
AS
BEGIN
    -- 1️ Kiểm tra nhân viên có tồn tại không
    IF NOT EXISTS (SELECT 1 FROM Employees WHERE employee_id = @employee_id)
        RETURN 0  -- Nhân viên không tồn tại
    
    -- 2️ Kiểm tra nhân viên đã check-out chưa
    IF EXISTS (SELECT 1 FROM Attendance 
               WHERE employee_id = @employee_id 
               AND work_date = @work_date 
               AND check_out_time IS NOT NULL)
        RETURN 1  -- Đã check-out
    
    -- 3️ Kiểm tra đã check-in nhưng chưa check-out
    IF EXISTS (SELECT 1 FROM Attendance 
               WHERE employee_id = @employee_id 
               AND work_date = @work_date 
               AND check_out_time IS NULL)
        RETURN 2  -- Đã check-in nhưng chưa check-out
    
    -- 4️ Nếu không có bản ghi nào trong Attendance → Chưa check-in
    RETURN 3
END


----------TRIGGER----------

----Trigger tự động cập nhật số giờ làm việc
create trigger Update_NumOfWork on Attendence for UPDATE
as 
	update Attendance
	set hours_worked = 
		(cast(datediff(second, '00:00:00', check_out_time) as int) -
		cast(datediff(second, '00:00:00', check_in_time) as int)) / 3600
	