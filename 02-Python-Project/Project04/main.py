def load_contacts():
    try:
        with open("contacts.json", "r", encoding="utf-8") as file:
            return json.loads(file.read())

    except:
        return []


def save_contacts(contacts):
    with open("contacts.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(contacts, ensure_ascii=False))
