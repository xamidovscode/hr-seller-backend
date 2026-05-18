import gzip
import os
import sys
import shutil
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import httpx

from app.core.settings import settings

BACKUP_CHAT_ID = "7478155511"


def pg_dump(dest_path: str) -> None:
    env = os.environ.copy()
    env["PGPASSWORD"] = settings.DB_PASSWORD

    cmd = [
        "pg_dump",
        "-h", settings.DB_HOST,
        "-p", str(settings.DB_PORT),
        "-U", settings.DB_USER,
        "-d", settings.DB_NAME,
        "--no-password",
        "-F", "p",
    ]

    with gzip.open(dest_path, "wb") as gz_file:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        if proc.returncode != 0:
            raise RuntimeError(f"pg_dump xatosi: {proc.stderr.decode()}")
        gz_file.write(proc.stdout)


def send_to_telegram(file_path: str, caption: str) -> None:
    url = f"https://api.telegram.org/bot{settings.SUPPORT_BOT_TOKEN}/sendDocument"
    with open(file_path, "rb") as f:
        response = httpx.post(
            url,
            data={"chat_id": BACKUP_CHAT_ID, "caption": caption},
            files={"document": (os.path.basename(file_path), f, "application/gzip")},
            timeout=120,
        )
    response.raise_for_status()


def run() -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"seller.sql.gz"

    tmp_dir = tempfile.mkdtemp()
    try:
        dest_path = os.path.join(tmp_dir, filename)
        print(f"Backup boshlandi: {filename}")

        pg_dump(dest_path)

        size_mb = os.path.getsize(dest_path) / 1024 / 1024
        caption = f"🗄 DB Backup\n📦 {filename}\n📏 {size_mb:.2f} MB\n🕐 {timestamp}"

        send_to_telegram(dest_path, caption)
        print(f"Backup yuborildi: {filename} ({size_mb:.2f} MB)")

    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == "__main__":
    run()