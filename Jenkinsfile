pipeline {
    agent {
        dockerfile {
            filename 'automated_tests/Dockerfile'
        }
    }
    stages {
        stage('Prepare for tests') {
            parallel {
                stage ('Verify requirements') {
                    steps {
                        script {
                            dir('automated_tests/tools') {
                                def reqs_verification = sh(script: 'python3.10 verify_requirements.py', returnStdout: true)
                                if (reqs_verification.contains('[ERR]')) {
                                    error("${reqs_verification}")
                                }
                            }
                        }
                    }
                }
                stage ('Code linting') {
                    steps {
                        script {
                            dir("automated_tests/") {
                                sh 'tox -e lint src'
                                sh 'tox -e lint automated_tests'
                            }
                        }
                    }
                }
                stage ('Compose images') {
                    stages {
                        stage ('Build image') {
                            steps {
                                script {
                                    sh 'docker compose up -d'
                                }
                            }
                            post {
                                always {
                                    script {
                                        sh 'docker compose down'
                                    }
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
                                    echo "STEP"
                                }
                            }
                        }
                    }
                }
            }
        }
        stage('Run tests') {
            parallel {
                stage ('Database tests') {
                    steps {
                        script {
                            sh 'docker compose up -d'
                            sh "sed -i 's/mongodb/localhost/1' src/pymongo_db.py"
                            dir("automated_tests/") {
                                sh "tox -e pymongo"
                            }
                        }
                    }
                    post {
                        always {
                            script {
                                sh 'docker compose down'
                                sh "sed -i 's/localhost/mongodb/1' src/pymongo_db.py"
                            }
                        }
                    }
                }
                stage ('Endpoints') {
                    steps {
                        script {
                            sh 'docker compose up -d'
                            sh "sed -i 's/mongodb/localhost/1' src/pymongo_db.py"
                            dir("automated_tests/") {
                                sh "tox -e pymongo"
                            }
                        }
                    }
                    post {
                        always {
                            script {
                                sh 'docker compose down'
                                sh "sed -i 's/localhost/mongodb/1' src/pymongo_db.py"
                            }
                        }
                    }
                }
            }
        }
        stage ('Scan for skipped tests') {
            when {
                expression {
                    return env.BRANCH_NAME == 'develop' || env.BRANCH_NAME == 'release'
                }
            }
            steps {
                script {
                    echo "STEP"
                }
            }
        }
        stage ('Upload results') {
            when {
                expression {
                    return env.BRANCH_NAME == 'develop' || env.BRANCH_NAME == 'release' || env.BRANCH_NAME == 'master'
                }
            }
            steps {
                script {
                    echo "STEP"
                }
            }
        }
    }
}