using System;
using System.Configuration;
using System.Data;
using MySql.Data.MySqlClient;

namespace NCKH
{
    public class DataClass
    {
        private static MySqlConnection conn;

        // Mở kết nối database
        private static void OpenDB()
        {
            string conStr = ConfigurationManager.ConnectionStrings["ConnectionString"].ConnectionString;
            conn = new MySqlConnection(conStr);
            conn.Open();
        }

        // Đóng kết nối
        private static void CloseDB()
        {
            if (conn != null && conn.State == ConnectionState.Open)
                conn.Close();
        }

        // Trả về kết quả truy vấn (SELECT)
        public static MySqlDataReader GetRecord(string sql)
        {
            OpenDB();
            MySqlDataReader r = null;
            try
            {
                MySqlCommand cmd = new MySqlCommand(sql, conn)
                {
                    CommandType = CommandType.Text
                };
                r = cmd.ExecuteReader(CommandBehavior.CloseConnection); // tự đóng kết nối khi reader đóng
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
                CloseDB();
            }
            return r;
        }

        // Hàm thực thi INSERT, UPDATE, DELETE
        public static int ExecuteCommand(string sql)
        {
            int result = 0;
            try
            {
                OpenDB();
                MySqlCommand cmd = new MySqlCommand(sql, conn);
                result = cmd.ExecuteNonQuery();
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
            finally
            {
                CloseDB();
            }
            return result;
        }
    }
}
