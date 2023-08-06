# Biomaj user

Biomaj user management library

# Status

development

# Web server


    export BIOMAJ_CONFIG=path_to_config.yml
    gunicorn biomaj_user.biomaj_user_service:app

Web processes should be behind a proxy/load balancer, API base url /api/user



3.0.2:
  add scripts to add/remove a user
3.0.1:
  move biomaj_user_service.py to package
3.0.0:
  separation of biomaj and biomaj_user


