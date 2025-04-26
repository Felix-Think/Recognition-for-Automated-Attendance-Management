-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: nckh
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `attendance`
--

DROP TABLE IF EXISTS `attendance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attendance` (
  `attendance_id` varchar(20) NOT NULL,
  `employee_id` varchar(20) DEFAULT NULL,
  `work_date` date NOT NULL,
  `check_in_time` datetime DEFAULT NULL,
  `check_out_time` datetime DEFAULT NULL,
  `hours_worked` float DEFAULT NULL,
  `status_atd` bit(1) DEFAULT NULL,
  PRIMARY KEY (`attendance_id`),
  KEY `employee_id` (`employee_id`),
  CONSTRAINT `attendance_ibfk_1` FOREIGN KEY (`employee_id`) REFERENCES `employees` (`employee_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attendance`
--

LOCK TABLES `attendance` WRITE;
/*!40000 ALTER TABLE `attendance` DISABLE KEYS */;
INSERT INTO `attendance` VALUES ('E001120425','E001','2025-04-12','2025-04-12 08:00:00','2025-04-12 17:00:00',9,_binary '\0'),('E001130425','E001','2025-04-13','2025-04-13 08:00:00','2025-04-13 17:00:00',9,_binary '\0'),('E001140425','E001','2025-04-14','2025-04-14 08:00:00','2025-04-14 17:30:00',9.5,_binary '\0'),('E001150425','E001','2025-04-15','2025-04-15 08:00:00','2025-04-15 18:00:00',10,_binary '\0'),('E001160425','E001','2025-04-16','2025-04-16 08:00:00','2025-04-16 17:00:00',9,_binary '\0'),('E001170425','E001','2025-04-17','2025-04-17 08:00:00','2025-04-17 17:00:00',9,_binary '\0'),('E001180425','E001','2025-04-18','2025-04-18 08:00:00','2025-04-18 17:00:00',9,_binary '\0'),('E002120425','E002','2025-04-12','2025-04-12 08:00:00','2025-04-12 17:00:00',9,_binary '\0'),('E002130425','E002','2025-04-13','2025-04-13 08:00:00','2025-04-13 17:00:00',9,_binary '\0'),('E002140425','E002','2025-04-14','2025-04-14 08:00:00','2025-04-14 17:00:00',9,_binary '\0'),('E002150425','E002','2025-04-15','2025-04-15 08:00:00','2025-04-15 17:00:00',9,_binary '\0'),('E002160425','E002','2025-04-16','2025-04-16 08:00:00','2025-04-16 17:00:00',9,_binary '\0'),('E002170425','E002','2025-04-17','2025-04-17 08:00:00','2025-04-17 17:00:00',9,_binary '\0'),('E002180425','E002','2025-04-18','2025-04-18 08:00:00','2025-04-18 17:00:00',9,_binary '\0'),('E003120425','E003','2025-04-12','2025-04-12 08:00:00','2025-04-12 17:00:00',9,_binary '\0'),('E003130425','E003','2025-04-13','2025-04-13 08:00:00','2025-04-13 17:00:00',9,_binary '\0'),('E003140425','E003','2025-04-14','2025-04-14 08:00:00','2025-04-14 17:00:00',9,_binary '\0'),('E003150425','E003','2025-04-15','2025-04-15 08:00:00','2025-04-15 17:00:00',9,_binary '\0'),('E003160425','E003','2025-04-16','2025-04-16 08:00:00','2025-04-16 17:00:00',9,_binary '\0'),('E003170425','E003','2025-04-17','2025-04-17 08:00:00','2025-04-17 17:00:00',9,_binary '\0'),('E003180425','E003','2025-04-18','2025-04-18 08:00:00','2025-04-18 17:00:00',9,_binary '\0');
/*!40000 ALTER TABLE `attendance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `department`
--

DROP TABLE IF EXISTS `department`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `department` (
  `department_id` varchar(10) NOT NULL,
  `department_name` varchar(100) NOT NULL,
  PRIMARY KEY (`department_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `department`
--

LOCK TABLES `department` WRITE;
/*!40000 ALTER TABLE `department` DISABLE KEYS */;
INSERT INTO `department` VALUES ('D01','Phòng Nhân sự'),('D02','Phòng Kỹ thuật'),('D03','Phòng Kế toán');
/*!40000 ALTER TABLE `department` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employees`
--

DROP TABLE IF EXISTS `employees`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employees` (
  `employee_id` varchar(20) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `gender` char(1) DEFAULT NULL,
  `birthday` date DEFAULT NULL,
  `department_id` varchar(10) DEFAULT NULL,
  `position` varchar(50) DEFAULT NULL,
  `hire_date` date DEFAULT NULL,
  `work_status` bit(1) DEFAULT NULL,
  `profile_pic` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`employee_id`),
  KEY `department_id` (`department_id`),
  CONSTRAINT `employees_ibfk_1` FOREIGN KEY (`department_id`) REFERENCES `department` (`department_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employees`
--

LOCK TABLES `employees` WRITE;
/*!40000 ALTER TABLE `employees` DISABLE KEYS */;
INSERT INTO `employees` VALUES ('E001','Nguyễn Văn A','M','1990-01-15','D01','Trưởng phòng','2015-06-01',_binary '',NULL),('E002','Trần Thị B','F','1992-05-20','D02','Kỹ sư','2018-03-10',_binary '',NULL),('E003','Lê Văn C','M','1995-09-25','D03','Kế toán viên','2020-11-05',_binary '',NULL);
/*!40000 ALTER TABLE `employees` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `employee_id` varchar(20) NOT NULL,
  `user_name` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`employee_id`,`user_name`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`employee_id`) REFERENCES `employees` (`employee_id`),
  CONSTRAINT `users_chk_1` CHECK ((`role` in (_utf8mb4'admin',_utf8mb4'user')))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('E001','test','123','admin'),('E002','abc','123','user'),('E003','john_doe','123','user');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'nckh'
--
/*!50003 DROP PROCEDURE IF EXISTS `Delete_Attendance_By_ID` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `Delete_Attendance_By_ID`(
    IN p_attendance_id VARCHAR(20)
)
BEGIN
    DELETE FROM Attendance
    WHERE attendance_id = p_attendance_id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `Get_Attendance_Report_ByMonthYear` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `Get_Attendance_Report_ByMonthYear`(
    IN in_month INT,
    IN in_year INT
)
BEGIN
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
        MONTH(a.work_date) = in_month 
        AND YEAR(a.work_date) = in_year
    GROUP BY 
        e.employee_id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `Get_Attendance_Report_ByMonthYear_Employee` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `Get_Attendance_Report_ByMonthYear_Employee`(
    IN in_month INT,
    IN in_year INT,
    IN in_employee_id varchar(10)
)
BEGIN
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
        e.employee_id = in_employee_id AND
        MONTH(a.work_date) = in_month AND 
        YEAR(a.work_date) = in_year
    GROUP BY 
        e.employee_id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `Get_Employee_Monthly_Info` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `Get_Employee_Monthly_Info`(
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
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `Insert_Daily_Attendance` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `Insert_Daily_Attendance`()
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
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_AddDepartment` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_AddDepartment`(
    IN p_department_id VARCHAR(10),
    IN p_department_name VARCHAR(100)
)
BEGIN
    -- Kiểm tra phòng ban đã tồn tại hay chưa
    IF EXISTS (
        SELECT 1 FROM Department WHERE department_id = p_department_id
    ) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Mã phòng ban đã tồn tại!';
    END IF;

    -- Thêm phòng ban
    INSERT INTO Department (department_id, department_name)
    VALUES (p_department_id, p_department_name);
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_AddEmployee` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_AddEmployee`(
    IN p_full_name VARCHAR(100),
    IN p_birthday DATE,
    IN p_gender CHAR(1),
    IN p_department_id VARCHAR(10),
    IN p_position VARCHAR(50),
    IN p_hire_date DATE,
    IN p_work_status BIT
)
BEGIN
    -- Kiểm tra phòng ban tồn tại
    IF NOT EXISTS (
        SELECT 1 FROM Department WHERE department_id = p_department_id
    ) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Phòng ban không tồn tại!';
    END IF;

    -- Kiểm tra trùng họ tên + ngày sinh
    IF EXISTS (
        SELECT 1 FROM Employees 
        WHERE full_name = p_full_name AND birthday = p_birthday
    ) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Nhân viên đã tồn tại (trùng tên và ngày sinh)!';
    END IF;

    -- Thêm nhân viên (ID sẽ được trigger tự sinh)
    INSERT INTO Employees (
        full_name, birthday, gender, department_id, position, hire_date, work_status
    )
    VALUES (
        p_full_name, p_birthday, p_gender, p_department_id, p_position, p_hire_date, p_work_status
    );
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_CheckInNow` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_CheckInNow`(
    IN p_attendance_id VARCHAR(20)
)
BEGIN
    -- Kiểm tra dòng tồn tại
    IF NOT EXISTS (
        SELECT 1 FROM Attendance WHERE attendance_id = p_attendance_id
    ) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'attendance_id không tồn tại!';
    END IF;

    -- Cập nhật check-in là thời gian hiện tại và trạng thái là 1 (đã check in)
    UPDATE Attendance
    SET 
        check_in_time = NOW(),
        status_atd = 1
    WHERE attendance_id = p_attendance_id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_CheckOutNow` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_CheckOutNow`(
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
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_DeleteDepartment` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_DeleteDepartment`(
    IN p_department_id VARCHAR(10)
)
BEGIN
    -- Kiểm tra mã phòng ban tồn tại
    IF NOT EXISTS (
        SELECT 1 FROM Department WHERE department_id = p_department_id
    ) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Phòng ban không tồn tại!';
    END IF;
    
    -- Xóa phòng ban
    DELETE FROM Department
    WHERE department_id = p_department_id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_DeleteEmployee` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_DeleteEmployee`(
    IN p_employee_id VARCHAR(20)
)
BEGIN
    -- Kiểm tra tồn tại
    IF NOT EXISTS (
        SELECT 1 FROM Employees WHERE employee_id = p_employee_id
    ) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Mã nhân viên không tồn tại!';
    END IF;

    -- Xóa nhân viên
    DELETE FROM Employees WHERE employee_id = p_employee_id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_DeleteUser` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_DeleteUser`(
    IN p_employee_id VARCHAR(20),
    IN p_user_name VARCHAR(50)
)
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM Users 
        WHERE employee_id = p_employee_id AND user_name = p_user_name
    ) THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Không tìm thấy user để xóa!';
    ELSE
        DELETE FROM Users 
        WHERE employee_id = p_employee_id AND user_name = p_user_name;
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_InsertUser` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_InsertUser`(
    IN p_employee_id VARCHAR(20),
    IN p_user_name VARCHAR(50),
    IN p_password VARCHAR(255),
    IN p_role VARCHAR(10)
)
BEGIN
    -- Kiểm tra tồn tại (theo cả khóa chính)
    IF EXISTS (
        SELECT 1 FROM Users 
        WHERE employee_id = p_employee_id AND user_name = p_user_name
    ) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'User đã tồn tại!';
    ELSE
        INSERT INTO Users (employee_id, user_name, password, role)
        VALUES (p_employee_id, p_user_name, p_password, p_role);
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_UpdateDepartment` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_UpdateDepartment`(
    IN p_department_id VARCHAR(10),
    IN p_department_name VARCHAR(100)
)
BEGIN
    -- Kiểm tra mã phòng ban tồn tại
    IF NOT EXISTS (
        SELECT 1 FROM Department WHERE department_id = p_department_id
    ) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Phòng ban không tồn tại!';
    END IF;
    
    -- Cập nhật thông tin phòng ban
    UPDATE Department
    SET department_name = p_department_name
    WHERE department_id = p_department_id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_UpdateEmployee` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_UpdateEmployee`(
    IN p_employee_id VARCHAR(20),
    IN p_full_name VARCHAR(100),
    IN p_birthday DATE,
    IN p_gender CHAR(1),
    IN p_department_id VARCHAR(10),
    IN p_position VARCHAR(50),
    IN p_hire_date DATE,
    IN p_work_status BIT
)
BEGIN
    -- Kiểm tra nhân viên tồn tại
    IF NOT EXISTS (
        SELECT 1 FROM Employees WHERE employee_id = p_employee_id
    ) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Mã nhân viên không tồn tại!';
    END IF;

    -- Cập nhật thông tin
    UPDATE Employees
    SET full_name = p_full_name,
        birthday = p_birthday,
        gender = p_gender,
        department_id = p_department_id,
        position = p_position,
        hire_date = p_hire_date,
        work_status = p_work_status
    WHERE employee_id = p_employee_id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_UpdateUser` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_UpdateUser`(
    IN p_employee_id VARCHAR(20),
    IN p_user_name VARCHAR(50),
    IN p_password VARCHAR(255),
    IN p_role VARCHAR(10)
)
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM Users 
        WHERE employee_id = p_employee_id AND user_name = p_user_name
    ) THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Không tìm thấy user để cập nhật!';
    ELSE
        UPDATE Users
        SET password = p_password,
            role = p_role
        WHERE employee_id = p_employee_id AND user_name = p_user_name;
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-26 13:17:06
