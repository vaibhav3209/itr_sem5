from datetime import datetime,date

from django.core.exceptions import ValidationError
from django.db import transaction, IntegrityError
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import logout,authenticate, login
from django.utils.timezone import now
from django.views.decorators.http import require_POST
from .decorators import student_login_required,admin_login_required
from .models import Student, StudentIssueLog, ComponentCategory
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from collections import defaultdict
from .models import Component


#=======================================================================
# 1. test your project by HTTP response
# def test(request):
#     return HttpResponse("hi")

# 2. add home page
def home(request):
    return render(request,'final/home.html')

# 3. login
def user_login(request):
    # ====== LOGIN  ======

    if request.method == 'POST'and request.POST.get("form_type") == "user_login":
            username = request.POST.get('username')
            password = request.POST.get('password')

            if username.endswith("admin"):
                admin_user = authenticate(request,username=username,password=password)

                if admin_user and admin_user.is_staff:
                    login(request, admin_user)
                    return redirect('final:admin_dashboard')
            try:
                student = Student.objects.get(std_roll_number=username.upper()) #yha pe bhi roll
                # number ko upercase
            except Student.DoesNotExist:
                messages.error(request, "Invalid email or password",extra_tags='error')
                return render(request, 'final/login.html')

            if check_password(password, student.std_password):
                request.session['student_id'] = student.std_id  # custom session
                request.session["student_name"] = student.std_full_name
                return redirect('final:student_dashboard')

            messages.error(request, "Invalid email or password.",extra_tags='error')

    # ====== Signup  =====
    if request.method == 'POST' and request.POST.get("form_type") == "user_signup":
        first_name = request.POST.get("first_name").lower()           #lower names store in db
        last_name = request.POST.get("last_name").lower()               #lower names store in db
        roll_number = request.POST.get("roll_number").upper()
        email = request.POST.get("college_email").lower()               #lower kiya isko bhi
        password = request.POST.get("password")
        phone_number=request.POST.get("phone_number")
        year_of_passing=request.POST.get("year_of_passing")

        # basic validation
        if Student.objects.filter(std_roll_number=roll_number).exists():
            messages.error(request, "Roll number already exists",extra_tags='error')
            return render(request, "final/login.html")

        if Student.objects.filter(std_college_email=email).exists():
            messages.error(request, "Email already registered",extra_tags='error')
            return render(request, "final/login.html")

        try:
            Student.objects.create(
                std_first_name=first_name,
                std_last_name=last_name,
                std_roll_number=roll_number,
                std_college_email=email,
                std_password=make_password(password),
                std_phone_number=phone_number,
                std_year_of_passing=year_of_passing
            )

        except ValidationError as e:
            return HttpResponseBadRequest(
                f"Cannot create user. Enter a valid roll number."
            )

        except IntegrityError:
            return HttpResponseBadRequest(
                "data violates constraints."
            )


        messages.success(request, "Registration successful. Please login.",extra_tags='success')
        return redirect("final:login")

    #initial login page
    return render(request, 'final/login.html',{'passing_years':range(date.today().year, date.today().year + 5)})


# 4. home page for student dashboard
#saara logic wrapper mein check ho rha hai
@student_login_required
def student_dashboard(request):
    student = request.student
    return render(request,"final/student_dashboard.html",{"student": student})


# 5. home page for admin dashboard
    # Only staff/admin can access

#note: default dict bhi access nhi hogi html se TABLE HI LOAD NHI HO RHI THI
@admin_login_required
def admin_dashboard(request):
    # jo nayi entry aayi hai uski both issue_Date, return_date null hogi
    requests_qs = (
        StudentIssueLog.objects
        .filter(std_issue_issue_date__isnull=True,
                std_issue_return_date__isnull=True)
        .values(
             'student__std_roll_number',
            'component__comp_name',
            'component__comp_category__comp_cate_category_name',      #since do f.k. lagai hai
            'std_issue_form_date',
            'component__comp_quantity_available',
            'std_issue_quantity_issued'
        )
        .order_by('component__comp_category__comp_cate_category_name', '-std_issue_form_date')
    )

    grouped_requests = defaultdict(list)
    for r in requests_qs:
        grouped_requests[r['component__comp_category__comp_cate_category_name']].append(r)
    # print(grouped_requests)
    return render(
        request,
        'final/admin_dashboard.html',
        {'grouped_requests': dict(grouped_requests)}
    )




# 6.  logout :: yha pe decorators nahi lagane as kabhi broken session unlogged user can also access
# this  button
def student_logout(request):
    request.session.flush()
    return redirect('final:login')

