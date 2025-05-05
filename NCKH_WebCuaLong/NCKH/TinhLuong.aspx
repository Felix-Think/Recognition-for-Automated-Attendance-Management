<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="TinhLuong.aspx.cs" Inherits="NCKH.TinhLuong" %>

<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
    <title>Employee Salary Details</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f9f9f9;
            color: #333;
        }
        h2 {
            color: #2c3e50;
        }
        form {
            max-width: 900px;
            margin: auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        label {
            font-weight: bold;
            margin-right: 10px;
        }
        select {
            padding: 5px;
            margin-right: 20px;
            border-radius: 4px;
            border: 1px solid #ccc;
            font-size: 1rem;
        }
        button {
            background-color: #2980b9;
            color: white;
            padding: 8px 16px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 1rem;
        }
        button:hover {
            background-color: #3498db;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            padding: 10px 8px;
            border: 1px solid #ddd;
            text-align: center;
            font-size: 0.9rem;
        }
        th {
            background-color: #2980b9;
            color: white;
        }
        @media (max-width: 600px) {
            table, thead, tbody, th, td, tr {
                display: block;
            }
            thead tr {
                display: none;
            }
            tr {
                margin-bottom: 1em;
                border-bottom: 2px solid #ddd;
            }
            td {
                text-align: right;
                padding-left: 50%;
                position: relative;
            }
            td::before {
                content: attr(data-label);
                position: absolute;
                left: 0;
                width: 50%;
                padding-left: 15px;
                font-weight: bold;
                text-align: left;
            }
        }
    </style>
</head>
<body>
    <form id="form1" runat="server">
        <h2>Employee Salary Details</h2>
        <div>
            <label for="ddlMonth">Select Month:</label>
            <asp:DropDownList ID="ddlMonth" runat="server" AutoPostBack="false"></asp:DropDownList>

            <label for="ddlYear">Select Years:</label>
            <asp:DropDownList ID="ddlYear" runat="server" AutoPostBack="false"></asp:DropDownList>

            <asp:Button ID="btnLoad" runat="server" Text="View Salary" OnClick="btnLoad_Click" />
        </div>

        <asp:GridView ID="GridView1" runat="server" AutoGenerateColumns="false" GridLines="None" AlternatingRowStyle-BackColor="#f2f2f2" Width="100%">
            <Columns>
                <asp:BoundField DataField="employee_id" HeaderText="Employee ID" ItemStyle-Width="10%" />
                <asp:BoundField DataField="full_name" HeaderText="Employee Name" ItemStyle-Width="20%" />
                <asp:BoundField DataField="total_hours" HeaderText="Total Hours Worked" DataFormatString="{0:N2}" ItemStyle-Width="10%" />
                <asp:BoundField DataField="overtime_hours" HeaderText="Overtime Hours" DataFormatString="{0:N2}" ItemStyle-Width="10%" />
                <asp:BoundField DataField="hourly_wage" HeaderText="Hourly Wage (VND)" DataFormatString="{0:N0}" ItemStyle-Width="10%" />
                <asp:BoundField DataField="salary_coefficient" HeaderText="Salary Coefficient" DataFormatString="{0:N2}" ItemStyle-Width="10%" />
                <asp:BoundField DataField="total_salary" HeaderText="Total Salary (VND)" DataFormatString="{0:N0}" ItemStyle-Width="15%" />
            </Columns>
        </asp:GridView>
    </form>
</body>
</html>