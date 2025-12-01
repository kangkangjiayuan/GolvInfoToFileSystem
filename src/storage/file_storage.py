"""文件存储 - File Storage

提供数据持久化到文件系统的功能。
Provides functionality to persist data to the file system.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..data_retrieval.models import DataRecord, SearchResult


class FileStorage:
    """文件存储类 - File Storage Class
    
    将数据记录存储到文件系统。
    Stores data records to the file system.
    """
    
    def __init__(self, base_path: str = "data"):
        """初始化文件存储 - Initialize file storage.
        
        Args:
            base_path: 存储数据的基础路径 - Base path for storing data.
        """
        self.base_path = Path(base_path)
        self._ensure_directory_exists()
    
    def _ensure_directory_exists(self) -> None:
        """确保存储目录存在 - Ensure storage directory exists."""
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def _get_record_path(self, record_id: str) -> Path:
        """获取记录文件路径 - Get record file path.
        
        Args:
            record_id: 记录ID - Record ID.
            
        Returns:
            记录文件的路径 - Path to the record file.
        """
        return self.base_path / f"{record_id}.json"
    
    def save_record(self, record: DataRecord) -> str:
        """保存数据记录 - Save a data record.
        
        Args:
            record: 要保存的数据记录 - Data record to save.
            
        Returns:
            保存的文件路径 - Path of the saved file.
        """
        file_path = self._get_record_path(record.id)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(record.to_json())
        return str(file_path)
    
    def load_record(self, record_id: str) -> Optional[DataRecord]:
        """加载数据记录 - Load a data record.
        
        Args:
            record_id: 记录ID - Record ID.
            
        Returns:
            数据记录，如果不存在则返回None - Data record or None if not found.
        """
        file_path = self._get_record_path(record_id)
        if not file_path.exists():
            return None
        
        with open(file_path, "r", encoding="utf-8") as f:
            return DataRecord.from_json(f.read())
    
    def delete_record(self, record_id: str) -> bool:
        """删除数据记录 - Delete a data record.
        
        Args:
            record_id: 记录ID - Record ID.
            
        Returns:
            是否成功删除 - Whether the deletion was successful.
        """
        file_path = self._get_record_path(record_id)
        if file_path.exists():
            file_path.unlink()
            return True
        return False
    
    def load_all_records(self) -> List[DataRecord]:
        """加载所有数据记录 - Load all data records.
        
        Returns:
            所有数据记录的列表 - List of all data records.
        """
        records = []
        for file_path in self.base_path.glob("*.json"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    record = DataRecord.from_json(f.read())
                    records.append(record)
            except (json.JSONDecodeError, KeyError):
                # 跳过无效的JSON文件 - Skip invalid JSON files
                continue
        return records
    
    def save_all_records(self, records: List[DataRecord]) -> int:
        """保存所有数据记录 - Save all data records.
        
        Args:
            records: 要保存的数据记录列表 - List of data records to save.
            
        Returns:
            成功保存的记录数 - Number of successfully saved records.
        """
        saved_count = 0
        for record in records:
            try:
                self.save_record(record)
                saved_count += 1
            except Exception:
                continue
        return saved_count
    
    def record_exists(self, record_id: str) -> bool:
        """检查记录是否存在 - Check if a record exists.
        
        Args:
            record_id: 记录ID - Record ID.
            
        Returns:
            记录是否存在 - Whether the record exists.
        """
        return self._get_record_path(record_id).exists()
    
    def get_record_count(self) -> int:
        """获取记录总数 - Get total record count.
        
        Returns:
            记录总数 - Total record count.
        """
        return len(list(self.base_path.glob("*.json")))
    
    def save_search_result(self, result: SearchResult, filename: Optional[str] = None) -> str:
        """保存搜索结果 - Save a search result.
        
        Args:
            result: 搜索结果 - Search result.
            filename: 文件名（可选） - Filename (optional).
            
        Returns:
            保存的文件路径 - Path of the saved file.
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"search_result_{timestamp}.json"
        
        file_path = self.base_path / filename
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(result.to_json())
        return str(file_path)
    
    def clear_all(self) -> int:
        """清除所有记录 - Clear all records.
        
        Returns:
            删除的记录数 - Number of deleted records.
        """
        deleted_count = 0
        for file_path in self.base_path.glob("*.json"):
            try:
                file_path.unlink()
                deleted_count += 1
            except Exception:
                continue
        return deleted_count
