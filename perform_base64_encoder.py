import base64

if __name__ == "__main__":
    password = "<PLACEHOLDER>"

    encoded_password = base64.b64encode(password.encode("utf-8")).decode("utf-8")
    print(encoded_password)