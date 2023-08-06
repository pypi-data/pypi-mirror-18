import gyt
import gyt.folder
# print(gyt.__file__)
import os
import pandas as pd

modulepath = os.path.dirname(__file__)

def test_folder():
    foldername = "project0815"
    projectpath = os.path.join(modulepath, foldername)

    contentfilepath = os.path.join(projectpath, gyt.folder.Folder.CONTENTFILENAME)
    # if os.path.exists(contentfilepath):
    #     os.remove(contentfilepath)

    newfile = os.path.join(projectpath, "new.txt")
    readme = os.path.join(projectpath, "README")
    if os.path.exists(newfile):
        os.remove(newfile)

    with open(readme, "w") as fh:
        fh.write("hello world")

    print(os.listdir(projectpath))

    f = gyt.folder.Folder(name=foldername, path=projectpath)
    f.import_files()
    f.get_content_status()
    print("!1", f.content)
    # print(f)
    # print(f.ls())
    # print("!", f.load().columns)
    with open(readme, "w") as fh:
        fh.write("hello world!")

    with open(newfile, "w") as fh:
        fh.write("hello world!")

    f.get_content_status()
    print("!2", f.content)
    assert f.name == foldername, f.name

def test_dump():
    dfdict = {'c37181811ebf400a9bd3e213c6e78870': {'hash': '55b84a9d317184fe61224bfb4a060fb0', 'mod': False, 'name': 'bigdata.dat'}, '4286d30ad3d64372a894c54b1701fb7b': {'hash': '5eb63bbbe01eeed093cb22bb8f5acdc3', 'mod': False, 'name': 'README'}}
    df = pd.DataFrame.from_dict(dfdict, orient="index")
    df.index.name = "idx"
    print(df)

if __name__ == '__main__':
    test_folder()
    #test_dump()