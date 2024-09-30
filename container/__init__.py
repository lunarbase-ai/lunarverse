# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
from time import sleep
from typing import Optional, Dict
from urllib.parse import urlparse

import docker
import requests
from docker.errors import ImageNotFound

from lunarcore.core.component import BaseComponent
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentModel
from lunarcore.core.typings.datatypes import DataType


class Container(
    BaseComponent,
    component_name="Container",
    component_description="""Runs a service in a Docker container based on the provided image. If necessary it downloads the image beforehand.
    It only supports already built images or downloadable from Docker registry.""",
    input_types={"endpoint": DataType.TEMPLATE, "parameters": DataType.JSON},
    output_type=DataType.JSON,
    component_group=ComponentGroup.SERVICES,
    image_name=None,
    container_name=None,
    registry_user="$LUNARENV::CONTAINER_REGISTRY_USER",
    registry_password="$LUNARENV::CONTAINER_REGISTRY_PASSWORD",
    container_env=None,
    startup_grace=5,
):
    CONTAINER_STARTUP_GRACE = 5

    def __init__(self, model: Optional[ComponentModel] = None, **kwargs):
        super().__init__(model=model, configuration=kwargs)
        self.client = docker.from_env()

    def run(
        self,
        endpoint: str,
        parameters: Optional[Dict] = None,
    ):
        if parameters is None:
            parameters = dict()

        parsed_endpoint = urlparse(endpoint)
        host, _, _ = parsed_endpoint.netloc.partition(":")
        if host not in ["localhost", "127.0.0.1"]:
            raise ValueError(f"Only localhost connections are supported. Got {host}")

        container_name = self.configuration.get("container_name")
        if container_name is None:
            container_name = f"lunar-container"
        container_name += f"_{self.component_model.id}"

        image_name = self.configuration.get("image_name")
        if image_name is None:
            raise ValueError(f"Expected image name configuration.")

        try:
            image = self.client.images.get(image_name)
        except ImageNotFound:
            image = self.client.images.pull(image_name, auth_config=dict())

        exposed_ports = image.attrs.get("Config", dict()).get("ExposedPorts", dict())
        config_ports = dict()
        if len(exposed_ports):
            for container_port in exposed_ports.keys():
                container_port_protocol = str(container_port).split("/")
                if len(container_port_protocol) == 1:
                    config_ports[int(container_port[0])] = (
                        "127.0.0.1",
                        int(container_port),
                    )
                elif len(container_port_protocol) == 2:
                    config_ports[container_port] = (
                        "127.0.0.1",
                        int(container_port_protocol[0]),
                    )
        envs = (self.configuration.get("container_env") or "").split(";")
        if len(envs) == 1 and envs[0] == "":
            envs = None
        container = self.client.containers.run(
            image=image_name,
            name=container_name,
            auto_remove=True,
            detach=True,
            ports=config_ports,
            environment=envs,
        )

        try:
            wait_pace = 1
            elapsed_time = 0
            while container.status != "running" and elapsed_time < int(
                self.configuration.get(
                    "startup_grace", self.__class__.CONTAINER_STARTUP_GRACE
                )
            ):
                sleep(wait_pace)
                elapsed_time += wait_pace
                continue

            if len(parameters) > 0:
                response = requests.post(endpoint, json=parameters)
            else:
                response = requests.get(endpoint)

            try:
                return response.json()
            except requests.exceptions.JSONDecodeError:
                return {"status_code": response.status_code, "content": response.text}
        finally:
            container.stop(timeout=10)
