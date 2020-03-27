import os
from wand.image import Image


def process(file_dir):
    """
    将pdf文件转换为jpg
    """
    for files in os.walk(file_dir):
        for file_name in files[2]:
            file_path = file_dir
            [file_name_prefix, file_name_suffix] = file_name.split('.')
            file = files[0] + '/' + file_name
            with(Image(filename=file, resolution=300)) as img:
                images = img.sequence
                pages = len(images)
                for i in range(pages):
                    images[i].type = 'truecolor'
                    save_name = save_dir + file_name_prefix + str(i) + '.jpg'
                    Image(images[i]).save(filename=save_name)


if __name__=="__main__":
    codepath = os.path.dirname(__file__)
    file_dir = codepath + '/PDF/综合/'
    save_dir = codepath + '/IMG/图片/'
    process(file_dir)