def admin_logout(request):
    logout(request)                     #django based logout hai
    return redirect("final:login")

# =============================================================
# *****      EXTRA LOGIC FOR STUDENT          *****

# 7.  starting from student_Dashboard.html
# 7.a.  issued items from sidebar

@student_login_required
def issued_items(request):
    student_id = request.session.get('student_id')

    grouped_currently_issued = defaultdict(list)
    grouped_previously_issued = defaultdict(list)

    for log in StudentIssueLog.objects.filter(student_id=student_id).select_related('component').only(
        'std_issue_quantity_issued',
        'std_issue_issue_date',
        'std_issue_return_date',
        'component__comp_category__comp_cate_category_name',
        'component__comp_name'
    ):
        #return date nhi hai to issued hi hai abhi
        if not log.std_issue_return_date:
            grouped_currently_issued[log.component.comp_category.comp_cate_category_name].append(log)
        else:
            grouped_previously_issued[log.component.comp_category.comp_cate_category_name].append(log)

    return render(request, "final/issued_items.html", {
        "grouped_current": dict(grouped_currently_issued),
        "grouped_previous": dict(grouped_previously_issued)
    })


# 7.b.   click request components from sidebar
#           then see all categories
@student_login_required
def request_components(request):
    return render(request, 'final/request_components.html')


# see sepcofoc items in a category
@student_login_required
def category_items(request, slug):
    category = get_object_or_404(
        ComponentCategory,
        comp_cate_category_name=slug
    )

    components = Component.objects.select_related('comp_category').filter(
        comp_category=category
    )

    return render(request, 'final/category_items.html', {
        'components': components,
        'category_name': category.comp_cate_category_name,
    })


