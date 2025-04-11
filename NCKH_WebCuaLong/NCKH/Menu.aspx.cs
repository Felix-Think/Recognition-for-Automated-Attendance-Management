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
                lblName.Text = "No username in session";
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
                        e.status
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
                                lblBirthday.Text = birthday.ToString("MMMM dd, yyyy");
                            }

                            if (reader["gender"] != DBNull.Value)
                            {
                                bool gender = Convert.ToBoolean(reader["gender"]);
                                lblGender.Text = gender ? "Male" : "Female";
                            }

                            lblDepartment.Text = reader["department_name"].ToString();
                            lblPosition.Text = reader["position"].ToString();

                            if (reader["hire_date"] != DBNull.Value)
                            {
                                DateTime hireDate = Convert.ToDateTime(reader["hire_date"]);
                                lblHireDate.Text = hireDate.ToString("MMMM dd, yyyy");
                            }

                            string status = reader["status"].ToString();
                            lblStatus.Text = status;
                            statusBadge.Attributes["class"] = status.ToLower() == "active" ? "badge" : "badge inactive";
                        }
                    }
                }
            }
        }
    }
}
