from dependency_injector import containers, providers

from src.config import settings
from src.db.database import Database


class DatabaseContainer(containers.DeclarativeContainer):
    config = providers.Dependency(settings.DatabaseSettings)

    db = providers.Singleton(
        Database,
        url=config.provided.url,
        echo=config.provided.echo
    )
