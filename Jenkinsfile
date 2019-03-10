def elastest_url = ''
node('et_in_et'){
    elastest(tss: ['EUS'], surefireReportsPattern: '**/target/surefire-reports/TEST-*.xml', project: 'ETinET', sut: 11) {        
        stage ('docker container')
            def mycontainer = docker.image('elastest/ci-docker-e2e:latest')
            mycontainer.pull()
            mycontainer.inside()  {
                sh 'env'
                stage ('prepare test')
                    git 'https://github.com/elastest/elastest-bigdata-service.git'
                    elastest_url = env.ET_SUT_PROTOCOL + '://' + env.ET_SUT_HOST + ':' + env.ET_SUT_PORT
                    
                stage ("Run tests")
                    try {
                        sh "cd e2e-test; mvn -B clean test -Dtest=EtInEtDemoTest -DetEtmApi=" + elastest_url + " -DeUser=elastest -DePass=3xp3r1m3nt47"
                    } catch(e) {
                        echo 'Err: ' + e.toString()
                    } finally {
                        step([$class: 'JUnitResultArchiver', testDataPublishers: [[$class: 'AttachmentPublisher']], testResults: '**/target/surefire-reports/TEST-*.xml'])
                    }
            }
    }
}
