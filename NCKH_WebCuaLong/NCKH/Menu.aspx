<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="Menu.aspx.cs" Inherits="NCKH.Menu" %>

<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
    <title>Employee Profile</title>
    <link rel="stylesheet" href="CSS/StyleUser.css" />
</head>
<body>
    <form id="form1" runat="server">
        <div class="card">
            <h1>Employee Profile</h1>

            <div class="card-header">
                <h3>
                    <asp:Label ID="lblName" runat="server" Text=""></asp:Label>
                </h3>
                <span id="statusBadge" runat="server" class="badge">
                    <asp:Label ID="lblStatus" runat="server" Text=""></asp:Label>
                </span>
            </div>

            <div class="card-body">
                <div class="info-item">
                    <p class="info-label">Salary this Month</p>
                    <p class="info-value">
                        <asp:Label ID="lblSalary" runat="server" Text=""></asp:Label>
                        &nbsp;
                        <asp:Button ID="btnViewWorkHours" runat="server" Text="📅" CssClass="icon-button" PostBackUrl="~/WorkHours.aspx" />
                    </p>
                </div>
                <div class="info-item">
                    <p class="info-label">Gender</p>
                    <p class="info-value">
                        <asp:Label ID="lblGender" runat="server" Text=""></asp:Label>
                    </p>
                </div>

                <div class="info-item">
                    <p class="info-label">Birthday</p>
                    <p class="info-value">
                        <asp:Label ID="lblBirthday" runat="server" Text=""></asp:Label>
                    </p>
                </div>

                <div class="info-item">
                    <p class="info-label">Department</p>
                    <p class="info-value">
                        <asp:Label ID="lblDepartment" runat="server" Text=""></asp:Label>
                    </p>
                </div>

                <div class="info-item">
                    <p class="info-label">Position</p>
                    <p class="info-value">
                        <asp:Label ID="lblPosition" runat="server" Text=""></asp:Label>
                    </p>
                </div>

                <div class="info-item">
                    <p class="info-label">Hire Date</p>
                    <p class="info-value">
                        <asp:Label ID="lblHireDate" runat="server" Text=""></asp:Label>
                    </p>
                </div>
            </div>

            <div class="card-footer">
                <p>Employee ID:
                    <asp:Label ID="lblEmployeeID" runat="server" Text=""></asp:Label>
                </p>
            </div>
        </div>
    </form>
</body>
</html>
