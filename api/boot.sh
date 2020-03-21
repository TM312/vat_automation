#!/bin/sh
echo Hello, world
source venv/bin/activate
while true; do
    python3 manage.py db upgrade
    if [[ "$?" == "0" ]]; then
    # [[]]: signifies a test is being made for truthiness.
    #$? a variable holding the exit code of the last run command
    # 0: standard exit code is 0
        break
    fi #closes the if statement
    echo Upgrade command failed, retrying in 5 secs...
    sleep 5
done
echo Script executed


# if [ "$FLASK_ENV" = "dev" ]
# then
#     echo "Creating the database tables..."
#     python3 manage.py fake_users_db
#     echo "Tables created"
# fi

# echo Starting gunicorn server...
# exec gunicorn -b :5000 --access-logfile - --error-logfile - wsgi:app