# 7.c.  submit request from right sidebar
@student_login_required
def submit_request(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("Invalid request method")

    component_ids = request.POST.getlist('component_ids[]')
    quantities = request.POST.getlist('quantities[]')
    print(component_ids,quantities)

    if not component_ids or not quantities:
        messages.error(request, "No components selected",extra_tags='error_requestcomp')
        return redirect('final:request_components')

    if len(component_ids) != len(quantities):
        return HttpResponseBadRequest("Mismatched data")


    student = request.student
    # print(type(student))
    # print(student.std_full_name,student.std_roll_number)

    # ---- FETCH ALL COMPONENTS IN ONE QUERY (FAST) ----
    # old one was giving multiple requset to database
    components_map = Component.objects.in_bulk(component_ids)

    issue_logs = []

    for comp_id, qty in zip(component_ids, quantities):
        component = components_map.get(int(comp_id))
        if not component:
            continue

        try:
            qty = int(qty)
            if qty <= 0:
                continue
        except ValueError:
            continue

        issue_logs.append(
            StudentIssueLog(
                student=student,
                component=component,
                std_issue_quantity_issued=qty,
                std_issue_form_date=datetime.now().date()
            )
        )

    if not issue_logs:
        messages.error(request, "Invalid component selection",extra_tags='error_requestcomp')
        return redirect('final:request_components')

    # ---- ATOMIC SAVE (SAFE) ----
    with transaction.atomic():
        StudentIssueLog.objects.bulk_create(issue_logs)

    messages.success(request, "Request submitted successfully",extra_tags='success_requestcomp')

    response = redirect('final:request_components')
    response.set_cookie('clearLocalStorage', 'true')  # frontend signal
    return response


# =============================================================
# *****      EXTRA LOGIC FOR adMIN          *****
@admin_login_required
def approved(request):
    # jo iisued entry hai uski return_date null hogi
    requests_approved = (StudentIssueLog.objects
                         .select_related("student", "component",
                                        "component__comp_category")
                         .filter(std_issue_issue_date__isnull=False,
                                 std_issue_return_date__isnull=True)
                         .values(
         'student__std_roll_number', 'std_issue_issue_date', 'component__comp_name',
        'component__comp_category__comp_cate_category_name', 'component__comp_quantity_available',
        'std_issue_quantity_issued').order_by('component__comp_category__comp_cate_category_name', '-std_issue_form_date'))

    # Step 2: Group by category
    grouped_requests = defaultdict(list)

    for req in requests_approved:
        grouped_requests[req['component__comp_category__comp_cate_category_name']].append(req)

    # print(grouped_requests.items())

    return render(request, 'final/approved.html', {
        'grouped_requests': dict(grouped_requests)})

@admin_login_required
def inventory(request):
    return render(request,"final/inventory.html")



@require_POST
@admin_login_required
def update_status(request):
    roll_number = request.POST.get("roll_number")
    form_date = request.POST.get("form_date")
    issue_date = request.POST.get("issue_date")
    component_name = request.POST.get("component_name")
    status_to_update = request.POST.get("status_to_update")
    # print("data is:", form_date, action, component_name, roll_number)


    if status_to_update in ("approve","reject"):
        logs = StudentIssueLog.objects.select_related("component", "student").filter(
            student__std_roll_number=roll_number,
            component__comp_name=component_name,
            std_issue_form_date=form_date
        )


    elif status_to_update == "return":
        logs = StudentIssueLog.objects.select_related("component", "student").filter(
            student__std_roll_number=roll_number,
            component__comp_name=component_name,
            std_issue_issue_date = issue_date,
            std_issue_return_date__isnull=True
        )

    else: return HttpResponse("Invalid action", status=400)

    if not logs.exists():
        return HttpResponse("Log not found", status=404)

    with transaction.atomic():
        if status_to_update == "reject":
            # Delete all matching logs
            deleted_count, _ = logs.delete()

            if deleted_count > 0:
                messages.success(request, "Log deleted successfully.")
            else:
                messages.error(request, "No matching log found.")

        else:
            for log in logs:
                component = Component.objects.select_for_update().get(
                    id=log.component_id
                )

                if status_to_update == "approve":
                    if component.comp_quantity_available < log.std_issue_quantity_issued:
                        return HttpResponse(
                            f"Not enough quantity available for {component.name}",
                            status=400
                        )

                    # Update log
                    log.std_issue_issue_date = now().date()

                    # Deduct stock
                    component.comp_quantity_available -= log.std_issue_quantity_issued
                    component.save()
                    log.save()

                elif status_to_update == "return":
                    log.std_issue_return_date = now().date()

                    component.comp_quantity_available += log.std_issue_quantity_issued
                    component.save()

                    log.save()
                    return redirect('final:approved')

    return redirect('final:admin_dashboard')

@admin_login_required
def inventory_items(request, slug):
    category = get_object_or_404(
        ComponentCategory,
        comp_cate_category_name=slug
    )

    components = Component.objects.select_related('comp_category').filter(
        comp_category=category
    )

    return render(request, 'final/inventory_items.html', {
        'components': components,
        'category_name': category.comp_cate_category_name,
    })

@admin_login_required
def all_students(request):
    students = Student.objects.all().order_by("std_roll_number")

    return render(request, "final/all_students.html", {
        "students": students
    })

@admin_login_required
def student_details(request,id):
    student = get_object_or_404(
        Student,
        std_id=id
    )

    issued_components = (
        StudentIssueLog.objects
        .select_related("component",'student')
        .filter(student_id=student.std_id)
        .order_by("-std_issue_issue_date")
    )

    return render(request, "final/student_details.html", {
        "student": student,
        "issued_components": issued_components
    })


@require_POST
@admin_login_required
def delete_component(request):
    component_id = request.POST.get('component_id')
    # print(component_id)
    component = get_object_or_404(Component, comp_id=component_id)

    # Get the Deleted status object
    deleted_status = get_object_or_404(StatusChoices, status_ch_status_label='Deleted')

    # Soft delete
    component.comp_status = deleted_status
    component.save(update_fields=['comp_status'])


#ye sab messages login form par dikh rhe hai inhe sahi karo
    messages.success(request, f"{component.comp_name} marked as deleted.")

    return render(request,'final/inventory.html')
    # =================same page pe rakhna isko sahi karo




#
# def add_component(request):
#     if request.method == "POST":
#             new_component = request.POST.get("component_name").strip()
#             quantity = int(request.POST.get("component_qty"))
#             category = request.POST.get("component_category")
#             date_of_purchase = request.POST.get("dateofpurchase")
#             # print(new_component,quantity,category,date_of_purchase)
#
#             obj, created = Component.objects.get_or_create(
#             name=new_component,
#
#             defaults={
#             "category":category,
#             "quantity": quantity,
#             "date_of_purchase": date_of_purchase,
#             "componentstatus": "working"
#             }
#             )
#
#             if not created:
#                 # If component already exists, add to existing quantity
#                 obj.quantity = obj.quantity + quantity
#
#                 obj.save()
#
#             if created:
#                 messages.success(request, f"Component '{new_component}' added in category {category}.")
#             else:
#                 messages.success(request, f"Component '{new_component}' updated, new total = {obj.quantity}.")
#
#
#             return redirect("dash:admindash")  # change to your list page/
#
#
#     return redirect('teacher_dash/inv_items.html')

