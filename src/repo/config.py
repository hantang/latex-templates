REPO_STRUCTS = [
    {
        "name": "thesis-templates",
        "groups": [
            "中国内地（大陆）高校",
            "中国港澳台地区高校",
            "美国地区高校",
            "其他国家（地区）高校",
        ],
        "categories": [
            "学位论文模板（LaTeX/Lyx）",
            "学位论文模板（Markdown）",
            "学位论文模板（Microsoft Word）",
            "学位论文模板（Typst）",
            "学位论文开题和选题报告（LaTeX/Lyx）",
            "学术演示文稿（LaTeX Beamer）",
        ],
    },
    {
        "name": "other-templates",
        "groups": [
            [
                "更多LaTeX/Lyx模板",
                ["LaTeX论文模板", "LaTeX简历模板", "LaTeX通用模板", "LaTeX绘图示例"],
            ],
            ["更多非LaTeX模板", ["Typst写作模板", "Markdown写作模板", "其他写作模板"]],
            [
                "补充资料",
                ["LaTeX资源", "Typst资源", "Markdown资源", "文献引用", "排版相关"],
            ],
        ],
    },
]

NAME_MAP = {
    "中国内地（大陆）高校": "region-zhs",
    "中国港澳台地区高校": "region-zht",
    "美国地区高校": "region-usa",
    "其他国家（地区）高校": "region-else",
    "更多LaTeX/Lyx模板": "more-latex",
    "更多非LaTeX模板": "more-stuff",
    "补充资料": "supplement",
    "学位论文模板（LaTeX/Lyx）": "thesis-latex",
    "学位论文模板（Markdown）": "thesis-markdown",
    "学位论文模板（Microsoft Word）": "thesis-msword",
    "学位论文模板（Typst）": "thesis-typst",
    "学位论文开题和选题报告（LaTeX/Lyx）": "report-latex",
    "学术演示文稿（LaTeX Beamer）": "presentation-latex",
    "LaTeX简历模板": "resume",
    "LaTeX绘图示例": "drawing",
    "LaTeX论文模板": "papers",
    "LaTeX通用模板": "commons",
    "Microsoft Word写作模板": "msword",
    "Markdown写作模板": "markdown",
    "Typst写作模板": "typst",
    "其他写作模板": "others",
    "LaTeX资源": "latex",
    "Markdown资源": "markdown",
    "Typst资源": "typst",
    "排版相关": "typography",
    "文献引用": "reference",
}

REPO_KEYS = [
    "id",
    "html_url",
    "full_name",
    "name",
    "owner_name",
    "owner_id",
    "owner_type",
    "homepage",
    "language",
    "description",
    "license_name",
    "topic_list",
    "pushed_at",
    "created_at",
    "updated_at",
    "stargazers_count",
    "forks_count",
    "watchers_count",
    "open_issues_count",
    "network_count",
    "subscribers_count",
    "archived",
    "disabled",
    "fork",
    "is_template",
    "private",
    "visibility",
]

REPO_KEY_ID = REPO_KEYS[0]
REPO_KEY_URL = REPO_KEYS[1]

COLUMNS = [
    "zh",
    "en",
    "count",
    "repository",
    "archived",
    "obsolete",
    "stargazers",
    "forks",
    "pushed_at",
    "created_at",
    "license",
    "description",
    "score",
    "badges",
    "desc",
    "title",
]

COLUMNS2 = COLUMNS[:12]

COLUMN_RENAME = {
    "index": "序号",
    "zh": "中文名",
    "en": "英文名",
    "count": "合计",
    "repository": "GitHub仓库",
    "archived": "已归档",
    "obsolete": "已荒废",
    "stargazers": "Star数",
    "forks": "Fork数",
    "pushed_at": "最新推送",
    "created_at": "创建时间",
    "license": "许可证",
    "description": "说明",
}
