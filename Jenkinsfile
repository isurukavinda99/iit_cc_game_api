// Jenkins file

pipeline {
    agent any

    environment {
        DOCKER_HUB_CREDENTIALS_ID = 'dockerhub'
        DOCKER_HUB_REPO = 'isurukavinda99/game_api'
        K8S_DEPLOY_FILE = 'game-api-deployment.yaml'
        K8S_SERVICE_FILE = 'game-service.yaml'
        K8S_SECRET_FILE = 'game-api-secret.yaml'
        K8S_HPA= 'game-api-hpa.yaml'
    }

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    echo '=== Building Docker Image ==='
                    dockerImage = docker.build("${DOCKER_HUB_REPO}:latest")
                }
            }
        }

        stage('Run API Tests') {

            steps {
                withCredentials([
                    string(credentialsId: 'db-host', variable: 'DB_HOST'),
                    string(credentialsId: 'db-name', variable: 'DB_NAME'),
                    string(credentialsId: 'db-user', variable: 'DB_USER'),
                    string(credentialsId: 'db-password', variable: 'DB_PASSWORD'),
                    string(credentialsId: 'db-port', variable: 'DB_PORT'),
                    string(credentialsId: 'cognito-user-pool-id', variable: 'COGNITO_USER_POOL_ID'),
                    string(credentialsId: 'cognito-client-id', variable: 'COGNITO_CLIENT_ID'),
                    string(credentialsId: 'aws-region', variable: 'AWS_REGION'),
                    string(credentialsId: 'oidc-token', variable: 'OIDC_TOKEN')
                ]) {
                    script {
                        echo '=== Running Tests in Docker Container ==='
                        sh """
                            docker run --rm \\
                                -p 8091:8081 \\
                                -e DB_HOST=${DB_HOST} \\
                                -e DB_NAME=${DB_NAME} \\
                                -e DB_USER=${DB_USER} \\
                                -e DB_PASSWORD=${DB_PASSWORD} \\
                                -e DB_PORT=${DB_PORT} \\
                                -e COGNITO_USER_POOL_ID=${COGNITO_USER_POOL_ID} \\
                                -e COGNITO_CLIENT_ID=${COGNITO_CLIENT_ID} \\
                                -e AWS_REGION=${AWS_REGION} \\
                                -e OIDC_TOKEN=${OIDC_TOKEN} \\
                                ${DOCKER_HUB_REPO}:latest \\
                                /bin/sh -c "uvicorn app.main:app --host 0.0.0.0 --port 8082 & sleep 15 && pytest app/tests/integration"

                        """
                    }
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', "${DOCKER_HUB_CREDENTIALS_ID}") {
                        dockerImage.push('latest')
                    }
                }
            }
        }

        stage('Install kubectl') {
            steps {
                sh '''
                    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
                    chmod +x kubectl
                    mkdir -p $HOME/bin
                    mv kubectl $HOME/bin/kubectl
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
                    sh """
                        export PATH=$HOME/bin:$PATH
                        kubectl apply -f ${K8S_SECRET_FILE} --validate=false
                        kubectl apply -f ${K8S_DEPLOY_FILE} --validate=false
                        kubectl apply -f ${K8S_SERVICE_FILE} --validate=false
                        kubectl apply -f ${K8S_HPA} --validate=false
                        kubectl rollout restart deployment/game-api-deployment
                        kubectl rollout status deployment/game-api-deployment
                    """
                }
            }
        }
    }

    post {
        success {
            echo '✅ Game API deployed successfully!'
        }
        failure {
            echo '❌ Deployment failed. Please check logs.'
        }
    }
}
