#!/bin/bash
curl -O https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.4.7/docs/install/iam_policy.json
#export awsarn=arn:aws:iam::465340416678:policy/AWSLoadBalancerControllerIAMPolicy
#export awsarn=`aws iam create-policy  --policy-name  AWSLoadBalancerControllerIAMPolicy --policy-document file://iam_policy.json | awk '{print $2}' -`
aws iam create-policy  --policy-name  AWSLoadBalancerControllerIAMPolicy --policy-document file://iam_policy.json || true
aws iam list-policies --query 'Policies[?PolicyName==`AWSLoadBalancerControllerIAMPolicy`].Arn' --output text > output
export awsarn=`cat output`
aws cloudformation delete-stack --stack-name eksctl-webapp-addon-iamserviceaccount-kube-system-aws-load-balancer-controller || true
sleep 30
#kubectl delete sa kube-system/aws-load-balancer-controller -n kube-system || true
eksctl create iamserviceaccount --cluster=webapp --namespace=kube-system --name=aws-load-balancer-controller --role-name AmazonEKSLoadBalancerControllerRole \
  --attach-policy-arn=$awsarn --approve
rm output
helm repo add eks https://aws.github.io/eks-charts && helm repo update
helm install aws-load-balancer-controller eks/aws-load-balancer-controller -n kube-system --set clusterName=$cluster  --set serviceAccount.create=false \
--set serviceAccount.name=aws-load-balancer-controller
helm repo add grafana https://grafana.github.io/helm-charts && helm repo update 
helm install loki grafana/loki-stack
helm install grafana grafana/grafana
helm install prometheus grafana/loki-stack
