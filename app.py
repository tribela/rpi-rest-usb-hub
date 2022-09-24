import re
import subprocess

import fastapi
import pydantic

app = fastapi.FastAPI()

SWITCH_PORT = 2


class StatusRequest(pydantic.BaseModel):
    status: str


def get_status(switch_id: int = SWITCH_PORT) -> str:
    try:
        output = subprocess.check_output(
            ["sudo", "/usr/sbin/uhubctl", "-p", str(switch_id)]
        ).decode("utf-8")
        status = re.search(r"Port \d+: \d+ (power|off)", output).group(1)

        if status == "power":
            return "on"
        elif status == "off":
            return "off"
    except subprocess.CalledProcessError | AttributeError:
        return "unknown"
    else:
        return "unknown"


@app.get("/switch")
def get_switch():
    return {"status": get_status()}


@app.post("/switch")
def post_switch(req: StatusRequest):
    switch = "on" if req.status == 'on' else "off"
    subprocess.check_call(
        ["sudo", "/usr/sbin/uhubctl", "-p", str(SWITCH_PORT), "-a", switch])
    return {"status": get_status()}
