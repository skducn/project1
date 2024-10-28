kill -9 $(pgrep flask)
nohup flask run --host=0.0.0.0 > /home/flask_chc/nohup.out 2>&1 &



