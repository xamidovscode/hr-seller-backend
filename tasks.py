from invoke import task

@task
def build(c):
    c.run("docker compose up --build -d")

@task
def down(c):
    c.run("docker compose down")

