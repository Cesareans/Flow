# coding=utf-8
import hashlib
import os

from base.config import Config_File_Path
from common.project_path import ProjectPath
from dispatch.handler.ihandler import PacketHandler, IHandler
from game.concept.md5_info import Md5Info
from packet.inbound.ask_file import AskFile
from packet.inbound.ask_file import AskMd5
from packet.outbound.config_file import FileContent
from packet.outbound.config_file import FileMD5s


def getFileMd5(fileName):
    if not os.path.isfile(fileName):
        return
    md5hash = hashlib.md5()
    with open(fileName, 'rb') as f:
        part = f.read()
        md5hash.update(part)
    #        while True:
    #            part = f.read(8096)
    #            if not part:
    #                break
    #        md5hash.update(part)
    f.close()
    return md5hash.hexdigest()


@PacketHandler(AskMd5)
class FetchAskMd5(IHandler):
    def handle(self, context, packet):
        md5List = []
        configPath = ProjectPath().filepath(Config_File_Path)
        for name in os.listdir(configPath):
            fileName = configPath + name
            md5 = getFileMd5(fileName)
            md5List.append(Md5Info(name, md5))
        context.fireOutboundHandle(FileMD5s(md5List))


@PacketHandler(AskFile)
class FetchAskedFiles(IHandler):

    def handle(self, context, packet):
        configPath = ProjectPath().filepath(Config_File_Path)
        for name in packet.fileNames:
            fileName = configPath + name
            with open(fileName, 'rb') as f:
                while True:
                    part = f.read(8096)
                    if not part:
                        context.fireOutboundHandle(FileContent(name, "", True))
                        break
                    context.fireOutboundHandle(FileContent(name, part, False))
