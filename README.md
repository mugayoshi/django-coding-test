# django-coding-test

1. Make sure you're in the root directory (django-coding-test), run the following command to run the server.
```sh
docker-compose up
```

2. To check if the API and the management commands work, run the commands below.
```sh
curl http://127.0.0.1:8000/api/health/
docker-compose exec web python manage.py sample_command
```

3. To feed sample data of channels and contents, run the following command.
```sh
docker-compose exec web python manage.py create_test_channel --title "My Test Channel" --content-count 2
```

4. After creating data, run this command to get the CSV file that contains rating of channels.
```sh
docker-compose exec web python manage.py export_channel_rating_csv
``` 

5. Run the tests by this command.
```sh
docker-compose exec web python manage.py test myapp.tests
```
