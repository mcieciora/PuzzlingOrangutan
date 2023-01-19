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
                        stage ('Build app') {
                            steps {
                                script {
                                    sh 'docker compose build'
                                }
                            }
                        }
                        stage ('Deploy image') {
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
                            def code_linting_image = docker.image('docker_test_image')
                            image.inside {
                                sh 'pwd'
                                sh 'python3.11 -m pylint automated_tests src --max-line-length=120 --disable=C0114'
                                sh 'date > test.txt'
                                archiveArtifacts 'test.txt'
                            }
                        }// sh 'docker run docker_test_image --rm -m pylint automated_tests src --max-line-length=120 --disable=C0114'
                    }
                }
            }
        }
        stage ('Start app and database') {
            steps {
                script {
                    sh 'docker compose up -d --rm'
                }
            }
        }
        stage ('Execute tests') {
            parallel {
                stage ('Database tests') {
                    steps {
                        script {
                            sh 'docker run --rm docker_test_image -m pytest -k pymongo -v --junitxml=pymongo_results.xml'
                        }
                    }
                }
                stage ('Endpoints tests') {
                    steps {
                        script {
                            sh 'docker run --rm docker_test_image -m pytest -k endpoints -v --junitxml=endpoints_results.xml'
                        }
                    }
                }
            }
        }
    }
    post {
        always {
            script {
                sh 'docker compose down'
                sh 'docker rmi -f docker_test_image puzzling_orangutan_db puzzling_orangutan_app'
            }
            cleanWs()
        }
    }
}