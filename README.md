# Company Management

## First run

1. Run `docker-compose build && docker-compose up`.
2. To create the database, run `docker-compose exec -it api python manage.py migrate`.
3. To create the superuser, run `docker-compose exec -it api python manage.py createsuperuser --email admin@example.com --username admin`.

## Admin panel

1. Open `http://localhost:8000/admin/`.
2. Use `admin@example.com` as an email and enter your password.
