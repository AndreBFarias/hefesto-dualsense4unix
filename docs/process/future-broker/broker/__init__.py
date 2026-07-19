"""Broker root hide-hidraw (BROKER-01).

O módulo `hidraw_broker` é AUTOCONTIDO (stdlib pura): o install copia só o
arquivo para /usr/local/lib/hefesto-dualsense4unix/hefesto-hidraw-broker e ele
roda no python3 do sistema como serviço system root. Ele mora no pacote para
ganhar o gate (ruff/mypy/pytest), não para ser importado pelo daemon — o daemon
fala com o broker pelo socket (`integrations.hidraw_broker_client`).
"""
