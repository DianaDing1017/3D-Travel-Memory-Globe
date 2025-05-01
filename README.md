# 🌍 3D Travel Memory Globe

An interactive 3D web application for visualizing and recording travel memories on a rotating digital globe. Users can place “memory pins” at locations they've visited, upload photos, write reflections, and relive global experiences in an emotional and immersive way.

---

## 🧭 Project Proposal

### 🔍 Project Objectives

This project aims to build an **interactive 3D globe web application** where users can **record and relive their travel memories**. By placing multimedia-rich “memory pins” on a rotating Earth interface, the platform encourages storytelling through photos, text, and sounds tied to specific locations. It provides a more **emotional and artistic experience** than traditional route-focused travel maps.

---

### 🎯 Target Users and Their Needs

| User Type         | Needs                                                                 |
|------------------|----------------------------------------------------------------------|
| Casual Travelers | A beautiful and fun way to log and revisit personal travel moments.  |
| Visual Thinkers  | A globe-centric, visual-first storytelling medium.                   |
| Creatives        | Tools to present travel stories with images, text, and ambient sound.|
| Private Users    | The ability to keep memories personal or selectively share them.     |

Unlike Google Earth or TravelMap, which focus on route exploration or satellite views, this project is about **emotional connection to place** — a personal globe of memories.
---

### 📦 Key Deliverables

- 🌍 A 3D interactive Earth (via **CesiumJS** or **Globe.gl**) with zoom/rotate capabilities.
- 📌 Memory pins: clickable points on the globe that store **user-generated content** (photos, descriptions, timestamps).
- 🔐 Simple user login system to support private and personal experiences.
- 🗂 Local or cloud-based file storage for user-uploaded media.
- 🧭 Optional timeline view to scroll through journeys chronologically.
- ✨ Clean, responsive UI design emphasizing emotional memory presentation.
- 🚀 Deployed version of the app (Heroku, Vercel, or Render).

---

### ⛓ Special Constraints

- **Rendering performance**: 3D graphics must be optimized for smooth interaction across devices.
- **File handling**: Uploading media requires size limits and secure processing (local or cloud).
- **User authentication**: Must be secure, even if simplified for demo purposes.
- **Scope control**: Avoid replicating full Google Earth functionality — focus on personal storytelling.

---

### 🌈 Expected Outcome

By the end of the 10-week timeline, the final deliverables will include:

- A functional 3D travel journal web app that supports:
  - User login/logout
  - Pinning locations on a 3D globe
  - Uploading and viewing multimedia content per location
- An artistic and intuitive user experience to explore travel memories emotionally.
- Well-documented source code hosted on GitHub with clean structure and modular design.
- Optional bonus features: AI-generated memory captions, music integration, private/public toggle.

This project is a creative fusion of geography, memory, and interaction — **a digital globe where emotions live**.

---

## 🛠 Tech Stack

- **Frontend**: HTML/CSS/JS, Globe.gl or CesiumJS  
- **Backend**: Flask (Python)  
- **Database**: SQLite or PostgreSQL  
- **Optional**: OpenAI API, Cloudinary/S3 for uploads

---

## 📁 Client info

Fiona Xu (jingx23@uw.edu)

## 💻 Virtual Environment Setup (Windows)

This project uses a Python virtual environment for dependency management.

1. Ensure you have Python 3.9+ installed. You can verify with:

   ```powershell
   python --version
   ```

2. Create a virtual environment in your project directory:

   ```powershell
   python -m venv venv
   ```

3. Activate the environment (Windows PowerShell):

   ```powershell
   .\venv\Scripts\activate
   ```

   If you're using VS Code, the environment may auto-activate (you'll see `(venv)` in the terminal or a message in the corner).

4. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

Now you're ready to run the app.


## 🛠️ Local Setup & Project Progress

### 🔧 Setup Instructions (Run Locally)

To run this project locally:

1. **Clone the repository**
   ```
   git clone https://github.com/DianaDing1017/3D-Travel-Memory-Globe.git
   cd 3D-Travel-Memory-Globe
   ```

2. **Create and activate virtual environment (Windows)**
   ```
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

4. **Run the app**
   ```
   python app.py
   ```
   The app will be accessible at: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

### 📌 Project Progress

- ✅ Flask backend initialized and running locally  
- ✅ Geopy integrated for location coordinate lookup  
- ✅ Firebase Storage & Firestore successfully storing uploaded media  
- ✅ Basic upload and retrieval API completed  
- 🚧 Currently building UI to display uploaded content by location  
- 🔜 Next: Add user authentication and timeline sorting
