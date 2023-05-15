# Company Management

## First run

1. Run `docker-compose build && docker-compose up`.
2. To create the database, run `docker-compose exec -it api python manage.py migrate`.

## Admin panel

1. To create the superuser, run `docker-compose exec -it api python manage.py createsuperuser --email admin@example.com`. Enter and repeat the password.
2. Open `http://localhost:8000/admin/`.
3. Use `admin@example.com` as an email and enter your password.


## Testing

Run `docker-compose exec -it api python manage.py test` to run all tests.
