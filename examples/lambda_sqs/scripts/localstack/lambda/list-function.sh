HOST=0.0.0.0
aws --endpoint-url=http://$HOST:4566 lambda list-functions --master-region us-east-1
aws --endpoint-url=http://localhost:4566 lambda list-functions --master-region us-east-2
