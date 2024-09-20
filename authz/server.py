import resource
from typing import List
from fastapi import Body, FastAPI
import vakt
from vakt.rules import Eq, StartsWith


app = FastAPI()


vakt_mem_storage = vakt.MemoryStorage()
vakt_mem_storage.add(
    vakt.Policy(
        1,
        actions=[Eq("read")],
        resources=[StartsWith("book/")],
        # resources=[Eq("book/1")],
        subjects=[Eq("andrej@loka.com")],
        effect=vakt.ALLOW_ACCESS,
    )
)
vakt_guard = vakt.Guard(vakt_mem_storage, vakt.RulesChecker())


@app.get("/can")
def can(subject: str, action: str, resource_id: str) -> bool:
    print("authz checking for", subject, action, resource_id)
    inquiry = vakt.Inquiry(subject=subject, action=action, resource=resource_id)
    return vakt_guard.is_allowed(inquiry)


@app.post("/filter")
def filter(subject: str, action: str, resource_ids: List[str] = Body()) -> List[str]:
    print("filtering", subject, action, resource_ids)
    filtered_ids = []
    for r_id in resource_ids:
        inquiry = vakt.Inquiry(subject=subject, action=action, resource=r_id)
        if vakt_guard.is_allowed(inquiry):
            filtered_ids.append(r_id)
    print(
        "original size of list was",
        len(resource_ids),
        "reduced it to",
        len(filtered_ids),
    )
    return filtered_ids
