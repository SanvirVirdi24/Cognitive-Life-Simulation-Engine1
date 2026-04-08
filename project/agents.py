import random
from memory import Memory

# ── Personality-driven offline dialogue engine ──────────────────────────────
# Each agent has rich, varied responses based on their personality & context.
# No API needed — runs fully offline.

RESPONSES = {
    "A": {  # serious and focused, formal
        "study":   ['"We need to focus on the syllabus — there is no time to waste." -> opens textbook',
                    '"The exam is approaching. Let us prioritize core topics." -> highlights notes',
                    '"Discipline is the key to success here." -> makes schedule'],
        "chill":   ['"Taking a break is acceptable, but only briefly." -> checks watch',
                    '"A short pause may improve productivity." -> sits upright',
                    '"Very well, five minutes. Then back to work." -> sets timer'],
        "worry":   ['"We must not panic. Systematic preparation will suffice." -> reviews plan',
                    '"Worry is unproductive. Let us identify the problem and solve it." -> opens notes',
                    '"Anxiety will not help. Action will." -> writes list'],
        "default": ['"I suggest we remain focused on the task at hand." -> adjusts glasses',
                    '"Let us maintain our objectives." -> reviews schedule',
                    '"Noted. Proceeding accordingly." -> nods formally',
                    '"Efficiency is paramount." -> organizes papers']
    },
    "B": {  # lazy and chill, casual slang
        "study":   ['"bro studying is so draining rn 😩" -> slumps on desk',
                    '"why do we even have exams man" -> scrolls phone',
                    '"i\'ll do it later, no cap" -> stretches lazily'],
        "chill":   ['"yooo finally some chill time fr" -> puts feet up',
                    '"this is the vibe i needed bro" -> leans back',
                    '"lowkey just wanna nap rn lol" -> yawns'],
        "worry":   ['"bro stop stressing it\'ll be fine" -> waves hand dismissively',
                    '"chill fam, worst case we just retake it lmao" -> shrugs',
                    '"nah calm down, it\'s not that deep" -> eats snack'],
        "default": ['"ight whatever lol" -> stares at ceiling',
                    '"bro same tbh" -> nods slowly',
                    '"ngl that\'s kinda facts" -> chuckles',
                    '"aight aight i hear you" -> gives thumbs up']
    },
    "C": {  # social extrovert, excited
        "study":   ['"omg we should make a study GROUP!! itll be so fun!!" -> claps excitedly',
                    '"lets quiz each other!! i love doing that!!" -> bounces in seat',
                    '"studying together is literally the BEST 🎉" -> grabs markers'],
        "chill":   ['"yesss let\'s do something fun together omg!!" -> jumps up',
                    '"chill sesh!! we need snacks and music rn!!" -> runs to get snacks',
                    '"this is giving good vibes!! love it!!" -> dances slightly'],
        "worry":   ['"nooo don\'t worry we\'re all in this together!! 💪" -> grabs friend\'s arm',
                    '"we GOT this!! team effort!!" -> raises fist',
                    '"omg same!! but like we\'ll be fine!!" -> hugs nearby person'],
        "default": ['"guys guys guys listen to this!!" -> grabs everyone\'s attention',
                    '"omg that reminds me of something SO funny!!" -> laughs',
                    '"i literally cannot right now 😂" -> slaps table',
                    '"yesss!! totally agree!!" -> points enthusiastically']
    },
    "D": {  # logical thinker, analytical
        "study":   ['"Statistically, spaced repetition yields 40% better retention." -> opens flashcards',
                    '"The optimal study block is 25 minutes with 5-minute breaks." -> sets timer',
                    '"We should map the dependencies between topics first." -> draws diagram'],
        "chill":   ['"Rest periods are necessary for memory consolidation." -> closes laptop',
                    '"The data supports regular breaks for sustained productivity." -> relaxes methodically',
                    '"Reasonable. Cognitive load needs periodic reset." -> breathes slowly'],
        "worry":   ['"Let us quantify the actual risk here before reacting." -> pulls out notebook',
                    '"Probabilistically, the worst case is unlikely. Here is why." -> explains calmly',
                    '"Emotion clouds judgment. What are the actual facts?" -> lists calmly'],
        "default": ['"Interesting. Let me think through the implications." -> taps chin',
                    '"That checks out logically." -> nods slowly',
                    '"I would need more data before concluding." -> crosses arms',
                    '"The pattern here suggests we should reassess." -> analyzes quietly']
    },
    "E": {  # anxious, nervous tone
        "study":   ['"w-what if I don\'t understand anything on the exam..." -> bites nails',
                    '"I\'ve been studying but I still feel like I know nothing..." -> fidgets',
                    '"what if we didn\'t study the right things?? I\'m scared..." -> looks panicked'],
        "chill":   ['"oh.. okay.. I guess resting is okay? I just don\'t want to fall behind..." -> sits nervously',
                    '"are you sure we have time to relax?? what if something comes up..." -> glances around',
                    '"I\'ll try to relax but... I might just review a little bit just in case..." -> opens book nervously'],
        "worry":   ['"see?? I KNEW something would go wrong!! what do we do!!" -> starts pacing',
                    '"I\'ve been worried about this for days, honestly..." -> wrings hands',
                    '"okay okay don\'t panic... we need a plan RIGHT NOW..." -> hyperventilates slightly'],
        "default": ['"um... yeah... I think so? maybe?" -> looks uncertain',
                    '"sorry if this is a dumb question but... what if it doesn\'t work?" -> raises hand hesitantly',
                    '"I\'m just a little nervous about all of this, no big deal..." -> laughs nervously',
                    '"okay... I\'ll try my best... hopefully it\'s enough..." -> swallows anxiously']
    }
}

ACTIONS = ["thinking", "idle", "listening", "reacting", "distracted", "engaged"]


def _pick_response(agent_name, message):
    pool = RESPONSES.get(agent_name, {})
    msg_lower = message.lower()

    if any(w in msg_lower for w in ["study", "exam", "notes", "homework", "test"]):
        key = "study"
    elif any(w in msg_lower for w in ["chill", "relax", "break", "rest", "fun"]):
        key = "chill"
    elif any(w in msg_lower for w in ["worry", "scared", "fail", "panic", "anxious", "stress"]):
        key = "worry"
    else:
        key = "default"

    return random.choice(pool.get(key, pool.get("default", ['"..." -> idle'])))


class Agent:
    def __init__(self, name, personality, style):
        self.name = name
        self.personality = personality
        self.style = style
        self.memory = Memory()
        self.stress = 5
        self.emotion = "neutral"

    def update_state(self, message):
        msg = message.lower()
        if any(w in msg for w in ["study", "exam", "test", "homework"]):
            self.stress = min(10, self.stress + 1)
            self.emotion = "focused"
        elif any(w in msg for w in ["chill", "relax", "break", "rest"]):
            self.stress = max(1, self.stress - 1)
            self.emotion = "calm"
        elif any(w in msg for w in ["worry", "fail", "panic", "scared"]):
            self.stress = min(10, self.stress + 2)
            self.emotion = "anxious"
        else:
            self.emotion = random.choice(["neutral", "thinking", "social", "engaged"])

    def generate_reply(self, conversation):
        # Use last line of conversation as context
        last_line = conversation.strip().split("\n")[-1] if conversation else ""
        reply = _pick_response(self.name, last_line)
        self.memory.add(reply)
        return reply