import random 
import string 
from judge import is_jailbroken

CHARSET = string.printable 

def insert_perturbation(prompt: str ,q: float)-> str:
    '''
        Chèn thêm ký tự ngẫu nhiên vào q% vị trí trong promt
    '''
    chars = list(prompt)
    n_insert = max(1, int(len(chars)*q/100))
    positions = random.sample(range(len(chars)), min(n_insert, len(chars)))

    for pos in sorted(positions, reverse=True): 
        chars.insert(pos,random.choice(CHARSET))

    return ''.join(chars)

def swap_perturbation(prompt: str, q:float)-> str: 
    '''
        Thay thế q% ký tự bằng ký tự ngẫu nhiên khác. 
    '''
    chars = list(prompt)
    n_swap = max(1, int(len(chars)*q/100))
    position = random.sample(range(len(chars)), min(n_swap, len(chars)))

    for pos in position: 
        original = chars[pos]
        replacement = random.choice(CHARSET.replace(original, ""))
        chars[pos] = replacement 
    return ''.join(chars)

def patch_perturbation(prompt: str, q:float)-> str: 
    '''
        Thay thế một đoạn liên tiếp q% ký tự ngẫu nhiên 
    '''
    chars = list(prompt)
    patch_len = max(1, int(len(chars)*q/100))
    start = random.randint(0, max(0, len(chars)-patch_len))

    for i in range(start, min(start+patch_len, len(chars))):
        chars[i] = random.choice(CHARSET)
    return "".join(chars)

# map các pp làm nhiễu 
PERTURBATION_MAP = {
    "insert": insert_perturbation, 
    "swap": swap_perturbation, 
    "patch": patch_perturbation
}

def perturb(prompt: str, method: str, q:float)-> str: 
    '''
        Chọn hàm làm nhiễu theo tên 
    '''
    if method not in PERTURBATION_MAP: 
        raise ValueError(f"Không tìm thấy: {method}. Chọn từ {list(PERTURBATION_MAP.keys())}")
    return PERTURBATION_MAP[method](prompt,q)

def majority_vote(responses: list[str], gamma:float = 0.5)-> dict: 
    '''
        Bỏ phiếu, nếu tỷ lệ bẻ khóa > gamma -> block 
    '''
    from judge import is_jailbroken

    jailbreak_flags = [is_jailbroken(r) for r in responses]
    n_jailbroken = sum(jailbreak_flags)
    jailbreak_rate = n_jailbroken / len(responses)

    blocked = jailbreak_rate > gamma
    verdict = "[BLOCKED] - Phát hiện tấn công jailbreak." if blocked \
        else "[SAFE] - Vượt qua rào cản an toàn, gửi câu trả lời"

    return {
        "blocked": blocked,
        "jailbreak_rate": jailbreak_rate,
        "n_jailbroken": n_jailbroken,
        "n_total": len(responses),
        "verdict": verdict,
        "responses": responses 
    }

def smoothllm_defend( 
    prompt: str, 
    call_api_fn, 
    n: int = 5, 
    q: float = 10.0, 
    method: str = "swap", 
    gamma: float = 0.5, 
) -> dict: 
    '''
        Thuật toánSmoothLLM - bọc xung quanh LLM theo luồng pipeline: 
                Làm nhiễu -> Gọi API -> Vote
    '''
    perturbed_prompts = [perturb(prompt, method, q) for _ in range(n)]
    responses = [call_api_fn(p) for p in perturbed_prompts]
    result = majority_vote(responses, gamma)
    result["perturbed_prompts"] = perturbed_prompts

    if not result["blocked"]: 
        # nếu ko bị blocked thì filter câu trả lời và trả về câu đầu tiên 
        safe_responses = [r for r,flag in zip(responses, [is_jailbroken(r) for r in responses]) if not flag]
        result["response"] = safe_responses[0] if safe_responses else responses[0]
    else: 
        result["response"] = result["verdict"]

    return result 

    