from flask import Flask, Response
from flask import request, abort
import video_maker
import requests
app = Flask(__name__)

'''
    Webservice para recebimento de requisição de processamento de vídeo.
'''

@app.route('/movie_api/process_video/', methods=['POST'])
def process_video():
    if not request.json or not 'id' in request.json:
        abort(400)
    print(request.json)
    try:
        rotation = int(request.json['rotation'])
    except:
        rotation = int("0")
    video_infos = {
        'id': request.json['id'],
        'images_path':request.json['path'],
        'rotation': rotation,
        'images_ext': request.json['files_extension'],
        'video_ext': request.json['video_ext'],
        'return_url': request.json['return_url'],
        'error_url': request.json['error_url']

    }
    processed = create_video(video_infos)
    if processed:
        return Response("Processed", status=200, mimetype='application/json')
    else:
        return Response("Fail on processing", status=500, mimetype='application/json')

'''
    Chamada das funções de criação de vídeos e feedback sobre a geração do vídeo.
'''
def create_video(video_infos):
	try:
		video = video_maker.make_video(image_folder=video_infos['images_path'], out_video_name='video', out_video_ext=video_infos['video_ext'], rotation_angle=video_infos['rotation'], image_ext=video_infos['images_ext'], vid_to_web=True)
		if video is not None:
			video_maker.move_images(video_infos['images_path'], video_infos['images_ext'])
			save_video(video_infos['id'], video_infos['return_url'])
			print("video created")
			return True
		else:
			inform_error(video_infos['id'], video_infos['error_url'])
			print("error")
			return False
	except:
		return False

'''
    Função de feedback sobre sucesso na geração de vídeo. 
'''
def save_video(json_id, return_url):
    try:
        request_url = return_url + str(json_id)
        r = requests.get(request_url)
        print(r.status_code)
    except:
        print("Deu ruim...")

'''
    Função de feedback sobre erro na geração de vídeo. 
'''
def inform_error(json_id, error_url):
    try:
        request_url = error_url + str(json_id)
        r = requests.get(request_url)
        print(r.status_code)
    except:
        print("Deu ruim...")


if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)
