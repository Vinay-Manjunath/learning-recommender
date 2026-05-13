pipeline {
    agent any

    environment {
        REGISTRY = "docker.io/vinaymanjunath"
        TAG = "latest"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                url: 'https://github.com/Vinay-Manjunath/learning-recommender.git'
            }
        }

        stage('Build Images') {
            steps {
                sh '''
                docker build -t $REGISTRY/learning-recommender-frontend:$TAG frontend
                docker build -t $REGISTRY/learning-recommender-gateway:$TAG backend/api-gateway
                docker build -t $REGISTRY/learning-recommender-user-service:$TAG backend/user-service
                docker build -t $REGISTRY/learning-recommender-feedback-service:$TAG backend/feedback-service
                docker build -t $REGISTRY/learning-recommender-recommendation-service:$TAG backend/recommendation-service
                '''
            }
        }

        stage('Push Images') {
            steps {
                sh '''
                docker push $REGISTRY/learning-recommender-frontend:$TAG
                docker push $REGISTRY/learning-recommender-gateway:$TAG
                docker push $REGISTRY/learning-recommender-user-service:$TAG
                docker push $REGISTRY/learning-recommender-feedback-service:$TAG
                docker push $REGISTRY/learning-recommender-recommendation-service:$TAG
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
