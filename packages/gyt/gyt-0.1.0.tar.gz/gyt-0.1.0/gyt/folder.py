"""Project folder"""

import pandas as pd
import uuid
import os
import hashlib
import logging

class Folder(object):
    """emulate a Folder"""
    _columns = ["filename", "mod", "hash"]
    CONTENTFILENAME = ".gyt"

    def __init__(self, *args, **kwargs):
        self.path = kwargs.get("path") or os.getcwd()
        self._content = pd.DataFrame(columns=self._columns)
        self._content.index.name = 'idx'
        self.load()

        self._metadata = kwargs.get("metadata") or {}
        try:
            self.uuid = uuid.UUID(kwargs.get("uuid"))
        except:
            self.uuid = uuid.uuid4()
        self.name = kwargs.get("name") or "N.N."

    @property
    def contentfilepath(self):
        return os.path.join(self.path, self.CONTENTFILENAME)

    @property
    def content(self):
        return self._content

    def import_files(self):
        self.get_content_status()
        self.dump()

    def get_hash(self, filepath):
        if os.path.exists(filepath):
            BLOCKSIZE = 65536
            hasher = hashlib.md5()
            with open(filepath, 'rb') as afile:
                buf = afile.read(BLOCKSIZE)
                while len(buf) > 0:
                    hasher.update(buf)
                    buf = afile.read(BLOCKSIZE)
            return hasher.hexdigest()

    def __str__(self):
        return "(f:%s)" % self.name

    def __repr__(self):
        return "(f:%s)" % self.name

    def ls(self, *args, **kwargs):
        """list dir"""
        return self._content

    def get_content_status(self):
        path = self.path
        content = self.content
        df0 = pd.DataFrame(columns=self._columns)
        df0.index.name = "idx"
        if path is None:
            return
        elif os.path.exists(path) and os.path.isdir(path):
            filenames = os.listdir(path)
            dfdict = {}
            for filename in filenames:
                if filename == self.CONTENTFILENAME:
                    continue

                hash = self.get_hash(os.path.join(path, filename))
#                print("!!!", filename, hash, any(content.filename.isin([filename])))
                if not any(content.filename.isin([filename])):
                    logging.debug("newfile: %s" % filename)
                    dfdict[uuid.uuid4().hex] = {"filename":filename, "mod":False, "hash":hash}
                elif any(content.filename.isin([filename])):
                    file_row = content[content.filename==filename].iloc[0]
                    logging.debug("file '%s' exist" % filename)
                    # print("!", (file_row.name, file_row["filename"]))
                    if file_row.hash!=hash:
                        logging.debug("file '%s' changed" % filename)
                        self._content.ix[file_row.name, 'mod'] = True
                    else:
                        self._content.ix[file_row.name, 'mod'] = False

            df = pd.DataFrame.from_dict(dfdict, orient="index")
            df.index.name = "idx"
            self._content = pd.concat([self._content, df])[self._columns]

    def dump(self):
        """dump content"""
        self._content.to_csv(os.path.join(self.contentfilepath), index_label="idx")

    def load(self):
        """load content"""
        if os.path.exists(self.contentfilepath):
            df = pd.read_csv(self.contentfilepath)
            df.index = df["idx"]
            # print("!!", df.head())
            # print(df.index)
            self._content = df[self._columns]
        return self._content

if __name__ == '__main__':
    os.remove(Folder.contentfilepath)
    f = Folder(name="root", path=os.getcwd())
    f.import_files(os.getcwd())
    print(f)
    print(f.ls())
