import csv
import json
from dataclasses import fields
from io import BytesIO
from typing import List, Dict, Any

import aiofiles

from app.mongodb.models import UserMongo


class ExportManager:

    def __init__(self, users: List[UserMongo]) -> None:
        self.rows = []
        self.users = users
        self.buffer = BytesIO()

    def _get_users_list(self) -> List[Dict[str, Any]]:
        """
        Convert the list of UserMongo objects to a list of dictionaries.
        """
        user_list = []
        for user in self.users:
            del user.message_silent_id
            del user.message_thread_id
            del user.message_silent_mode
            user_list.append(user.to_dict())
        return user_list

    async def save_as_json(self) -> bytes:
        """
        Save the data as a JSON file and return the file content as bytes.

        Returns:
            bytes: The content of the JSON file as bytes.
        """
        async with aiofiles.tempfile.NamedTemporaryFile("w+", suffix=".json", delete=True) as f:
            data = json.dumps(self._get_users_list(), ensure_ascii=False, indent=2, sort_keys=True)
            await f.write(data)
            await f.seek(0)
            self.buffer = f.buffer.read()

        return self.buffer

    async def save_as_csv(self):
        async with aiofiles.tempfile.NamedTemporaryFile("w+", suffix=".csv", delete=True) as f:
            excluded_fields = ["message_silent_id", "message_thread_id", "message_silent_mode"]
            fieldnames = [field.name for field in fields(UserMongo) if field.name not in excluded_fields]

            writer = csv.DictWriter(f, fieldnames, restval="null", quoting=csv.QUOTE_ALL)
            await writer.writeheader()
            users_list = self._get_users_list()

            for user in users_list:
                user_data = {field.name: getattr(user, field.name)
                             for field in fields(UserMongo) if
                             field.name not in excluded_fields}
                await writer.writerow(user_data)
            await f.seek(0)
            self.buffer = f.buffer.read()

        return self.buffer
