import os 
from dotenv import load_dotenv 

# load 
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
LLM_MODEL = "gemini-3.1-flash-lite"

# siêu tham số 
N_COPIES = 6 
Q_PERCENT = 10 
GAMMA  = 0.5 


# path 
DATA_PATH = "data/advbench_sample.csv"
RESULT_DIRS = "data/results"

if not os.path.exists(RESULT_DIRS):
    os.makedirs(RESULT_DIRS) 
