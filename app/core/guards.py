CONTACT_URL = "https://sciqusams.com/contact/"

def is_sciqus_related(question: str) -> bool:
    keywords = [
        "sciqus",
        "ams",
        "ticket",
        "ticketing",
        "vendor",
        "portal",
        "account",
        "renewal",
        "proposal",
        "pricing",
        "license",
        "contract",
        "customer",
        "support"
    ]
    q = question.lower()
    return any(k in q for k in keywords)


def out_of_scope_response() -> str:
    return (
        "I’m here to help with questions related to Sciqus AMS.\n\n"
        "For more information or specific queries, please contact us here:\n"
        f"{CONTACT_URL}"
    )


def is_greeting(text: str) -> bool:
    greetings = [
        "hi", "hello", "hey",
        "good morning", "good afternoon", "good evening"
    ]
    t = text.lower().strip()
    return t in greetings or any(t.startswith(g) for g in greetings)


def greeting_response() -> str:
    return (
        "Hello! 👋\n\n"
        "Welcome to Sciqus AMS.\n"
        "How can I help you today?"
    )
