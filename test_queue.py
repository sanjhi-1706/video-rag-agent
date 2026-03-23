from rq import Queue
from redis import Redis
from app.workers.tasks import test_job   # ✅ IMPORTANT

redis_conn = Redis()
q = Queue(connection=redis_conn)

job = q.enqueue(test_job)

print("📩 Job queued:", job.id)