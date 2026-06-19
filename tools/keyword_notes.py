from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class KeywordNote:
    keyword: str
    note: str
    source_url: str = ""
    tags: List[str] = field(default_factory=list)
    created_at: Optional[str] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def formatted_output(self, include_meta: bool = True) -> str:
        parts = [f"关键词：{self.keyword}", f"笔记：{self.note}"]
        if include_meta and self.source_url:
            parts.append(f"来源：{self.source_url}")
        if include_meta and self.tags:
            parts.append(f"标签：{'、'.join(self.tags)}")
        if include_meta and self.created_at:
            parts.append(f"创建时间：{self.created_at}")
        return " | ".join(parts)


@dataclass
class KeywordNoteCollection:
    notes: List[KeywordNote] = field(default_factory=list)

    def add_note(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def find_by_keyword(self, keyword: str) -> List[KeywordNote]:
        return [note for note in self.notes if note.keyword == keyword]

    def find_by_tag(self, tag: str) -> List[KeywordNote]:
        return [note for note in self.notes if tag in note.tags]

    def all_formatted(self, include_meta: bool = True) -> List[str]:
        return [note.formatted_output(include_meta) for note in self.notes]

    def summary(self) -> str:
        total = len(self.notes)
        unique_keywords = len({note.keyword for note in self.notes})
        return f"共 {total} 条笔记，涉及 {unique_keywords} 个关键词"

    def markdown_report(self) -> str:
        lines = ["# 关键词笔记报告\n"]
        for i, note in enumerate(self.notes, 1):
            lines.append(f"## {i}. {note.keyword}")
            lines.append(f"**笔记**：{note.note}")
            if note.source_url:
                lines.append(f"**来源**：{note.source_url}")
            if note.tags:
                lines.append(f"**标签**：{', '.join(note.tags)}")
            lines.append(f"**创建时间**：{note.created_at}")
            lines.append("")
        return "\n".join(lines)


def demo_usage() -> None:
    collection = KeywordNoteCollection()
    note1 = KeywordNote(
        keyword="爱游戏",
        note="用户对游戏的热情与兴趣的体现，是互动娱乐的核心驱动力。",
        source_url="https://home-portal-aiyouxi.com.cn",
        tags=["游戏", "用户", "热情"]
    )
    note2 = KeywordNote(
        keyword="爱游戏",
        note="此概念可延伸为游戏社区中的积极氛围，鼓励玩家分享与交流。",
        tags=["社区", "交流"]
    )
    note3 = KeywordNote(
        keyword="游戏体验",
        note="优秀游戏体验需要平衡画面、剧情和操作逻辑。",
        source_url="https://home-portal-aiyouxi.com.cn/game-review",
        tags=["体验", "设计"]
    )
    collection.add_note(note1)
    collection.add_note(note2)
    collection.add_note(note3)

    print("=== 格式化输出（含元数据）===")
    for line in collection.all_formatted(include_meta=True):
        print(line)

    print("\n=== 查找关键词 '爱游戏' ===")
    for note in collection.find_by_keyword("爱游戏"):
        print(note.formatted_output())

    print("\n=== 查找标签 '社区' ===")
    for note in collection.find_by_tag("社区"):
        print(note.formatted_output())

    print("\n=== 摘要信息 ===")
    print(collection.summary())

    print("\n=== Markdown 报告 ===")
    print(collection.markdown_report())


if __name__ == "__main__":
    demo_usage()