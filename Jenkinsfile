pipeline {
    agent any
    stages {
        stage ('Prepare images') {
            parallel {
                stage ('Build test image') {
                    steps {
                        script {
                            sh 'docker build -t docker_test_image -f automated_tests/test.Dockerfile .'
                        }
                    }
                }
                stage ('Compose app') {
                    stages {
                        stage ('Build app image') {
                            steps {
                                script {
                                    sh 'docker compose build'
                                }
                            }
                        }
                        stage ('Deploy app image') {
                            when {
                                expression {
                                    return env.BRANCH_NAME == 'develop' || env.BRANCH_NAME == 'release' || env.BRANCH_NAME == 'master'
                                }
                            }
                            steps {
                                script {
                                    echo "Deploy app image to registry"
                                }
                            }
                        }
                    }
                }
            }
        }
        stage ('Test preparation') {
            parallel {
                stage ('Verify requirements') {
                    steps {
                        script {
                            def reqs_verification = sh(script: 'docker run --rm docker_test_image automated_tests/tools/verify_requirements.py', returnStdout: true)
                            if (reqs_verification.contains('[ERR]')) {
                                error("${reqs_verification}")
                            }
                        }
                    }
                }
                stage ('Code linting') {
                    steps {
                        script {
                            sh 'docker run --rm docker_test_image -m pylint automated_tests --max-line-length=120 --disable=C0114,E0401'
                            sh 'docker run --rm docker_test_image -m pylint src --max-line-length=120 --disable=C0114,E0401'
                        }
                    }
                }
            }
        }
        stage ('Start app and database') {
            steps {
                script {
                    sh 'docker compose up -d'
                }
            }
        }
        stage ('WAIT') {
            steps {
                input('Do you want to proceed?')
            }
        }
        stage ('Database tests') {
            steps {
                script {
                    sh 'docker network ls'
                    sh 'docker run --network=puzzlingorangutan_default --name database_tests docker_test_image -m pytest -k pymongo -v --junitxml=pymongo_results.xml automated_tests'
                }
            }
            post {
                always {
                    sh 'docker cp database_tests:/app/pymongo_results.xml .'
                    archiveArtifacts 'pymongo_results.xml'
                    sh 'docker rm database_tests'
                }
            }
        }
        stage ('Endpoints tests') {
            steps {
                script {
                    sh 'docker run --network=host --name endpoints_tests docker_test_image -m pytest -k endpoints -v --junitxml=endpoints_results.xml automated_tests'
                }
            }
            post {
                always {
                    sh 'docker cp endpoints_tests:/app/endpoints_results.xml .'
                    archiveArtifacts 'endpoints_results.xml'
                    sh 'docker rm endpoints_tests'
                }
            }
        }
        stage ('Upload results') {
            steps {
                script {
                    echo 'Upload results to ExultantRhino if develop|master|release branch'
                }
            }
        }
    }
    post {
        always {
            script {
                sh 'docker compose down'
                // sh 'docker rmi -f docker_test_image puzzling_orangutan_db puzzling_orangutan_app'
                dir ('.') {
                    deleteDir()
                }
                junit '*.xml'
            }
        }
    }
}