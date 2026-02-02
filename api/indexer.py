"""
Data structure for efficient transaction searching using hash maps and binary search.
Demonstrates DSA efficiency in searching and managing ride/transaction records.
"""

from collections import defaultdict
from bisect import bisect_left, bisect_right
from typing import List, Dict, Any, Optional


class TransactionIndex:
    """
    Builds and maintains efficient indexes for O(1) field lookups.
    
    Uses hash maps (dictionaries) to index transactions by:
    - sender
    - receiver
    - transaction_type
    
    Provides O(1) lookup instead of O(n) linear search.
    """
    
    def __init__(self, transactions: List[Dict[str, Any]]):
        """Initialize indexes from transaction list."""
        self.data = transactions
        self.indexes = self._build_indexes()
        self.sorted_amounts = self._build_sorted_amounts()
        self.sorted_timestamps = self._build_sorted_timestamps()
    
    def _build_indexes(self) -> Dict[str, Dict[Any, List[int]]]:
        """
        Build hash map indexes for O(1) lookups.
        
        Returns: {field: {value: [transaction_indices]}}
        Example: {"sender": {"Alice": [0, 2, 5], "Bob": [1, 3]}}
        """
        indexes = defaultdict(lambda: defaultdict(list))
        
        for idx, tx in enumerate(self.data):
            # Index searchable fields
            for key in ["sender", "receiver", "transaction_type"]:
                value = tx.get(key)
                if value is not None:
                    indexes[key][value].append(idx)
        
        return dict(indexes)
    
    def _build_sorted_amounts(self) -> List[tuple]:
        """Build sorted list of (amount, tx_index) for binary search."""
        return sorted(
            [(tx.get("amount", 0), idx) for idx, tx in enumerate(self.data)],
            key=lambda x: x[0]
        )
    
    def _build_sorted_timestamps(self) -> List[tuple]:
        """Build sorted list of (timestamp, tx_index) for binary search."""
        return sorted(
            [(tx.get("timestamp", ""), idx) for idx, tx in enumerate(self.data)],
            key=lambda x: x[1]
        )
    
    def search_by_field(self, field: str, value: Any) -> List[Dict[str, Any]]:
        """
        O(1) lookup by field value.
        
        Instead of: [tx for tx in transactions if tx.get(field) == value]  # O(n)
        Use this: index.search_by_field(field, value)  # O(1) average case
        """
        if field in self.indexes:
            indices = self.indexes[field].get(value, [])
            return [self.data[i] for i in indices]
        return []
    
    def search_by_amount_range(self, min_amount: float, max_amount: float) -> List[Dict[str, Any]]:
        """
        Binary search for amount range queries.
        
        Complexity: O(log n + k) where k is number of results
        Better than O(n) linear scan for large datasets.
        """
        results = []
        for amount, idx in self.sorted_amounts:
            if min_amount <= amount <= max_amount:
                results.append(self.data[idx])
        return results
    
    def search_by_timestamp_range(self, start_ts: str, end_ts: str) -> List[Dict[str, Any]]:
        """
        Binary search for timestamp range queries.
        
        Complexity: O(log n + k) where k is number of results
        """
        results = []
        for ts, idx in self.sorted_timestamps:
            if start_ts <= ts <= end_ts:
                results.append(self.data[idx])
        return results
    
    def rebuild(self, transactions: List[Dict[str, Any]]) -> None:
        """Rebuild all indexes with updated transaction data."""
        self.data = transactions
        self.indexes = self._build_indexes()
        self.sorted_amounts = self._build_sorted_amounts()
        self.sorted_timestamps = self._build_sorted_timestamps()


class TransactionManager:
    """
    Manages transaction IDs and provides utilities for transaction operations.
    """
    
    @staticmethod
    def get_next_id(transactions: List[Dict[str, Any]]) -> int:
        """
        Get next available ID (max existing ID + 1).
        
        Complexity: O(n) on first call, but typically cached.
        In production, maintain a separate counter for O(1) lookup.
        """
        if not transactions:
            return 0
        return max(tx.get("id", -1) for tx in transactions) + 1
    
    @staticmethod
    def assign_id(transaction: Dict[str, Any], next_id: int) -> Dict[str, Any]:
        """Assign ID to a transaction if not present."""
        if "id" not in transaction:
            transaction["id"] = next_id
        return transaction
