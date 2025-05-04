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
                     <!-- Search + Add/Edit -->
                     <div class="form-actions">
                        <asp:TextBox ID="txtSearchEmp" runat="server" CssClass="input" placeholder="Search by Name"></asp:TextBox>
                        <asp:Button ID="btnSearchEmp" runat="server" Text="Search" CssClass="button" OnClick="btnSearchEmp_Click" />
                     </div>
                     <!-- GridView -->
                     <asp:GridView ID="employeesTable" runat="server" CssClass="table table-striped tr" AutoGenerateColumns="False" 
                        DataKeyNames="employee_id"
                        OnRowEditing="employeesTable_RowEditing"
                        OnRowUpdating="employeesTable_RowUpdating"
                        OnRowCancelingEdit="employeesTable_RowCancelingEdit"
                        OnRowDataBound="employeesTable_RowDataBound"
                        OnRowDeleting="employeesTable_RowDeleting">

                        <Columns>
                           <asp:BoundField DataField="employee_id" HeaderText="ID" ReadOnly="True" />
                           <asp:TemplateField HeaderText="Full Name">
                              <ItemTemplate>
                                 <%# Eval("full_name") %>
                              </ItemTemplate>
                              <EditItemTemplate>
                                 <asp:TextBox ID="txtEditFullName" runat="server" Text='<%# Bind("full_name") %>' CssClass="input" />
                              </EditItemTemplate>
                           </asp:TemplateField>
                           <asp:BoundField DataField="birthday" HeaderText="Birthday" DataFormatString="{0:dd/MM/yyyy}"/>
                           <asp:TemplateField HeaderText="Gender">
                              <ItemTemplate>
                                 <%# Eval("gender") %>
                              </ItemTemplate>
                              <EditItemTemplate>
                                 <asp:DropDownList ID="ddlEditGender" runat="server" CssClass="input">
                                    <asp:ListItem Text="Male" Value="Male" />
                                    <asp:ListItem Text="Female" Value="Female" />
                                    <asp:ListItem Text="Other" Value="Other" />
                                 </asp:DropDownList>
                              </EditItemTemplate>
                           </asp:TemplateField>
                           <asp:TemplateField HeaderText="Department">
                              <ItemTemplate>
                                 <%# Eval("department_name") %>
                              </ItemTemplate>
                              <EditItemTemplate>
                                 <asp:DropDownList ID="ddlEditDept" runat="server" CssClass="input" />
                              </EditItemTemplate>
                           </asp:TemplateField>
                           <asp:TemplateField HeaderText="Position">
                              <ItemTemplate>
                                 <%# Eval("position") %>
                              </ItemTemplate>
                              <EditItemTemplate>
                                 <asp:TextBox ID="txtEditPosition" runat="server" Text='<%# Bind("position") %>' CssClass="input" />
                              </EditItemTemplate>
                           </asp:TemplateField>
                           <asp:BoundField DataField="hire_date" HeaderText="Hire Date" DataFormatString="{0:dd/MM/yyyy}" ReadOnly ="True" />
                           <asp:TemplateField HeaderText="Status">
                              <ItemTemplate>
                                 <span class='<%# Convert.ToBoolean(Eval("work_status")) ? "badge success" : "badge destructive" %>'>
                                 <%# Convert.ToBoolean(Eval("work_status")) ? "present" : "absent" %>
                                 </span>
                              </ItemTemplate>
                           </asp:TemplateField>
                           <asp:CommandField ShowEditButton="True" ShowDeleteButton="True"/>
                        </Columns>
                     </asp:GridView>
                  </div>
                  <!-- Attendance Table -->
                  <div class="card tab-content" id="attendance" style="display:none;">
                     <div class="card-header">
                        <div class="card-title">Attendance</div>
                        <div class="card-description">View employee attendance records</div>
                     </div>
                     <!-- Search + Add/Edit -->
                     <div class="form-actions">
                        <asp:TextBox ID="txtSearchAtd" runat="server" CssClass="input" placeholder="Search by Employee ID"></asp:TextBox>
                        <asp:Button ID="btnSearchAtd" runat="server" Text="Search" CssClass="button" OnClick="btnSearchAtd_Click" />
                     </div>
                     <!-- GridView -->
                     <asp:GridView ID="attendanceTable" runat="server" CssClass="table table-striped" AutoGenerateColumns="false">
                        <Columns>
                           <asp:BoundField DataField="attendance_id" HeaderText="ID" />
                           <asp:BoundField DataField="employee_id" HeaderText="Employee ID" />
                           <asp:BoundField DataField="work_date" HeaderText="Date" DataFormatString="{0:yyyy-MM-dd}" />
                           <asp:BoundField DataField="check_in_time" HeaderText="Check-in" />
                           <asp:BoundField DataField="check_out_time" HeaderText="Check-out" />
                           <asp:BoundField DataField="hours_worked" HeaderText="Hours" />
                           <asp:TemplateField HeaderText="Status ">
                              <ItemTemplate>
                                 <span class='<%# Convert.ToBoolean(Eval("status_atd")) ? "badge success" : "badge destructive" %>'>
                                 <%# Convert.ToBoolean(Eval("status_atd" + "" + "" + "")) ? "present" : "absent" %>
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
                     <div class="form-actions">
                        <asp:TextBox ID="txtSearchDept" runat="server" CssClass="input" placeholder="Search by Department Name"></asp:TextBox>
                        <asp:Button ID="btnSearchDept" runat="server" Text="Search" CssClass="button" OnClick="btnSearchDept_Click" />
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
                 window.location.hash = tabId; // Cập nhật hash URL
             }

             // Đọc hash URL khi tải trang
             window.onload = function () {
                 if (window.location.hash) {
                     var tabId = window.location.hash.substring(1);
                     if (document.getElementById(tabId)) {
                         showTab(tabId);
                     }
                 }
             };
         </script>
      </form>
   </body>
</html>