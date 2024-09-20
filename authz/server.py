from fastapi import FastAPI
import vakt
from vakt.rules import Eq

app = FastAPI()

vakt_mem_storage = vakt.MemoryStorage()
vakt_mem_storage.add(
    vakt.Policy(
        1,
        actions=[Eq("read")],
        resources=[Eq("books")],
        subjects=[Eq("andrej@loka.com")],
        effect=vakt.ALLOW_ACCESS,
    )
)
vakt_guard = vakt.Guard(vakt_mem_storage, vakt.RulesChecker())


@app.get("/")
def index(action: str, resource: str):
    subject = "andrej@loka.com"
    inquiry = vakt.Inquiry(action=action, resource=resource, subject=subject)
    if vakt_guard.is_allowed(inquiry):
        return "This action is allowed! :)"
    else:
        return "This is forbidden. :("
