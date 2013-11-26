copy:
	cp /home/8/devekar/WWW/DM5/tm_train.csv ./
	cp /home/8/devekar/WWW/DM5/tm_test.csv ./
	
run_algo1:
	python Algo1.py tm_train.csv tm_test.csv -s5m3 -c80
	
run_algo2:
	python Algo2.py tm_train.csv tm_test.csv Kmeans_clusters_8.txt -s5m3 -c80
	
clean:
	rm -rf *.tmp *.pyc