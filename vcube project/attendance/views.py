from django.shortcuts import render
from .models import Attendance

# View to display all attendance records
def attendance_mark(request):
    # Get all attendance records, newest first
    records = Attendance.objects.all().order_by('-date', '-time')
    
    return render(request, 'attendance/attendance_mark.html', {'records': records})
