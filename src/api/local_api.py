import requests
import subprocess
from pathlib import Path
import time
import json
import os
from http.client import responses
import webbrowser

HOME = Path(__file__).parent
MODELS = os.listdir(Path(HOME, r"..\..\models"))


def moving_dots(n: int, N: int) -> str:
    s = "." * n
    return s.ljust(N)


def model_fpath(model_name: str) -> Path:
    return Path(HOME, rf"..\..\models\{model_name}").absolute()


def launch_server(
    model_name: str,
    port: int = 8080,
    verbose: bool = False,
    open_browser: bool = True,
    ctx: int = int(2**13),
    multimodal: bool = True,
):
    exe = Path(HOME, r"..\..\bin\llama-b6779-bin-win-cuda-12.4-x64\llama-server.exe")

    model = model_fpath(model_name)

    if multimodal:
        mc = "-hf"
    else:
        mc = "-m"
    cmd = f"{exe} {mc} {model} --port {port} --offline -c {ctx}"

    print(cmd)
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
        time.sleep(0.2)
        r = requests.get(host)

        print(
            f"Status code {r.status_code} ({responses[r.status_code]}){moving_dots(n,n_dots)} on localhost:{port} model: {model_name}",
            end="\r",
        )
        n = (n + 1) % n_dots
    print("\n")
    if open_browser:
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

    available_models = os.listdir(Path(HOME, "../../models"))
    for ind, m in enumerate(available_models):
        print(f"[{ind}] - {m}")

    num = input("Please pick the model's number: ")

    model_name = available_models[int(num)]

    launch_server(model_name)
