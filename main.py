from fastapi import FastAPI
from pydantic import BaseModel
import io
import traceback
import contextlib
import base64
import matplotlib.pyplot as plt

app = FastAPI()

class CodeRequest(BaseModel):
    code: str

@app.post("/execute")
def execute_code(payload: CodeRequest):
    output = io.StringIO()
    result = {"stdout": "", "image_base64": None}
    local_vars = {}

    try:
        with contextlib.redirect_stdout(output):
            exec(payload.code, {"plt": plt}, local_vars)

        result["stdout"] = output.getvalue()

        if plt.get_fignums():
            buf = io.BytesIO()
            plt.savefig(buf, format="png")
            buf.seek(0)
            result["image_base64"] = base64.b64encode(buf.read()).decode('utf-8')
            plt.close("all")

    except Exception:
        result["stdout"] = "ERROR:\\n" + traceback.format_exc()

    return result
