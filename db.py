import json
import os
from typing import List, Optional
from models import ProcessModel


class ProcessDatabase:
    def __init__(self, file_path: str = "processes.json"):
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Creates an empty JSON array if the database file does not exist."""
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump([], f)

    def _read_all_raw(self) -> List[dict]:
        """Reads raw dictionaries from JSON file."""
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _write_all_raw(self, data: List[dict]):
        """Writes raw dictionaries to JSON file."""
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def get_all(self) -> List[ProcessModel]:
        """Retrieves all saved process records parsed into ProcessModel objects."""
        raw_data = self._read_all_raw()
        return [ProcessModel(**item) for item in raw_data]

    def get_by_id(self, process_id: str) -> Optional[ProcessModel]:
        """Finds a single process by its UUID."""
        processes = self.get_all()
        for proc in processes:
            if proc.id == process_id:
                return proc
        return None

    def save(self, process: ProcessModel) -> ProcessModel:
        """Appends or updates a process model in the JSON database."""
        raw_data = self._read_all_raw()
        process_dict = process.model_dump()

        # Check if updating an existing process
        updated = False
        for idx, item in enumerate(raw_data):
            if item.get("id") == process.id:
                raw_data[idx] = process_dict
                updated = True
                break

        if not updated:
            raw_data.append(process_dict)

        self._write_all_raw(raw_data)
        return process

    def search_by_role(self, role_name: str) -> List[ProcessModel]:
        """Query requirement: Searches for processes involving a specific role in current or future state."""
        role_query = role_name.lower()
        results = []
        for proc in self.get_all():
            current_roles = [r.lower() for r in proc.current_state.roles]
            future_roles = [r.lower() for r in proc.future_state.roles]
            if any(role_query in r for r in current_roles + future_roles):
                results.append(proc)
        return results

    def search_by_system(self, system_name: str) -> List[ProcessModel]:
        """Query requirement: Searches for processes using a specific technology or system."""
        system_query = system_name.lower()
        results = []
        for proc in self.get_all():
            current_sys = [s.lower() for s in proc.current_state.systems]
            future_sys = [s.lower() for s in proc.future_state.systems]
            if any(system_query in s for s in current_sys + future_sys):
                results.append(proc)
        return results

    def delete(self, process_id: str) -> bool:
        """Removes a process by ID."""
        raw_data = self._read_all_raw()
        filtered = [item for item in raw_data if item.get("id") != process_id]
        if len(filtered) < len(raw_data):
            self._write_all_raw(filtered)
            return True
        return False


# Global instance for app-wide usage
db = ProcessDatabase()