"""The Language Buddies: one list, read by the build, the Speech Mode screen, the app and buddies.js.

To bring a Buddy back or add one, set "active" to True. With one active Buddy the Switch Buddy
button is hidden; with two or more it cycles through the active ones in this order.

- id:     internal id saved in the learner's progress (keep `mila` and `rio` as they are)
- file:   model and picture name: buddy-models/<file>.glb (or buddy-gen/out/<file>.glb) and <file>.webp
- gender: "f" or "m", used to prefer a matching browser voice
"""

ROSTER = [
    {   # the chibi template (references/model.glb), optimised by buddy-gen/optimize_template.py
        "id": "kairo", "file": "template", "name": "Kairo", "from": "your Language Buddy", "gender": "m",
        "greet": "Hey! I'm Kairo. Let's talk.",
        "alt": "Kairo, a Language Buddy with long locs and an orange beanie, in a striped jacket",
        "active": True,
    },
    {
        "id": "mila", "file": "ruby", "name": "Ruby", "from": "from London", "gender": "f",
        "greet": "Hi! I'm Ruby. Let's talk.",
        "alt": "Ruby, a Language Buddy from London in a blue rain jacket with yellow headphones round her neck",
        "active": False,
    },
    {
        "id": "rio", "file": "max", "name": "Max", "from": "from New York", "gender": "m",
        "greet": "Hey! I'm Max. Let's talk.",
        "alt": "Max, a Language Buddy from New York in a blue and yellow varsity jacket, holding a coffee cup",
        "active": False,
    },
]

ACTIVE = [b for b in ROSTER if b["active"]]
assert ACTIVE, "at least one Buddy must be active"


def js():
    """The active roster for the browser (written into assets/config.js on every page)."""
    import json
    keep = ("id", "file", "name", "from", "gender", "greet")
    return "window.W2S_BUDDIES = " + json.dumps([{k: b[k] for k in keep} for b in ACTIVE]) + ";\n"
