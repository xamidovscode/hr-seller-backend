from invoke import task


@task
def build(c):
    c.run("docker compose up --build -d")


@task
def down(c):
    c.run("docker compose down")


@task
def migrate(c):
    c.run("docker compose exec hr-seller-api alembic upgrade head")

