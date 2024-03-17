import argparse
import logging
from repo import RepoLists, RepoStats


def run(data_dir, doc_dir, csv_dir, readme_file, stats_file, token):
    repolist = RepoLists(data_dir, doc_dir, csv_dir, readme_file)
    links = repolist.get_links()

    repostats = RepoStats(stats_file)
    result = repostats.process(links, token)

    if result:
        repostats.save()
        repolist.rebulid(repostats)

    repolist.update_wiki(repostats)
    repolist.update_readme(repostats)


if __name__ == "__main__":
    fmt = "%(asctime)s %(filename)s %(levelname)s %(message)s"
    logging.basicConfig(level=logging.INFO, format=fmt)

    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="..", type=str)
    parser.add_argument("--token", default=None, type=str)
    args = parser.parse_args()

    token = args.token
    basedir = args.base

    data_dir = f"{basedir}/data"
    doc_dir = f"{basedir}/wiki/docs"
    csv_dir = f"{basedir}/wiki/csv"
    stats_file = f"{basedir}/resource/repo-stats.json"
    readme_file = f"{basedir}/README.md"

    run(data_dir, doc_dir, csv_dir, readme_file, stats_file, token)
