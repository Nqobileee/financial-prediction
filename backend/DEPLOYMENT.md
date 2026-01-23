# 🚀 Render Deployment Guide

## ✅ Deployment Checklist Completed

### 🧱 Backend Prep
- ✅ **Framework**: Flask confirmed
- ✅ **Main file**: `main.py` created (Render entry point)
- ✅ **Listen on 0.0.0.0**: Configured in main.py
- ✅ **CORS support**: Enabled with flask-cors
- ✅ **Root endpoint**: `/` provides API info
- ✅ **Health endpoint**: `/api/health` for monitoring

### 📦 Dependencies
- ✅ **requirements.txt**: Updated with all dependencies
- ✅ **All packages listed**: pandas, numpy, scikit-learn, flask, flask-cors, gunicorn
- ✅ **Unused libraries**: Removed

### 🧪 Local Testing
- ✅ **Local run**: Use `python main.py`
- ✅ **Test endpoints**: Use `python test_api.py`
- ✅ **No runtime errors**: Verified

## 📋 Files Created for Deployment

1. **main.py** - Entry point for Render
2. **render.yaml** - Render configuration
3. **build.sh** - Build script
4. **Procfile** - Alternative deployment support
5. **test_api.py** - Local testing script
6. **requirements.txt** - Updated dependencies

## 🌐 Render Deployment Steps

### Step 1: Prepare Repository
```bash
# Make sure all files are in the backend directory
cd backend
git add .
git commit -m "Prepare backend for Render deployment"
git push origin main
```

### Step 2: Render Configuration
1. **Service Type**: Web Service
2. **Build Command**: `pip install -r requirements.txt`
3. **Start Command**: `gunicorn --bind 0.0.0.0:$PORT main:application`
4. **Environment**: Python 3.10+
5. **Root Directory**: `/backend` (if deploying from subdirectory)

### Step 3: Environment Variables
Set these in Render dashboard:
- `PYTHON_VERSION`: `3.10.12`
- `PORT`: `10000` (Render will set this automatically)

### Step 4: Deploy
1. Connect your GitHub repository
2. Select the backend directory
3. Use the configuration above
4. Deploy!

## 🔧 Local Development

### Start the API
```bash
cd backend
python main.py
```

### Test Endpoints
```bash
# In another terminal
python test_api.py
```

### Manual Testing
```bash
# Health check
curl http://localhost:5000/api/health

# Root endpoint
curl http://localhost:5000/

# Prediction (POST with sample data)
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d @sample_request.json
```

## 📱 Mobile Integration

Once deployed, your Next.js frontend can connect to:
```javascript
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'https://your-app-name.onrender.com'
  : 'http://localhost:5000';
```

## 🔍 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API info and status |
| `/api/health` | GET | Health check |
| `/api/predict` | POST | Financial health prediction |
| `/api/train` | POST | Retrain model (admin) |

## 🛠️ Troubleshooting

### Common Issues:
1. **Import errors**: Check requirements.txt has all dependencies
2. **Port binding**: Render sets PORT environment variable
3. **File paths**: Use relative paths in Python imports
4. **Model loading**: Ensure .pkl files are in repository

### Logs:
- Check Render logs for startup errors
- Use logging in main.py for debugging
- Health endpoint shows model status

## 🔒 Security Notes

For production deployment, consider:
- Authentication for `/api/train` endpoint
- Rate limiting on prediction endpoint
- Input validation and sanitization
- HTTPS enforcement
- API key protection

## ✅ Ready for Deployment!

Your backend is now ready for Render deployment with:
- ✅ Production-ready Flask app
- ✅ Gunicorn WSGI server
- ✅ Health monitoring
- ✅ CORS enabled
- ✅ Error handling
- ✅ Logging configured