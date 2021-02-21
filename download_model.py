import requests

file_url = "https://www.dropbox.com/s/y7fcoou7qsttab7/model.save?dl=1"

r = requests.get(file_url, stream=True)

with open("model.save", "wb") as pdf:
    for chunk in r.iter_content(chunk_size=1024):

        # writing one chunk at a time to pdf file
        if chunk:
            pdf.write(chunk)