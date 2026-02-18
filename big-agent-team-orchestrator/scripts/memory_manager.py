#!/usr/bin/env python3
"""
Memory Manager - Handles shared knowledge and context persistence

This script manages shared memory spaces, context injection for agent handoffs,
tracks project state and decision history, enables cross-agent knowledge sharing.
"""

import json
import time
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict, field
from enum import Enum
from pathlib import Path
import threading

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class MemoryType(Enum):
    """Types of memory that can exist"""

    TASK_RESULTS = "task_results"
    DECISION_HISTORY = "decision_history"
    COMMON_KNOWLEDGE = "common_knowledge"
    AGENT_CONTEXT = "agent_context"
    TEMPORARY = "temporary"


@dataclass
class MemoryEntry:
    """Represents a piece of stored memory"""

    id: str
    content: Dict[str, Any]
    memory_type: MemoryType
    created_at: float = field(default_factory=time.time)
    accessed_at: float = field(default_factory=time.time)
    source_agent: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.created_at == 0:
            self.created_at = time.time()
        if self.accessed_at == 0:
            self.accessed_at = time.time()


@dataclass
class SharedContext:
    """Represents a shared context for the entire team"""

    project_id: str
    name: str
    description: str
    created_at: float = field(default_factory=time.time)
    last_updated: float = field(default_factory=time.time)
    global_state: Dict[str, Any] = field(default_factory=dict)
    agent_states: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)

    def __post_init__(self):
        if self.created_at == 0:
            self.created_at = time.time()
        if self.last_updated == 0:
            self.last_updated = time.time()


