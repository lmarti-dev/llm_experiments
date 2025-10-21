import requests
import subprocess
from pathlib import Path
import time
import json
import os
from http.client import responses
import webbrowser
from settings import ONLY_ANSWER, DEFAULT_MODEL

HOME = Path(__file__).parent
MODELS = os.listdir(Path(HOME, r"..\..\models"))


def moving_dots(n: int, N: int) -> str:
    s = "." * n
    return s.ljust(N)


def launch_server(model_name: str, port: int = 8080, verbose: bool = False):
    exe = Path(HOME, r"..\..\bin\llama-b6779-bin-win-cuda-12.4-x64\llama-server.exe")
    print(f"Calling {exe}")

    if model_name is None:
        model_name = "SmolLM2-360M-Q2_K.gguf"

    model = Path(HOME, rf"..\..\models\{model_name}").absolute()
    print(f"Loading model at {model}")

    cmd = f"{exe} -m {model} --port {port}"

    if verbose:
        kwargs = {"stdout": subprocess.PIPE}
    else:
        kwargs = {"stderr": subprocess.DEVNULL, "stdout": subprocess.DEVNULL}

    server = subprocess.Popen(cmd, **kwargs)
    host = f"http://localhost:{port}"
    r = requests.get(host)
    n = 0
    n_dots = 5
    while r.status_code == 503:
        time.sleep(1)
        r = requests.get(host)

        print(
            f"Status code {r.status_code} ({responses[r.status_code]}){moving_dots(n,n_dots)} on localhost:{port} model: {model_name}",
            end="\r",
        )
        n = (n + 1) % n_dots
    print("\n")
    print(f"Opening {host}")
    webbrowser.open(host)


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
    model_name = DEFAULT_MODEL
    launch_server(model_name)
