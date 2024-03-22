import json
import logging
import re
from pathlib import Path

import pandas as pd

from .config import COLUMN_RENAME, NAME_MAP, REPO_STRUCTS, COLUMNS2, COLUMNS
from .repostats import RepoStats
from .utils import strftime, strip_url, strip, strptime, get_pinyin_key

TAG_ARCHIVED = "📦"  # :package:
TAG_OBSOLETE = "🔒️"  # :lock:
TAG_REMOVED = "🗑️"  # :wastebasket:
REPO_STATS_URL = "https://flat.badgen.net/github"
REPO_STATS_KEYS = ["stars", "forks", "last-commit", "license"]


def _get_status_obsolete(repo_info, date_now, date_gap=1461):
    """4 years = 365*4 + 1 = 1461"""
    date_update = max([repo_info[key] for key in ["pushed_at", "created_at"]])
    date_update = strptime(date_update)
    if (date_now - date_update).days > date_gap:
        return TAG_OBSOLETE
    return None


def _get_status_archive(repo_info):
    return TAG_ARCHIVED if repo_info["archived"] else None


def _get_score(stargazers, fork):
    return stargazers + fork * 2


def _get_badges(repo, pushed_at, created_at, stargazers, forks, license_name):
    values = [stargazers, forks, pushed_at, license_name]

    badges = []
    for key, val in zip(REPO_STATS_KEYS, values):
        badges.append(f"![{key}={val}]({REPO_STATS_URL}/{key}/{repo})")
    badges = " ".join(badges)
    return f"🎉`{created_at}` {badges}".rstrip()


def _get_description(description):
    return strip(
        re.sub(r"\\(latex)\\?", r"\1", description, flags=re.IGNORECASE)
        if description
        else description
    )


def _get_desc(archived, obsolete, description):
    tags = "/".join([v for v in [archived, obsolete] if v])
    desc = " ".join([tags, (f"`{description}`" if description else "")])
    return desc.strip()


def _get_title(zh_name, en_name, repository):
    return f"**{zh_name}**（{en_name}）: {repository}" if zh_name else repository


def to_df(entries, repo_dict, date_now):
    logging.debug(f"to df: entries={len(entries)}, repo_dict={len(repo_dict)}, date_now={date_now}")
    out = []
    for entry in entries:
        out_entries = []
        archived_cnt = 0
        obsolete_cnt = 0
        for link in entry["links"]:
            if link not in repo_dict:
                logging.warning(f"Missing link = {link}")
                continue
            repo_info = repo_dict[link]
            archived = _get_status_archive(repo_info)
            obsolete = _get_status_obsolete(repo_info, date_now)
            if archived:
                archived_cnt += 1
            if obsolete:
                obsolete_cnt += 1
            full_name, url = repo_info["full_name"], repo_info["html_url"]
            # TODO COLUMNS
            result = {
                "zh": entry.get("zh"),
                "en": entry.get("en"),
                "count": len(entry["links"]),
                "repository": f"[{full_name}]({url})",
                "archived": archived,
                "obsolete": obsolete,
                "stargazers": repo_info["stargazers_count"],
                "forks": repo_info["forks_count"],
                # "subscribers":repo_info["subscribers_count"],
                "pushed_at": repo_info["pushed_at"].split("T")[0],
                "created_at": repo_info["created_at"].split("T")[0],
                # "updated_at": repo_info["updated_at"].split("T")[0],
                "license": repo_info["license_name"],
                "description": _get_description(repo_info["description"]),
            }
            # more
            result["score"] = _get_score(result["stargazers"], result["forks"])
            result["badges"] = _get_badges(
                repo_info["full_name"],
                result["pushed_at"],
                result["created_at"],
                result["stargazers"],
                result["forks"],
                result["license"],
            )
            result["desc"] = _get_desc(archived, obsolete, result["description"])
            result["title"] = _get_title(
                result["zh"], result["en"], result["repository"]
            )
            out_entries.append(result)
        for res in out_entries:
            res["count"] = "{}/{}/{}".format(res["count"], archived_cnt, obsolete_cnt)
        out.extend(out_entries)
    if len(out) == 0:
        df = pd.DataFrame(data=None, columns=COLUMNS)
    else:
        df = pd.DataFrame(out)
    df = df.fillna(" ").astype(str)
    df = df.reset_index()
    return df


def to_list(df_entry, top=10, order=True):
    key = "score"
    df_entry[key] = df_entry[key].astype("int")
    df_entry2 = df_entry[df_entry[key] > 0]
    if order:
        df_entry2 = df_entry2.sort_values([key, "pushed_at", "created_at"], ascending=False)
    if top > 0:
        df_entry2 = df_entry2.head(top)

    texts = []
    blank = " " * 2
    entries = df_entry2.to_dict("records")
    for e in entries:
        texts.append("- " + e["title"])
        texts.extend([f"{blank}- {v}" for v in [e["desc"], e["badges"]] if v])
    if len(df_entry2) < len(df_entry):
        texts.append("- ...")
    return texts


