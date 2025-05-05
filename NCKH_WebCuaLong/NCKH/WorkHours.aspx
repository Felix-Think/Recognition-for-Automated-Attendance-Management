<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="WorkHours.aspx.cs" Inherits="NCKH.WorkHours" %>

<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
    <title>Working Hours Details</title>
    <link rel="stylesheet" href="CSS/StyleUser .css" />
    <style>
        body {
            background-color: #f1f1f1;
            font-family: Arial, sans-serif;
        }

        .card {
            max-width: 800px;
            margin: 40px auto;
            background-color: #fff;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        }

        h1 {
            text-align: center;
            font-size: 2em;
            margin-bottom: 20px;
            color: #333;
        }

        .total-hours {
            margin-top: 20px; 
            margin-bottom: 10px; 
            font-weight: bold;
            font-size: 1.2em;
            text-align: right;
            color: #666;
        }

        .work-hours-table {
            width: 100%;
            border-collapse: collapse;
            table-layout: fixed;
            margin-top: 10px;
        }

        .work-hours-table th,
        .work-hours-table td {
            padding: 10px;
            text-align: center;
            border-bottom: 1px solid #ccc;
            width: 25%;
            word-wrap: break-word;
        }

        .work-hours-table th {
            font-weight: bold;
            color: #000;
        }

        .card-header {
            background-color: #f2f2f2;
            padding: 10px;
            border-bottom: 1px solid #ccc;
        }

        .card-body {
            padding: 20px;
        }
    </style>
</head>

<body>
    <form id="form1" runat="server">
        <div class="card">
            <div class="card-header">
                <h1>Working Hours Details</h1>
            </div>

            <div class="card-body">
                <asp:Label ID="lblEmployeeName" runat="server" CssClass="total-hours" />
                <asp:Label ID="lblSummary" runat="server" CssClass="total-hours" />


                <table class="work-hours-table">
                    <thead>
                        <tr>
                            <th>Work Date</th>
                            <th>Check-in Time</th>
                            <th>Check-out Time</th>
                            <th>Hours Worked</th>
                        </tr>
                    </thead>
                    <tbody id="workHoursTable" runat="server">
                    </tbody>
                </table>
            </div>
        </div>
    </form>
</body>
</html>
