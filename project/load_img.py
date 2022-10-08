import os, re #태그 제거

def get_sources(path, directory_name, series_num):
    img_path = path+"/"+directory_name+"/"+series_num
    os.chdir(img_path)
    return os.listdir(img_path)

images = get_sources("C:/Users/hgene/Downloads", "조조코믹스", "작별인사 3화")
print(os.getcwd())
print(images)

