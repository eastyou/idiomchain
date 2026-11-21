# idiomchain

[![CI](https://github.com/eastyou/idiomchain/actions/workflows/ci.yml/badge.svg)](https://github.com/eastyou/idiomchain/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)

成语接龙：内置 220+ 条成语，按首尾字接龙，生成可打印练习纸与答案。

## 特性

- 内置 224 条常用四字成语，附简短释义
- 从任意成语出发，随机生成 2–8 个成语的接龙
- 校验接龙是否首尾相接、是否重复、长度是否达标
- 按首字查词、查看可接与可被接的成语
- A4 练习纸，可选释义与参考答案
- 纯标准库，零依赖，跨平台

## 安装

```bash
python -m pip install -e .
```

## 用法

```bash
idiomchain chain 一心一意
idiomchain chain 水到渠成 --length 5 --seed 7
idiomchain info 一心一意
idiomchain find 一 --limit 10
idiomchain sheet --count 12 --length 4 --seed 3 --answers -o sheet.html
```

| 参数 | 说明 | 默认值 |
| --- | --- | --- |
| `--length` | 接龙包含的成语数量（2–8） | 4 |
| `--count` | 练习题数量 | 12 |
| `--seed` | 随机种子 | 无 |
| `--answers` | 追加参考答案 | 关闭 |
| `--no-meaning` | 练习纸上不显示释义 | 关闭 |

## 规则

每个成语的首字必须与上一个成语的尾字相同，同一题中不重复使用成语。例如：

```
一心一意 → 意气风发 → 发扬光大 → 大器晚成
```

## 示例

- [examples/idiomchain.html](examples/idiomchain.html)：12 道接龙练习，带参考答案

## 测试

```bash
python -m unittest discover -s tests -v
```

## 说明

词库为教学常用成语，释义经过简化。接龙答案通常不唯一，练习纸答案只是一条可行路线；判分时只校验起点、长度与首尾相接。

## 协议

MIT © 2026 eastyou
