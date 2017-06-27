node('docker'){
    stage "Container Prep"
        echo("the node is up")
        def mycontainer = docker.image('sgioldasis/ci-docker-in-docker:latest')
        mycontainer.pull() // make sure we have the latest available from Docker Hub
        mycontainer.inside("-u jenkins -v /var/run/docker.sock:/var/run/docker.sock:rw") {

            git 'https://github.com/elastest/elastest-data-manager.git'
            git 'https://github.com/elastest/elastest-bigdata-service.git'
            
            // stage "Test"
            //     sh 'ls -la'
            //     echo ("Starting maven tests")
            //     echo ("No tests yet, but these would be integration at least")
            //     sh 'which docker'
                
            stage "Verify"
                sh 'pwd && ls -l && cd .. && pwd && ls -l'

            stage "Build Spark Base image - Package"
                echo ("building..")
                //need to be corrected to the organization because at the moment elastestci can't create new repositories in the organization
                def spark_base_image = docker.build("elastest/ebs-spark-base:0.5.0","./spark")

            stage "Run EDM docker-compose"
                sh 'cd ./elastest-data-manager && chmod +x bin/startup-linux.sh && bin/startup-linux.sh'
                echo ("EDM System is running..")

            stage "Run EBS docker-compose"
                sh 'cd .. && chmod +x bin/startup-linux.sh && bin/startup-linux.sh'
                echo ("EBS System is running..")
                
            stage "publish"
                echo ("publishing..")
                withCredentials([[
                    $class: 'UsernamePasswordMultiBinding', 
                    credentialsId: 'elastestci-dockerhub',
                    usernameVariable: 'USERNAME',
                    passwordVariable: 'PASSWORD']]) {
                        sh 'docker login -u "$USERNAME" -p "$PASSWORD"'
                        //here your code 
                        spark_base_image.push()
                    }

        }
}