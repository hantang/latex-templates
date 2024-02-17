from itertools import chain
import logging
import random
import re
import time
import pypinyin


def strip(s, blank=True):
    if s is None:
        return s
    return re.sub(r"\s+", " " if blank else "", s).strip()


def strip_url(link):
    return strip(link, False).rstrip("/")


def get_pinyin_key(val):
    if isinstance(val, dict):
        val = val.get("zh", "")

    if isinstance(val, str) and val:
        """chinese chars to pinyin"""
        s = val
        o = re.sub(r"[（）]", "", s)
        o = "".join(chain.from_iterable(pypinyin.pinyin(o, style=pypinyin.Style.TONE3)))
        if s.startswith("（"):
            o = "~" + o
        val = o
    return val


def random_sleep(idx, step=10, second=5):
    if idx % step == 0:
        s = random.randint(max(1, second // 4), max(second, 1))
        logging.info(f"Step={idx}/{step}, sleep {s}/{second} seconds")
        time.sleep(s)
        return True
    return False


def get_headers(tokens=None):
    headers = None
    if tokens:
        tokens = tokens.split(",")
        token = random.choice(tokens)
        logging.info(f"Setting headers token={token[:2]}...{token[-1]}")
        # headers = {
        #     "Accept": "application/vnd.github.v3+json",
        #     "Authorization": f"Bearer {token}",
        #     "X-GitHub-Api-Version": "2022-11-28",
        # }
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
        }
    return headers
