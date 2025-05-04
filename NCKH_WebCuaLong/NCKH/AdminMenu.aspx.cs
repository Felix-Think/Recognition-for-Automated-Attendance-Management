using MySql.Data.MySqlClient;
using System;
using System.Configuration;
using System.Data;
using System.Data.SqlClient;
using System.Linq;
using System.Web.UI;
using System.Web.UI.WebControls;

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
                ViewState["CurrentTab"] = "employees"; // Mặc định hiển thị Employees
            }
        }

        // Hàm tải dữ liệu nhân viên từ MySQL
        private void LoadEmployees()
        {
            using (MySqlConnection conn = new MySqlConnection(connectionString))
            {
                conn.Open();
                string query = @"
                    SELECT e.employee_id, e.full_name, e.birthday, e.gender, 
                           e.department_id, d.department_name, e.position, 
                           e.hire_date, e.work_status 
                    FROM Employees e
                    JOIN Department d ON e.department_id = d.department_id";

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
                string query = @"
                    SELECT attendance_id, employee_id, work_date, 
                           check_in_time, check_out_time, hours_worked, 
                           status_atd 
                    FROM Attendance";

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

        private void SearchEmployees()
        {
            string searchText = txtSearchEmp.Text.Trim();
            using (MySqlConnection conn = new MySqlConnection(connectionString))
            {
                string query = @"
            SELECT e.employee_id, e.full_name, e.birthday, e.gender, 
                   e.department_id, d.department_name, e.position, 
                   e.hire_date, e.work_status 
            FROM Employees e
            JOIN Department d ON e.department_id = d.department_id
            WHERE e.full_name LIKE @search";

                MySqlDataAdapter da = new MySqlDataAdapter(query, conn);
                da.SelectCommand.Parameters.AddWithValue("@search", "%" + searchText + "%");
                DataTable dt = new DataTable();
                da.Fill(dt);
                employeesTable.DataSource = dt;
                employeesTable.DataBind();
            }
        }


        private void SearchAttendance()
        {
            string searchText = txtSearchAtd.Text.Trim();
            using (MySqlConnection conn = new MySqlConnection(connectionString))
            {
                string query = "SELECT * FROM Attendance WHERE employee_id LIKE @search";
                MySqlDataAdapter da = new MySqlDataAdapter(query, conn);
                da.SelectCommand.Parameters.AddWithValue("@search", "%" + searchText + "%");
                DataTable dt = new DataTable();
                da.Fill(dt);
                attendanceTable.DataSource = dt;
                attendanceTable.DataBind();
            }
        }

        private void SearchDepartments()
        {
            string searchText = txtSearchDept.Text.Trim();
            using (MySqlConnection conn = new MySqlConnection(connectionString))
            {
                string query = "SELECT * FROM Department WHERE department_name LIKE @search";
                MySqlDataAdapter da = new MySqlDataAdapter(query, conn);
                da.SelectCommand.Parameters.AddWithValue("@search", "%" + searchText + "%");
                DataTable dt = new DataTable();
                da.Fill(dt);
                departmentTable.DataSource = dt;
                departmentTable.DataBind();
            }
        }
        //Search button
        protected void btnSearchEmp_Click(object sender, EventArgs e)
        {
            SearchEmployees();
            ViewState["CurrentTab"] = "employees";
            ScriptManager.RegisterStartupScript(this, GetType(), "showTab", $"showTab('employees');", true);
        }

        protected void btnSearchAtd_Click(object sender, EventArgs e)
        {
            SearchAttendance();
            ViewState["CurrentTab"] = "attendance";
            ScriptManager.RegisterStartupScript(this, GetType(), "showTab", $"showTab('attendance');", true);
        }

        protected void btnSearchDept_Click(object sender, EventArgs e)
        {
            SearchDepartments();
            ViewState["CurrentTab"] = "department";
            ScriptManager.RegisterStartupScript(this, GetType(), "showTab", $"showTab('department');", true);
        }
        //Edit button
        protected void employeesTable_RowEditing(object sender, GridViewEditEventArgs e)
        {
            employeesTable.EditIndex = e.NewEditIndex;
            LoadEmployees();
            ScriptManager.RegisterStartupScript(this, GetType(), "showTab", $"showTab('employees');", true);
        }

        protected void employeesTable_RowCancelingEdit(object sender, GridViewCancelEditEventArgs e)
        {
            employeesTable.EditIndex = -1;
            LoadEmployees();
            ScriptManager.RegisterStartupScript(this, GetType(), "showTab", $"showTab('employees');", true);
        }
        //updating
        protected void employeesTable_RowUpdating(object sender, GridViewUpdateEventArgs e)
        {
            GridViewRow row = employeesTable.Rows[e.RowIndex];
            string empID = employeesTable.DataKeys[e.RowIndex].Value.ToString();
            string name = ((TextBox)row.FindControl("txtEditFullName")).Text.Trim();
            string gender = ((DropDownList)row.FindControl("ddlEditGender")).SelectedValue;
            string departmentID = ((DropDownList)row.FindControl("ddlEditDept")).SelectedValue;
            string position = ((TextBox)row.FindControl("txtEditPosition")).Text.Trim();

            using (MySqlConnection conn = new MySqlConnection(connectionString))
            {
                string query = "UPDATE Employees SET full_name = @name, gender = @gender, department_id = @department, position = @position WHERE employee_id = @id";
                MySqlCommand cmd = new MySqlCommand(query, conn);
                cmd.Parameters.AddWithValue("@name", name);
                cmd.Parameters.AddWithValue("@gender", gender);
                cmd.Parameters.AddWithValue("@department", departmentID);
                cmd.Parameters.AddWithValue("@position", position);
                cmd.Parameters.AddWithValue("@id", empID);

                try
                {
                    conn.Open();
                    cmd.ExecuteNonQuery();
                }
                catch (MySqlException ex)
                {
                    Response.Write("Lỗi: " + ex.Message);
                }
                finally
                {
                    conn.Close();
                }
            }

            employeesTable.EditIndex = -1;
            LoadEmployees();
            ScriptManager.RegisterStartupScript(this, GetType(), "showTab", $"showTab('employees');", true);
        }
        protected void employeesTable_RowDataBound(object sender, GridViewRowEventArgs e)
        {
            if (e.Row.RowType == DataControlRowType.DataRow)
            {
                // Gán confirm cho nút Delete (LinkButton trong CommandField)
                foreach (Control control in e.Row.Cells[e.Row.Cells.Count - 1].Controls)
                {
                    if (control is LinkButton button && button.CommandName == "Delete")
                    {
                        button.OnClientClick = "return confirm('Are you sure you want to delete this employee?');";
                    }
                }

                // Nếu đang edit thì gán dữ liệu cho dropdown
                if (employeesTable.EditIndex == e.Row.RowIndex)
                {
                    DropDownList ddlDepartment = (DropDownList)e.Row.FindControl("ddlEditDept");
                    if (ddlDepartment != null)
                    {
                        using (MySqlConnection conn = new MySqlConnection(connectionString))
                        {
                            conn.Open();
                            string query = "SELECT department_id, department_name FROM Department";
                            MySqlCommand cmd = new MySqlCommand(query, conn);
                            MySqlDataReader reader = cmd.ExecuteReader();

                            ddlDepartment.DataSource = reader;
                            ddlDepartment.DataTextField = "department_name";
                            ddlDepartment.DataValueField = "department_id";
                            ddlDepartment.DataBind();
                            reader.Close();
                        }

                        string currentDeptId = DataBinder.Eval(e.Row.DataItem, "department_id").ToString();
                        ddlDepartment.SelectedValue = currentDeptId;
                    }
                }
            }
        }


        protected void employeesTable_RowDeleting(object sender, GridViewDeleteEventArgs e)
        {
            string empID = employeesTable.DataKeys[e.RowIndex].Value.ToString();

            string connectionString = "server=localhost;user id=root;password=1234;database=nckh;";

            using (MySqlConnection conn = new MySqlConnection(connectionString))
            {
                conn.Open();

                // 1. Xóa dữ liệu Attendance
                string deleteAttendance = "DELETE FROM Attendance WHERE employee_id = @employee_id";
                using (MySqlCommand cmd = new MySqlCommand(deleteAttendance, conn))
                {
                    cmd.Parameters.AddWithValue("@employee_id", empID);
                    cmd.ExecuteNonQuery();
                }

                // 2. Xóa tài khoản Users
                string deleteUsers = "DELETE FROM Users WHERE employee_id = @employee_id";
                using (MySqlCommand cmd = new MySqlCommand(deleteUsers, conn))
                {
                    cmd.Parameters.AddWithValue("@employee_id", empID);
                    cmd.ExecuteNonQuery();
                }

                // 3. Xóa nhân viên
                string deleteEmployee = "DELETE FROM Employees WHERE employee_id = @employee_id";
                using (MySqlCommand cmd = new MySqlCommand(deleteEmployee, conn))
                {
                    cmd.Parameters.AddWithValue("@employee_id", empID);
                    cmd.ExecuteNonQuery();
                }
            }

            LoadEmployees(); 
            LoadAttendance();
        }

        protected void btnGoSalary_Click(object sender, EventArgs e)
        {
            Response.Redirect("TinhLuong.aspx");
        }
    }
}
