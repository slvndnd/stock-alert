import json
import os


class StateStore:

    def __init__(self, path="data/status.json"):
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)

        if not os.path.exists(path):
            self._write({})

    def load(self):

        if not os.path.exists(self.path):
            return {}

        try:
            with open(self.path, "r", encoding="utf-8") as f:
                content = f.read().strip()

                if not content:
                    return {}

                return json.loads(content)

        except json.JSONDecodeError:
            print("⚠️ JSON corrompu détecté → reset state")

            # backup du fichier cassé
            backup_path = self.path + ".corrupt"
            try:
                os.rename(self.path, backup_path)
            except:
                pass

            return {}

    def save(self, data):

        tmp_path = self.path + ".tmp"

        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        # 🔥 écriture atomique (TRÈS important)
        os.replace(tmp_path, self.path)

    def _write(self, data):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)