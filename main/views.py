from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from django.conf.urls.static import static
from imutils import face_utils
import imutils
import numpy as np
import collections
import dlib
import cv2
import requests
import time
from pathlib import Path
import os.path
from main.models import Imagem
from main.serializers import ImagemSerializer


class ImagemViewSet(viewsets.ModelViewSet):
    queryset = Imagem.objects.all()
    serializer_class = ImagemSerializer

    def post(self, request, format=None):
        return JsonResponse({'data':str(request.data)})

def arts(request):
    return JsonResponse({
        'arts':[
            {   
                'id': 1,
                'description': 'Duas irmãs (no terraço), 1889 - Renoir',
                'imagelink': 'http://167.99.54.80:8043/media/arts/image9.jpg'
            },
            {   
                'id': 2,
                'description': 'Moça com livro, 1899 - Almeida Júnior',
                'imagelink': 'http://167.99.54.80:8043/media/arts/image8.jpg'
            },
            {
                'id': 3,
                'description': 'Amolação interrompida, 1894 - Almeida Júnior',
                'imagelink': 'https://lh5.googleusercontent.com/YsZcAZ_wBVdDtDHXUtMnsNh4_NYnvqJfM6kv5GOrKR7FldAu13tmtRn8kyaFA5AkImKOpeteKhyXO1ngttezFzYB1ThfmH3ytQmWEoMYo0P_sRq0GT9PI9xFU8Z2bmcaoPTxBGU'
            },
            {
                'id': 4,
                'description': 'Autorretrato (???) - Arthur Timóteo da Costa',
                'imagelink': 'https://lh3.googleusercontent.com/MGLm7CY5qBjHLAPYTHFmz6NXVRKKVJIgyzwfju_hTxPbN8cA0cveuo_KDrTlElI3obGR7Mupu6gCZbNpA7MoMFLWjeidu3VI0aeJAYPzHQ2oQIKWo89xR5ZdBYJ71dN6gq6ANP0'
            },
            {
                'id': 5,
                'description': 'OS RETIRANTES (1944) - PORTINARI',
                'imagelink': 'https://lh5.googleusercontent.com/w2CVde-laakCRt81BJhufgLMg-OvzguXFvJwZxdAVidTLm26uSwfDA3pIzykH00f2kac5Qn9M7wEYh2y5jtqcc-9ZjWszI5_BriCM1dVWCS5VQeMvspLijQfmyriu5eh4jioknk'
            },
            {
                'id': 6,
                'description': 'O GRITO (1893) – EVARD MUNCH',
                'imagelink': 'https://lh3.googleusercontent.com/G51Qjjg7rGIRpTDydld2HsqzQUzsD2xE-4uYLqofnadpBA0Zz1m10Vle1foRaalvnDmB_3RFp60nk_CQApYHWYUVW0LxihOELMrAM9YDvt0dPBpJ1FMkF1wd5nVStvXG5UgrK3o'
            },
            {   'id': 7,
                'description': 'São João (1969) - Emiliano Di Cavalcanti',
                'imagelink': 'https://lh3.googleusercontent.com/Te1LlDXCLFyj1rTwHSHd4eqfktUWA3is-0vnZ0gDU8DpbUAqT-5lvIBz_0mHr6rHr3Onz3-_Xl8r1Mmrc8tWU2otgYd-4LuXXm-Yhu74UCzHHMXcXh8YfO4alaWjdob8b62HyOI'
            },
            {   
                'id': 8,
                'description': 'Festa Junina (?) – Anita Malfatti',
                'imagelink': 'https://lh3.googleusercontent.com/yjtmmhHW1FJInCZUjVrhPwPqvzR47iQJfuj6cBeIK01sbVDv0dQofNcRTlt_HhmNmvVnmJCW1DmU1Nzy0nWQ6LkhW5xfIJIJaq_x1X2W8uDTZL-TMDGe9HO68rAVWtAChjU0PSg'
            },
            {   'id': 9,
                'description': 'Festa Popular (??) - Djanira da Motta e Silva',
                'imagelink': 'https://lh5.googleusercontent.com/Fw2qLo-7JTYECl2N7KY5c5Lg8B0QGaiSHVzOLb_gPQVqrXtrTlwV692zRc0By7oM-n_rRCAgT0e78ffqj0Dr8G9nMazitm56xqocnAToTAJHcdhr9aK226RxzyK-PIM_cTplskw'
            },
            {
                'id': 10,
                'description': 'Afresco para Teatro (1925) – Di Cavalcanti',
                'imagelink': 'https://lh6.googleusercontent.com/GifEpDOZ1YFHHdun3L_tNI7hIUfVoD0fIMr6ZvuDpo7xU-Ma5yEofrkaaUYbJh7UfeQkiii2UrsdnMnEk_i0P4fGV2nwS26SEo7y7HsmsCZ-LTyE5wgUKEP4FxCJPQ'
            },
            {   'id': 11,
                'description': 'Mulheres Protestando (1941) – Di Cavalcanti',
                'imagelink': 'https://lh3.googleusercontent.com/ofaBS_GPKvZCmy4pVDzOnqFc_a9_AkV4emLh38MCoMwA_EKnqXOvCgD6mhJMHJP3tHrIkjQi96z6LDRjodlCLppzAFJNSb3-HtVJ81jF9KokOa17j5LmJ3y9Zqsch9b7cXdvgDU'
            },
            {
                'id': 12,
                'description': 'Operários (1933) – Tarsila do Amaral',
                'imagelink': 'https://lh6.googleusercontent.com/0sTG4um61V9HuBzDDeB4UJz6x79D0HfGAAzSm71UTmhKIM7iWe4hVLdojP1Kg33qmj9lQwJ4v_YFlYSwpKDTJOZ9vCgtd_dgj5C1JrMHYnxVYTJqoWIvnUnXw8K_tNf2w-I-9ss'
            },
        ]
    }, status=200)
    
