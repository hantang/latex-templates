import logging
import traceback
import requests

from .config import REPO_KEY_ID, REPO_KEY_URL, REPO_KEYS
from .utils import get_headers, random_sleep, strip_url


def _get_repo_topics(data):
    return {"topic_list": ", ".join(data["topics"])}


def _get_repo_license(data):
    license_name = data["license"]
    return {"license_name": license_name.get("spdx_id") if license else None}  # name


def _get_repo_owner(data):
    return {
        "owner_id": data["owner"]["id"],
        "owner_name": data["owner"]["login"],
        "owner_type": data["owner"]["type"],
    }


def query_github_repo(repo_url, tokens=None):
    api_base = "https://api.github.com/repos"
    api_domain = "github.com/"
    headers = get_headers(tokens)

    repo_name = repo_url.split(api_domain)[-1].strip("/")
    api_url = f"{api_base}/{repo_name}"
    repo_stats = None
    try:
        response = requests.get(api_url, headers=headers)
    except Exception:
        return repo_stats, 403

    if response.status_code == 200:
        repo_data = response.json()
        repo_stats = {key: repo_data.get(key) for key in REPO_KEYS}
        repo_stats[REPO_KEY_URL] = strip_url(repo_stats[REPO_KEY_URL])
        repo_stats.update(_get_repo_owner(repo_data))
        repo_stats.update(_get_repo_topics(repo_data))
        repo_stats.update(_get_repo_license(repo_data))
    else:
        logging.warning(f"Error: repo={repo_name}, status_code={response.status_code}")
    return repo_stats, response.status_code


def get_repo_stats_id(repo_stats):
    return str(repo_stats[REPO_KEY_ID])


def get_repo_stats_url(repo_stats):
    return repo_stats[REPO_KEY_URL]


class Repo:
    def __init__(self, url, stats=None) -> None:
        self.url = url
        self.repo_stats = {} if stats is None else stats
        self.error = False
        self.is_403 = False

    def query(self, tokens, sleep=False):
        try:
            stats, status_code = query_github_repo(self.url, tokens)
            if status_code == 200:
                self.repo_stats = stats
            else:
                logging.info(f"Error, status_code={status_code}, url={self.url}")
                if status_code == 403:
                    self.is_403 = True
                else:
                    self.error = True
        except Exception:
            traceback.print_exc()
        if sleep:
            random_sleep(1, step=1, second=2)

    def get_stats(self):
        return self.repo_stats

    def get_id(self):
        return str(self.repo_stats[REPO_KEY_ID])

    def get_url(self):
        return self.repo_stats[REPO_KEY_URL]

    def get_url_raw(self):
        return self.url
