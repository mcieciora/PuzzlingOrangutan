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
        stage ('Before tests checks') {
            parallel {
                stage ('Verify requirements') {
                    steps {
                        script {
                            def reqs_verification = sh('docker run docker_test_image automated_tests/tools/verify_requirements.py', returnStdout: true)
                            if (reqs_verification.contains('[ERR]')) {
                                error("${reqs_verification}")
                            }
                        }
                    }
                }
                stage ('Code linting') {
                    steps {
                        script {
                            sh 'docker run docker_test_image -m pylint automated_tests src --max-line-length=120 --disable=C0114'
                        }
                    }
                }
            }
        }
    }
}