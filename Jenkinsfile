pipeline {
    agent any
    stages {
        stage('Prepare for tests') {
            parallel {
                stage ('Verify requirements') {
                    steps {
                        script {
                            echo "STEP"
                        }
                    }
                }
                stage ('Code linting') {
                    steps {
                        script {
                            echo "STEP"
                        }
                    }
                }
                stage ('Compose images') {
                    steps {
                        stage ('Build image') {
                            steps {
                                script {
                                    echo "STEP"
                                }
                            }
                        }
                        stage ('Deploy image') {
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
                            echo "STEP"
                        }
                    }
                }
                stage ('Endpoints') {
                    steps {
                        script {
                            echo "STEP"
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