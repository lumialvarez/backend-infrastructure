def APP_VERSION
def INTERNAL_IP
def REMOTE_HOME
pipeline {
   agent any
   environment {
      DOCKERHUB_CREDENTIALS=credentials('dockerhub-lmalvarez')
      SSH_MAIN_SERVER = credentials("SSH_MAIN_SERVER")
      DATASOURCE_PASSWORD = credentials("DATASOURCE_PASSWORD")
   }
   stages {
      stage('Get Version') {
         steps {
            script {
               APP_VERSION = sh (
                  script: "grep -m 1 -Po '[0-9]+[.][0-9]+[.][0-9]+' CHANGELOG.md",
                  returnStdout: true
               ).trim()
            }
            script {
               currentBuild.displayName = "#" + currentBuild.number + " - v" + APP_VERSION
            }
            script{
                if(currentBuild.previousSuccessfulBuild) {
                    lastBuild = currentBuild.previousSuccessfulBuild.displayName.replaceFirst(/^#[0-9]+ - v/, "")
                    echo "Last success version: ${lastBuild} \nNew version to deploy: ${APP_VERSION}"
                    if(lastBuild == APP_VERSION)  {
                         //currentBuild.result = 'ABORTED'
                         //error("Aborted: A version that already exists cannot be deployed a second time")
                    }
                }
            }
         }
      }
      stage('Pull') {
        steps {
            script {
                INTERNAL_IP = sh (
                    script: '''ssh ${SSH_MAIN_SERVER} 'sudo bash script_internal_ip.sh' ''',
                    returnStdout: true
                ).trim()
            }

            script {
                REMOTE_HOME = sh (
                    script: ''' ssh ${SSH_MAIN_SERVER} 'pwd' ''',
                    returnStdout: true
                ).trim()
            }

            sh "python replace-variables.py ${WORKSPACE}/backend-services/docker-compose.yaml DATASOURCE_PASSWORD=${DATASOURCE_PASSWORD} INTERNAL_IP=${INTERNAL_IP}"
            sh 'cat ${WORKSPACE}/backend-services/docker-compose.yaml'

            sh "ssh ${SSH_MAIN_SERVER} 'sudo rm -rf ${REMOTE_HOME}/tmp_jenkins/${JOB_NAME}'"
            sh "ssh ${SSH_MAIN_SERVER} 'sudo mkdir -p -m 777 ${REMOTE_HOME}/tmp_jenkins/${JOB_NAME}'"

            sh "scp -r ${WORKSPACE}/backend-services/* ${SSH_MAIN_SERVER}:${REMOTE_HOME}/tmp_jenkins/${JOB_NAME}"

            sh "ssh ${SSH_MAIN_SERVER} 'docker-compose -f ${REMOTE_HOME}/tmp_jenkins/${JOB_NAME}/docker-compose.yaml pull' "
        }
      }
      stage('Deploy') {
         steps {
             sh "ssh ${SSH_MAIN_SERVER} 'docker-compose -f ${REMOTE_HOME}/tmp_jenkins/${JOB_NAME}/docker-compose.yaml up -d' "
         }
      }
   }
}