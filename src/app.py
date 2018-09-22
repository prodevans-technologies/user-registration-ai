from flask import Flask, render_template, request, redirect, Response, jsonify
from flask_mysqldb import MySQL
import yaml
from src.camera import VideoCamera

video_camera = None
global_frame = None

email = None
start = False

app = Flask(__name__)

# Configure db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    global video_camera
    global start
    if video_camera == None:
        video_camera = VideoCamera()

    # Checking the capturing if started or not
    if(not video_camera.check_capture()):
        start = video_camera.check_capture()

    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        name = userDetails['name']
        email = userDetails['email']
        mobile = userDetails['contact_no']
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO users(name, email,mobile) VALUES(%s, %s,%s)", (name, email, mobile))
        mysql.connection.commit()
        cur.close()
        return redirect('/users')
    return render_template('index.html')

@app.route('/detect', methods=['GET'])
def detect():
    return render_template('detect.html')

@app.route('/record_status', methods=['POST'])
def record_status():
    global video_camera
    global email
    global start
    if video_camera == None:
         video_camera = VideoCamera()

    json = request.get_json()
    print('Json', json)
    status = json['data']['status']
    email = json['data']['email']

    if status == "true":
        # video_camera.start_capture(email)
        start = True
        return jsonify(result="started")
    else:
        if(start):
            return jsonify(result="completed")
        else:
            return jsonify(result="still in progress...")


@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM users")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('users.html', userDetails=userDetails)


def video_stream():
    global video_camera
    global global_frame

    global email
    global start
    if video_camera == None:
        video_camera = VideoCamera()

    while True:
        frame = video_camera.get_frame(email, save=start)
        if frame != None:
            global_frame = frame
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n\r\n')

def video_stream_fase_detect():
    global video_camera
    global global_frame

    if video_camera == None:
        video_camera = VideoCamera()

    while True:
        frame = video_camera.detect_person()

        if frame != None:
            global_frame = frame
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n\r\n')

@app.route('/video_viewer')
def video_viewer():
    return Response(video_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/detect_faces')
def detect_faces():
    return Response(video_stream_fase_detect(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)
