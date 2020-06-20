import requests

gallery3d_server = 'https://veryimportantlot.com/gallery3d/api/auth'


def get_user_id_ext(uuid):
    temp_user_id = requests.get(gallery3d_server + '?key=' + uuid)
    if temp_user_id:
        if temp_user_id == 0:
            return None
        else:
            return temp_user_id.text
    else:
        return None
