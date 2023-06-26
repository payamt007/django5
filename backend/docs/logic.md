# How this project works?

- In the model layer, two models, Feed and Post, were considered, and they have a one-to-many relationship (each Feed has many Posts).
- For parsing RSS feeds, a Python library called [feedparser ](https://github.com/kurtmckee/feedparser) was used. I never try to reinvent the wheel!
- Feeds and posts data are saved in a PostgreSQL database after parsing.
- The last update time of each feed is saved in Redis cache to prevent consuming resources for parsing a feed that has not been updated.
- [Celery bit ](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html) was used for running periodic fetching of posts because it is robust and battle-tested in production environments.
- Celery needs a message broker, and based on the descriptions in the Celery docs, we can choose between Redis or RabbitMQ. I chose RabbitMQ because it guarantees better message persistence in the event of failure.
- The main celery config file is located in `sendcld.celery` that also include the celery beat config.
- The celery tasks are located inside `base.tasks`
- Two tasks are defined for Celery: one for fetching link data (base.tasks.read_feed_links) and another one for retrying failed tasks (retry_failed_feeds).
- Celery beat was used as the scheduler tool for running the main task of updating feeds every 5 minutes.
- In case of failure, retry_failed_feeds is called after 2, 5, and 8 minutes. If the retry is successful, the feed will go back to the normal 5-minute schedule.
- The api module is a REST API written using the Django REST Framework to access and alter the saved data of posts.
- For generating documentation, the popular [Mkdocs ](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html) library was used.