class MemoryManager:
    """Main memory management class for multi-agent coordination"""

    def __init__(self, storage_path: Optional[str] = None):
        """
        Initialize the memory manager

        Args:
            storage_path: Path to store persistent memory (optional)
        """
        self.storage_path = storage_path
        self.contexts: Dict[str, SharedContext] = {}
        self.memory_entries: Dict[str, MemoryEntry] = {}
        self.context_memory_map: Dict[str, List[str]] = {}
        self.lock = threading.RLock()

        # Create storage directory if needed
        if self.storage_path:
            Path(self.storage_path).mkdir(parents=True, exist_ok=True)

        logger.info("Memory Manager initialized")

    def create_context(self, context: SharedContext) -> str:
        """
        Create and initialize a new shared context

        Args:
            context: The SharedContext to create

        Returns:
            context_id: The ID of the created context
        """
        with self.lock:
            context_id = context.project_id
            self.contexts[context_id] = context
            self.context_memory_map[context_id] = []
            logger.info(f"Created context: {context_id}")
            return context_id

    def get_context(self, context_id: str) -> Optional[SharedContext]:
        """Retrieve a shared context"""
        with self.lock:
            return self.contexts.get(context_id)

    def add_memory(
        self,
        content: Dict[str, Any],
        memory_type: MemoryType,
        source_agent: str = "",
        context_id: str = "",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Add a memory entry to the system

        Args:
            content: The content to store
            memory_type: Type of memory
            source_agent: Agent that created the memory
            context_id: Context to associate with (if not using default)
            metadata: Additional metadata

        Returns:
            entry_id: The ID of the created memory entry
        """
        with self.lock:
            entry = MemoryEntry(
                id=f"mem-{int(time.time())}-{len(self.memory_entries)}",
                content=content,
                memory_type=memory_type,
                source_agent=source_agent,
                metadata=metadata or {},
            )

            self.memory_entries[entry.id] = entry

            # Add to appropriate context
            if context_id:
                if context_id not in self.context_memory_map:
                    self.context_memory_map[context_id] = []
                self.context_memory_map[context_id].append(entry.id)
            else:
                for cid, mids in self.context_memory_map.items():
                    if cid in [c.project_id for c in self.contexts.values()]:
                        self.context_memory_map[cid].append(entry.id)

            logger.info(
                f"Added memory entry: {entry.id} (type={memory_type.value}, "
                f"agent={source_agent}, context={context_id})"
            )
            return entry.id

    def get_context_memory(
        self,
        context_id: str,
        memory_type: Optional[MemoryType] = None,
        limit: Optional[int] = None,
    ) -> List[MemoryEntry]:
        """
        Retrieve memory entries for a specific context

        Args:
            context_id: The context to query
            memory_type: Filter by memory type (optional)
            limit: Maximum number of entries to return (optional)

        Returns:
            List of memory entries
        """
        with self.lock:
            context = self.contexts.get(context_id)
            if not context:
                return []

            # Get all memory IDs for this context
            memory_ids = self.context_memory_map.get(context_id, [])

            # Filter by type if specified
            if memory_type:
                memory_ids = [
                    mid
                    for mid in memory_ids
                    if self.memory_entries[mid].memory_type == memory_type
                ]

            # Retrieve entries
            entries = [self.memory_entries[mid] for mid in memory_ids]
            entries.sort(key=lambda x: x.created_at, reverse=True)

            # Apply limit
            if limit:
                entries = entries[:limit]

            # Update access times
            for entry in entries:
                entry.accessed_at = time.time()

            return entries

    def add_to_agent_state(
        self,
        context_id: str,
        agent_id: str = "",
        state_data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Update agent-specific state within a context

        Args:
            context_id: The context to update
            agent_id: The agent to update
            state_data: New state data to add/merge
        """
        with self.lock:
            context = self.contexts.get(context_id)
            if not context:
                logger.warning(f"Context {context_id} not found")
                return

            if not state_data:
                state_data = {}

            if agent_id not in context.agent_states:
                context.agent_states[agent_id] = {}

            # Merge with existing state
            context.agent_states[agent_id].update(state_data)
            context.last_updated = time.time()

            logger.info(f"Updated agent {agent_id} state in context {context_id}")

    def get_agent_state(
        self, context_id: str, agent_id: str = "", keys: Optional[List[str]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve agent-specific state from a context

        Args:
            context_id: The context to query
            agent_id: The agent to query
            keys: Specific keys to retrieve (optional)

        Returns:
            Agent state dictionary
        """
        with self.lock:
            context = self.contexts.get(context_id)
            if not context:
                return None

            agent_state = context.agent_states.get(agent_id, {})

            if keys:
                return {k: agent_state.get(k) for k in keys if k in agent_state}

            return agent_state

    def save_to_disk(self) -> None:
        """Save memory state to disk for persistence"""
        if not self.storage_path:
            return

        with self.lock:
            try:
                save_data = {
                    "contexts": {
                        cid: asdict(ctx) for cid, ctx in self.contexts.items()
                    },
                    "memory_entries": {
                        eid: {
                            "id": e.id,
                            "content": e.content,
                            "memory_type": e.memory_type.value,
                            "created_at": e.created_at,
                            "accessed_at": e.accessed_at,
                            "source_agent": e.source_agent,
                            "metadata": e.metadata,
                        }
                        for eid, e in self.memory_entries.items()
                    },
                    "context_memory_map": self.context_memory_map,
                }

                filepath = Path(self.storage_path) / "memory_store.json"
                with open(filepath, "w") as f:
                    json.dump(save_data, f, indent=2)

                logger.info(f"Saved memory state to {filepath}")

            except Exception as e:
                logger.error(f"Error saving memory state: {e}")

    def load_from_disk(self) -> int:
        """
        Load memory state from disk

        Returns:
            Number of entries loaded
        """
        if not self.storage_path:
            return 0

        with self.lock:
            try:
                filepath = Path(self.storage_path) / "memory_store.json"
                if not filepath.exists():
                    return 0

                with open(filepath, "r") as f:
                    save_data = json.load(f)

                # Reconstruct contexts
                for ctx_id, ctx_data in save_data.get("contexts", {}).items():
                    self.contexts[ctx_id] = SharedContext(
                        project_id=ctx_data["project_id"],
                        name=ctx_data["name"],
                        description=ctx_data["description"],
                        created_at=ctx_data["created_at"],
                        last_updated=ctx_data["last_updated"],
                        global_state=ctx_data.get("global_state", {}),
                        agent_states=ctx_data.get("agent_states", {}),
                        dependencies=ctx_data.get("dependencies", []),
                    )

                # Reconstruct memory entries
                entry_ids = []
                for eid, entry_data in save_data.get("memory_entries", {}).items():
                    self.memory_entries[eid] = MemoryEntry(
                        id=entry_data["id"],
                        content=entry_data["content"],
                        memory_type=MemoryType(entry_data["memory_type"]),
                        created_at=entry_data["created_at"],
                        accessed_at=entry_data.get("accessed_at"),
                        source_agent=entry_data.get("source_agent"),
                        metadata=entry_data.get("metadata", {}),
                    )
                    entry_ids.append(eid)

                # Reconstruct context map
                self.context_memory_map = save_data.get("context_memory_map", {})

                logger.info(
                    f"Loaded {len(self.memory_entries)} memory entries from disk"
                )
                return len(self.memory_entries)

            except Exception as e:
                logger.error(f"Error loading memory state: {e}")
                return 0


class ContextInjector:
    """Helper class for context injection scenarios"""

    @staticmethod
    def prepare_handoff_context(
        source_agent: str, target_agent: str, context_id: str, key_info: str = ""
    ) -> Dict[str, Any]:
        """
        Prepare context information for agent handoff

        Args:
            source_agent: Agent transferring information
            target_agent: Agent receiving information
            context_id: Context being handed off
            key_info: Summary of key information to transfer

        Returns:
            Handoff context dictionary
        """
        return {
            "handoff_type": "agent_to_agent",
            "source_agent": source_agent,
            "target_agent": target_agent,
            "context_id": context_id,
            "key_info": key_info,
            "timestamp": time.time(),
        }

    @staticmethod
    def merge_contexts(
        primary_context: SharedContext, secondary_context: SharedContext
    ) -> SharedContext:
        """
        Merge two contexts into a new one

        Args:
            primary_context: Primary context (preserved)
            secondary_context: Secondary context to merge

        Returns:
            Merged SharedContext
        """
        merged = SharedContext(
            project_id=f"merged-{int(time.time())}",
            name=f"{primary_context.name} + {secondary_context.name}",
            description=f"Context merge from {secondary_context.project_id}",
            dependencies=[primary_context.project_id, secondary_context.project_id],
        )

        # Merge global state
        merged.global_state = primary_context.global_state.copy()
        merged.global_state.update(secondary_context.global_state)

        # Merge agent states
        for agent_id, state in secondary_context.agent_states.items():
            if agent_id in merged.agent_states:
                merged.agent_states[agent_id].update(state)
            else:
                merged.agent_states[agent_id] = state

        return merged


def main():
    """Example usage of the Memory Manager"""

    # Initialize memory manager
    manager = MemoryManager(storage_path="/tmp/agent_team_memory")

    # Create a context
    context = SharedContext(
        project_id="demo-project",
        name="Demo Project",
        description="Example agent team context",
        global_state={"status": "active", "progress": 0},
    )
    context_id = manager.create_context(context)

    # Add some memory entries
    manager.add_memory(
        content={"decision": "use_react_framework", "reason": "scalability"},
        memory_type=MemoryType.DECISION_HISTORY,
    )

    manager.add_memory(
        content={"api_endpoint": "/api/v1/users", "method": "POST"},
        memory_type=MemoryType.TASK_RESULTS,
        source_agent="backend-dev-1",
    )

    # Get context memory
    entries = manager.get_context_memory(context_id)
    print(f"Found {len(entries)} entries in context")

    # Save to disk
    manager.save_to_disk()

    return manager


if __name__ == "__main__":
    main()
