
To run server -->
    1) unzip folder
    2) pip install -r requirements.txt
    3) cd backend
    4) python manage.py makemigrations
    5) python manage.py migrate
    6) python manage.py runserver


To create a new form -->
    1) go to admin panel and login (username:admin, password:admin)
    2) Add a new form
    3) Enter unique name for your form
    4) Upload csv file in proper format as used in example (Errors for wrong format inserted are not handled)
    5) keep all other fields as null and save this form
    6) Now just remember form name and enter it as formname in api urls


Api's available -->
    /myform/<formname>/
        get ==> all form entries created in that given form
        post ==> additional form entry creation if data is valid

    /myform/<formname>/<id>/
        put ==> update form entry if valid
        delete ==> delete form entry

