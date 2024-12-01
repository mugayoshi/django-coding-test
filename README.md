# django-coding-test

## Steps

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

4. After creating data in the database, run this command to get the CSV file that contains rating of channels.
```sh
docker-compose exec web python manage.py export_channel_rating_csv
``` 

5. Run the tests by this command.
```sh
docker-compose exec web python manage.py test myapp.tests
```

## Approach

I followed the steps below for this challenge.

1. Crate a base of a Django app
1. Create a health check endpoint and a sample command
1. Define models
1. Implement commands to feed the data
1. Implement the endpoint that returns the list of channels
1. Implement the command of exporting the ratings of channels and its test
1. Dockerize the app

### Rating channels

To implement the command, I wanted to get the rating data by a query like this:
```sql
SELECT 
    channel.id, 
    channel.title, 
    AVG(content.rating) as avg_rating
FROM 
    channel 
JOIN 
    content ON channel.id = content.channel_id
GROUP BY 
    channel.id, channel.title
HAVING 
    COUNT(content.id) > 0
ORDER BY 
    avg_rating DESC
```
Therefore, I used `annotate` function by utilizing Django lookup functions that traverses the relationship between Channel and Content (`contents__rating`).  
Also, I made sure selecting channels with at least one content by `filter` and `Q` functions. (`.filter(Q(contents__isnull=False))`)  
The actual function is defined in `myapp/services/channel_rating_service.py`.