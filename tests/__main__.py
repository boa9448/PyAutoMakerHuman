import sys
import argparse
import threading
from PyAutoMakerFace import *

parser = argparse.ArgumentParser()
parser.add_argument("--addr", type = str, default = "0.0.0.0", help = "The IP address of the server to bind to.")
parser.add_argument("--port", type = int, default = 8080, help = "The Port of the server to bind to.")
parser.add_argument("--view", type = str, default = "no", help ="view type : no, cam, mask_detect, face_detect")
args = parser.parse_args()

faceProc = FaceUtil()
faceProc.maskInit()

app = Flask(__name__)

@app.route("/")
def index():
    return "ㅎㅇㅎㅇ 위대원이 만든 페이지임"

@app.route("/face_process", methods = ["GET", "POST"])
def process():
    if request.method == "POST":
        f = request.files['file']
        data = f.read()
        file_name = str(time.time()) + "_" + f.filename

        image = cv2.imdecode(np.array(bytearray(data), np.uint8), -1)
        infoList = []

        if image is not None:
            infoList = faceProc.maskDetect(image, 0.5)

            for info in infoList:
                faceProc.draw(image, info["roi"], info["mask"], info["proba"]
                            , (0, 255, 0) if info["mask"] else (0, 0, 255))

        cv2.imwrite("static/temp/" + file_name, image)

        anno_html = f"""
        <html>
            <body>
            {json.dumps(infoList)}
            <img src = \"static/temp/{file_name}\">
            </body>
        </html>
        """
        
        return anno_html

@app.route("/face")
def face():
    face_html = """
    <html>
        <body>
            <form action ="/face_process" method = "POST"
            enctype ="multipart/form-data">
            <input type="file" name="file"/>
            <input type="submit"/>
            </form>
        </body>
    </html>
    """
    return face_html


if __name__ == "__main__":
    os.chdir(rootDir)
    print("\n" * 3)
    print("=" * 50)
    print(f"server current work path : {os.getcwd()}")
    print(f"server addr : {args.addr}")
    print(f"server port : {args.port}")

    threading.Thread(target = demo_view, args = (args.view,)).start()
    serve(app, host= args.addr, port = args.port)