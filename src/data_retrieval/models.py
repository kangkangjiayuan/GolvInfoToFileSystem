"""数据模型 - Data Models

定义数据检索系统中使用的数据模型。
Defines data models used in the data retrieval system.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
import json
import uuid


@dataclass
class DataRecord:
    """数据记录模型 - Data Record Model
    
    表示一条检索到的数据记录。
    Represents a single data record retrieved from a source.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    content: str = ""
    source: str = ""
    category: str = ""
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """将数据记录转换为字典 - Convert record to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "source": self.source,
            "category": self.category,
            "tags": self.tags,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DataRecord":
        """从字典创建数据记录 - Create record from dictionary."""
        data = data.copy()
        if "created_at" in data and isinstance(data["created_at"], str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        if "updated_at" in data and isinstance(data["updated_at"], str):
            data["updated_at"] = datetime.fromisoformat(data["updated_at"])
        return cls(**data)
    
    def to_json(self) -> str:
        """将数据记录转换为JSON字符串 - Convert record to JSON string."""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
    
    @classmethod
    def from_json(cls, json_str: str) -> "DataRecord":
        """从JSON字符串创建数据记录 - Create record from JSON string."""
        return cls.from_dict(json.loads(json_str))


@dataclass
class SearchResult:
    """搜索结果模型 - Search Result Model
    
    表示一次搜索操作的结果。
    Represents the result of a search operation.
    """
    query: str = ""
    records: List[DataRecord] = field(default_factory=list)
    total_count: int = 0
    page: int = 1
    page_size: int = 10
    search_time_ms: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """将搜索结果转换为字典 - Convert result to dictionary."""
        return {
            "query": self.query,
            "records": [r.to_dict() for r in self.records],
            "total_count": self.total_count,
            "page": self.page,
            "page_size": self.page_size,
            "search_time_ms": self.search_time_ms,
            "timestamp": self.timestamp.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SearchResult":
        """从字典创建搜索结果 - Create result from dictionary."""
        data = data.copy()
        if "records" in data:
            data["records"] = [DataRecord.from_dict(r) for r in data["records"]]
        if "timestamp" in data and isinstance(data["timestamp"], str):
            data["timestamp"] = datetime.fromisoformat(data["timestamp"])
        return cls(**data)
    
    def to_json(self) -> str:
        """将搜索结果转换为JSON字符串 - Convert result to JSON string."""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
    
    @classmethod
    def from_json(cls, json_str: str) -> "SearchResult":
        """从JSON字符串创建搜索结果 - Create result from JSON string."""
        return cls.from_dict(json.loads(json_str))
