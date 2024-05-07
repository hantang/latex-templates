# LaTeX 写作环境

## TeX 发行套装

- [:link: TeXLive](https://tug.org/texlive/): 支持 Windows, Linux
  - [:link: MacTeX](https://www.tug.org/mactex/)：支持 macOS，TeXLive 的 macOS 分发版
- [:link: MikTeX](https://miktex.org/): 主要支持 Windows

```shell
# macOS 环境配置
brew install mactex-no-gui
brew install tex-live-utility

# 修改镜像【可选】
sudo tlmgr option repository https://mirrors.tuna.tsinghua.edu.cn/CTAN/systems/texlive/tlnet
# 更多参见：https://help.mirrorz.org/CTAN/
# 更新【可选】
sudo tlmgr update --self --all
```

备注：

1. 也可以选择体积更小的`basictex`。
2. `tex-live-utility`即 TeX 的包管理工具`tlmgr`
3. `mactex-no-gui`相比`mactex`去掉了一些 GUI 程序（推荐）。

## 专用编辑器

- [:link: WinEdt](https://www.winedt.com/): 收费软件，仅 Window。
- [:link: Texifier](https://www.texifier.com)（原 TexPad）: 收费软件，仅 macOS，正在支持 Windows。
- [:link: TeXmaker](https://www.xm1math.net/texmaker/): 开源免费跨平台。
- [:link: TeXStudio](https://www.texstudio.org/): 开源免费跨平台。
- [:link: TeXworks](https://tug.org/texworks/): TexLive 自带，功能简单。
- [:link: TeXShop](https://pages.uoregon.edu/koch/texshop/): MacTeX 自带，功能简单。

## 通用编辑器

- [Visual Studio Code](https://code.visualstudio.com)

  - 推荐插件 [:simple-github: James-Yu/LaTeX-Workshop](https://github.com/James-Yu/LaTeX-Workshop)
    ![](https://img.shields.io/github/stars/James-Yu/LaTeX-Workshop?style=flat-square)
    ![](https://img.shields.io/github/license/James-Yu/LaTeX-Workshop?style=flat-square)
    ![](https://img.shields.io/github/last-commit/James-Yu/LaTeX-Workshop?style=flat-square)
  - 开源版本 [:simple-github: VSCodium/vscodium](https://github.com/VSCodium/vscodium)
    ![](https://img.shields.io/github/stars/VSCodium/vscodium?style=flat-square)
    ![](https://img.shields.io/github/license/VSCodium/vscodium?style=flat-square)
    ![](https://img.shields.io/github/last-commit/VSCodium/vscodium?style=flat-square)

- [Zed](https://zed.dev)
- [Lapce](https://lapce.dev)
- Vim, Emacs, NeoVim 等

## 在线平台

- [:link: Overleaf](https://www.overleaf.com/) （ShareLaTeX 已经合并到 Overleaf）
- [:link: TeXPage](https://www.texpage.com): 国内最近新出的 LaTeX 在线平台（中国版`Overleaf`）。

---

## 参考资料

- [:link: [LaTeX 指南] 互联网上的 LaTeX 资源](https://zhuanlan.zhihu.com/p/44137623)
- [:simple-github: LaTeXStudio 知识王国](https://github.com/latexstudio/LaTeX-TeXWiki)
- [:link: The LaTeX Project - Useful Links](https://www.latex-project.org/help/links/)
- [:link: TeX Users Group - TeX Resources on the Web](https://www.tug.org/interest.html),
