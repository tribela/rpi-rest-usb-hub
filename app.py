import re
import subprocess

import fastapi
import pydantic

app = fastapi.FastAPI()


class StatusRequest(pydantic.BaseModel):
    status: str


def get_status(switch_id: int) -> str:
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


@app.get("/switches/{switch_id}")
def get_switch(switch_id: int):
    return {"status": get_status(switch_id)}


@app.post("/switches/{switch_id}")
def post_switch(switch_id: int, req: StatusRequest):
    switch = "on" if req.status == 'on' else "off"
    subprocess.check_call(
        ["sudo", "/usr/sbin/uhubctl", "-p", str(switch_id), "-a", switch])
    return {"status": get_status(switch_id)}
