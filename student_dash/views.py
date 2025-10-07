from django.contrib import  messages
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect,get_object_or_404
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User
from base.decorators import student_login_required
from django.contrib.auth.hashers import make_password, check_password
from base.models import Student, Component
from student_dash.models import StudentIssueLog
from django.utils.timezone import now
from django.views.decorators.http import require_POST
from collections import defaultdict
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

@student_login_required
def inventory_request(request):
    return render(request, 'student_dash/inventory_request_view.html')
 
@student_login_required
def components(request):
    categories = dict(Component.CATEGORY_CHOICES)
    return render(request, 'student_dash/inventory_request_view.html', {'categories': categories})


@student_login_required
def category_items(request, category_key):
    components = Component.objects.filter(category=category_key)
    category_name = dict(Component.CATEGORY_CHOICES).get(category_key, "Unknown")
    return render(request, 'student_dash/category_items.html', {
        'components': components,
        'category_name': category_name,
    })


@student_login_required
def submit_request(request):
    if request.method == 'POST':
        component_ids = request.POST.getlist('component_ids[]')
        quantities = request.POST.getlist('quantities[]')

        if len(component_ids) != len(quantities):
            return HttpResponseBadRequest("Mismatched data")

        student = request.student
        # print(type(student))
        # print(student.full_name,student.roll_number)

        for comp_id, qty in zip(component_ids, quantities):
            try:
                component = Component.objects.get(id=comp_id)
            except Component.DoesNotExist:
                continue

            StudentIssueLog.objects.create(
                student=student,
                # studentid = student,
                component=component,
                quantity_issued=int(qty),
                form_date = now().date(),
                status_from_teacher='Pending',
                status_from_student='Requested',  # or leave default
            )

        response = redirect('dash:components')
        response.set_cookie('clearLocalStorage', 'true')  # instruct frontend to clear
        return response


#by vaibhav malav
def admindashboard(request):
    requests_distinct = (StudentIssueLog.objects.filter(status_from_student = "Requested").values(
        'student__full_name','student__roll_number','form_date','component__name',
        'component__category','component__quantity',
        'quantity_issued').order_by('component__category','-form_date'))
                         # .distinct())
    # print(requests_distinct)
    # if request.method == 'POST':
    # return render(request, 'teacher_dash/teacher_dashboard.html',
    #                   {'requests_distinct':requests_distinct})
    # return HttpResponse("not a post emthi from admin")

    # Step 2: Group by category
    grouped_requests = defaultdict(list)

    for req in requests_distinct:
        grouped_requests[req['component__category']].append(req)

    # print(grouped_requests.items())

    return render(request, 'teacher_dash/teacher_dashboard.html', {
        'grouped_requests': dict(grouped_requests)})

@require_POST
@require_POST
def update_status(request):
    roll_number = request.POST.get("roll_number")
    form_date = request.POST.get("form_date")
    component_name = request.POST.get("component_name")
    action = request.POST.get("action")
    # print("data is:", form_date, action, component_name, roll_number)

    # Get all matching requests (avoids MultipleObjectsReturned error)
    logs = StudentIssueLog.objects.filter(
        student__roll_number=roll_number,
        component__name=component_name,
        form_date=form_date
    )

    if not logs.exists():
        return HttpResponse("Log not found", status=404)

    for log in logs:
        if action == "approve":
            log.status_from_teacher = "Approved"
            log.status_from_student = "Issued"
            log.issue_date = now().date()

            # Deduct from stock
            component = log.component
            if component.quantity >= log.quantity_issued:
                component.quantity -= log.quantity_issued
                component.save()
            else:
                return HttpResponse(
                    f"Not enough quantity available for {component.name}",
                    status=400
                )

        elif action == "reject":
            log.status_from_teacher = "Rejected"
            log.status_from_student = "Rejectedbyteacher"
            # No quantity deduction for rejection

        log.save()

    return redirect('dash:admindash')



def approved_requests(request):
    requests_approved = (StudentIssueLog.objects.filter(status_from_student="Issued",
                                                        status_from_teacher="Approved").values(
        'student__full_name', 'student__roll_number', 'issue_date', 'component__name',
        'component__category', 'component__quantity',
        'quantity_issued').order_by('component__category', '-form_date'))

    # Step 2: Group by category
    grouped_requests = defaultdict(list)

    for req in requests_approved:
        grouped_requests[req['component__category']].append(req)

    # print(grouped_requests.items())

    return render(request, 'teacher_dash/approved.html', {
        'grouped_requests': dict(grouped_requests)})

