from threading import Lock


_processed_incidents: set[str] = set()
_lock = Lock()


def mark_if_new(incident_sys_id: str) -> bool:
    with _lock:
        if incident_sys_id in _processed_incidents:
            return False

        _processed_incidents.add(incident_sys_id)
        return True