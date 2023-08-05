#!/usr/bin/env python3
import sys

from docker_ascii_map.argument_parser import get_input_parameters
from docker_ascii_map.ascii_render import Renderer
from docker_ascii_map.docker_config import ConfigParser

if __name__ == '__main__':
    color_mode = get_input_parameters()[0]
    config_parser = ConfigParser()
    renderer = Renderer()

    config = config_parser.get_configuration()
    # print(config)
    text = renderer.render(config, encoding=sys.stdout.encoding, color=color_mode)
    print(text)
