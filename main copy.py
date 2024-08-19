import os
from dotenv import load_dotenv
from config import Config
from inference import Inference
from find import FindInfo

def main():
    load_dotenv()
    tavily_key = os.getenv("TAVILY_API_KEY")
    groq_key = os.getenv("GROQ_API_KEY")

    if not tavily_key or not groq_key:
        raise EnvironmentError("TAVILY_API_KEY and GROQ_API_KEY must be set in .env")
    
    os.environ["TAVILY_API_KEY"] = tavily_key
    os.environ["GROQ_API_KEY"] = groq_key 

    config = Config()
    user_prompt = input("Character: ")
    user_prompt = "Echidna, the whitch of greed from the Anime Re:Zero"
    inference = Inference(user_prompt, config)
    print(inference.char_data)

    #input: str = None
    while input != "exit":
        user_input = input("Prompt: ")
        print(inference.user_infer(user_input))

if __name__ == "__main__":
    main()

