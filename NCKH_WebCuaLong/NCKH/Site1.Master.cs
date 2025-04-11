using System;
using System.Web;
using System.Web.UI;
using MySql.Data.MySqlClient;

namespace NCKH
{
    public partial class Site1 : System.Web.UI.MasterPage
    {
        protected void Page_Load(object sender, EventArgs e) { }

        protected void btnLogin_Click(object sender, EventArgs e)
        {
            string username = txtUsername.Text.Trim();
            string password = txtPassword.Text.Trim();

            string sql = "SELECT password, role FROM Users WHERE user_name = @username";

            MySqlDataReader myDr = null;

            try
            {
                string conStr = System.Configuration.ConfigurationManager.ConnectionStrings["ConnectionString"].ConnectionString;
                using (MySqlConnection conn = new MySqlConnection(conStr))
                {
                    conn.Open();
                    MySqlCommand cmd = new MySqlCommand(sql, conn);
                    cmd.Parameters.AddWithValue("@username", username);
                    myDr = cmd.ExecuteReader();

                    if (myDr.HasRows)
                    {
                        myDr.Read();
                        string storedPassword = myDr.GetString("password");
                        string role = myDr.GetString("role");

                        if (storedPassword == password)
                        {
                            Session["username"] = username; // ✅ Gán session tại đây
                            Session["role"] = role;

                            if (role == "user")
                                Response.Redirect("Menu.aspx");
                            else if (role == "admin")
                                Response.Redirect("AdminMenu.aspx");
                            else
                                ShowAlert("Không có quyền truy cập");
                        }
                        else
                        {
                            ShowAlert("Sai tài khoản hoặc mật khẩu");
                        }
                    }
                    else
                    {
                        ShowAlert("Sai tài khoản hoặc mật khẩu");
                    }
                }
            }
            catch (Exception ex)
            {
                ShowAlert("Lỗi: " + ex.Message);
            }
            finally
            {
                if (myDr != null && !myDr.IsClosed)
                    myDr.Close();
            }
        }

        private void ShowAlert(string message)
        {
            ScriptManager.RegisterClientScriptBlock(this, this.GetType(),
                "alertMessage", $"alert('{message}')", true);
        }
    }
}
