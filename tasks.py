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


def _user_cmd(role, username, full_name, password, phone, percentage, duration):
    cmd = (
        f"python scripts/create_user.py {role}"
        f" --username {username}"
        f' --full-name "{full_name}"'
        f" --password {password}"
    )
    if phone:
        cmd += f" --phone {phone}"
    if role == "seller":
        cmd += f" --percentage {percentage} --duration {duration}"
    return cmd


@task(
    help={
        "username": "Login uchun username",
        "full-name": "To'liq ismi",
        "password": "Parol",
        "phone": "Telefon raqam (ixtiyoriy)",
        "percentage": "Foiz (default: 0)",
        "duration": "Muddat oyda (default: 0)",
        "docker": "Docker konteyner ichida ishlatish",
    }
)
def create_seller(
    c,
    username,
    full_name,
    password,
    phone=None,
    percentage=0,
    duration=0,
    docker=False,
):
    """Yangi seller yaratish."""
    cmd = _user_cmd("seller", username, full_name, password, phone, percentage, duration)
    if docker:
        c.run(f"docker exec hr-seller-endpoints {cmd}")
    else:
        c.run(cmd)


@task(
    help={
        "username": "Login uchun username",
        "full-name": "To'liq ismi",
        "password": "Parol",
        "phone": "Telefon raqam (ixtiyoriy)",
        "docker": "Docker konteyner ichida ishlatish",
    }
)
def create_admin(
    c,
    username,
    full_name,
    password,
    phone=None,
    docker=False,
):
    """Yangi admin yaratish."""
    cmd = _user_cmd("admin", username, full_name, password, phone, 0, 0)
    if docker:
        c.run(f"docker exec hr-seller-endpoints {cmd}")
    else:
        c.run(cmd)

