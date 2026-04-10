import threading
from worker_cnpj import start_worker as start_cnpj_worker
from worker_db import start_worker as start_db_worker


if __name__ == "__main__":
    t1 = threading.Thread(target=start_cnpj_worker)
    t2 = threading.Thread(target=start_db_worker)

    t1.start()
    t2.start()

    t1.join()
    t2.join()
