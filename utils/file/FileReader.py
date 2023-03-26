class FileReader(object):
    def __init__(self, filename="", readRow=None, rowInd=0):
        """

        :param filename: test file path
        :param readRow:  文件中所有行组成的list 包括空行
        :param rowInd: 当前读到的行数
        """
        if readRow is None:
            readRow = []
        self._filename = filename
        self._readRow = readRow
        self._rowInd = rowInd
        self.readFile2Row()

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, filename):
        self._filename = filename

    @property
    def readRow(self):
        return self._readRow

    @readRow.setter
    def readRow(self, readRow):
        self._readRow = readRow
        self._rowInd = 0

    @property
    def rowInd(self):
        return self._rowInd

    @rowInd.setter
    def rowInd(self, rowInd):
        self._rowInd = rowInd

    def userowInd(self, index):
        try:
            return self._readRow[index]
        except IndexError:
            print("超出下标")
            return None

    def nextRow(self):
        try:
            self.rowInd += 1
            return self._readRow[self._rowInd - 1]
        except IndexError:
            self.rowInd -= 1
            return None

    def readFile2Row(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as ffr:
                line = ffr.readline()
                while line:
                    # txt_data = eval(line)
                    self._readRow.append(line.strip('\n'))
                    # print(type(line))
                    line = ffr.readline()
            # print(self.readRow)
        except FileNotFoundError:
            print('无法打开指定的文件!')
        except LookupError:
            print('指定了未知的编码!')
        except UnicodeDecodeError:
            print('读取文件时解码错误!')
        finally:
            ffr.close()


if __name__ == '__main__':
    fr = FileReader(filename="../../lexerO/test.txt")
    # fr.readFile2Row()
    # print(fr.userowInd(5))
    # ut = fr.nextRow()
    # while ut is not None:
    #     print(ut)
    #     ut = fr.nextRow()
    print(fr.readRow)
