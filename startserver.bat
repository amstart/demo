call C:\Tools\Anaconda\envs\demoslogic\Scripts\activate.bat
set DATABASE_URL=postgres://Jochen:6104@localhost:5432/[project_slug]
python manage.py runserver
PAUSE