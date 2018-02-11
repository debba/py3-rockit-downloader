import sys
import os
import json


class RockitTrack:
    def __init__(self, title, duration, author, album, track, referer):
        self.title = title
        self.duration = duration
        self.author = author
        self.track = track
        self.album = album
        self.referer = referer

    def getTitle(self):
        return self.title

    def download(self, requests):
        s = requests.Session()
        s.headers.update({'referer': self.referer})
        response = s.post('https://www.rockit.it/web/include/ajax.play.php', {'id': self.track, '0k': 'okmobile'})
        resp = json.loads(response.content)
        aw_url = resp['url']

        if aw_url is "":
            print("[ERROR] Track " + self.title + " not exists, is not downloadable.")
            return

        filename = "download/" + self.album.replace(" ", "_") + "/" + self.title.replace(" ", "_") + ".mp3"
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, 'wb') as file:
            print("Download " + self.title + "...\n")
            s = requests.Session()
            s.headers.update({'referer': self.referer})
            response = s.get(aw_url, stream=True)
            total_length = response.headers.get('content-length')

            if total_length is None:
                file.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    file.write(data)
                    done = int(50 * dl / total_length)
                    sys.stdout.write("\r[%s%s] %d of 100 percent" % ('=' * done, ' ' * (50 - done), done * 2))
                    sys.stdout.flush()
                print("\n[SUCCESS] Track " + self.title + " downloaded successfully.")
