# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：      paramiko
   Description:
   Author:          Lijiamin
   date：           2023/4/10 20:47
-------------------------------------------------
   Change Activity:
                    2023/4/10 20:47
-------------------------------------------------
"""
from typing import Optional, Any, List
from pydantic import BaseModel
from netpalm.backend.core.models.models import Webhook


class ParamikoConnectionArgs(BaseModel):
    host: Optional[str] = None
    username: str
    password: str
    timeout: int
    port: int


class ParamikoGetConfig(BaseModel):
    connection_args: ParamikoConnectionArgs
    command: Any
    webhook: Optional[Webhook] = None