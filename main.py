import json
import logging
import sqlite3
from typing import List

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class ConfigData(BaseModel):
    A: List[str]
    B: List[str]
    C: List[str]
    D: List[str]
    E: List[str]
    F: List[str]


def runserver():
    uvicorn.run(
        app,  # можно передать сам объект app
        host="0.0.0.0",  # или "0.0.0.0" чтобы был доступен извне
        port=63421,
        log_level="info"  # уровень логов: debug / info / warning / error
    )


@app.get("/")
def read_root():
    logging.log(level=logging.INFO, msg=f"read_root")
    with sqlite3.connect('presets.db') as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM presets")
        names = cursor.fetchall()
        name_list = [row[0] for row in names]

        return name_list


@app.get("/{config_name}")
def read_config(config_name: str):
    logging.log(level=logging.INFO, msg=f"read_config: {config_name}")
    with sqlite3.connect('presets.db') as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT json_data FROM presets WHERE name = ?", (config_name,))
        buff = cursor.fetchone()
        if buff and buff[0]:
            return json.loads(buff[0])
    return {"error": "Config not found"}


@app.post("/{config_name}")
def write_config(config_name: str, payload: ConfigData):
    logging.log(level=logging.INFO, msg="write_config: {config_name}")
    data_json = json.dumps(payload.model_dump(), ensure_ascii=False, indent=None)
    with sqlite3.connect('presets.db') as connection:
        cursor = connection.cursor()
        cursor.execute('''
                    INSERT OR REPLACE INTO presets(name, json_data)
                    VALUES (?, ?) ''',
                       (
                           config_name,
                           data_json
                       )
                       )
        connection.commit()
    return {
        "status": "success",
        "config_name": config_name,
        "message": "Данные успешно сохранены"
    }


if __name__ == "__main__":
    with sqlite3.connect('presets.db') as connection:
        cursor = connection.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS presets(
        name TEXT PRIMARY KEY NOT NULL,
        json_data JSON NOT NULL
        )''')

    runserver()
