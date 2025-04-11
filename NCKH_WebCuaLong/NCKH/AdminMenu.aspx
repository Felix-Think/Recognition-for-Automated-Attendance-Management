<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="AdminMenu.aspx.cs" Inherits="NCKH.AdminMenu" %>

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Employee Management System</title>
  <link rel="stylesheet" href="CSS/StyleAdmin.css" />
</head>
<body>
  <form id="form1" runat="server">
  <div class="container">
    <h1>Employee Management System</h1>
    <div class="grid">
      <div class="card">
        <div class="card-header">
          <div class="card-title">Database Tables</div>
          <div class="card-description">Select a table to view its data</div>
        </div>
        <div class="tabs-list">
          <button type="button" class="tab-button active" onclick="showTab('employees')">👤 Employees</button>
          <button type="button" class="tab-button" onclick="showTab('attendance')">🗘️ Attendance</button>
          <button type="button" class="tab-button" onclick="showTab('department')">🏢 Department</button>
        </div>
      </div>

      <div id="content">
        <!-- Employees Table -->
        <div class="card tab-content" id="employees">
          <div class="card-header">
            <div class="card-title">Employees</div>
            <div class="card-description">View and manage employee information</div>
          </div>
          <asp:GridView ID="employeesTable" runat="server" CssClass="table table-striped tr" AutoGenerateColumns="false">
            <Columns>
                <asp:BoundField DataField="employee_id" HeaderText="ID" />
                <asp:BoundField DataField="full_name" HeaderText="Full Name" />
                <asp:BoundField DataField="birthday" HeaderText="Birthday" DataFormatString="{0:MMM dd, yyyy}" />
                <asp:BoundField DataField="gender" HeaderText="Gender" />
                <asp:BoundField DataField="department_id" HeaderText="Department" />
                <asp:BoundField DataField="position" HeaderText="Position" />
                <asp:BoundField DataField="hire_date" HeaderText="Hire Date" DataFormatString="{0:MMM dd, yyyy}" />
                <asp:TemplateField HeaderText="Status">
                    <ItemTemplate>
                        <span class='<%# Eval("status").ToString() == "active" ? "badge success" : "badge destructive" %>'>
                            <%# Eval("status") %>
                        </span>
                    </ItemTemplate>
                </asp:TemplateField>
            </Columns>
          </asp:GridView>
          <asp:SqlDataSource ID="SqlDataSource1" runat="server"></asp:SqlDataSource>
        </div>

        <!-- Attendance Table -->
        <div class="card tab-content" id="attendance" style="display:none;">
          <div class="card-header">
            <div class="card-title">Attendance</div>
            <div class="card-description">View employee attendance records</div>
          </div>
          <asp:GridView ID="attendanceTable" runat="server" CssClass="table table-striped" AutoGenerateColumns="false">
            <Columns>
              <asp:BoundField DataField="attendance_id" HeaderText="ID" />
              <asp:BoundField DataField="work_date" HeaderText="Date" DataFormatString="{0:yyyy-MM-dd}" />
              <asp:BoundField DataField="check_in_time" HeaderText="Check-in" />
              <asp:BoundField DataField="check_out_time" HeaderText="Check-out" />
              <asp:BoundField DataField="status" HeaderText="Status" />
              <asp:BoundField DataField="hours_worked" HeaderText="Hours" />
              <asp:TemplateField HeaderText="Status">
                <ItemTemplate>
                    <span class='<%# Eval("status").ToString() == "present" ? "badge success" : Eval("status").ToString() == "absent" ? "badge destructive" : "badge outline" %>'>
                        <%# Eval("status") %>
                    </span>
                </ItemTemplate>
              </asp:TemplateField>
            </Columns>
          </asp:GridView>
        </div>

        <!-- Department Table -->
        <div class="card tab-content" id="department" style="display:none;">
          <div class="card-header">
            <div class="card-title">Department</div>
            <div class="card-description">View department information</div>
          </div>
          <asp:GridView ID="departmentTable" runat="server" CssClass="table table-striped" AutoGenerateColumns="false">
            <Columns>
              <asp:BoundField DataField="department_id" HeaderText="Department ID" />
              <asp:BoundField DataField="department_name" HeaderText="Department Name" />
            </Columns>
          </asp:GridView>
        </div>
      </div>
    </div>
  </div>

  <script>
      function showTab(tabId) {
          document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
          document.querySelectorAll('.tab-content').forEach(tab => tab.style.display = 'none');
          document.getElementById(tabId).style.display = 'block';
          event.target.classList.add('active');
      }
  </script>
</form>
</body>
</html>
