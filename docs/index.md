# Feed reader documentation

# Running the project

1. Install Docker on your OS by following the instructions [https://docs.docker.com/engine/install/](Here)
2. Run the command :`docker compose up -d`
3. Open [http://127.0.0.1:8000](http://127.0.0.1:8000) link in your browser for viewing main page of the project.
4. Open the following link in your browser to view the project documentation: [http://127.0.0.1:7000](http://127.0.0.1:7000).

# Running the tests

1. First Run the project with `docker compose up -d`
2. Run `docker compose exec web python manage.py test`
3. You would see logs of tests in the terminal

# How add New feeds?

1. Go to swagger docs page [http://127.0.0.1:8000/api/swagger](http://127.0.0.1:8000/api/swagger) 
2. Add a new feed by sending a POST request to `/api/posts` and enter the required information. 
3. The system will start a background process to check your feed links every 5 minutes.

# How follow or unfollow feeds?

- First get all feed using `get` request to `/api/feeds/` and get the feed `id`
- Send patch request to `/api/feeds/{id}/` route. For example  `followed=false` . `id` is obtained from previous step. Feed after creating has by default `followed=true` 

# How view and filter the saved posts?

1. Use `/api/filter-posts` route. Note that all posts are by default `followed=false` and `readed=false`


# How make post read or followed?

- Use `/api/filter-posts` route. Note that all posts are by default `followed=false` and `readed=false`

1. First filter posts to find a post and use its `id`
2. Send patch request to `/api/posts/{id}/` route. For example  `followed=true` and `readed=true`. `id` is obtained from previous step.


# What technologies used?

1. Django for base of system because of its great features
2. Celery for running background and periodic tasks
3. Redis as message broker for celery because it is robust and battle tested for production and supports message persistence
4. Redis for caching because it is ultra-fast