from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="STARTELEBOT",
    settings_files=["settings.toml", ".secrets.toml"],
    load_dotenv=True,
    environments=True,
    env_switcher="STARTELEBOT_ENV"
)

print(f"Config iniciada em modo: {settings.current_env}")
