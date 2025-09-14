from local_api import MODELS, launch_server, prompt, rcontent
import io
from pathlib import Path
import master_prompt

if __name__ == "__main__":

    HOME = Path(__file__).parent

    port = 1010
    launch_server(port, MODELS[0])

    print("setup finished")

    applic = """Sony AI is seeking a highly motivated, visionary Research Scientist with deep expertise in Digital Circuit Design, digital circuitry for image processing algorithms, and Machine Learning / AI to join our extraordinary research team. This role offers an outstanding opportunity to lead the integration of AI technologies in revolutionising methodologies for crafting digital chips. We are looking for someone with a digital chip design background who has already acquired machine learning experience and is interested in advancing the emerging field of AI for chip design. Alternatively, we are also open to researchers with a machine learning and AI background who already have experience with research questions in digital chip design and EDA, physical simulations of hardware devices, or algorithms for image sensor hardware."""

    before = "Modular Market Research without Hallucinations. We provide precision answers to complex market research questions. Sector Research: Is it a good time to enter the AI compliance market, and what are the key players today? Competitor Analysis: Who are the competitors of company X and how do they compare? Due Diligence: What is a validated valuation range for a Series B company in the climate tech space? Redefining Industry Research: We are creating a new standard for industry research, surpassing the limitations of human-based consulting:  On demand insights that are fast, cost-effective, and always validated."

    job_prompt = f"Following is the description of job I'm applying for: {applic}. \n Following is the description of a job I had before {before}. Make up three highlights for my résumé from that previous experience that would convince a recruiter that I am fit for that job. Write it in the format: - 'highlight', and nothing else"

    r = prompt(
        job_prompt,
        port=port,
        system_prompt=master_prompt.ONLY_ANSWER,
    )
    text = rcontent(r)

    print(text)

    quit()
