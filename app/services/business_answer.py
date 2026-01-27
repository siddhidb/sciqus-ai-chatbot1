from app.core.feature_selector import select_features_for_business
from app.knowledge.features import FEATURES
import os

CONTACT = os.getenv("CONTACT_URL")

def build_business_answer(business_type: str):
    selected = select_features_for_business(business_type)

    if not selected:
        return (
            "Based on your business type, I couldn't find a suitable "
            "match in Sciqus AMS features. Please contact our team."
            f"\n\nGet in touch: {CONTACT}"
        )

    response = (
        f"For a {business_type} business, Sciqus AMS can help you in these ways:\n\n"
    )

    for f in selected:
        response += (
            f"• **{f}** – {FEATURES[f]['description']}\n"
            f"  Learn more: {FEATURES[f]['url']}\n\n"
        )

    response += f"If you'd like to use these services, contact us here:\n{CONTACT}"

    return response
