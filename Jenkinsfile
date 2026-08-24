pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/alinaermilova17/OTUS-Auto-web-QA-2026-SELENIUM.git'
            }
        }

        stage('Setup Environment') {
            steps {
                sh '''
                    echo "=== Проверка окружения ==="
                    python3 --version
                    pip3 --version
                    allure --version

                    echo "=== Установка зависимостей ==="
                    pip3 install --break-system-packages pytest pytest-xdist allure-pytest selenium requests python-dotenv faker

                    echo "=== Создание .env ==="
                    cat > .env << 'EOF'
BASE_URL=http://prestashop:80
LOGIN=demo@prestashop.com
PASSWORD=prestashop_demo
BROWSER=chrome
BROWSER_VERSION=latest
EXECUTOR=selenoid
EXECUTOR_URL=http://selenium-hub:4444/wd/hub
EOF

                    echo "=== Проверка .env ==="
                    cat .env
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    echo "=== Запуск тестов ==="
                    echo "Содержимое проекта:"
                    ls -la

                    if [ -d "tests_selenium" ]; then
                        cd tests_selenium
                        mkdir -p allure-results
                        python3 -m pytest tests/ -v --alluredir=allure-results
                    else
                        echo "❌ tests_selenium не найдена"
                        find . -name "test_*.py" -type f
                        exit 1
                    fi
                '''
            }
        }

        stage('Allure Report') {
            steps {
                script {
                    allure([
                        includeProperties: false,
                        jdk: '',
                        properties: [],
                        reportBuildPolicy: 'ALWAYS',
                        results: [[path: 'tests_selenium/allure-results']]
                    ])
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: '**/allure-results/*', allowEmptyArchive: true
            cleanWs()
        }
        success {
            echo '✅ Тесты успешно завершены!'
        }
        failure {
            echo '❌ Тесты завершились с ошибками.'
        }
    }
}