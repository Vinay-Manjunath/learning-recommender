pipeline {
    agent any

    environment {
        REGISTRY = "docker.io/vinayksm86"
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

        stage('Docker Login & Push') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
        
                    docker push docker.io/vinaymanjunath/learning-recommender-frontend:latest
                    docker push docker.io/vinaymanjunath/learning-recommender-gateway:latest
                    docker push docker.io/vinaymanjunath/learning-recommender-user-service:latest
                    docker push docker.io/vinaymanjunath/learning-recommender-feedback-service:latest
                    docker push docker.io/vinaymanjunath/learning-recommender-recommendation-service:latest
                    '''
                }
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
