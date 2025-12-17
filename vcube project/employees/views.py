import base64
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee
from .forms import EmployeeForm

# List all employees
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employees/employee_list.html', {'employees': employees})

# Add a new employee
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            employee = form.save(commit=False)

            # ✅ Handle captured image from webcam
            captured_data = request.POST.get('captured_image')
            if captured_data:
                format, imgstr = captured_data.split(';base64,')
                ext = format.split('/')[-1]
                employee.face_image = ContentFile(
                    base64.b64decode(imgstr),
                    name=f"employee_{employee.name}.{ext}"
                )

            employee.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'employees/employee_create.html', {'form': form})

# Edit an existing employee
def employee_edit(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            employee = form.save(commit=False)

            # ✅ Handle new captured image if provided
            captured_data = request.POST.get('captured_image')
            if captured_data:
                format, imgstr = captured_data.split(';base64,')
                ext = format.split('/')[-1]
                employee.face_image = ContentFile(
                    base64.b64decode(imgstr),
                    name=f"employee_{employee.name}.{ext}"
                )

            employee.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employees/employee_create.html', {'form': form, 'edit': True})

# Delete an employee
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    employee.delete()
    return redirect('employee_list')
