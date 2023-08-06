# Biomaj user

Biomaj user management library

Creation/deletion/... scripts should not be accessible to end user, only to admin.
End users can have access to their API Key via the biomaj-watcher interface.


# Web server

    export BIOMAJ_CONFIG=path_to_config.yml
    gunicorn biomaj_user.biomaj_user_service:app

Web processes should be behind a proxy/load balancer, API base url /api/user

# Managing users

    usage: biomaj-users.py [-h] -A ACTION [-C </path/to/config.yml>] [-E EMAIL] -U <username> [-P <password>]

Availables actions: create, delete, update, view, renew (apikey) 


3.0.3:
  move biomaj_create_user and biomaj_delete_user to biomaj_users script with cmd line options
3.0.2:
  add scripts to add/remove a user
3.0.1:
  move biomaj_user_service.py to package
3.0.0:
  separation of biomaj and biomaj_user


