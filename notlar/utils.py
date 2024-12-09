import json
import os
from django.conf import settings


def read_json_file():
    json_path = os.path.join(
        settings.BASE_DIR, "notlar", "universities.json"
    )  # JSON dosyasının yolu
    with open(json_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data  # Veriyi geri döndür
