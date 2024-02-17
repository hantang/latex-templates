import argparse
import logging
from repo import RepoLists, RepoStats


def run(datadir, docdir, csvdir, readme_file, stats_file, token):
    repolist = RepoLists(datadir, docdir, csvdir, readme_file)
    links = repolist.get_links()

    repostats = RepoStats(stats_file, links)
    if repostats.process(token):
        repostats.save()
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
    
    datadir = f"{basedir}/data"
    docdir = f"{basedir}/wiki/docs"
    csvdir = f"{basedir}/wiki/csv"
    stats_file = f"{basedir}/resource/repo-stats.json"
    readme_file = f"{basedir}/README.md"

    run(datadir, docdir, csvdir, readme_file, stats_file, token)
