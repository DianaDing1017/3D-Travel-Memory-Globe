from flask import Flask, render_template, jsonify, request, send_from_directory
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import os
from datetime import datetime
from werkzeug.utils import secure_filename
import uuid
import json

app = Flask(__name__)

# 初始化地理编码器
geolocator = Nominatim(user_agent="travelmap_3d_globe_app", timeout=10)

# 设置上传文件夹
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov'}

# 确保上传文件夹存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_coordinates(city):
    try:
        location = geolocator.geocode(city, language='en')
        if location:
            return {
                "lat": location.latitude,
                "lon": location.longitude,
                "name": location.address.split(',')[0]
            }
        return None
    except GeocoderTimedOut:
        return {"error": "Geocoding service timed out. Please try again."}
    except Exception as e:
        return {"error": f"Error searching location: {str(e)}"}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/location/<city>')
def get_location(city):
    try:
        coordinates = get_coordinates(city)
        if coordinates and "error" not in coordinates:
            return jsonify(coordinates)
        return jsonify({"error": coordinates.get("error", "Location not found")}), 404
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        print('Upload request received')
        if 'file' not in request.files:
            print('No file part in request')
            return jsonify({'error': 'No file part'}), 400
            
        file = request.files['file']
        if file.filename == '':
            print('No selected file')
            return jsonify({'error': 'No selected file'}), 400
            
        if not allowed_file(file.filename):
            print('File type not allowed:', file.filename)
            return jsonify({'error': 'File type not allowed'}), 400
            
        location_id = request.form.get('location_id')
        if not location_id:
            print('No location_id provided')
            return jsonify({'error': 'No location_id provided'}), 400
            
        print('Processing file:', file.filename)
        print('Location ID:', location_id)
        
        # 生成唯一文件名
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        
        print('Saving file to:', file_path)
        file.save(file_path)
        print('File saved successfully')
        
        # 创建媒体记录
        media = {
            'id': str(uuid.uuid4()),
            'location_id': location_id,
            'filename': filename,
            'file_path': file_path,
            'url': f"/static/uploads/{unique_filename}",
            'type': file.content_type,
            'created_at': datetime.now().isoformat()
        }
        
        # 保存媒体信息
        media_list = []
        if os.path.exists(os.path.join(UPLOAD_FOLDER, 'media.json')):
            with open(os.path.join(UPLOAD_FOLDER, 'media.json'), 'r', encoding='utf-8') as f:
                media_list = json.load(f)
                
        media_list.append(media)
        
        with open(os.path.join(UPLOAD_FOLDER, 'media.json'), 'w', encoding='utf-8') as f:
            json.dump(media_list, f, ensure_ascii=False, indent=2)
            
        print('Media record saved')
        return jsonify(media)
        
    except Exception as e:
        print('Upload error:', str(e))
        return jsonify({'error': str(e)}), 500

@app.route('/api/location/<location_id>/media', methods=['GET'])
def get_location_media(location_id):
    try:
        print('Getting media for location:', location_id)
        if not os.path.exists(os.path.join(UPLOAD_FOLDER, 'media.json')):
            print('No media.json file found')
            return jsonify([])
            
        with open(os.path.join(UPLOAD_FOLDER, 'media.json'), 'r', encoding='utf-8') as f:
            media_list = json.load(f)
            
        location_media = [m for m in media_list if m['location_id'] == location_id]
        print('Found media:', location_media)
        return jsonify(location_media)
        
    except Exception as e:
        print('Error getting media:', str(e))
        return jsonify({'error': str(e)}), 500

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/api/all-media')
def get_all_media():
    try:
        if not os.path.exists(os.path.join(UPLOAD_FOLDER, 'media.json')):
            return jsonify([])
        with open(os.path.join(UPLOAD_FOLDER, 'media.json'), 'r', encoding='utf-8') as f:
            media_list = json.load(f)
        return jsonify(media_list)
    except Exception as e:
        print('Error getting all media:', str(e))
        return jsonify({'error': str(e)}), 500

@app.route('/api/delete-media/<media_id>', methods=['DELETE'])
def delete_media(media_id):
    try:
        # 读取media.json
        media_json_path = os.path.join(UPLOAD_FOLDER, 'media.json')
        if not os.path.exists(media_json_path):
            return jsonify({'error': 'No media.json file found'}), 404
        with open(media_json_path, 'r', encoding='utf-8') as f:
            media_list = json.load(f)
        # 查找要删除的media
        media = next((m for m in media_list if m['id'] == media_id), None)
        if not media:
            return jsonify({'error': 'Media not found'}), 404
        # 删除文件
        if os.path.exists(media['file_path']):
            os.remove(media['file_path'])
        # 移除media记录
        media_list = [m for m in media_list if m['id'] != media_id]
        with open(media_json_path, 'w', encoding='utf-8') as f:
            json.dump(media_list, f, ensure_ascii=False, indent=2)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 