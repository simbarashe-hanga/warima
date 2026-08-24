def detect_intent(text: str, session):
    text = text.lower().strip()

    if text in ["hi", "hello", "hey"]:
        return {"intent": "greeting"}

    if "contribute" in text:
        return {"intent": "start_contribution"}

    if "agent" in text:
        return {"intent": "agent"}

    if "portfolio" in text or "wallet" in text:
        return {"intent": "portfolio"}

    if "pigs" in text or "pig" in text:
        return {"intent": "pigs"}

    if text.startswith("buy"):
        # Extract amount: "buy-500" -> 500
        parts = text.split()
        amount = 0
        if len(parts) > 1 and parts[1].isdigit():
            amount = int(parts[1])
        return {"intent": "buy_pig", "amount": amount}

    if text.startswith("sell"):
        parts = text.split()
        pig_id = 0
        if len(parts) > 1 and parts[1].isdigit():
            pig_id = int(parts[1])
        return {"intent": "sell_pig", "pig_id": pig_id}

    if text.startswith("health"):
        parts = text.split()
        pig_id = 0
        if len(parts) > 1 and parts[1].isdigit():
            pig_id = int(parts[1])
        return {"intent": "health", "pig_id": pig_id}

    if text == "1":
        return {"intent": "confirm"}

    if text == "2":
        return {"intent": "cancel"}
    
    if text.isdigit():
        return {"intent": "provide_amount", "amount": int(text)}

    return {"intent": "unknown"}
