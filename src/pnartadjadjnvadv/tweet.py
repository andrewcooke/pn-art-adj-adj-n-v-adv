
from twitter import OAuth, Twitter


class Tweet:

    def __init__(self, path):
        self.__twitter = Twitter(auth=self.__oauth(path))

    def __oauth(self, path):
        with open(path, 'r') as input:
            c_key, c_secret, a_token, a_secret = \
                map(lambda x: x.strip(), input.readlines())
            return OAuth(a_token, a_secret, c_key, c_secret)

    def write(self, append, epoch, sentence):
        if append:
            try: self.__twitter.statuses.update(status=sentence)
            except Exception as e: print(e)


if __name__ == '__main__':
    tp = Tweet('/home/andrew/project/wordstamp/twitter')
    tp.write(True, None, 'test')
