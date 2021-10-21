import enum
import pathlib

import ujson
from pydantic import BaseModel


class URL(enum.Enum):
    DB_URL_INSIDE_CONTAINER = 'postgres://admin:admin1234@db/phone_numbers_database'
    DB_URL_OUTSIDE_CONTAINER = 'postgres://admin:admin1234@localhost:5432/phone_numbers_database'


class Codes(enum.Enum):
    """Codes for responses"""
    PHONE_NUMBER_IS_BLOCKED = 1
    PHONE_NUMBER_IS_NOT_BLOCKED = 0


class ProjectSettings(BaseModel):
    debug: bool
    excel_file_path: str

    project_dir = pathlib.Path(__file__).parent.parent.resolve()

    @classmethod
    def load_project_settings(cls, config_path: pathlib.Path) -> 'ProjectSettings':
        """Load all required settings for project from config.json"""
        project_config = ujson.load(config_path.open('r'))
        return cls(
            debug=project_config.get('debug'),
            excel_file_path=project_config.get('excel_file_path'),
        )


settings = ProjectSettings.load_project_settings(pathlib.Path('./config.json'))
