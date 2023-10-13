import json
import subprocess
from typing import IO, AnyStr, List

import paramiko
from paramiko.channel import ChannelFile

from endpoints.endpoint import Endpoint,  Image


class SSHChannel(IO[AnyStr]):
    def __init__(self, chan: ChannelFile):
        self.chan = chan

    def close(self) -> None:
        self.chan.close()

    def read(self, __n: int = ...) -> AnyStr:
        return self.chan.read(__n)

    def write(self, __s: AnyStr) -> int:
        self.chan.write(__s)
        return len(__s)


class DockerCLIEndpoint(Endpoint):
    def error(self) -> str:
        return ""

    def _parse_size(self, size: str) -> float:
        units = ["GB", "MB", "KB", "B"]
        factor = [1 << 30, 1 << 20, 1 << 10, 1]
        for i in range(len(units)):
            u = units[i]
            if u in size:
                size = size.replace(u, "")
                return float(size) * factor[i]
        return float(size)

    def _parse_docker_images(self, data) -> List[Image]:
        ans = []
        for line in data.split('\n'):
            line = line.strip()
            if not line:
                continue
            j = json.loads(line)
            img = Image(
                f'{j.get("Repository")}:{j.get("Tag")}',
                self._parse_size(j.get("Size")),
                j.get("ID"),
            )
            ans.append(img)
        return ans

    def _separate_addr(self, addr: str) -> (str, int):
        if ':' in addr:
            x = addr.split(':', 2)
            return x[0], int(x[1])
        return addr, 22

    def _connect_ssh(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        addr, port = self._separate_addr(self.addr)
        ssh.connect(
            hostname=addr,
            port=port,
            username=self.user,
            password=self.password,
        )
        return ssh

    def get_images(self) -> List[Image]:
        if self.addr == "localhost":
            data = subprocess.check_output(["docker", "images", "--format", "json"]).decode()
        else:
            ssh = self._connect_ssh()
            _, stdout, stderr = ssh.exec_command("docker images --format json")
            stderr = stderr.read().decode()
            if stderr:
                raise RuntimeError(stderr)
            data = stdout.read()
        return self._parse_docker_images(data)

    def get_image_stream(self, image: Image) -> IO[AnyStr]:
        if self.addr == "localhost":
            pro = subprocess.Popen(["docker", "save", image.name()], stdout=subprocess.PIPE)
            return pro.stdout
        else:
            ssh = self._connect_ssh()
            _, stdout, _ = ssh.exec_command(f"docker save {image.name}")
            return SSHChannel(stdout)

    def create_image_stream(self, image: Image) -> IO[AnyStr]:
        if self.addr == "localhost":
            pro = subprocess.Popen(["docker", "load"], stdin=subprocess.PIPE)
            return pro.stdin
        else:
            ssh = self._connect_ssh()
            stdin, _, _ = ssh.exec_command(f"docker load")
            return SSHChannel(stdin)

    def __init__(self, _type, _addr, _user, _pass):
        super().__init__(_type, _addr, _user, _pass)
        assert (_type == "Docker CLI")
        self.addr = _addr
        self.user = _user
        self.password = _pass
