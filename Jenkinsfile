pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Vinay-Manjunath/learning-recommender.git'
            }
        }

        stage('Build Images') {
            steps {
                sh '''
                docker build -t learning-recommender-frontend:latest frontend
                docker build -t learning-recommender-gateway:latest backend/api-gateway
                docker build -t learning-recommender-user-service:latest backend/user-service
                docker build -t learning-recommender-feedback-service:latest backend/feedback-service
                docker build -t learning-recommender-recommendation-service:latest backend/recommendation-service
                '''
            }
        }

        stage('Load into Minikube') {
            steps {
                sh '''
                minikube image load learning-recommender-frontend:latest
                minikube image load learning-recommender-gateway:latest
                minikube image load learning-recommender-user-service:latest
                minikube image load learning-recommender-feedback-service:latest
                minikube image load learning-recommender-recommendation-service:latest
                '''
            }
        }

        stage('Deploy via Ansible') {
            steps {
                sh '''
                ansible-playbook -i ansible/inventory ansible/deploy.yml
                '''
            }
        }
    }
}