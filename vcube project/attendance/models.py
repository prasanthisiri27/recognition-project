from django.db import models
from employees.models import Employee
from datetime import date

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    time = models.TimeField(auto_now_add=True)
    status = models.CharField(max_length=10, default='Present')

    def __str__(self):
        return f"{self.employee.name} - {self.date}"

