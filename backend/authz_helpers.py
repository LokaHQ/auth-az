from typing import Any, List
import requests as r


class Authz:
    def can(self, subject: str, action: str, resource_id) -> bool:
        print(f"checking can: {subject}, {action}, {resource_id}")
        response = r.get(
            f"http://localhost:8002/can?subject={subject}&action={action}&resource_id={resource_id}"
        )
        return response.json()

    def filter(self, subject: str, action: str, resource_ids: List[str]) -> List[str]:
        print(f"filtering {subject}, {action} for {resource_ids}")
        response = r.post(
            f"http://localhost:8002/filter?subject={subject}&action={action}",
            json=resource_ids,
        )
        print(response.text)
        return response.json()
