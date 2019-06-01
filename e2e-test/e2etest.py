node('et_in_et'){
    try {
        elastest(tss: ['EUS'], surefireReportsPattern: '**/target/surefire-reports/TEST-*.xml', project: 'ETinET', sut: 7) {
            def elastest_url = ''
            stage ('docker container')
                def mycontainer = docker.image('elastest/ci-docker-e2e:latest')
                mycontainer.pull()
                mycontainer.inside("-u root -v /var/run/docker.sock:/var/run/docker.sock:rw -v /dev/shm:/dev/shm")  {
                    sh 'env'
		    sh 'apt-get -y install python3-pip'
		    sh 'apt-get -y install python3-setuptools'
		    sh 'pip3 install requests'	
            stage ('prepare test')
                        git 'https://github.com/elastest/elastest-bigdata-service.git'
                        elastest_url = env.ET_SUT_PROTOCOL + env.SHARED_ELASTEST_USER +":"+ env.SHARED_ELASTEST_PASS+"@"+env.ET_SUT_HOST+":"+env.ET_SUT_PORT
                      
                    stage ("Run tests")
					{
                    try {
                        sh "cd e2e-test;python3 e2etest.py ${elastest_url}"
			} catch(e) {
                        	echo 'Err: ' + e.toString()
									}    
					}  //end of "Run Tests" block
                }
        }
    } catch (err) {
        if (currentBuild.result != "UNSTABLE") {
            def errString = err.toString()
            echo 'Error: ' + errString
            currentBuild.result = getJobStatus(errString)
        }
        echo 'Error!!! Send email to the people responsible for the builds.'
        emailext body: 'Please go to  ${BUILD_URL}  and verify the build',
        replyTo: '${BUILD_USER_EMAIL}', 
        subject: 'Job ${JOB_NAME} - ${BUILD_NUMBER} RESULT: ${BUILD_STATUS}', 
        to: '${MAIL_LIST}'

        throw err
    }
}

def getJobStatus(exceptionString) {
    def status = 'SUCCESS'
    if (exceptionString.contains('exit code 1')) {
        status = 'FAILURE'
    } else {
        status = 'ABORTED'
    }
    return status;
}
