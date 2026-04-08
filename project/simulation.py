from agents import Agent
import random

agents = []
conversation = []
running = False


def init_simulation():
    global agents, conversation, running

    agents = [
        Agent("A", "serious and focused", "formal"),
        Agent("B", "lazy and chill", "casual slang"),
        Agent("C", "social extrovert", "excited"),
        Agent("D", "logical thinker", "analytical"),
        Agent("E", "anxious", "nervous tone")
    ]

    conversation = ["A: Hey guys, what’s up?"]
    running = True


def step_simulation():
    global conversation

    if not running:
        return None

    speaker = random.choice(agents)

    context = "\n".join(conversation[-6:])

    reply = speaker.generate_reply(context)

    log = f"{speaker.name}: {reply}"

    conversation.append(log)

    # influence others
    for agent in agents:
        agent.update_state(reply)

    return {
        "logs": [log],
        "agents": agents
    }


def stop_simulation():
    global running
    running = False