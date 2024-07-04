import datetime

tabs = {"default":  "",
        "solar":    "\t",
        "pool":     "\t\t",
        "probe":    "\t\t\t",
        "pump":     "\t\t\t\t"}


def note(msg = "", tab = "default", n = 1):
    text = "\n"*n+tabs[tab]+msg
    with open("loggen.txt", "a") as f:
        f.write(text)
        f.close()

#note("message this and that", "pump", 3) for 3 empty lines and the text with 4 indents
