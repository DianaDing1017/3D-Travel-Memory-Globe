from flask import Flask, render_template, jsonify, request
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import firebase_admin
from firebase_admin import credentials, storage, firestore
import os
from datetime import datetime
from werkzeug.utils import secure_filename
import uuid
import tempfile

app = Flask(__name__)

# 初始化地理编码器
geolocator = Nominatim(user_agent="my_earth_app")

try:
    # 初始化 Firebase
    cred = credentials.Certificate('firebase-key.json')
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'travelmap-developer.appspot.com'  # 使用你的项目ID
    })
    
    # 获取 Firebase 服务
    db = firestore.client()
    bucket = storage.bucket()
    print("Firebase initialized successfully!")
except Exception as e:
    print(f"Error initializing Firebase: {str(e)}")
    
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov'}
TEMP_FOLDER = tempfile.gettempdir()  # 使用系统临时目录

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_coordinates(city):
    try:
        location = geolocator.geocode(city)
        if location:
            return {
                "lat": location.latitude,
                "lon": location.longitude,
                "name": city
            }
        return None
    except GeocoderTimedOut:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/location/<city>')
def get_location(city):
    coordinates = get_coordinates(city)
    if coordinates:
        return jsonify(coordinates)
    return jsonify({"error": "Location not found"}), 404

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    location_id = request.form.get('location_id')
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        try:
            # 生成唯一文件名
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            
            # 创建临时文件
            temp_path = os.path.join(TEMP_FOLDER, unique_filename)
            file.save(temp_path)
            
            try:
                # 上传到 Firebase Storage
                blob = bucket.blob(f'media/{unique_filename}')
                blob.upload_from_filename(temp_path)
                
                # 设置文件为公开访问
                blob.make_public()
                
                # 保存文件信息到 Firestore
                media_ref = db.collection('media').document()
                media_ref.set({
                    'location_id': location_id,
                    'filename': filename,
                    'storage_path': f'media/{unique_filename}',
                    'url': blob.public_url,
                    'type': file.content_type or filename.rsplit('.', 1)[1].lower(),
                    'uploaded_at': datetime.utcnow()
                })
                
                return jsonify({
                    'message': 'File uploaded successfully',
                    'url': blob.public_url,
                    'id': media_ref.id
                })
                
            except Exception as e:
                return jsonify({'error': f'Firebase error: {str(e)}'}), 500
            
            finally:
                # 确保临时文件被删除
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                    
        except Exception as e:
            return jsonify({'error': f'Server error: {str(e)}'}), 500
            
    return jsonify({'error': 'File type not allowed'}), 400

@app.route('/api/location/<location_id>/media', methods=['GET'])
def get_location_media(location_id):
    try:
        # 查询指定位置的所有媒体文件
        media_refs = db.collection('media').where('location_id', '==', location_id).stream()
        media_list = []
        
        for media in media_refs:
            media_data = media.to_dict()
            media_data['id'] = media.id
            media_list.append(media_data)
            
        return jsonify(media_list)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 