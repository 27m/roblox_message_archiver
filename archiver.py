import httpx


def main():
    client = httpx.Client()
    cookie = input("paste your cookie nerd:")
    head = {
        "cookie": f".ROBLOSECURITY={cookie}",
        "referer": "https://www.roblox.com"
    }

    msg_count = client.get("https://privatemessages.roblox.com/v1/messages/unread/count", headers=head).json()['count']
    print(f"{msg_count} messages found!")
    if input("custom keywords? y or n: ") == "y":
        keywords = input("insert keywords seperated by commas. (ex: bot, op):").split(", ")
    else:
        keywords = []
    if input("archive all roblox generated trade messages? y or n: ").lower() == "y":
        keywords.extend(["your trade", "trade request", "trade is complete"])
    print(f"keywords: {keywords}")

    ids_to_archive = []
    inbox = client.get("https://privatemessages.roblox.com/v1/messages?messageTab=inbox&pageNumber=0", headers=head).json()
    pages = inbox["totalPages"]
    for i in range(pages):
        inbox = client.get(f"https://privatemessages.roblox.com/v1/messages?messageTab=inbox&pageNumber={i}", headers=head).json()
        messages = inbox['collection']
        for msg in messages:
            content = f"{msg['subject']} {msg['body']}".lower()
            for keyword in keywords:
                if keyword in content:
                    ids_to_archive.append(msg['id'])
                    break

    print(f"archiving {len(ids_to_archive)} messages")

    csrf_request = client.post('https://catalog.roblox.com/v1/catalog/items/details', headers=head)
    csrf = csrf_request.headers['x-csrf-token']

    post_headers = {
        "cookie": f".ROBLOSECURITY={cookie}",
        "x-csrf-token": csrf
    }

    for i in range(0, len(ids_to_archive), 10):
        id_chunk = ids_to_archive[i:i + 10]
        print(id_chunk)
        body = {
            "messageIds": id_chunk
        }
        request = client.post("https://privatemessages.roblox.com/v1/messages/archive", headers=post_headers, json=body).json()
        print(request)


if __name__ == "__main__":
    main()