class RepoList:
    def __init__(self, data_dir, config, is_thesis=True) -> None:
        self.data_dir = data_dir
        self.config = config
        self.is_thesis = is_thesis

        self.key_zh = "zh"
        self.key_en = "en"
        self.key_links = "links"

        self.name = self._init_file()
        self.file = Path(self.data_dir, self.name)
        self.groups = self._init_groups()
        self.data = self._read_file()

    def _init_file(self):
        config = self.config
        return config["name"] + ".json"

    def _init_groups(self):
        config = self.config
        if "categories" in config:
            categories = config["categories"]
            return [[group, categories] for group in config["groups"]]
        else:
            return config["groups"]

    def _read_file(self):
        file = self.file
        if not file.exists():
            logging.warning("Error file `{file}` does not exist")
            return None

        logging.info(f"Read file `{file}`")
        with open(file) as f:
            return json.load(f)

    def get_links(self):
        links = []
        repo_data = self.data
        if not repo_data:
            return links
        for _, group_values in repo_data.items():
            for _, cate_values in group_values.items():
                for entry in cate_values:
                    links.extend([strip_url(link) for link in entry[self.key_links]])
        return links

    def update_data(self, stats, dup_links):
        file = self.file
        repo_data = self.data
        groups = self.groups

        error_links = stats.get_error_repos()
        renamed_links_dict = stats.get_renamed_repos()

        logging.info(f"Process file = {file}")
        out_repo_data = {}
        for group, categories in groups:
            for cate in categories:
                entries = []
                for entry in repo_data[group][cate]:
                    links2 = []
                    for link in entry[self.key_links]:
                        link = strip_url(link)
                        if link in dup_links:
                            logging.info(f"Duplicated repo: {link}")
                            continue
                        if link in renamed_links_dict:
                            link2 = renamed_links_dict[link]
                            logging.info(f"Renamed repo: {link} -> {link2}")
                            link = link2
                        if link in error_links:
                            logging.info(f"Error repo: {link}")
                            continue

                        dup_links.append(link)
                        links2.append(link)

                    entry2 = {}
                    if self.key_zh in entry:
                        entry2[self.key_zh] = entry[self.key_zh]
                        entry2[self.key_en] = entry[self.key_en]
                    entry2[self.key_links] = sorted(links2)
                    entries.append(entry2)

                entries = sorted(entries, key=get_pinyin_key)  # TODO
                if group not in out_repo_data:
                    out_repo_data[group] = {}
                out_repo_data[group][cate] = entries

        self.data = out_repo_data
        return dup_links

    def save(self):
        file = self.file
        out_repo_data = self.data
        logging.info(f"Rebuild file = {file}")
        with open(file, "w") as fw:
            json.dump(out_repo_data, fw, indent=2, ensure_ascii=False)

    def _to_df(self, stats: RepoStats):
        repo_data = self.data
        groups = self.groups
        date_now = stats.now
        repo_dict = stats.get_repos_dict()
        logging.info(f"stats repo dict = {len(repo_dict)}")

        df_list = []
        for group, categories in groups:
            for cate in categories:
                entries = repo_data[group][cate]
                df = to_df(entries, repo_dict, date_now)
                df_list.append((group, cate, df))
        return df_list

    def save_wiki(self, doc_dir, csv_dir, stats):
        csv_dir = Path(csv_dir)
        doc_dir = Path(doc_dir)
        if not csv_dir.exists():
            logging.info(f"Make dir {csv_dir}")
            csv_dir.mkdir(parents=True)
        if not doc_dir.exists():
            logging.info(f"Make dir {doc_dir}")
            doc_dir.mkdir(parents=True)

        columns = COLUMNS2
        if not self.is_thesis:
            columns = columns[2:]
        df_list = self._to_df(stats)
        md_texts = {}
        logging.info("Save to wiki csv")
        for group, cate, df in df_list:
            group_name = NAME_MAP[group]
            cate_name = NAME_MAP[cate]
            savefile = Path(csv_dir, f"{group_name}-{cate_name}.csv")
            logging.info(f"Save to csv to {savefile}")
            df2 = df[["index"] + columns].rename(columns=COLUMN_RENAME)
            df2.to_csv(savefile, index=False)
            if group not in md_texts:
                md_texts[group] = [f"# {group}"]
            md_texts[group].extend(
                [
                    f"## {cate}",
                    f'{{{{ read_csv("../{csv_dir.name}/{savefile.name}") }}}}',
                ]
            )

        logging.info("Save to wiki docs")
        for group, texts in md_texts.items():
            group_name = NAME_MAP[group]
            savefile = Path(doc_dir, f"{group_name}.md")
            logging.info(f"Save to markdown to {savefile}")
            with open(savefile, "w") as fw:
                fw.write("\n\n".join(texts).strip() + "\n")

    def get_thesis_list(self, stats, zh=True, latex=True, top=10):
        topic1 = "学位论文模板"
        topic2 = "LaTeX"
        groups = self.groups[:2] if zh else self.groups[2:4]
        df_list = self._to_df(stats)

        keywords = []
        for group, categories in groups:
            for cate in categories:
                if topic1 not in cate:
                    continue
                if latex and topic2 in cate:
                    keywords.append((group, cate))
                if not latex and topic2 not in cate:
                    keywords.append((group, cate))
        df = [df for group, cate, df in df_list if (group, cate) in keywords]
        df = pd.concat(df)
        out = to_list(df, top=top)

        toc = []
        texts = []
        prefix = "" if latex else "非"
        if out:
            header = f"### {topic1}（{prefix}{topic2}）"
            toc.append(header)
            texts = ["", header, ""] + out
        return toc, texts

    def get_other_list(self, stats, top=5):
        details = ["<details>\n<summary>点击展开</summary>", "</details>"]
        groups = self.groups
        df_list = self._to_df(stats)

        keywords = [group for group, _ in groups]
        toc = []
        texts = []
        for group, cate, df in df_list:
            if group not in keywords:
                continue
            out = to_list(df, top=top)
            if out:
                header = f"### {cate}"
                toc.append(header)
                texts.extend(["", header, "", details[0], ""] + out + ["", details[1]])
        return toc, texts


