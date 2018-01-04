node('docker'){
    stage "Container Prep"
        echo("the node is up")
        //sh 'echo 262144 | sudo tee /proc/sys/vm/max_map_count'
        def mycontainer = docker.image('sgioldasis/ci-docker-in-docker')
        mycontainer.pull()
        mycontainer.inside("-u jenkins -v /var/run/docker.sock:/var/run/docker.sock:rw") {

            // Get EDM source code
            git 'https://github.com/elastest/elastest-data-manager.git'

            stage "Run EDM docker-compose"
                sh 'chmod +x bin/* && bin/teardown-ci.sh && bin/startup-ci.sh'
                echo ("EDM System is running..")               

            // Get EBS source code
            git 'https://github.com/elastest/elastest-bigdata-service.git'
            
            stage "Build REST API image - Package"
                echo ("building..")
                sh 'cd rest-api; docker build --build-arg GIT_COMMIT=$(git rev-parse HEAD) --build-arg COMMIT_DATE=$(git log -1 --format=%cd --date=format:%Y-%m-%dT%H:%M:%S) -f rest-api/Dockerfile . -t elastest/ebs:latest'
                def rest_api_image = docker.image("elastest/ebs:latest")

            stage "Build Spark Base image - Package"
                echo ("building..")
                sh 'cd spark; docker build --build-arg GIT_COMMIT=$(git rev-parse HEAD) --build-arg COMMIT_DATE=$(git log -1 --format=%cd --date=format:%Y-%m-%dT%H:%M:%S) . -t elastest/ebs-spark:latest'
                def spark_base_image = docker.image("elastest/ebs-spark:latest")

            // Run EBS docker-compose
            stage "Run EBS docker-compose"
                sh 'chmod +x bin/* && bin/teardown-linux.sh && bin/startup-linux.sh'
                echo ("EBS System is running..")

            stage "Unit tests"
                echo ("Starting unit tests...")
                sh 'bin/run-tests.sh'
                step([$class: 'JUnitResultArchiver', testResults: '**/rest-api/nosetests.xml'])

            stage "Cobertura"
                //sh 'bin/run-tests.sh'
                sh('cd rest-api && git rev-parse HEAD > GIT_COMMIT')
                    git_commit=readFile('rest-api/GIT_COMMIT')
                    
                sh 'export GIT_COMMIT=$git_commit'
              
                sh 'export GIT_BRANCH=master'
                def codecovArgs = "-v -t $COB_EBS_TOKEN"
                // def codecovArgs = "-v -t 64f66b26-1b9c-48ab-b412-9021cdbc36cd"
                        
                echo "$codecovArgs"
                
                def exitCode = sh(
                    returnStatus: true,
                    script: "curl -s https://codecov.io/bash | bash -s - $codecovArgs")
                    if (exitCode != 0) {
                        echo( exitCode +': Failed to upload code coverage to codecov')
                    }

            stage "publish"
                echo ("publishing..")
                withCredentials([[
                    $class: 'UsernamePasswordMultiBinding', 
                    credentialsId: 'elastestci-dockerhub',
                    usernameVariable: 'USERNAME',
                    passwordVariable: 'PASSWORD']]) {
                        sh 'docker login -u "$USERNAME" -p "$PASSWORD"'
                        //here your code 
                        rest_api_image.push()
                        spark_base_image.push()
                    }

        }
}