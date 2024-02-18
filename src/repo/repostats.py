from pathlib import Path
import json
import logging

from .config import REPO_KEY_URL
from .utils import random_sleep, strftime, strptime, nowtime
from .repo import Repo


class RepoStats:
    def __init__(self, filename) -> None:
        self.filename = filename
        self.repos = []
        self.error_repos = []
        self.renamed_repos = {}
        self.links_exists = []

        self._now = nowtime()
        self._lasttime = None
        self._update = False

        self.temp_file = "temp/temp.json"
        self.key_repos = "repositories"
        self.key_error = "error"
        self.key_renamed = "renamed"
        self.key_update = "update_time"
        self.key_renamed_url = "url"
        self.key_renamed_alias = "alias"
        self.key_time = "update_time"

        self._read_file()

    def _read_file(self):
        file = Path(self.filename)
        if file.exists():
            logging.info(f"Read and init file = {file}")
            with open(file) as f:
                data = json.load(f)

            self.repos = data[self.key_repos]
            self.error_repos = data[self.key_error]
            self.renamed_repos = data[self.key_renamed]
            self.links_exists = self.get_repos_links()

            self._lasttime = strptime(data[self.key_update])
            if (self.now - self._lasttime).days >= 1:
                self._update = True

    def query(self, links, tokens):
        temp_file = Path(self.temp_file)
        key_repos = self.key_repos
        key_error = self.key_error

        logging.info(f"Query repo api: repo_list = {len(links)}")
        temp_data = {key_repos: [], key_error: []}
        if temp_file.exists():
            logging.info(f"Read temp file={temp_file}")
            with open(temp_file) as f:
                temp_data = json.load(f)
        else:
            if not temp_file.parent.exists():
                logging.info(f"Create temp file dir {temp_file.parent}")
                temp_file.parent.mkdir(parents=True)

        queried_links = [e[0] for e in temp_data[key_repos]] + temp_data[key_error]
        logging.info(f"Query repo api: queried = {len(queried_links)}")

        total = len(links)
        for idx, repo_url in enumerate(links):
            if repo_url in queried_links:
                continue
            if (idx + 1) % 5 == 0 or idx == 0:
                logging.info(f"Query repo api: round = {idx+1:03d}/{total:03d}")

            random_sleep(idx + 1, step=29, second=29)
            repo = Repo(repo_url)
            repo.query(tokens, sleep=idx % 3 == 0)

            if repo.repo_stats:
                temp_data[key_repos].append([repo_url, repo.repo_stats])
            elif repo.error:
                temp_data[key_error].append(repo_url)
            with open(temp_file, "w") as f:
                json.dump(temp_data, f, indent=2, ensure_ascii=False)

            if repo.is_403:
                logging.info("Query break, status code is 403")
                break

        with open(temp_file, "w") as f:
            json.dump(temp_data, f, indent=2, ensure_ascii=False)
        queried_cnt = len(temp_data[key_repos])
        error_cnt = len(temp_data[key_error])
        logging.info(
            f"Query repo api: queried/error/total = {queried_cnt}/{error_cnt}/{total}"
        )

        temp_repo_data = {
            key_repos: [Repo(url, stats) for url, stats in temp_data[key_repos]],
            key_error: temp_data[key_error],
        }
        return temp_repo_data

    def process(self, links_todo, token=None, retry=5):
        key_repos = self.key_repos
        key_error = self.key_error
        key_renamed_url = self.key_renamed_url
        key_renamed_alias = self.key_renamed_alias
        delta_links = [link for link in links_todo if link not in self.links_exists]

        # omit same update
        if not self._update:
            if len(delta_links) == 0:
                logging.info(f"No update, last update at {self._lasttime}.")
                return False
            else:
                logging.info("Only update new links!")
                links = delta_links
                is_update_all = False
        else:
            logging.info("Update all links!")
            links = links_todo
            is_update_all = True

        if token:
            logging.info(f"Setting headers token={token[:2]}...{token[-1]}")

        # query repo stats
        for i in range(retry):
            logging.info(f">> Retry ... {i+1}/{retry}")
            temp_repo_data = self.query(links, token)
            if len(temp_repo_data[key_repos]) == len(links):
                break
            else:
                random_sleep(1, 1, 180)
        if len(temp_repo_data[key_repos]) != len(links):
            logging.warning("Error repo links count")
            return False
        logging.info(f"Process repo: temp data = {len(temp_repo_data[key_repos])}")

        renamed_repos = self.renamed_repos
        logging.info(f"Before process repo: renamed = {len(renamed_repos)}")

        error_repos = self.error_repos
        logging.info(f"Before process repo: error = {len(error_repos)}")

        repos = {} if is_update_all else self.repos
        for repo in temp_repo_data[key_repos]:
            repo_id = repo.get_id()
            raw_repo_url = repo.get_url_raw()
            new_repo_url = repo.get_url()
            repos[repo_id] = repo.get_stats()

            if new_repo_url != raw_repo_url:
                if repo_id in renamed_repos:
                    renamed_repos[repo_id][key_renamed_alias].append(raw_repo_url)
                else:
                    renamed_repos[repo_id] = {
                        key_renamed_url: new_repo_url,
                        key_renamed_alias: [new_repo_url, raw_repo_url],
                    }
        renamed_repos = {
            k: {
                key_renamed_url: v[key_renamed_url],
                key_renamed_alias: sorted(set(v[key_renamed_alias])),
            }
            for k, v in renamed_repos.items()
        }
        error_repos = sorted(set(error_repos + temp_repo_data[key_error]))

        self.repos = [repos[repo_id] for repo_id in sorted(repos.keys())]
        self.error_repos = error_repos
        self.renamed_repos = renamed_repos
        len_info = (
            f"{len(self.repos)}/{len(self.error_repos)}/{len(self.renamed_repos)}"
        )
        logging.info("Processed repo: total/error/renamed repos = " + len_info)
        return True

    def output(self):
        return {
            self.key_time: strftime(self._now if self._update else self._lasttime),
            self.key_repos: self.repos,
            self.key_error: self.error_repos,
            self.key_renamed: self.renamed_repos,
        }

    def get_repos(self):
        return self.repos

    def get_repos_dict(self):
        return {repo[REPO_KEY_URL]: repo for repo in self.repos} if self.repos else {}

    def get_repos_links(self):
        return [repo[REPO_KEY_URL] for repo in self.repos] if self.repos else []

    def get_error_repos(self):
        return self.error_repos

    def get_renamed_repos(self):
        key_url = self.key_renamed_url
        key_alias = self.key_renamed_alias
        return {
            li: items[key_url]
            for items in self.renamed_repos.values()
            for li in items[key_alias]
            if items[key_url] != li
        }

    @property
    def now(self):
        return self._now

    def save(self):
        stats_file = self.filename
        out = self.output()
        logging.info(f"Save to {stats_file}")
        with open(stats_file, "w") as f:
            json.dump(out, f, indent=2, ensure_ascii=False)
