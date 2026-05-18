import subprocess
from invoke import task


DOCKER_CONTAINER = "hr-seller-endpoints"


def _is_docker_running():
    try:
        result = subprocess.run(
            ["docker", "inspect", "-f", "{{.State.Running}}", DOCKER_CONTAINER],
            capture_output=True, text=True
        )
        return result.stdout.strip() == "true"
    except FileNotFoundError:
        return False


def _run_script(c, args: str):
    cmd = f"python scripts/create_user.py {args}"
    if _is_docker_running():
        c.run(f"docker exec {DOCKER_CONTAINER} {cmd}")
    else:
        c.run(cmd)


@task
def build(c):
    c.run("docker compose up --build -d")


@task
def down(c):
    c.run("docker compose down")


@task
def migrate(c):
    c.run("docker exec hr-seller-endpoints alembic upgrade head")


@task
def run(c):
    c.run("uvicorn app.main:app --reload")


@task
def create_seller(c):
    """seller/seller username va parol bilan seller yaratish."""
    _run_script(c, 'seller --username seller --full-name "Seller User" --password seller')


@task
def create_admin(c):
    """admin/admin username va parol bilan admin yaratish."""
    _run_script(c, 'admin --username admin --full-name "Admin User" --password admin')


@task
def worker(c):
    """Celery worker'ni local'da ishga tushirish."""
    c.run("celery -A app.core.celery.celery_app worker --loglevel=info --concurrency=4")


@task
def beat(c):
    """Celery beat'ni local'da ishga tushirish."""
    c.run("celery -A app.core.celery.celery_app beat --loglevel=info")


@task
def flower(c):
    """Celery flower monitoring UI (http://localhost:5555)."""
    c.run("celery -A app.core.celery.celery_app flower --port=5555")
