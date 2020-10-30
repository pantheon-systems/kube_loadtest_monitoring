#!/bin/bash
MODE="notification"
SLACK_SECRET_KEY="xxxxxxxxxxxxxxxxxxxxxxxxxxx"

gcloud auth activate-service-account --key-file ~/kube_loadtest_monitoring/keys/gsk.json
gcloud --quiet config set project pantheon-psapps
#gcloud container clusters get-credentials locust-kube-cluster-20190711160428 --zone us-west1
gcloud container clusters list 
gcloud container clusters list | grep locust-kube-cluster | awk  '{print $1}' > ~/kube_loadtest_monitoring/containers.txt


sleep 5
echo "Start!"

while read p; do
  echo "$p"
  gcloud --quiet container clusters get-credentials "$p" --region us-west1
  gcloud container clusters describe "$p" --region us-west1 --format json | jq -r .createTime
 
  DATE_CREATED=$(gcloud container clusters describe "$p" --region us-west1 --format json | jq -r .createTime)
  kubectl resource-capacity >  ~/kube_loadtest_monitoring/capacity.txt 
  TARGET_URL=`kubectl get secret locust-secret -o jsonpath='{.data.target_url}' | base64 --decode`
  EXTERNAL_IP=`kubectl get service locust-master -o jsonpath='{.status.loadBalancer.ingress[0].ip}'`
  GIT_USERNAME=`kubectl get secret locust-secret -o jsonpath='{.data.git_username}' | base64 --decode`  
  CLUSTER=($p)
  python ~/kube_loadtest_monitoring/app/post_to_slack.py $EXTERNAL_IP $SLACK_SECRET_KEY "$GIT_USERNAME" $MODE $TARGET_URL $DATE_CREATED $CLUSTER
done <~/kube_loadtest_monitoring/containers.txt