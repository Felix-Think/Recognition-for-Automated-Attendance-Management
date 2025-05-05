using System;
using MySql.Data.MySqlClient;
using System.Web.UI;

namespace NCKH
{
    public partial class WorkHours : System.Web.UI.Page
    {
        private string connectionString = "server=localhost;user id=root;password=1234;database=nckh;";

        protected void Page_Load(object sender, EventArgs e)
        {
            if (!IsPostBack)
            {
                LoadWorkHours();
            }
        }

        private void LoadWorkHours()
        {
            string username = Session["username"] as string;

            if (string.IsNullOrEmpty(username))
            {
                lblEmployeeName.Text = "Account not found.";
                return;
            }

            using (MySqlConnection conn = new MySqlConnection(connectionString))
            {
                conn.Open();

                string employeeId = GetEmployeeId(conn, username);
                if (string.IsNullOrEmpty(employeeId))
                {
                    lblEmployeeName.Text = "Employee not found.";
                    return;
                }

                string fullName = GetEmployeeFullName(conn, employeeId);
                lblEmployeeName.Text = fullName + "<br/>"; // Thêm <br/> để xuống dòng

                workHoursTable.InnerHtml = ""; // Reset table

                string query = @"
            SELECT work_date, check_in_time, check_out_time, hours_worked 
            FROM Attendance 
            WHERE employee_id = @employeeId 
                AND MONTH(work_date) = MONTH(CURRENT_DATE())
                AND YEAR(work_date) = YEAR(CURRENT_DATE())
            ORDER BY work_date";

                using (MySqlCommand cmd = new MySqlCommand(query, conn))
                {
                    cmd.Parameters.AddWithValue("@employeeId", employeeId);

                    using (MySqlDataReader reader = cmd.ExecuteReader())
                    {
                        double totalHours = 0;
                        int workDays = 0;

                        while (reader.Read())
                        {
                            string workDate = Convert.ToDateTime(reader["work_date"]).ToString("dd/MM/yyyy");
                            string checkIn = reader["check_in_time"] != DBNull.Value
                                ? Convert.ToDateTime(reader["check_in_time"]).ToString("HH:mm")
                                : "N/A";
                            string checkOut = reader["check_out_time"] != DBNull.Value
                                ? Convert.ToDateTime(reader["check_out_time"]).ToString("HH:mm")
                                : "N/A";
                            double hoursWorked = reader["hours_worked"] != DBNull.Value
                                ? Convert.ToDouble(reader["hours_worked"])
                                : 0;

                            if (hoursWorked > 0)
                                workDays++;

                            totalHours += hoursWorked;

                            workHoursTable.InnerHtml += $"<tr><td>{workDate}</td><td>{checkIn}</td><td>{checkOut}</td><td>{hoursWorked}</td></tr>";
                        }

                        lblSummary.Text = $"Days Worked: {workDays} days<br/>Total Hours Worked: {totalHours} hours";
                    }
                }
            }
        }

        private string GetEmployeeFullName(MySqlConnection conn, string employeeId)
        {
            string query = "SELECT full_name FROM Employees WHERE employee_id = @employeeId";
            using (MySqlCommand cmd = new MySqlCommand(query, conn))
            {
                cmd.Parameters.AddWithValue("@employeeId", employeeId);
                object result = cmd.ExecuteScalar();
                return result != null ? result.ToString() : "Unknown";
            }
        }

        private string GetEmployeeId(MySqlConnection conn, string username)
        {
            string query = "SELECT employee_id FROM Users WHERE user_name = @username";
            using (MySqlCommand cmd = new MySqlCommand(query, conn))
            {
                cmd.Parameters.AddWithValue("@username", username);
                return cmd.ExecuteScalar() as string;
            }
        }
    }
}