def main(request):
    if request.method == 'GET':
        res = {'message':'gleisin', 'caracteristca':'lindo'}
        return JsonResponse(res)

# @action(detail=True, methods=['post'])
# def receiveImage(request):
#     try:
#         file = request.data['file']
#     except KeyError:
#         raise ParseError('Request has no resource file attached')
#     # file = request.data['file']
#     # if os.path.isfile(file):
#     #     return JsonResponse({'error': 'imagem carregada'})
#     # else:
#     #     return JsonResponse({'message': 'imagem nao carregada'})
def imagetest(request):
    # return JsonResponse({'error': str(Path(__file__).resolve().parent.parent)})
    # return JsonResponse({'error': path})
    if os.path.isfile('static/img/rface-no-bg.png'):
        img = cv2.imread('static/img/rface-no-bg.png')
        cv2.imwrite('static/img/kkkkkk.png', img)
        return JsonResponse({'error': 'imagem carregada'})
    else:
        return JsonResponse({'message': 'imagem nao carregada'})
    # image = cv2.imread("../static/img/rface-no-bg.png")
    # if image.size == 0:
    #     return JsonResponse({'error': 'imagem não carregada'})
    # else:
    #     return JsonResponse({'message': 'imagem carregada'})
    # print(image)

def image(request):        
    def face_remap(shape):
        remapped_image = cv2.convexHull(shape)
        return remapped_image

    """
    MAIN CODE STARTS HERE
    """
    # load the input image, resize it, and convert it to grayscale
    inicio = time.time()
    image = cv2.imread('static/img/rface-no-bg.png')
    if not os.path.isfile('static/img/rface-no-bg.png'):
        return JsonResponse({'message': 'imagem nao carregada'})
    image = imutils.resize(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    out_face = np.zeros_like(image)

    # initialize dlib's face detector (HOG-based) and then create the facial landmark predictor
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('static/dlib/shape_predictor_68_face_landmarks.dat')

    # detect faces in the grayscale image
    rects = detector(gray, 1)

    # loop over the face detections
    for (i, rect) in enumerate(rects):
        """
        Determine the facial landmarks for the face region, then convert the facial landmark (x, y)-coordinates to a NumPy array
        """
        shape = predictor(gray, rect)
        
        shape = face_utils.shape_to_np(shape)
        
        #initialize mask array
        remapped_shape = np.zeros_like(shape) 
        feature_mask = np.zeros((image.shape[0], image.shape[1]))   
    
        remapped_shape = face_remap(shape)
        cv2.fillConvexPoly(feature_mask, remapped_shape[0:27], 1)
        # cv2.imshow("mask_inv2",  p)
        # cv2.waitKey()
        # Change this value until it looks the best.
        
        feature_mask = feature_mask.astype(np.bool)
        
        out_face[feature_mask] = image[feature_mask]
        # cv2.imshow("mask_inv",  out_face)
        # cv2.waitKey()
        cv2.imwrite('static/img/out_face2.png', out_face)

        response = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            files={'image_file': open('static/img/out_face2.png', 'rb')},
            data={'size': 'auto'},
            headers={'X-Api-Key': 'Tqcdq9M1bzhzBJoLoX4XZ6xa'},
        )
        if response.status_code == requests.codes.ok:
            with open('static/img/result.png', 'wb') as out:
                out.write(response.content)
        else:
            print("Error:", response.status_code, response.text)
    res = {'message':'tempo de execução', 'time':(time.time() - inicio)}
    return JsonResponse(res)
