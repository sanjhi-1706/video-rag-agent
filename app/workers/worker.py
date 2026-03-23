import os
from rq import Worker, Queue
from redis import Redis

# 🔥 FIX FOR MAC (IMPORTANT)
os.environ["OBJC_DISABLE_INITIALIZE_FORK_SAFETY"] = "YES"

redis_conn = Redis()

if __name__ == "__main__":
    print("🚀 Worker starting...")

    worker = Worker(
        [Queue(connection=redis_conn)],
        connection=redis_conn
    )

    print("👷 Worker listening on 'default' queue...")
    worker.work(with_scheduler=False)