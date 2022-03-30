import os
from pathlib import Path
from typing import List

from app.conf.settings import settings


class FetchAppsModel:

    @classmethod
    def fetch_applications_models(cls):
        apps_models = []
        for app in settings.APPLICATIONS_DIR.iterdir():
            if not app.is_dir():
                continue

            for app_path in [p for p in app.iterdir() if p.name.startswith('models')]:
                if app_path.is_file() and app_path.name.endswith('.py'):
                    apps_models.extend(cls._extract_models_from_app(app_path))
                if app_path.is_dir():
                    apps_models.extend(cls._extract_models_from_app_models_dir(app_path))

        return apps_models

    @classmethod
    def _build_model_path(cls, app_name, models: List[str]):
        root_dir = settings.APPLICATIONS_DIR.parent.name
        apps_folder = settings.APPLICATIONS_DIR.name
        return [f'{root_dir}.{apps_folder}.{app_name}.{model_name}' for model_name in models]

    @classmethod
    def _extract_models_from_app_models_dir(cls, path: Path):
        app_name = path.parent.name
        model_names = [f'models.{model.stem}' for model in path.iterdir() if '__' not in model.name]
        print(model_names)
        return cls._build_model_path(app_name, model_names)

    @classmethod
    def _extract_models_from_app(cls, path: Path):
        app_name = path.parent.name
        model_names = [path.stem]
        return cls._build_model_path(app_name, model_names)



fetch_applications_models = FetchAppsModel.fetch_applications_models