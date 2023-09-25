# Python web scrapper project

# Running the project with docker

1. Run the command :`docker compose up -d`
2. Open [http://127.0.0.1:8000](http://127.0.0.1:8000) link in your browser for viewing main page of the project.
3. Open the following link in your browser to view the project
   documentation: [http://127.0.0.1:7000](http://127.0.0.1:7000).

# Running the tests

1. First Run the project with `docker compose up -d`
2. Run `docker compose exec api python manage.py test`
3. You would see logs of tests in the terminal

# Configuration parameters
Add FEED_READER dictionary to django setting file fr this parameters:

FEED_READER = {  
    "MAX_FEED_READER_ERRORS": Maximum retries times if any error occurred,  
    "FEED_READER_RETRY_TIME": Time in seconds if you want to retry errored feed links,  
    "DEFAULT_PARSING_TIME_LOOP": Time in second between parsing feed links,  
}  

# Build your favorite UI

By using api exposed in swagger page you can build your favorite UI using modern front end JavaScript frameworks like
React.  
Go to swagger docs page via [http://127.0.0.1:8000/api/swagger](http://127.0.0.1:8000/api/swagger)

# Adding New feed

1. Register a user to system with POST request to `/auth/register`
2. Login user with request to `/auth/token`
3. Add a new feed by sending a POST request to `/api/posts` and enter the required information.
4. The system will start a background process to fetch feed links every 5 minutes.

# How follow or unfollow feeds?

- First get all feed using `get` request to `/api/feeds/` and get the feed `id`
- Send patch request to `/api/feeds/{id}/` route. For example  `followed=false` . `id` is obtained from previous step.
  Feed after creating has by default `followed=true`

# How view and filter the saved posts?

1. Use `/api/filter-posts` route. Note that all posts are by default `followed=false` and `readed=false`

# How make post read or followed?

- Use `/api/filter-posts` route. Note that all posts are by default `followed=false` and `readed=false`

1. First filter posts to find a post and use its `id`
   **2. Send patch request to `/api/posts/{id}/` route. For example  `followed=true` and `readed=true`. `id` is obtained
   from previous step.

# What technologies used?

1. Django for base of system because of its great features
2. Celery for running background and periodic tasks
3. Redis as message broker for celery because it is robust and battle tested for production and insures message
   persistence
4. Redis for caching because it is ultra-fast