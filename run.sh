docker run -d --name exosky --restart=always -v "$(pwd)/tmp/:/app/tmp/" -p 8601:8601 --network=host exosky:v1 streamlit run app.py --server.port=8601
