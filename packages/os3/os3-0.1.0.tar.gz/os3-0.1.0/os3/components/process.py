# -*- coding: utf-8 -*-
import psutil

from os3.components import GradaleComponent


class Process(psutil.Process, GradaleComponent):
    pass