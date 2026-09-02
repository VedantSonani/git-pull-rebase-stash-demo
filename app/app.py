APP_NAME = "Git Demo App"
VERSION = "1.0"
ENVIRONMENT = "production"


def get_message():
    return "Hello from Git Demo App -- Remote"


def get_status():
    return f"{APP_NAME} v{VERSION} ({ENVIRONMENT})"


if __name__ == "__main__":
    print(get_status())
    print(get_message())
