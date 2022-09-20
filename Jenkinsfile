pipeline {
  agent any
  stages {
    stage('version') {
      steps {
        sh 'python --version'
      }
    }
    stage('script') {
      steps {
        sh 'python casti_pop.py'
      }
    }
  }
}