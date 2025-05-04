using System;
using MySql.Data.MySqlClient;
using System.Web.UI;

namespace NCKH
{
    public partial class Menu : System.Web.UI.Page
    {
        private string connectionString = "server=localhost;user id=root;password=1234;database=nckh;";

        protected void Page_Load(object sender, EventArgs e)
        {
            if (!IsPostBack)
            {
                LoadEmployeeProfile();
            }
        }

        private void LoadEmployeeProfile()
        {
            string username = Session["username"] as string;

            if (string.IsNullOrEmpty(username))
            {
                lblName.Text = "Không tìm thấy tài khoản.";
                return;
            }

            using (MySqlConnection conn = new MySqlConnection(connectionString))
            {
                conn.Open();

                string query = @"
                    SELECT 
                        e.employee_id,
                        e.full_name,
                        e.birthday,
                        e.gender,
                        d.department_name,
                        e.position,
                        e.hire_date,
                        e.work_status
                    FROM Users u
                    JOIN Employees e ON u.employee_id = e.employee_id
                    LEFT JOIN Department d ON e.department_id = d.department_id
                    WHERE u.user_name = @username
                ";

                using (MySqlCommand cmd = new MySqlCommand(query, conn))
                {
                    cmd.Parameters.AddWithValue("@username", username);

                    using (MySqlDataReader reader = cmd.ExecuteReader())
                    {
                        if (reader.Read())
                        {
                            lblEmployeeID.Text = reader["employee_id"].ToString();
                            lblName.Text = reader["full_name"].ToString();

                            if (reader["birthday"] != DBNull.Value)
                            {
                                DateTime birthday = Convert.ToDateTime(reader["birthday"]);
                                lblBirthday.Text = birthday.ToString("dd/MM/yyyy");
                            }

                            string gender = reader["gender"].ToString();
                            switch (gender)
                            {
                                case "M":
                                    lblGender.Text = "Nam";
                                    break;
                                case "F":
                                    lblGender.Text = "Nữ";
                                    break;
                                default:
                                    lblGender.Text = "Khác";
                                    break;
                            }

                            lblDepartment.Text = reader["department_name"].ToString();
                            lblPosition.Text = reader["position"].ToString();

                            if (reader["hire_date"] != DBNull.Value)
                            {
                                DateTime hireDate = Convert.ToDateTime(reader["hire_date"]);
                                lblHireDate.Text = hireDate.ToString("dd/MM/yyyy");
                            }

                            bool workStatus = Convert.ToBoolean(reader["work_status"]);
                            lblStatus.Text = workStatus ? "Đang làm" : "Đã nghỉ";
                            statusBadge.Attributes["class"] = workStatus ? "badge active" : "badge inactive";

                            // Tải lương tháng hiện tại
                            LoadMonthlySalary(reader["employee_id"].ToString());
                        }
                        else
                        {
                            lblName.Text = "Không tìm thấy thông tin nhân viên.";
                        }
                    }
                }
            }
        }

        private void LoadMonthlySalary(string employeeId)
        {
            using (MySqlConnection conn = new MySqlConnection(connectionString))
            {
                conn.Open();
                using (MySqlCommand cmd = new MySqlCommand("Get_Employee_Monthly_Info", conn))
                {
                    cmd.CommandType = System.Data.CommandType.StoredProcedure;

                    cmd.Parameters.AddWithValue("@p_thang", DateTime.Now.Month);
                    cmd.Parameters.AddWithValue("@p_nam", DateTime.Now.Year);
                    cmd.Parameters.AddWithValue("@p_employee_id", employeeId);

                    using (MySqlDataReader reader = cmd.ExecuteReader())
                    {
                        while (reader.Read())
                        {
                            string info = reader["Thông tin"].ToString();
                            string value = reader["Giá trị"].ToString();

                            if (info == "Thực nhận")
                            {
                                lblSalary.Text = string.IsNullOrEmpty(value) ? "0 VNĐ" : value + " VNĐ";
                                break;
                            }
                        }
                    }
                }
            }
        }
    }
}
