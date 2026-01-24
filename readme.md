# Index :
- [Markdown Notations](#-tags-used-so-you-remember)
- [Features](#features)
- [Installation](#installation)
- [Directory Structure Map](#directory-structure)
- [Project Guide Know hows](#project-guidelines)
- [MY Mistakes](#mistakes-that-i-have-done)
- [Testing](#how-to-test)
- [Django important Functionalities](django-functionalities)
- [My Learnings](#-things-i-learnt-new-besides-django)

---------------------------------------------------------------------------
### 🔑 ***Tags used (so I remember)***
- `##` → section heading
- `***text***` → bold + italic emphasis
- `-` → bullet points
- `` `code` `` → inline code
- ``` ``` → code block
- `>` → note / important message
- enter for two lines to give space between each list point 
---------------------------------------------------------------------------



---------------------------------------------------------------------------
## 🚀 Features

- **Student Registration**
  - Register students using roll number and basic details
  - Remaining details can be completed later from the dashboard


- **Email Verification**
  - Email verification required before issuing any components
  - Prevents unauthorized access


- **Admin / Teacher Dashboard**
  - Centralized dashboard for teachers/admins
  - View all students and issued components
  - Approve or reject component issue requests


- **Component Issuance System**
  - Track issued components with issue date and quantity
  - Maintain complete issuance history per student
  - Prevent issuing components beyond available quantity


- **Student Profile View**
  - Clickable roll number to view full student details
  - Displays all components issued to one particular student


- **Secure Configuration**
  - Environment variables managed via `.env` file
  - Sensitive data hidden from version control
  - Row Level Security 
  - Django auth


- **Role-Based Access**
  - Separate access for students and teachers/admins
  - Django superuser support for admin panel

    
- **Scalable Design**
  - Optimized queries using `select_related` and `prefetch_related`
  - Pagination-ready for large student datasets
---------------------------------------------------------------------------


---------------------------------------------------------------------------
## ⚙️ ***Installation***

- **Clone the repository**


- Make a virtual environment inside the cloned directory and install all dependencies


- Go to the `settings.py` file inside `teststudy/` and check the hidden configuration 
  tags  
  - `config()`  
  - `os.getenv()`


- These values must be defined in your own `.env` file inside the `CONFIG/` directory
> 📌 **Remember:** ⚠️ keep the ``.env`` file there only. (NOT UPLOAD)
  

- If you want to use a ***local database***:
  - Uncomment `db.sqlite3` lines
  - Do this  in the `DATABASES` section of `settings.py`


```
- Run this command :: python manage.py migrate
📝 This will create the database file the first time it is run
```

- Create a Django superuser
(This will help in the teacher login panel)
    
    `python manage.py createsuperuser`   


-  then use username and password to login to teacher panel.

> 📌 **Remember:**  username should be 10digit only as set by me in> 


`login.html` and `model Student` constraints


- Check whether the project is running

  `python manage.py runserver`
---------------------------------------------------------------------------


---------------------------------------------------------------------------
## ***DIRECTORY STRUCTURE***
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
---------------------------------------------------------------------------

---------------------------------------------------------------------------
## PROJECT GUIDELINES

1.  Kept small Letters of all column names.


2.  Every column will start from a prefix of its table name. 


    comp_cate_                   ==>>  for Component_categories
    comp_attribute_              ==>>  for Component model
    std_attribute_               ==>>  for Student model
    std_issue_                  ==>>  for StudentIssueLog model
  

3. see table definitions from the `models.py` file.


4. >📌 **Remember:**  keep DEBUG == TRUE in development and
         DEBUG == False in production as u don't want users to see errors.


5. Put business logic in `models.py` file and HTML, session based(HTTPRequest) in ``views.py``.
---------------------------------------------------------------------------


---------------------------------------------------------------------------
# MISTAKES THAT I HAVE DONE  (***IMPORTANT***)


1.  We didn't used `Django--User model` as it was slow.......
      
(it may be due to our wrong code but it was.) and we don't accept our product to be SLOW....
I TRIED `shifting to USer model` AFTER MAKING PROTOTYPE OF OUR PROJECT (which was a very bad 
decision costing me 2 days
       and i have to SHIFT BACK TO ORIGINAL PROTOTYPE)


2.   You should not write `html`,`css`,`js` all in one file. why? 
- a. If you wan the same css in some files. You have to write it everywhere!!! 
- b. let's say you used all code in one file but if you have to change anything in the repeated 
  code you have to change in `EVERY FILE`

  
>📌 **Remember:**  Never delete or change  schema from database online if online databse you 
     are using  
     (Except you can delete 
     data from table from anywhere)

> ***IMPACT***:: otherwise your local `migrations` and `migrations` table in database  will 
     conflict then it will be a problem.

> ***Solution***: command `python manage.py makemigrations --fake`   but it is not worth it.


3. `<str:category>` in `urls.py` not allow `micro / boards` urls with spaced, underscores. 

Thats why companies uses `SLUG FIELDS` To better fit the urls. (BUT i don't used them here 😄)

> ***SOLUTION*** :: slash lagane k liye `<path:category_key>` kardo


4. > ***NOTE***:   `url == admin/`  will point to django admin. So if i wented to write teacher 
   > dashboard add the keyword Teacher not admin

---------------------------------------------------------------------------
## HOW to Test for all possible bugs:

1. 

---------------------------------------------------------------------------

---------------------------------------------------------------------------
## Django Functionalities

### 1. how Related_name works in a foreign key:: It allows easy reverse queries. 

        student = Student.objects.get(id=1)
            student.issue_logs.all()

     means:::: Give me all issue log records that belong to this student.


Category table

| id | category_name        |
|----|----------------------|
| 1  | Sensors              |
| 2  | Microcontrollers     |


Component

| id | component_name | category_id |
|----|----------------|-------------|
| 1  | DHT11          | 1           |
| 2  | Ultrasonic     | 1           |
| 3  | Arduino Uno    | 2           |
| 4  | ESP32          | 2           |


| Query | Without related_name           | With related_name           |
|------|--------------------------------|-----------------------------|
| Get category of component | `component.comp_category`      | `component.comp_category`   |
| Get components of category | `category.component_set.all()` | `category.componentcategory_fkey.all()` |


### 2.  `__` means “go inside model”  if we are referncing two models you will see this in html code.


### 3. 🧠 Django ORM → SQL Mental Mapping

| Django ORM          | SQL Think        |
|---------------------|------------------|
| `.filter()`         | `WHERE`          |
| `.select_related()` | `JOIN`           |
| `.only()`           | `SELECT columns` |
| `.all()`            | `SELECT *`       |


| Django ORM | SQL Equivalent | Notes                                                          |
|------------|----------------|----------------------------------------------------------------|
| `Component.objects.filter(comp_category_id=1)` | `SELECT * FROM component WHERE comp_category_id = 1;` | Filters rows by condition                                      |
| `Component.objects.select_related("comp_category")` | `SELECT component.*, category.* FROM component INNER JOIN category ON component.comp_category_id = category.id;` | Joins related FK table to avoid extra queries                  |
| `Component.objects.only("comp_name", "comp_quantity_available")` | `SELECT id, comp_name, comp_quantity_available FROM component;` | Fetch only selected columns; others deferred                   |
| `comp = Component.objects.only("comp_name").first()`<br>`comp.comp_price` | `SELECT comp_price FROM component WHERE id = 1;` | gets first row . Accessing deferred field triggers extra query |
|  `logs = request.user.student.issue_logs.all()` | `SELECT * FROM studentissuelog WHERE student_id = <current_student_id>;` | Fetch all issue logs for a student |
| `student.issue_logs.filter(status_from_teacher="Approved").count()` | `SELECT COUNT(*) FROM studentissuelog WHERE student_id = <student_id> AND status_from_teacher = 'Approved';` | Count only approved items |
|  `student.issue_logs.filter(component=component, status_from_teacher="Pending").exists()` | `SELECT 1 FROM studentissuelog WHERE student_id = <student_id> AND component_id = <component_id> AND status_from_teacher = 'Pending' LIMIT 1;` | Returns True if a pending request exists |
---------------------------------------------------------------------------


### 4.✅ `Advantages of Django ORM:`  
- Pros
    - ✔ Safe (SQL injection protected)
    - ✔ Readable & maintainable
    - ✔ Easy to refactor
    - ✔ DB-agnostic (Postgres / SQLite / MySQL)
    - ✔ Django handles joins efficiently
    - ✔ Easier for teammates (or future you)

- Cons
  - ❌ Very complex queries can get ugly
  - ❌ Rare edge-case optimizations harder


### `Why not Raw SQL!!!`

- Pros
    - ✔ Absolute control
    - ✔ Best for very complex aggregations
    - ✔ Can squeeze last 5–10% performance

- Cons
  - ❌ Easy to introduce bugs
  - ❌ Hard to maintain
  - ❌ DB-specific
  - ❌ No automatic security unless careful
  - ❌ Harder to refactor models
---------------------------------------------------------------------------
## THINGS I LEARNT NEW BESIDES "DJANGO"

1. 
---------------------------------------------------------------------------


---------------------------------------------------------------------------
 


*********************************
FUTURE TO DO'S
*********************************

3. admin.site.urls ko env mein daalna

6. add compnent ka button hta diya from inventory.html

7. cateogy k cards jo aate hai usko dynamic karna

8. Agar har lab mein implement karna to kaise setup karenge iska dekho

- [ ] TOdo : add er diagram if possible

- [ ] introduction 