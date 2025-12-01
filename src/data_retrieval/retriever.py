"""数据检索器 - Data Retriever

提供数据检索功能，支持从本地存储中检索数据。
Provides data retrieval functionality, supports retrieving data from local storage.
"""

import time
from typing import Any, Callable, Dict, List, Optional
from .models import DataRecord, SearchResult


class DataRetriever:
    """数据检索器 - Data Retriever
    
    提供数据检索和搜索功能。
    Provides data retrieval and search functionality.
    """
    
    def __init__(self, records: Optional[List[DataRecord]] = None):
        """初始化检索器 - Initialize the retriever.
        
        Args:
            records: 初始数据记录列表 - Initial list of data records.
        """
        self._records: Dict[str, DataRecord] = {}
        if records:
            for record in records:
                self._records[record.id] = record
    
    def add_record(self, record: DataRecord) -> None:
        """添加数据记录 - Add a data record.
        
        Args:
            record: 要添加的数据记录 - Data record to add.
        """
        self._records[record.id] = record
    
    def remove_record(self, record_id: str) -> bool:
        """删除数据记录 - Remove a data record.
        
        Args:
            record_id: 要删除的记录ID - ID of the record to remove.
            
        Returns:
            是否成功删除 - Whether the deletion was successful.
        """
        if record_id in self._records:
            del self._records[record_id]
            return True
        return False
    
    def get_record(self, record_id: str) -> Optional[DataRecord]:
        """获取指定ID的数据记录 - Get a data record by ID.
        
        Args:
            record_id: 记录ID - Record ID.
            
        Returns:
            数据记录，如果不存在则返回None - Data record or None if not found.
        """
        return self._records.get(record_id)
    
    def get_all_records(self) -> List[DataRecord]:
        """获取所有数据记录 - Get all data records.
        
        Returns:
            所有数据记录的列表 - List of all data records.
        """
        return list(self._records.values())
    
    def search(
        self,
        query: str,
        fields: Optional[List[str]] = None,
        page: int = 1,
        page_size: int = 10,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> SearchResult:
        """搜索数据记录 - Search data records.
        
        Args:
            query: 搜索关键词 - Search query.
            fields: 要搜索的字段列表 - List of fields to search in.
            page: 页码 - Page number.
            page_size: 每页记录数 - Number of records per page.
            category: 分类过滤 - Category filter.
            tags: 标签过滤 - Tag filter.
            
        Returns:
            搜索结果 - Search result.
        """
        start_time = time.time()
        
        if fields is None:
            fields = ["title", "content", "source"]
        
        # 过滤和搜索 - Filter and search
        matching_records = []
        query_lower = query.lower()
        
        for record in self._records.values():
            # 分类过滤 - Category filter
            if category and record.category != category:
                continue
            
            # 标签过滤 - Tag filter
            if tags and not any(tag in record.tags for tag in tags):
                continue
            
            # 关键词搜索 - Keyword search
            if query:
                found = False
                for field in fields:
                    value = getattr(record, field, "")
                    if isinstance(value, str) and query_lower in value.lower():
                        found = True
                        break
                if not found:
                    continue
            
            matching_records.append(record)
        
        # 分页 - Pagination
        total_count = len(matching_records)
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        page_records = matching_records[start_idx:end_idx]
        
        search_time_ms = (time.time() - start_time) * 1000
        
        return SearchResult(
            query=query,
            records=page_records,
            total_count=total_count,
            page=page,
            page_size=page_size,
            search_time_ms=search_time_ms
        )
    
    def search_by_category(self, category: str) -> List[DataRecord]:
        """按分类搜索数据记录 - Search records by category.
        
        Args:
            category: 分类名称 - Category name.
            
        Returns:
            匹配的数据记录列表 - List of matching records.
        """
        return [r for r in self._records.values() if r.category == category]
    
    def search_by_tags(self, tags: List[str], match_all: bool = False) -> List[DataRecord]:
        """按标签搜索数据记录 - Search records by tags.
        
        Args:
            tags: 标签列表 - List of tags.
            match_all: 是否需要匹配所有标签 - Whether to match all tags.
            
        Returns:
            匹配的数据记录列表 - List of matching records.
        """
        if match_all:
            return [r for r in self._records.values() 
                    if all(tag in r.tags for tag in tags)]
        else:
            return [r for r in self._records.values() 
                    if any(tag in r.tags for tag in tags)]
    
    def get_categories(self) -> List[str]:
        """获取所有分类 - Get all categories.
        
        Returns:
            分类列表 - List of categories.
        """
        categories = set()
        for record in self._records.values():
            if record.category:
                categories.add(record.category)
        return sorted(list(categories))
    
    def get_tags(self) -> List[str]:
        """获取所有标签 - Get all tags.
        
        Returns:
            标签列表 - List of tags.
        """
        tags = set()
        for record in self._records.values():
            tags.update(record.tags)
        return sorted(list(tags))
    
    def count(self) -> int:
        """获取记录总数 - Get total record count.
        
        Returns:
            记录总数 - Total record count.
        """
        return len(self._records)
