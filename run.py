import os
import shutil
import subprocess
import sys


VECTOR_DB_PATH = "/vector_db"


def reset_vector_db():
    if os.path.exists(VECTOR_DB_PATH):
        print("Удаляем старую vector_db...")
        shutil.rmtree(VECTOR_DB_PATH)
    print("vector_db очищена")


def ingest():
    print("Запуск ingest (загрузка лекций)...")
    subprocess.run([sys.executable, "-m", "rag.ingest"], check=True)


def start_api():
    print("Запуск API сервера...")
    subprocess.run(
        ["uvicorn", "api.main:app", "--reload", "--port", "8000"],
        check=True
    )


if __name__ == "__main__":

    reset_vector_db()

    ingest()

    start_api()