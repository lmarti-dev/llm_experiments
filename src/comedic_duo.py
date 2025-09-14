from local_api import MODELS, launch_server, prompt, rcontent
import io
from pathlib import Path
import master_prompt

HOME = Path(__file__).parent

idiot = 1010
serious = 2020

launch_server(idiot, MODELS[0])
launch_server(serious, MODELS[0])


print("setup finished")

n_steps = 10

r = prompt(
    "Hey, make up a secret I could tell to somebody ",
    port=idiot,
    system_prompt=master_prompt.ONLY_ANSWER,
)
text = rcontent(r)

print(text)

conversation = []

for x in range(n_steps):
    print(x)
    if x % 2 == 1:
        port = idiot
    else:
        port = serious
    r = prompt(
        f"this guy is lying to you, what should I tell without revealing what he's hiding, without revealing that you know he's lying: {text}",
        port=port,
        system_prompt=master_prompt.ONLY_ANSWER,
    )
    text = rcontent(r)
    conversation.append(text)
    print(text)

with io.open(Path(HOME, "file.txt"), "w+") as f:
    f.write("\n".join(conversation))


quit()
