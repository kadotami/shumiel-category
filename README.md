#shumiel category

起動
sudo gunicorn -c gunicorn_conf.py app:app

停止
sudo kill `cat tmp/gunicorn.pid`