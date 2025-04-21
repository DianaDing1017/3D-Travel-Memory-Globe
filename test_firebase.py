import firebase_admin
from firebase_admin import credentials, storage, firestore

def test_firebase_connection():
    try:
        # 初始化 Firebase
        cred = credentials.Certificate('firebase-key.json')
        firebase_admin.initialize_app(cred, {
            'storageBucket': 'travelmap-developer.appspot.com'
        })
        
        # 测试 Firestore 连接
        db = firestore.client()
        test_doc = db.collection('test').document()
        test_doc.set({
            'test': 'Hello Firebase!'
        })
        print("✅ Firestore connection successful!")
        
        # 测试 Storage 连接
        bucket = storage.bucket()
        test_blob = bucket.blob('test/test.txt')
        test_blob.upload_from_string('Hello Firebase Storage!')
        print("✅ Storage connection successful!")
        
        # 清理测试数据
        test_doc.delete()
        test_blob.delete()
        print("✅ Test data cleaned up!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing Firebase connection: {str(e)}")
        return False

if __name__ == '__main__':
    test_firebase_connection() 