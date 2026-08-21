pipeline {
    agent {
        docker {
            image 'docker:24-cli'
            args '-v /var/run/docker.sock:/var/run/docker.sock -e HOME=/tmp'
        }
    }

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        DOCKERHUB_USER = 'fabriceoliviertine'
        IMAGE_TAG = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'RÃ©cupÃ©ration du code depuis GitHub...'
                checkout scm
            }
        }
        stage('Build Backend Image') {
            steps {
                echo 'Construction de l\'image backend...'
                sh 'docker build -t $DOCKERHUB_USER/smarttask-backend:$IMAGE_TAG ./backend'
                sh 'docker tag $DOCKERHUB_USER/smarttask-backend:$IMAGE_TAG $DOCKERHUB_USER/smarttask-backend:latest'
            }
        }
        stage('Build Frontend Image') {
            steps {
                echo 'Construction de l\'image frontend...'
                sh 'docker build -t $DOCKERHUB_USER/smarttask-frontend:$IMAGE_TAG ./frontend'
                sh 'docker tag $DOCKERHUB_USER/smarttask-frontend:$IMAGE_TAG $DOCKERHUB_USER/smarttask-frontend:latest'
            }
        }
        stage('Login to Docker Hub') {
            steps {
                echo 'Connexion au registre Docker Hub...'
                sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
            }
        }
        stage('Push Images') {
            steps {
                echo 'Publication des images sur Docker Hub...'
                sh 'docker push $DOCKERHUB_USER/smarttask-backend:$IMAGE_TAG'
                sh 'docker push $DOCKERHUB_USER/smarttask-backend:latest'
                sh 'docker push $DOCKERHUB_USER/smarttask-frontend:$IMAGE_TAG'
                sh 'docker push $DOCKERHUB_USER/smarttask-frontend:latest'
            }
        }
    }

    post {
        success {
            echo 'Pipeline exÃ©cutÃ© avec succÃ¨s : images construites et publiÃ©es.'
        }
        failure {
            echo 'Le pipeline a Ã©chouÃ©. Consultez les journaux ci-dessus pour identifier l\'erreur.'
        }
        always {
            sh 'docker logout || true'
        }
    }
}
