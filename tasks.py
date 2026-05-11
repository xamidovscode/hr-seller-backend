from invoke import task


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