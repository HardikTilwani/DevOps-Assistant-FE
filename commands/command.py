import requests as req

def run_command(server_ip, command):
    url = f"http://{server_ip}/cgi-bin/DevOps-Assistant-BE/command.py?command={command}"
    res = req.get(url)
    contents = res.text
    return contents