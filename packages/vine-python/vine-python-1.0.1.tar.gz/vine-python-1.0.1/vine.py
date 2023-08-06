import requests


class API:
    api_base_url = 'https://api.vineapp.com/'

    @classmethod
    def search_user(cls, name, **kwargs):
        return cls.get('users/search/{name}'.format(name=name), **kwargs)

    @classmethod
    def get_video(cls, video_id, **kwargs):
        video = cls.get('timelines/posts/s/{video_id}'.format(video_id=video_id), **kwargs)

        if 'data' in video and 'records' in video['data'] and video['data']['records']:
            return video['data']['records'][0]

        return None

    @classmethod
    def get_profile(cls, user_id, **kwargs):
        return cls.get('users/profiles/{user_id}'.format(user_id=user_id), **kwargs)

    @classmethod
    def get_tag_videos(cls, tag, **kwargs):
        return cls.get('timelines/tags/{tag}'.format(tag=tag), **kwargs)

    @classmethod
    def get_user_videos(cls, user_id, **kwargs):
        return cls.get('timelines/users/{user_id}'.format(user_id=user_id), **kwargs)

    @classmethod
    def get(cls, endpoint, **kwargs):
        return cls.response(requests.get(cls.api_base_url+endpoint, params=kwargs))

    @staticmethod
    def response(response):
        return response.json()
