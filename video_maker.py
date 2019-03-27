import cv2
from cv2 import VideoWriter, imread, imwrite
import os, imutils, shutil


'''
    Método para juntar as imagens da pasta selecionada em um vídeo no formato AVI.
    Os parâmetros necessários para o funcionamento são :
    
    image_folder - Path da pasta que contem as imagens a serem processadas. Ex.: "/home/logdev/imagens/" [string]
    out_video_name - Nome do vídeo que será gerado pela função (sem a extensão). Ex.: "video_veiculo" [string]
    out_video_ext - Extensão do vídeo que será gerado pela função. Ex.: ".mp4" [string]
    rotation_angle - Angulo de rotação que deverá ser aplicado às imagens. Ex.: -90 [int]
    image_ext - Extensão das imagens da pasta que serão utilizadas. Ex.: ".jpg" [string]
    vid_to_web - Flag para chamada da função de transformação do video para formato web. Ex.: True [bool]
'''
def make_video(image_folder, out_video_name, out_video_ext, rotation_angle, image_ext, vid_to_web, fps=5, size=None, is_color=True, format="FMP4"):
    """
    Create a video from a list of images.
 
    @param      outvid      output video
    @param      images      list of images to use in the video
    @param      fps         frame per second
    @param      size        size of each frame
    @param      is_color    color
    @param      format      see http://www.fourcc.org/codecs.php
    @return                 see http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html
 
    The function relies on http://opencv-python-tutroals.readthedocs.org/en/latest/.
    By default, the video will have the size of the first image.
    It will resize every image to this size before adding them to the video.
    """
    images = [image_folder+img for img in os.listdir(image_folder) if img.endswith(image_ext)]
    fourcc = cv2.cv.CV_FOURCC(*format)
    vid = None
    image_thumb = None
    image_thumb_path = None
    images.sort()
    for image in images:
        if not os.path.exists(image):
            raise FileNotFoundError(image)
        print(image)
        img = imread(image)
        if image_thumb is None and image[-6:] == "00.jpg":
            image_thumb = imutils.rotate_bound(img, rotation_angle)
            image_thumb_path = image
        if(rotation_angle):
            img = imutils.rotate_bound(img, rotation_angle)
        if vid is None:
            if size is None:
                size = img.shape[1], img.shape[0]
            print(image_folder + out_video_name)
            vid = VideoWriter((image_folder + out_video_name+".avi"), fourcc, float(fps), size, is_color)
        vid.write(img)
    if vid is not None:
        vid.release()
    if image_thumb is not None:
        imwrite(image_thumb_path, image_thumb)
    if vid_to_web:
        make_for_web(image_folder, (out_video_name+".avi"), (out_video_name+out_video_ext))
    print(vid)
    return vid

'''
    Função para converter o vídeo original do formato AVI para MP4, utilizando os codecs de vídeo compatíveis com a tag <video> do HTML 5
'''
def make_for_web(video_path, original_video_name, video_name):
    original_video= video_path+original_video_name
    new_video= video_path+video_name
    os.system("ffmpeg -y -i "+original_video+" -f mp4 -vcodec libx264 -profile:v main -acodec aac " +new_video)

'''
    Função para mover os arquivos de imagem originais para uma nova pasta. A intenção é evitar que o arquivo de vídeo seja alterado após ser 
    gerado (Chamada dupla [por bug ou erro] do método de geração de vídeo)
'''
def move_images(images_folder, image_ext):
    path = images_folder+"thumbs/"
    os.mkdir(path)
    for img in os.listdir(images_folder):
        image = images_folder+img
        if image.endswith(image_ext):
            shutil.move(image, path+img)
