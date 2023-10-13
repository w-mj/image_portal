import json
import subprocess
from typing import IO, AnyStr, List

import paramiko

from endpoints.endpoint import Endpoint, HostItem, Image


class DockerCLIEndpoint(Endpoint):
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
                self._parse_size(j.get("ID"))
            )
            ans.append(img)
        return ans

    def _separate_addr(self, addr: str) -> (str, int):
        if ':' in addr:
            x = addr.split(':', 2)
            return x[0], int(x[1])
        return addr, 22

    def get_images(self) -> List[Image]:
        if self.host.get_addr() == "localhost":
            data = subprocess.check_output(["docker", "images", "--format", "json"]).decode()
        else:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            addr, port = self._separate_addr(self.host.get_addr())
            ssh.connect(
                hostname=addr,
                port=port,
                username=self.host.get_user(),
                password=self.host.get_pass()
            )
            _, stdout, stderr = ssh.exec_command("docker images --format json")
            stderr = stderr.read().decode()
            if stderr:
                raise RuntimeError(stderr)
            data = stdout.read()
        return self._parse_docker_images(data)

    def get_image_stream(self, image: Image) -> IO[AnyStr]:
        pass

    def create_image_stream(self, image: Image) -> IO[AnyStr]:
        pass

    def __init__(self, host: HostItem):
        super().__init__(host)
        assert (host.get("type") == "Docker CLI")
        self.host = host
