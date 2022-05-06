from flask import Flask, render_template, request
import requests as req
import speech_recognition as sr

from commands.command import run_command
from docker.python_on_docker import python_on_docker
from docker.httpd_on_docker import httpd_on_docker
from hadoop.hadoop_cluster import create_hadoop_cluster
from kubernetes.kubernetes_cluster import configure_kube_master, configure_kube_slave
from aws.ha_arch_on_aws import launch_ec2_instance, create_ebs_volume, attach_ebs_volume, upload_to_s3_bucket, create_cloudfront_distribution

app = Flask("DevOps Assistant")

server_ip = ""
#aws instance public ip

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/menu")
def menu():
    template = "menu.html"
    return render_template(template)

@app.route("/task")
def task():
    choice = request.args.get("choice")
    template = "menu.html"
    if choice == "1":
        template = "command/command.html"
    elif choice == "2":
        contents = python_on_docker(server_ip)
        template = "response.html"
    elif choice == "3":
        template = "docker/httpd_docker.html"
    elif choice == "4":
        template = "hadoop/hadoop_cluster.html"
    elif choice == "5":
        template = "kubernetes/kubernetes_cluster.html"
    elif choice == "6":
        template = "aws/ha_arch_on_aws.html"
    else:
        template = "menu.html"
    return render_template(template)

@app.route("/run-commands")
def run_commands():
    command = request.args.get("command")
    contents = run_command(server_ip, command)
    template = "response.html"
    return render_template(template, response=contents)

@app.route("/httpd-on-docker")
def httpd_docker():
    image_name = request.args.get("image-name")
    contents = httpd_on_docker(server_ip, image_name)
    template = "response.html"
    return render_template(template, response=contents)

@app.route("/create-hadoop-cluster")
def hadoop_cluster():
    namenode_ip = request.args.get("namenode-ip")
    namenode_port = request.args.get("namenode-port")
    namenode_directory = request.args.get("namenode-directory")
    datanode_ip = request.args.get("datanode-ip")
    datanode_directory = request.args.get("datanode-directory")
    contents = create_hadoop_cluster(server_ip, namenode_ip, namenode_port, namenode_directory, datanode_ip, datanode_directory)
    template = "response.html"
    return render_template(template, response=contents)

@app.route("/configure-kubernetes-master")
def config_kube_master():
    pod_network_cidr = request.args.get("pod-network-cidr")
    owner = request.args.get("owner")
    group = request.args.get("group")
    contents = configure_kube_master(server_ip, pod_network_cidr, owner, group)
    template = "response.html"
    return render_template(template, response=contents)

@app.route("/configure-kubernetes-slave")
def config_kube_slave():
    kube_join_command = request.args.get("kube-join-command")
    contents = configure_kube_slave(server_ip, kube_join_command)
    template = "response.html"
    return render_template(template, response=contents)

@app.route("/launch-ec2-instance")
def launch_instance():
    image_id = request.args.get("image-id")
    instance_type = request.args.get("instance-type")
    count = request.args.get("count")
    subnet_id = request.args.get("subnet-id")
    security_group_id = request.args.get("security-group-id")
    key_name = request.args.get("key-name")
    contents = launch_ec2_instance(server_ip, image_id, instance_type, count, subnet_id, security_group_id, key_name)
    template = "response.html"
    return render_template(template, response=contents)

@app.route("/create-ebs-volume")
def create_ebs_vol():
    availability_zone = request.args.get("availability-zone")
    volume_type = request.args.get("volume-type")
    size = request.args.get("size")
    key = request.args.get("key")
    value = request.args.get("value")
    contents = create_ebs_volume(server_ip, availability_zone, volume_type, size, key, value)
    template = "response.html"
    return render_template(template, response=contents)

@app.route("/attach-ebs-volume")
def attach_ebs_vol():
    volume_id = request.args.get("volume-id")
    instance_id = request.args.get("instance-id")
    device_name = request.args.get("device-name")
    contents = attach_ebs_volume(server_ip, volume_id, instance_id, device_name)
    template = "response.html"
    return render_template(template, response=contents)

@app.route("/upload-to-s3-bucket")
def upload_to_bucket():
    local_file_location = request.args.get("local-file-location")
    s3_bucket_location = request.args.get("s3-bucket-location")
    acl = request.args.get("acl")
    contents = upload_to_s3_bucket(server_ip, local_file_location, s3_bucket_location, acl)
    template = "response.html"
    return render_template(template, response=contents)

@app.route("/create-cloudfront-distribution")
def create_distribution():
    bucket_name = request.args.get("bucket-name")
    default_root_object = request.args.get("default-root-object")
    contents = create_cloudfront_distribution(server_ip, bucket_name, default_root_object)
    template = "response.html"
    return render_template(template, response=contents)

# Voice recognition
@app.route("/get-voice")
def get_voice():
    template = "menu.html"
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
    userRequest = recognizer.recognize_google(audio)

    if ((("run" in userRequest) or ("execute" in userRequest)) and (("commands" in userRequest) or ("command" in userRequest))):
        template = "command/command.html"
    elif ((("create" in userRequest) or ("provision" in userRequest) or ("configure" in userRequest) or ("launch" in userRequest)) and ((("python" in userRequest) or ("Python" in userRequest)) and ("docker" in userRequest))):
        contents = python_on_docker(server_ip)
        template = "response.html"
    elif ((("create" in userRequest) or ("provision" in userRequest) or ("configure" in userRequest) or ("launch" in userRequest)) and ((("httpd" in userRequest) or ("apache" in userRequest) or ("Apache" in userRequest)) and ("docker" in userRequest))):
        template = "docker/httpd_docker.html"
    elif ((("create" in userRequest) or ("provision" in userRequest) or ("configure" in userRequest) or ("launch" in userRequest)) and ((("hadoop" in userRequest) or ("hdfs" in userRequest) or (("Hadoop" in userRequest))) and ("cluster" in userRequest))):
        template = "hadoop/hadoop_cluster.html"
    elif ((("create" in userRequest) or ("provision" in userRequest) or ("configure" in userRequest) or ("launch" in userRequest)) and ((("kubernetes" in userRequest) or ("k8s" in userRequest)) and ("cluster" in userRequest))):
        template = "kubernetes/kubernetes_cluster.html"
    elif ((("create" in userRequest) or ("provision" in userRequest) or ("configure" in userRequest) or ("launch" in userRequest)) and (("HA" in userRequest) or (("High" in userRequest) and ("availability" in userRequest)) or ("infrastructure" in userRequest)) and (("aws" in userRequest) or (("Amazon" in userRequest) and ("cloud" in userRequest)))):
        template = "aws/ha_arch_on_aws.html"
    else:
        print("Unable to perform!")
        template = "menu.html"
    return render_template(template, response=userRequest)

app.run(host="0.0.0.0", port=8080)