@require_POST
def return_status(request):
    roll_number = request.POST.get("roll_number")
    component_name = request.POST.get("component_name")
    issue_date = request.POST.get("issue_date")

    # print("data is:", component_name, roll_number,issue_date)

    # Get all matching requests (avoids MultipleObjectsReturned error)
    logs = StudentIssueLog.objects.filter(
        student__roll_number=roll_number,
        component__name=component_name,
        issue_date = issue_date,
        return_date__isnull=True
    )

    if not logs.exists():
        return HttpResponse("Log not found", status=404)

    if logs.count() > 1:
        return HttpResponse("Multiple active logs found for this student and component", status=400)

    # Safe: only one log exists
    log = logs.first()

    log.status_from_teacher = "Returned"
    log.status_from_student = "Returned"
    log.return_date = now().date()

    # Deduct from stock
    component = log.component
    component.quantity += log.quantity_issued
    component.save()

    log.save()

    return redirect("dash:approved_requests")


def rejected_requests(request):

    return render(request,"teacher_dash/rejected.html")

def change_inventory(request):
    return render(request,"teacher_dash/inventory.html")

def inv_items(request, category_key):
    components = Component.objects.filter(category=category_key)
    category_name = dict(Component.CATEGORY_CHOICES).get(category_key, "Unknown")
    return render(request, 'teacher_dash/inv_items.html'
                  , {
        'components': components,
        'category_name': category_name,
    })

def delete_component(request):
    if request.method == "POST":
        # data = (request.POST)
        # for kwy,value in data.items():
        #     print(f"{kwy}:{value}")
        component_name = request.POST.get('comp_name')
        # component_category = request.POST.get('comp_category')
        # print(component_category,component_name)


        try:
            component = Component.objects.get(name=component_name)
            component.componentstatus = 'Deleted'
            component.save()
        except Component.DoesNotExist:
            # You might want to add a message here for "not found"
            messages.error(request, f"Component  not found.")

    return render(request,'teacher_dash/inventory.html')




def add_component(request):
    if request.method == "POST":
            new_component = request.POST.get("component_name").strip()
            quantity = int(request.POST.get("component_qty"))
            category = request.POST.get("component_category")
            date_of_purchase = request.POST.get("dateofpurchase")
            # print(new_component,quantity,category,date_of_purchase)

            obj, created = Component.objects.get_or_create(
            name=new_component,
            
            defaults={
            "category":category,
            "quantity": quantity,
            "date_of_purchase": date_of_purchase,
            "componentstatus": "working"
            }
            )

            if not created:
                # If component already exists, add to existing quantity
                obj.quantity = obj.quantity + quantity

                obj.save()

            if created:
                messages.success(request, f"Component '{new_component}' added in category {category}.")
            else:
                messages.success(request, f"Component '{new_component}' updated, new total = {obj.quantity}.")


            return redirect("dash:admindash")  # change to your list page/


    return redirect('teacher_dash/inv_items.html')


def student_issues(request, roll_number):
    # Current issued items
    current_issues = (
        StudentIssueLog.objects
        .filter(student__roll_number=roll_number, status_from_student="Issued")
        .values(
            'component__name',
            'component__category',
            'quantity_issued',
            'form_date',
            'issue_date',
            'return_date',
            'status_from_student'
        )
        .order_by('component__category', '-issue_date')
    )

    # Previously issued (returned) items
    previous_issues = (
        StudentIssueLog.objects
        .filter(student__roll_number=roll_number, status_from_student="Returned")
        .values(
            'component__name',
            'component__category',
            'quantity_issued',
            'form_date',
            'issue_date',
            'return_date',
            'status_from_student'
        )
        .order_by('component__category', '-return_date')
    )

    # Group by category
    grouped_current = defaultdict(list)
    grouped_previous = defaultdict(list)

    for item in current_issues:
        grouped_current[item['component__category']].append(item)

    for item in previous_issues:
        grouped_previous[item['component__category']].append(item)

    return render(request, "student_dash/issues.html", {
        "grouped_current": dict(grouped_current),
        "grouped_previous": dict(grouped_previous),
        "roll_number": roll_number
    })