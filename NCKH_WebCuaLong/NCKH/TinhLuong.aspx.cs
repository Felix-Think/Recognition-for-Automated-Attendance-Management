using System;
using System.Data;
using MySql.Data.MySqlClient;
using System.Configuration;
using System.Web.UI.WebControls;

namespace NCKH
{
    public partial class TinhLuong : System.Web.UI.Page
    {
        // Define base hourly wage and salary coefficient (these could be configurable)
        const decimal BaseHourlyWage = 100000; // example 100,000 VND per hour
        const decimal SalaryCoefficient = 1.5m; // example multiplier

        protected void Page_Load(object sender, EventArgs e)
        {
            if (!IsPostBack)
            {
                // Load months and years for dropdowns
                LoadMonths();
                LoadYears();
                // Load default data for current month/year
                ddlMonth.SelectedValue = DateTime.Now.Month.ToString();
                ddlYear.SelectedValue = DateTime.Now.Year.ToString();
                LoadEmployeeSalaries(DateTime.Now.Month, DateTime.Now.Year);
            }
        }

        private void LoadMonths()
        {
            ddlMonth.Items.Clear();
            for (int m = 1; m <= 12; m++)
            {
                ddlMonth.Items.Add(new System.Web.UI.WebControls.ListItem(m.ToString(), m.ToString()));
            }
        }

        private void LoadYears()
        {
            ddlYear.Items.Clear();
            int currentYear = DateTime.Now.Year;
            for (int y = currentYear - 5; y <= currentYear; y++)
            {
                ddlYear.Items.Add(new System.Web.UI.WebControls.ListItem(y.ToString(), y.ToString()));
            }
        }

        protected void btnLoad_Click(object sender, EventArgs e)
        {
            int month = int.Parse(ddlMonth.SelectedValue);
            int year = int.Parse(ddlYear.SelectedValue);
            LoadEmployeeSalaries(month, year);
        }

        private void LoadEmployeeSalaries(int month, int year)
        {
            string connectionString = ConfigurationManager.ConnectionStrings["ConnectionString"].ConnectionString;
            DataTable dt = new DataTable();

            using (MySqlConnection conn = new MySqlConnection(connectionString))
            {
                string sql = @"
            SELECT 
                e.employee_id,
                e.full_name,
                IFNULL(SUM(a.hours_worked), 0) AS total_hours,
                IFNULL(SUM(CASE WHEN a.hours_worked > 8 THEN a.hours_worked - 8 ELSE 0 END), 0) AS overtime_hours
            FROM employees e
            LEFT JOIN attendance a ON e.employee_id = a.employee_id 
                AND MONTH(a.work_date) = @month AND YEAR(a.work_date) = @year
            GROUP BY e.employee_id, e.full_name
            ORDER BY e.employee_id";

                MySqlCommand cmd = new MySqlCommand(sql, conn);
                cmd.Parameters.AddWithValue("@month", month);
                cmd.Parameters.AddWithValue("@year", year);

                MySqlDataAdapter da = new MySqlDataAdapter(cmd);
                da.Fill(dt);
            }

            // Tính toán thêm cột lương
            dt.Columns.Add("hourly_wage", typeof(decimal));
            dt.Columns.Add("salary_coefficient", typeof(decimal));
            dt.Columns.Add("total_salary", typeof(decimal));

            foreach (DataRow row in dt.Rows)
            {
                decimal totalHours = Convert.ToDecimal(row["total_hours"]);
                decimal overtimeHours = Convert.ToDecimal(row["overtime_hours"]);
                decimal hourlyWage = BaseHourlyWage;
                decimal salaryCoeff = SalaryCoefficient;

                decimal totalSalary = totalHours * hourlyWage * salaryCoeff;

                row["hourly_wage"] = hourlyWage;
                row["salary_coefficient"] = salaryCoeff;
                row["total_salary"] = totalSalary;
            }

            GridView1.DataSource = dt;
            GridView1.DataBind();
        }
    }
}
