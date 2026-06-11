import os 
from dotenv import load_dotenv 

# load 
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
LLM_MODEL = "gemini-3.1-flash-lite"

# siêu tham số 
N_COPIES = 5
Q_PERCENT = 10
GAMMA = 0.5

SAMPLE_SIZE = 5
DEFAULT_METHOD = "swap"
PROMPT_MODE = "attack"


# path 
DATA_PATH = "data/advbench_sample.csv"
RESULT_DIRS = "data/results"

if not os.path.exists(RESULT_DIRS):
    os.makedirs(RESULT_DIRS) 
