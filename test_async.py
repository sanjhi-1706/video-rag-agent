from rq import Queue
from redis import Redis
from app.workers.tasks import process_video

redis_conn = Redis()
q = Queue(connection=redis_conn)

url = input("Enter YouTube URL: ")

job = q.enqueue(process_video, url)

print("📩 Job queued:", job.id)