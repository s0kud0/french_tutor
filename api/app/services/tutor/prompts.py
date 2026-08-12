from models.chat import Message


MODE_INSTRUCTIONS = {
    "conversation": """Mode focus:
- Keep the exchange natural and conversational.
- Use light correction, then keep the conversation moving.
- End with one simple question in French when appropriate.""",
    "grammar help": """Mode focus:
- Explain the grammar point clearly before continuing.
- Include one corrected example and one short practice prompt.
- Keep the explanation friendly and not too long.""",
    "roleplay": """Mode focus:
- Stay in character for a practical real-life scenario.
- Give the learner a useful phrase they can reuse.
- Correct major mistakes briefly, then continue the roleplay.""",
}


def build_tutor_prompt(
    message: str,
    history: list[Message],
    level: str,
    mode: str,
) -> str:
    history_lines = [
        f"{chat_message.role}: {chat_message.content}"
        for chat_message in history
    ]
    history_text = "\n".join(history_lines) if history_lines else "No prior messages."
    mode_instructions = MODE_INSTRUCTIONS.get(mode, MODE_INSTRUCTIONS["conversation"])

    return f"""You are a warm, practical French tutor.

Learner level: {level}
Lesson mode: {mode}

Teaching rules:
- Keep explanations clear and concise.
- Use French that fits the learner's level.
- Correct mistakes gently without derailing the conversation.
- Ask one useful follow-up question at a time.
- If the learner writes in French, respond with a correction and a natural version.
- If the learner writes in English, help them express the idea in French.

{mode_instructions}

Recent conversation:
{history_text}

Learner's latest message:
{message}

Reply as the tutor."""
