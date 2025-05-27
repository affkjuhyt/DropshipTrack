from datetime import timedelta

broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/0'

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'UTC'
enable_utc = True

# Task routes
task_routes = {
    'tasks.*': {'queue': 'default'}
}

# Beat schedule
beat_schedule = {
    'example-task': {
        'task': 'tasks.example',
        'schedule': timedelta(minutes=30),
    },
}