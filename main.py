import json
import sqlite3

import uvicorn
from fastapi import FastAPI

app = FastAPI()


def runserver():
    uvicorn.run(
        app,  # можно передать сам объект app
        host="127.0.0.1",  # или "0.0.0.0" чтобы был доступен извне
        port=8000,
        log_level="info"  # уровень логов: debug / info / warning / error
    )


@app.get("/")
def read_root():
    result = "error"
    with sqlite3.connect('presets.db') as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM presets")
        names = cursor.fetchall()
        result = json.dumps(names)
    return result


@app.get("/{config_name}")
def read_item(config_name: str | None = None):
    result = "error"
    print(config_name)
    with sqlite3.connect('presets.db') as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT json_data FROM presets WHERE name = ?", (config_name,))
        buff = cursor.fetchone()
        if buff:
            result = buff
    return result


if __name__ == "__main__":
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    with sqlite3.connect('presets.db') as connection:
        cursor = connection.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS presets(
        name TEXT PRIMARY KEY NOT NULL,
        json_data JSON NOT NULL
        )''')

        cursor.execute('''
            INSERT OR REPLACE INTO presets(name, json_data)
            VALUES (?, ?) ''',
            (
            "test",
            json.dumps(data)
            ))

        cursor.execute('''
            INSERT OR REPLACE INTO presets(name, json_data)
            VALUES (?, ?) ''',
            (
            "test2",
            json.dumps(data)
            ))

        cursor.execute("SELECT * FROM presets")
        presets = cursor.fetchall()
        print(presets)

        runserver()
