import requests


class BaseScraper:

    headers = {
        "User-Agent":
        "Mozilla/5.0"
    }

    def download(self, url):

        response = requests.get(
            url,
            headers=self.headers,
            timeout=30
        )

        response.raise_for_status()

        return response.text