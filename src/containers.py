from dependency_injector import containers, providers

from src.config import settings
from src.db.containers import DatabaseContainer


class AppContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[])

    database = providers.Container(DatabaseContainer, config=settings.db)
