from app.core.qa_engine import answer_question

while True:
    q = input("\nAsk about Sciqus AMS (type 'exit' to quit): ")
    if q.lower() == "exit":
        break

    answer = answer_question(q)
    print("\n🤖 Answer:\n", answer)
