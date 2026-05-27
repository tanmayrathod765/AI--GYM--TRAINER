Run the app in Docker (includes necessary OpenGL / Mesa libs)

Build locally:

```bash
docker build -t ai-gym-coach:latest .
```

Run locally:

```bash
docker run --rm -p 8501:8501 \
  -e GROQ_API_KEY=your_key_here \
  ai-gym-coach:latest
```

Deploy to a Docker-friendly host (Render, Railway, Fly, etc.) if Streamlit Cloud's apt packages are restricted.
