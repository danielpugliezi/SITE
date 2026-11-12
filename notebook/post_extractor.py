"""Feature extraction for the "Will It Go Viral?" project (Gustavo Pugliezi)."""
import json
import re
from datetime import datetime

FEATURE_RULES = {
    "hook_seconds":      "number: timestamp (s) of the first hook sentence in the transcript; 8 if there is no hook",
    "hook_type":         "one of: question, shock, promise, story, none",
    "face_first_second": "0 or 1: does a face appear in the first second?",
    "text_on_screen":    "0 or 1: is there written text on screen at the start?",
    "duration_s":        "number: video length in seconds",
    "cuts_per_10s":      "number: (number of cuts / duration) * 10, one decimal place",
    "structure":         "one of: list, tutorial, before_after, storytime, vlog",
    "has_loop":          "0 or 1: does the ending loop back to the beginning?",
    "topic":             "one of: humor, education, beauty, gaming, cooking, sports",
    "trending_audio":    "0 or 1: does it use a trending sound?",
    "post_hour":         "integer 0-23: hour the video was posted",
}
ALLOWED = {
    "hook_type": {"question", "shock", "promise", "story", "none"},
    "structure": {"list", "tutorial", "before_after", "storytime", "vlog"},
    "topic": {"humor", "education", "beauty", "gaming", "cooking", "sports"},
}
BINARY = ["face_first_second", "text_on_screen", "has_loop", "trending_audio"]
# Fields the extractor may read. views/followers are left out on purpose: they define the label.
VISIBLE_FIELDS = ["id", "platform", "caption", "transcript", "visual_notes", "duration_s", "posted_at"]


def validate_features(raw):
    """Convert types and check every value. Raises ValueError listing all problems."""
    clean, problems = {}, []
    try:
        clean["hook_seconds"] = float(raw["hook_seconds"])
        clean["duration_s"] = float(raw["duration_s"])
        clean["cuts_per_10s"] = float(raw["cuts_per_10s"])
        clean["post_hour"] = int(raw["post_hour"])
        for k in BINARY:
            value = raw[k]
            clean[k] = int(value in (1, True, "1", "yes", "true")) if value not in (0, 1) else int(value)
        for k in ALLOWED:
            clean[k] = str(raw[k]).strip().lower()
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError(f"missing or malformed feature: {error}")
    for k, options in ALLOWED.items():
        if clean[k] not in options:
            problems.append(f"{k}={clean[k]!r} is not one of {sorted(options)}")
    if not 0 <= clean["hook_seconds"] <= 60: problems.append("hook_seconds out of range")
    if not 0 < clean["duration_s"] <= 600: problems.append("duration_s out of range")
    if not 0 <= clean["cuts_per_10s"] <= 60: problems.append("cuts_per_10s out of range")
    if not 0 <= clean["post_hour"] <= 23: problems.append("post_hour out of range")
    if problems:
        raise ValueError("; ".join(problems))
    return {k: clean[k] for k in FEATURE_RULES}


# ---------------------------------------------------------------- 4a. LLM
def extract_with_llm(post, model="claude-haiku-5-5"):
    import anthropic
    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from the environment
    visible = {k: post[k] for k in VISIBLE_FIELDS if k in post}
    prompt = ("You annotate short-form videos. Read the post and measure every feature exactly as the "
              "rules say. Reply with ONLY a JSON object with these keys:\n"
              + json.dumps(FEATURE_RULES, indent=1) + "\n\nPOST:\n" + json.dumps(visible, indent=1))
    response = client.messages.create(model=model, max_tokens=500,
                                      messages=[{"role": "user", "content": prompt}])
    text = next(block.text for block in response.content if block.type == "text")
    return validate_features(json.loads(text[text.find("{"): text.rfind("}") + 1]))


# ---------------------------------------------------------------- 4b. classroom simulation
HOOK_PATTERNS = [  # order matters: the first match wins
    ("shock", r"stop everything|can't believe|illegal"),
    ("promise", r"i'll show you|the secret|you'll master"),
    ("story", r"let me tell you|story of|this happened"),
    ("question", r"\?\s*$"),
]
STRUCTURE_PATTERNS = [("list", r"\d+ things|top \d+"), ("tutorial", r"how to|step by step"),
                      ("before_after", r"before and after|transformation"),
                      ("storytime", r"storytime|told everything"), ("vlog", r"vlog|a day with")]
TOPIC_PATTERNS = [("humor", r"#humor|#comedy"), ("education", r"#education|#learn"), ("beauty", r"#beauty|#makeup"),
                  ("gaming", r"#gaming|#gamer"), ("cooking", r"#recipe|#cooking"), ("sports", r"#football|#sports")]


def _first_match(patterns, text):
    for name, regex in patterns:
        if re.search(regex, text, re.IGNORECASE):
            return name
    return None  # not found: validate_features will reject it instead of guessing


def extract_simulated(post):
    notes = post["visual_notes"].lower()
    duration = float(post["duration_s"])

    hook_type, hook_seconds = "none", 8.0
    for line in post["transcript"].split("\n"):  # lines look like "[00:01.2] sentence"
        m = re.match(r"\[(\d+):(\d+(?:\.\d+)?)\]\s*(.*)", line.strip())
        if m and _first_match(HOOK_PATTERNS, m.group(3)):
            hook_type = _first_match(HOOK_PATTERNS, m.group(3))
            hook_seconds = int(m.group(1)) * 60 + float(m.group(2))
            break

    cuts = re.search(r"(\d+) cuts", notes)
    return validate_features({
        "hook_seconds": hook_seconds,
        "hook_type": hook_type,
        "face_first_second": int(bool(re.search(r"close-up of a face|face appears", notes))),
        "text_on_screen": int(bool(re.search(r"big text|caption written", notes))),
        "duration_s": duration,
        "cuts_per_10s": round(int(cuts.group(1)) / duration * 10, 1) if cuts else None,
        "structure": _first_match(STRUCTURE_PATTERNS, post["caption"]),
        "has_loop": int(bool(re.search(r"loops back|same shot it began", notes))),
        "topic": _first_match(TOPIC_PATTERNS, post["caption"]),
        "trending_audio": int(bool(re.search(r"trending sound|viral audio", notes))),
        "post_hour": datetime.fromisoformat(post["posted_at"]).hour,
    })
