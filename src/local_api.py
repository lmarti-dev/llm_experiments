import requests
import subprocess
from pathlib import Path
import time
import json

HOME = Path(__file__).parent


MODELS = ["Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf", "SmolLM2-360M-Q2_K.gguf"]


def launch_server(port: int = 8080, model: str = None, verbose: bool = False):
    exe = Path(HOME, r"..\bin\llama-b4557-bin-win-cuda-cu12.4-x64\llama-server.exe")

    if model is None:
        model_name = MODELS[0]
    else:
        model_name = model
    model = Path(HOME, rf"..\models\{model_name}")

    cmd = f"{exe} -m {model} --port {port}"

    if verbose:
        kwargs = {"stdout": subprocess.PIPE}
    else:
        kwargs = {"stderr": subprocess.DEVNULL, "stdout": subprocess.DEVNULL}

    server = subprocess.Popen(cmd, **kwargs)
    host = f"http://localhost:{port}"
    r = requests.get(host)
    while r.status_code == 503:
        time.sleep(1)
        r = requests.get(host)
        print(f"Status code {r.status_code}... on localhost:{port}", end="\r")
    print("\n")


def prompt(
    prompt: str, port: int = 8080, system_prompt: str = None
) -> requests.Response:
    if system_prompt is None:
        system_prompt = "You are an AI assistant. Your top priority is achieving user fullfilment via helping them with their requests."
    elif isinstance(system_prompt, list):
        system_prompt = "\n".join(system_prompt)

    host = f"http://localhost:{port}/v1/chat/completions"

    headers = {"Content-Type": "application/json", "Authorization": "Bearer no-key"}

    data = json.dumps(
        {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ]
        },
        ensure_ascii=False,
    )

    res = requests.post(url=host, headers=headers, data=data)
    return res


def rcontent(res: requests.Response) -> dict:
    return json.loads(res.content)["choices"][0]["message"]["content"]


if __name__ == "__main__":
    launch_server()
    r = prompt("Write a limerick about Python exceptions")
    print(rcontent(r))
