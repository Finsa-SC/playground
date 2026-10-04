## Free Wifi
WIFI_NAME = "Hadroh modern semut ireng"

def get_password() -> str:
    password = ""

    odd = []
    for i in range(20):
        if i % 2 == 0:
            odd.append(str(i))
    password += "".join(odd[-3:])

    password += odd[0] * 4

    return password

print(get_password())