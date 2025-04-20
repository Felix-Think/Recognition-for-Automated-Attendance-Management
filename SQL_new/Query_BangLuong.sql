SELECT 
    e.employee_id AS 'Mã NV',
    SUM(CASE WHEN DAY(a.work_date) = 1 THEN a.hours_worked ELSE NULL END) AS '1',
    SUM(CASE WHEN DAY(a.work_date) = 2 THEN a.hours_worked ELSE NULL END) AS '2',
    SUM(CASE WHEN DAY(a.work_date) = 3 THEN a.hours_worked ELSE NULL END) AS '3',
    SUM(CASE WHEN DAY(a.work_date) = 4 THEN a.hours_worked ELSE NULL END) AS '4',
    SUM(CASE WHEN DAY(a.work_date) = 5 THEN a.hours_worked ELSE NULL END) AS '5',
    SUM(CASE WHEN DAY(a.work_date) = 6 THEN a.hours_worked ELSE NULL END) AS '6',
    SUM(CASE WHEN DAY(a.work_date) = 7 THEN a.hours_worked ELSE NULL END) AS '7',
    SUM(CASE WHEN DAY(a.work_date) = 8 THEN a.hours_worked ELSE NULL END) AS '8',
    SUM(CASE WHEN DAY(a.work_date) = 9 THEN a.hours_worked ELSE NULL END) AS '9',
    SUM(CASE WHEN DAY(a.work_date) = 10 THEN a.hours_worked ELSE NULL END) AS '10',
    SUM(CASE WHEN DAY(a.work_date) = 11 THEN a.hours_worked ELSE NULL END) AS '11',
    SUM(CASE WHEN DAY(a.work_date) = 12 THEN a.hours_worked ELSE NULL END) AS '12',
    SUM(CASE WHEN DAY(a.work_date) = 13 THEN a.hours_worked ELSE NULL END) AS '13',
    SUM(CASE WHEN DAY(a.work_date) = 14 THEN a.hours_worked ELSE NULL END) AS '14',
    SUM(CASE WHEN DAY(a.work_date) = 15 THEN a.hours_worked ELSE NULL END) AS '15',
    SUM(CASE WHEN DAY(a.work_date) = 16 THEN a.hours_worked ELSE NULL END) AS '16',
    SUM(CASE WHEN DAY(a.work_date) = 17 THEN a.hours_worked ELSE NULL END) AS '17',
    SUM(CASE WHEN DAY(a.work_date) = 18 THEN a.hours_worked ELSE NULL END) AS '18',
    SUM(CASE WHEN DAY(a.work_date) = 19 THEN a.hours_worked ELSE NULL END) AS '19',
    SUM(CASE WHEN DAY(a.work_date) = 20 THEN a.hours_worked ELSE NULL END) AS '20',
    SUM(CASE WHEN DAY(a.work_date) = 21 THEN a.hours_worked ELSE NULL END) AS '21',
    SUM(CASE WHEN DAY(a.work_date) = 22 THEN a.hours_worked ELSE NULL END) AS '22',
    SUM(CASE WHEN DAY(a.work_date) = 23 THEN a.hours_worked ELSE NULL END) AS '23',
    SUM(CASE WHEN DAY(a.work_date) = 24 THEN a.hours_worked ELSE NULL END) AS '24',
    SUM(CASE WHEN DAY(a.work_date) = 25 THEN a.hours_worked ELSE NULL END) AS '25',
    SUM(CASE WHEN DAY(a.work_date) = 26 THEN a.hours_worked ELSE NULL END) AS '26',
    SUM(CASE WHEN DAY(a.work_date) = 27 THEN a.hours_worked ELSE NULL END) AS '27',
    SUM(CASE WHEN DAY(a.work_date) = 28 THEN a.hours_worked ELSE NULL END) AS '28',
    SUM(CASE WHEN DAY(a.work_date) = 29 THEN a.hours_worked ELSE NULL END) AS '29',
    SUM(CASE WHEN DAY(a.work_date) = 30 THEN a.hours_worked ELSE NULL END) AS '30',
    SUM(CASE WHEN DAY(a.work_date) = 31 THEN a.hours_worked ELSE NULL END) AS '31',
	31 - COUNT(a.work_date) AS so_ngay_nghi,
    SUM(CASE WHEN a.hours_worked > 8 THEN a.hours_worked - 8 ELSE 0 END) AS 'Số giờ tăng ca'
FROM 
    Employees e
LEFT JOIN 
    Attendance a ON e.employee_id = a.employee_id
WHERE 
    MONTH(a.work_date) = 4 AND YEAR(a.work_date) = 2025
GROUP BY 
    e.employee_id;