class RepoLists:
    def __init__(self, data_dir, doc_dir, csv_dir, readme_file) -> None:
        self.data_dir = data_dir
        self.doc_dir = doc_dir
        self.csv_dir = csv_dir
        self.readme_file = readme_file

        self.thesis_repo_list = RepoList(data_dir, REPO_STRUCTS[0], is_thesis=True)
        self.other_repo_list = RepoList(data_dir, REPO_STRUCTS[1], is_thesis=False)

    def get_links(self):
        links1 = self.thesis_repo_list.get_links()
        links2 = self.other_repo_list.get_links()

        links = sorted(set(links1 + links2))
        return links

    def rebulid(self, stats: RepoStats):
        dup_links = []
        dup_links = self.thesis_repo_list.update_data(stats, dup_links)
        dup_links = self.other_repo_list.update_data(stats, dup_links)
        logging.info(f"dup links = {len(dup_links)}")

        self.thesis_repo_list.save()
        self.other_repo_list.save()

    def update_wiki(self, stats: RepoStats):
        self.thesis_repo_list.save_wiki(self.doc_dir, self.csv_dir, stats)
        self.other_repo_list.save_wiki(self.doc_dir, self.csv_dir, stats)

    def update_readme(self, stats: RepoStats):
        logging.info("Update README file")
        toc = ["## 说明"]
        head_list = [
            "## 最受欢迎的LaTeX学位论文模板（中文）",
            "## 最受欢迎LaTeX学位论文模板（其他）",
            "## 更多模板资源",
        ]
        wiki = [
            "# Beyond LaTeX Templates",
            "**Welcome to awesome latex-templates wiki!**",
        ]
        update_date = strftime(stats.now, fmt="%Y-%m-%d")
        logging.info(f"Update time={update_date}")

        readme_file = self.readme_file
        if not Path(readme_file).exists():
            logging.warning(f"Readme file {readme_file} does not exist")
            return

        # list
        thesis = self.thesis_repo_list
        toc0a, text0a = thesis.get_thesis_list(stats, True, latex=True, top=25)
        toc0b, text0b = thesis.get_thesis_list(stats, True, latex=False, top=15)
        toc1a, text1a = thesis.get_thesis_list(stats, False, latex=True, top=15)
        toc1b, text1b = thesis.get_thesis_list(stats, False, latex=False, top=10)

        toc2, text2 = self.other_repo_list.get_other_list(stats, top=5)

        # toc
        toc += [head_list[0]] + toc0a + toc0b
        toc += [head_list[1]] + toc1a + toc1b
        toc += [head_list[2]] + toc2
        toc_list = []
        for line in toc:
            hashtag, title = re.findall(r"(#+) (.+)", line)[0]
            hash_len = (len(hashtag) - 2) * 2
            title2 = title.lower().replace(" ", "-")
            title2 = re.sub("[（）()]", "", title2)
            toc_list.append("{}- [{}](#{})".format(" " * hash_len, title, title2))

        # sections        
        sections = ["lastmod", "toc", "toplist0", "toplist1", "toplist2"]
        paragraphs = [
            f"最近更新：*{update_date}*",
            "\n".join(toc_list),
            "\n".join([head_list[0]] + text0a + text0b),
            "\n".join([head_list[1]] + text1a + text1b),
            "\n".join([head_list[2]] + text2),
        ]

        # update readme
        logging.info(f"Read {readme_file}")
        with open(readme_file) as f:
            text = f.read()

        for sec, para in zip(sections, paragraphs):
            logging.info(f"sec = {sec}")
            begin, end = f"<!-- {sec} -->", f"<!-- end-{sec} -->"
            pattern = rf"{begin}(.|\n)+{end}"
            to = "\n\n".join([begin, para, end])
            text = re.sub(pattern, lambda m: to, text)

        logging.info(f"Save to {readme_file}")
        with open(readme_file, "w") as fw:
            fw.write(text)

        # update wiki/index.md
        wiki_file = Path(self.doc_dir, "index.md")
        wiki = wiki + paragraphs[2:4]
        logging.info(f"Save to wiki: {wiki_file}")
        with open(wiki_file, "w") as fw:
            fw.write("\n\n".join(wiki) + "\n")
