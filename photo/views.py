from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.conf.urls.static import static
from django.http import JsonResponse
from .serializers import UploadSerializer
from PIL import Image
import PIL
from imutils import face_utils
import imutils
import numpy as np
import collections
import dlib
import cv2
import requests
import time
import os
import random, string

# ViewSets define the view behavior.
class UploadViewSet(ViewSet):
    serializer_class = UploadSerializer

    def list(self, request):
        return Response("GET API")

    def create(self, request):
        print(request.FILES)
        file_uploaded = request.FILES.get('file_uploaded')
        # content_type = file_uploaded.content_type
        # im1 = Image.open(file_uploaded)
        # im1.save('static/img/gleisin-google-4-3.png')
        # return auto_rotate(file_uploaded)
        # return Response('test')
        im1 = Image.open(file_uploaded)
        im1.save('static/img/app-image.png')
        return process_image('static/img/app-image.png')
        # response = "POST API and you have uploaded a {} file".format(content_type)
        # return Response(response)

def process_image(image_url):        
    def face_remap(shape):
        remapped_image = cv2.convexHull(shape)
        return remapped_image

    """
    MAIN CODE STARTS HERE
    """
    # load the input image, resize it, and convert it to grayscale
    inicio = time.time()
    image = cv2.imread(image_url)
    # if not os.path.isfile(image):
    #     return JsonResponse({'message': 'imagem nao carregada'})
    image = imutils.resize(image, width=300, height=200)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    out_face = np.zeros_like(image)

    # initialize dlib's face detector (HOG-based) and then create the facial landmark predictor
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('static/dlib/shape_predictor_81_face_landmarks.dat')

    # detect faces in the grayscale image
    rects = detector(gray, 1)

    if not rects:
        res = {'message':'tempo de execução', 'time':(time.time() - inicio)}
        return JsonResponse({
            "tempo de execução":res,
            "message": 'Não foi possivel processar a imagem'
        }, status = 400)
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
            headers={'X-Api-Key': 'Gv8Aur8wRteDAhF6ri8MrXuv'},
        )
        if response.status_code == requests.codes.ok:
            name_file_image = (''.join(random.choice(string.ascii_letters) for i in range(8))) + '.png'
            local_fold = 'static/' + name_file_image
            with open(local_fold, 'wb') as out:
                out.write(response.content)
        else:
            print("Error:", response.status_code, response.text)
            res = {'message':'tempo de execução', 'time':(time.time() - inicio)}
            return JsonResponse({
                "tempo de execução":res,
                "message": response.text
            })
    res = {'message':'tempo de execução', 'time':(time.time() - inicio)}
    return JsonResponse({
        "tempo de execução":res, 
        "link": f'http://192.168.0.106:8001/media/{name_file_image}'
    })

def auto_rotate(path_original):
    """ This function autorotates a picture """
    image = Image.open(path_original)
    path = 'media/img/rodada.png'
    try:
        exif = image._getexif()
    except AttributeError as e:
        return Response("Could not get exif - Bad image!")

    (width, height) = image.size
    # print "\n===Width x Heigh: %s x %s" % (width, height)
    if not exif:
        if width > height:
            print('passei aq ')
            image = image.rotate(90)
            image.save('media/img/app-image-certa.png', quality=100)
            print('passei aq2 ')
            return Response('True')
    else:
        orientation_key = 274 # cf ExifTags
        if orientation_key in exif:
            orientation = exif[orientation_key]
            rotate_values = {
                3: 180,
                6: 270,
                8: 90
            }
            if orientation in rotate_values:
                # Rotate and save the picture
                image = image.rotate(rotate_values[orientation])
                print('image', image)
                image.save('media/img/app-image-certa.png', quality=100, exif=str(exif))
                return Response('True')
        else:
            if width > height:
                image = image.rotate(90)
                image.save('media/img/app-image-certa.png', quality=100, exif=str(exif))
                return Response('True')

    return Response('False')