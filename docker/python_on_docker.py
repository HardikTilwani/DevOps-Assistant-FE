import requests as req

def python_on_docker(server_ip):
    url = f"http://{server_ip}/cgi-bin/DevOps-Assistant-BE/docker.py?x=python"
    res = req.get(url)
    contents = res.text
    return contents