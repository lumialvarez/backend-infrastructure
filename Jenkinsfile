def APP_VERSION
def REMOTE_HOME
pipeline {
    agent any
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-lmalvarez')
        SSH_MAIN_SERVER = credentials("SSH_MAIN_SERVER")
        DATASOURCE_PASSWORD = credentials("DATASOURCE_PASSWORD")
        RABBITMQ_URL = credentials("RABBITMQ_URL")
        DB_URL = credentials("DB_URL")
        POSTGRES_PASSWORD = credentials("POSTGRES_PASSWORD")
        JWT_SECRET = credentials("JWT_SECRET")
    }
    stages {
        stage('Get Version') {
            steps {
                script {
                    APP_VERSION = sh(
                            script: "grep -m 1 -Po '[0-9]+[.][0-9]+[.][0-9]+' CHANGELOG.md",
                            returnStdout: true
                    ).trim()
                }
                script {
                    currentBuild.displayName = "#" + currentBuild.number + " - v" + APP_VERSION
                }
                script {
                    if (currentBuild.previousSuccessfulBuild) {
                        lastBuild = currentBuild.previousSuccessfulBuild.displayName.replaceFirst(/^#[0-9]+ - v/, "")
                        echo "Last success version: ${lastBuild} \nNew version to deploy: ${APP_VERSION}"
                        if (lastBuild == APP_VERSION) {
                            if (currentBuild.changeSets.size() > 0) {
                                echo "Same version with changes is denied"
                                currentBuild.result = 'ABORTED'
                                error("Aborted: A version that already exists cannot be deployed a second time")
                            } else {
                                echo "Same version without changes is permitted"
                            }
                        }
                    }
                }
            }
        }
        stage('Pull') {
            steps {
                script {
                    REMOTE_HOME = sh(
                            script: ''' ssh ${SSH_MAIN_SERVER} 'pwd' ''',
                            returnStdout: true
                    ).trim()
                }

                sh "echo 'DB_URL=${DB_URL} ' > ./backend-services/settings.conf"
                sh "echo 'RABBITMQ_URL=${RABBITMQ_URL} ' >> ./backend-services/settings.conf"
                sh "echo 'JWT_SECRET_KEY=${JWT_SECRET} ' >> ./backend-services/settings.conf"
                sh "echo 'POSTGRES_PASSWORD=${POSTGRES_PASSWORD} ' >> ./backend-services/settings.conf"

                sh "ssh ${SSH_MAIN_SERVER} 'sudo rm -rf ${REMOTE_HOME}/tmp_jenkins/${JOB_NAME}'"
                sh "ssh ${SSH_MAIN_SERVER} 'sudo mkdir -p -m 777 ${REMOTE_HOME}/tmp_jenkins/${JOB_NAME}'"

                sh "scp -r ${WORKSPACE}/backend-services/* ${SSH_MAIN_SERVER}:${REMOTE_HOME}/tmp_jenkins/${JOB_NAME}"

                sh "ssh ${SSH_MAIN_SERVER} 'docker-compose -f ${REMOTE_HOME}/tmp_jenkins/${JOB_NAME}/docker-compose.yaml " +
                        "--env-file ${REMOTE_HOME}/tmp_jenkins/${JOB_NAME}/settings.conf pull' "
            }
        }
        stage('Deploy') {
            steps {
                sh "ssh ${SSH_MAIN_SERVER} 'docker-compose -f ${REMOTE_HOME}/tmp_jenkins/${JOB_NAME}/docker-compose.yaml " +
                        "--env-file ${REMOTE_HOME}/tmp_jenkins/${JOB_NAME}/settings.conf up -d' "
            }
        }
    }
}