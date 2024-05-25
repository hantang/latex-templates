---
name: 模板推荐
about: 推荐LaTex等格式的学位论文模板
title: "[TEMPLATE]"
labels: template
assignees: ''

---

## 推荐模板

- 模板说明：（属于哪所高校（或通用）的模板）
- 模板列表
```json
[
{
  "genre": "", // 必填
  "language": "", // 必填
  "count": 0,
  "links": [
    "https://github.com/aa/bb", // 必填
  ]
}
]
```

## 格式说明（提交时候删除这部分）

示例：
- 模板说明：（属于或适合哪所高校（或通用）的模板）
- 模板列表
```json
[
{
  "genre": "thesis",
  "language": "latex",
  "count": 0,
  "links": [
    "https://github.com/aa/bb",
    "https://github.com/aa/cc",
    "https://github.com/xx/yy"
  ]
},
{
  "genre": "other",
  "language": "latex",
  "count": 0,
  "links": [
    "https://github.com/xx/zz"
  ]
}
]
```

JSON格式中字段说明：
- `genre`允许取值:
  - `thesis`: 学位论文（包括dissertation）
  - `presentation`: 演示文档（PPT， Slides）
  - `paper`: 一般论文（包括期刊、会议论文等）
  - `report`: 论文开题报告，实验报告，课程作业报告，竞赛模板，基金、项目的申请书等
  - `resume`: 简历（CV）
  - `book`: 书籍（手册等）
  - `other`: 其他（不属于上面，如信件等）
- `language`允许取值:
  - `latex`: LaTeX格式书写
  - `lyx`: LyX套件书写
  - `typst`: Typst格式书写
  - `markdown`: Markdown格式书写
  - `ms-word`: 微软Word文档
  - `powerpoint`: 微软PPT文档
  - `other`: 其他文档格式
- `links`: 填写github仓库URL（不要以`/`结尾）
- `count`: 自动生成，默认0即可。
