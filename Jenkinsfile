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

                    echo "=== Создание .env в tests_selenium ==="
                    cat > tests_selenium/.env << 'EOF'
BASE_URL=http://prestashop:80
LOGIN=demo@prestashop.com
PASSWORD=prestashop_demo
BROWSER=chrome
BROWSER_VERSION=latest
EXECUTOR=selenoid
EXECUTOR_URL=http://selenium-hub:4444/wd/hub
EOF

                    echo "=== Проверка .env ==="
                    cat tests_selenium/.env
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    echo "=== Запуск тестов ==="
                    cd tests_selenium
                    mkdir -p allure-results
                    python3 -m pytest tests/ -v \
                        --executor=selenoid \
                        --executor_url=http://selenium-hub:4444/wd/hub \
                        --browser=chrome \
                        --browser_version=150.0 \
                        --url=http://prestashop:80 \
                        --alluredir=allure-results -n 2
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