***************************
DIRECTORY STRUCTURE
****************************

project_root/

    ├── manage.py

    ├── README.md

    ├── .gitignore  (not on github)

    ├── db.sqlite3  (not on github)

    │──extra_Scripts/
            ├── test_db.py
            ├── export_fixture.py
    


    ├── staticfilesforproduction/     (not on github) # collectstatic output (production)

    ├── config/                         # Non-code configuration
        ├── .env
        └── requirements.txt


    ├── teststudy(package)/                  # Project settings & config
        ├── __init__.py
        ├── settings.py
        ├── urls.py
        ├── asgi.py
        └── wsgi.py


    ├── final(package)/                      # Main Django app
        ├── __init__.py
        ├── admin.py
        ├── apps.py
        ├── decorators.py
        ├── models.py
        ├── views.py
        ├── urls.py
        ├── migrations(package)/
            └── __init__.py
        
        ├── templates/
            └── final/
                └── *.html
        
        ├── static/
           └── final/
               ├── css/
               ├── js/
               └── images/
       
           ├── management(package)/
                ├── __init__.py
                └── commands(package)/
                    ├── __init__.py
                    └── import_components.py


*******************************
SETUP
*******************************
1. Clone the repo
2. Make environment inside the cloned directory and install all dependencies
3. go to settings.py file inside teststudy and see the hidden tags 

    ex::  config() , os.getenv()

    Those things have to be made in .env file of your own in the "CONFIG" DIRECTORY
4. if you want local databse then uncomment the db.sqlite3 file <br>
   in databses section in settings.py file only :: <br>
    
    "python manage.py migrate" will make the database file when we do it for first time.
5. create superuser django (this will help in teacher login panel)
6. check whether it's runnnin. <br> python manage.py runserver

*******************************
PROJECT GUIDELINES
*******************************
1.  keep all the column names of database consistent..
    Wwe have kept small letters for everything

    comp_attribute              ==>>  for Component model
    std_attribute               ==>>  for Student model
    std_issue_                  ==>>  for StudentIssueLog model
    del_std_                    ==>>  for DeletedStudent model
    del_std_issue_              ==>>  for DeletedStudentIssueLog model


*******************************
MISTAKES THAT I HAVE DONE
*******************************

1.  we didn't used Django--User model as it was slow(it may be due to our
    wrong code but it was)
    and we don't accept our product to be SLOW....
    I TRIED AFTER MAKING PROTOTYPE OF OUR PROJECT (which was a very bad
    decision costing me 2 days
    and i have to SHIFT BACK TO ORIGINAL PROTOTYPE)

2.  you don't need to do {% load static %} every page you extend....
    just make global js,css,html besides base_layout and  add extra blocks
    for every new css/js file.


3.  keep DEBUG == TRUE in development and
         DEBUG == False in production as u don't want users to see errors

4.  ***IMP****
    Earlier i have put the business logic in VIEWS.PY file..
    now we have added all business logic in MODELS.PY

5.)


*********************************
THINGS I LEARNT NEW BESIDES ""DJANGO""
*********************************
1.  to refer things in different apps you write like this
    "from ..student_dash.urls import app_name"          .. means 2 previous directory

2.  Basic Routing:
    path('', include('core.urls')),                         # home, landing pages
    path('accounts/', include('accounts.urls')),            # start of accounts
    path('admin/', admin.site.urls),


    /                    → Home
    /accounts/login/     → Login
    /admin/              → Admin

3.  ADVANTAGE OF USING "RELATED NAME" in models when creating a foreign key
    ***** foreignkey.relatedname.function   *****
        student = Student.objects.get(id=1)
            student.issue_logs.all()

     means:::: Give me all issue log records that belong to this student.

     we can save writing this ==>>  StudentIssueLog.objects.filter(student=student)

    **** Practical usage (REAL examples)   ****
    ** Show student history
        logs = request.user.student.issue_logs.all()

    ** Count issued items
        student.issue_logs.filter(status_from_teacher="Approved").count()

    ** Check if student already requested a component
        student.issue_logs.filter(
            component=component,
            status_from_teacher="Pending"
        ).exists()


4.  DJANGO ORM FUNCTIONS
    .filter() → which rows
    .select_related() → join tables
    .only() → which columns

5. ✅ Django ORM (what you’re using now)
Pros
✔ Safe (SQL injection protected)
✔ Readable & maintainable
✔ Easy to refactor
✔ DB-agnostic (Postgres / SQLite / MySQL)
✔ Django handles joins efficiently
✔ Easier for teammates (or future you)

Cons
❌ Very complex queries can get ugly
❌ Rare edge-case optimizations harder
❌ Raw SQL

Pros
✔ Absolute control
✔ Best for very complex aggregations
✔ Can squeeze last 5–10% performance

Cons
❌ Easy to introduce bugs
❌ Hard to maintain
❌ DB-specific
❌ No automatic security unless careful
❌ Harder to refactor models

5:  NOTE:   never delete or change model schema from databse online
           otherwise your local migrations and migrations table online will conflict
           then it will be a problem.

    solution:  migrations --fake   but it is not worth it.
*********************************
FUTURE TO DO'S
*********************************

1. set models k columns ki size for better databse storage

2. load fresh new components

3. admin.site.urls ko env mein daalna

4. database tables mein jaise status hai, category names hai unko integer values dedo vo table mein
rahna   COMPONENT_STATUS = [
        ('Defective', 'Defective'),
        ('Deleted', 'Deleted'),
        ("working", 'working')
    ]
    isme se kisi jagah par 0 ,1, 2, kar sakte hai kya

5. <!--rejected /htlm mrin kuch karna hai kya ya ye bas view only page rakhna hai-->

6. add compnent ka button hta diya from inventory.html

7. cateogy k cards jo aate hai usko dynamic karna