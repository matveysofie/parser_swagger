import difflib
from hashlib import md5
import os
import shutil
import sys

from common.dir_config import BACKUPDIR, SWAGGERDIR
from utils.logger import log

if not os.path.exists(SWAGGERDIR):
    os.makedirs(SWAGGERDIR)


class HandleDirFile(object):
    def read_file(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as fileHandle:
                return fileHandle.readlines()
        except IOError as e:
            log.error("Не удалось прочитать файл: " + str(e))
            sys.exit()

    def md5_file(self, filename):
        m = md5()
        try:
            with open(filename, 'rb') as file:
                m.update(file.read())
        except Exception as e:
            log.error("Не удалось прочитать файл: " + str(e))
        return m.hexdigest()

    def diff_files(self, filename1, filename2):
        file1Md5 = self.md5_file(filename1)
        file2Md5 = self.md5_file(filename2)

        if file1Md5 != file2Md5:
            lines1 = self.read_file(filename1)
            lines2 = self.read_file(filename2)
            d = difflib.HtmlDiff()
            result = d.make_file(lines1, lines2, filename1, filename2, context=True)
            try:
                with open(diffFile, 'a', encoding='utf-8') as result_file:
                    result_file.write(result)
            except Exception as e:
                log.error("Не удалось выполнить запись в файл: " + str(e))

    def move_file(self, srcPath, destPath):
        try:
            shutil.move(srcPath, destPath)
        except Exception as e:
            raise e

    def copy_dir(self, srcPath, destPath):
        if os.path.isdir(destPath):
            log.info(f"{destPath} - удаление, если существует")
            shutil.rmtree(destPath)
        try:
            shutil.copytree(srcPath, destPath)
        except Exception as e:
            raise e

    def copy_file(self, srcPath, destPath):
        destFiles = set(self.get_file_list(destPath))
        srcFiles = set(self.get_file_list(srcPath))

        missingFiles = srcFiles - destFiles
        for file in missingFiles:
            log.info(f"Файл {file} не существует в каталоге резервной копии")
            destDir = os.path.join(BACKUPDIR, os.path.dirname(file))
            os.makedirs(destDir, exist_ok=True)
            shutil.copyfile(file, os.path.join(destDir, os.path.basename(file)))

    def diff_dir_files(self, srcPath, destPath):
        if os.path.isfile(diffFile):
            try:
                shutil.copyfile(diffFile, backupDiffFile)
                os.remove(diffFile)
            except Exception as e:
                log.error(f"Резервное копирование или удаление файла {diffFile}, ошибка!")
                raise e
        else:
            log.info(f"Файл не найден: {diffFile}")

        srcFiles = self.get_file_list(srcPath)
        destFiles = self.get_file_list(destPath)

        for srcFile in srcFiles:
            for destFile in destFiles:
                if os.path.basename(srcFile) == os.path.basename(destFile):
                    self.diff_files(srcFile, destFile)

    def get_file_list(self, dirPath):
        file_list = []
        for root, _, files in os.walk(dirPath):
            for file in files:
                file_list.append(os.path.join(root, file))
        return file_list


handlefile = HandleDirFile()
