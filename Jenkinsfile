pipeline {
  agent any
  stages {
    stage('version') {
      steps {
        sh 'python3 --version'
      }
    }
    stage('script') {
      steps {
        sh 'python casti_pop.py'
      }
    }
  }
}