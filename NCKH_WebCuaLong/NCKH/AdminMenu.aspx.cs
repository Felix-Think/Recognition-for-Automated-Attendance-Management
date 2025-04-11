using MySql.Data.MySqlClient;
using System;
using System.Data;

namespace NCKH
{
    public partial class AdminMenu : System.Web.UI.Page
    {
        // Cấu hình kết nối MySQL
        private string connectionString = "server=localhost;user id=root;password=1234;database=nckh;";

        protected void Page_Load(object sender, EventArgs e)
        {
            if (!IsPostBack)
            {
                LoadEmployees();
                LoadAttendance();
                LoadDepartments();
            }
        }

        // Hàm tải dữ liệu nhân viên từ MySQL
        private void LoadEmployees()
        {
            using (MySqlConnection conn = new MySqlConnection(connectionString))
            {
                conn.Open();
                string query = "SELECT e.employee_id, e.full_name, e.birthday, e.gender, e.department_id, e.position, e.hire_date, e.status, d.department_name " +"FROM Employees e, Department d " + "WHERE e.department_id = d.department_id";

                MySqlDataAdapter adapter = new MySqlDataAdapter(query, conn);
                DataTable dt = new DataTable();
                adapter.Fill(dt);
                employeesTable.DataSource = dt;
                employeesTable.DataBind();
            }
        }

        // Hàm tải dữ liệu chấm công từ MySQL
        private void LoadAttendance()
        {
            using (MySqlConnection conn = new MySqlConnection(connectionString))
            {
                conn.Open();
                string query = "SELECT a.attendance_id, a.employee_id, a.work_date, a.check_in_time, a.check_out_time, a.hours_worked, a.status FROM Attendance a";
                MySqlDataAdapter adapter = new MySqlDataAdapter(query, conn);
                DataTable dt = new DataTable();
                adapter.Fill(dt);
                attendanceTable.DataSource = dt;
                attendanceTable.DataBind();
            }
        }

        // Hàm tải dữ liệu phòng ban từ MySQL
        private void LoadDepartments()
        {
            using (MySqlConnection conn = new MySqlConnection(connectionString))
            {
                conn.Open();
                string query = "SELECT department_id, department_name FROM Department";
                MySqlDataAdapter adapter = new MySqlDataAdapter(query, conn);
                DataTable dt = new DataTable();
                adapter.Fill(dt);
                departmentTable.DataSource = dt;
                departmentTable.DataBind();
            }
        }
    }
}
