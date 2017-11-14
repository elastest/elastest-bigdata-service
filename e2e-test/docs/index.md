# End-to-end tests of ElasTest Big Data Service (EBS)

This project contains end-to-end (E2E) tests aiming to verify the correctness of the ElasTest Big Data Service (EBS) through the Test Orchestration and Recommendation Manager (TORM).

In order to implement these test we use [Selenium WebDriver], which is an web testing framework to automate the navigation and verification of web applications using a given test logic. In this case, we use Java to implement the test, and [JUnit 5] as base testing framework. In order to ease the management on web browsers in the tests, we use an open source JUnit 5 extension called [selenium-jupiter].

The following E2E tests are going to be implemented:

1. Use of EBS as support service.

The following sections of this document summarizes the main parts of these tests.

## Use of EBS as support service

This test in implemented in the test [EBSSupportServiceE2eTest.java]. As can be seen, this class extends a parent class: [EBSBaseTest.java]. This parent class contains a common setup for tests (annotated with JUnit 5's `@BeforeEach`):

```java
    @BeforeEach
    void setup() {
        String etmApi = getProperty("etEmpApi");
        if (etmApi != null) {
            tormUrl = etmApi;
        }
        log.info("Using URL {} to connect to TORM", tormUrl);
    }
```

This piece of code read the JVM argument called `etEmpApi` to find out the TORM URL. The value of this argument is supposed to be configured previously to the test execution, and this is done in the [Jenkins pipeline]:

```
stage ("E2E tests") {
   try {
      sh "cd e2e-test; mvn -B clean test -DetEmpApi=http://${etEmpApi}:8091/"
   } catch(e) {
      sh 'docker ps | awk "{print $NF}" | grep EBS | xargs docker logs'
   }
   step([$class: 'JUnitResultArchiver', testResults: '**/target/surefire-reports/TEST-*.xml'])
}
```

The structure of the actual test (method annotated with JUnit 5's annotation `@Test` in ) is as follows:


```java
@Tag("e2e")
@DisplayName("E2E tests of EBS through TORM")
@ExtendWith(SeleniumExtension.class)
public class EBSSupportServiceE2eTest extends EBSBaseTest {

    final Logger log = getLogger(lookup().lookupClass());

    @Test
    @DisplayName("EBS as support service")
    void testSupportService(ChromeDriver driver) throws Exception {
        // Test logic
    }

}
```

In addition to the JUnit 5 annotation for tagging and naming (`@Tag` and `@DisplayName`), we see that we are using the [selenium-jupiter] extension, declaring it using the annotation `@ExtendWith(SeleniumExtension.class)`. Thanks to the dependency injection feature of JUnit 5, the extension creates proper WebDriver instances for tests. In this case, simply declaring this instance in the test arguments (in this case, `ChromeDriver driver`), we can use a browser (in this case Chrome) in our test is a seamless way. The Jenkins job is configured properly to use a Docker image ([elastest/ci-docker-e2e]) in which several browsers (Chrome and Firefox) are ready to be used by tests.

Regarding the test logic, it is basically an specific application of Selenium WebDriver to test the web GUI provided by the TORM. For instance, the first part of the test is the following:

```java
        log.info("Navigate to TORM and start support service");
        driver.manage().window().setSize(new Dimension(1024, 1024));
        driver.manage().timeouts().implicitlyWait(5, SECONDS); // implicit wait
        driver.get(tormUrl);
        startTestSupportService(driver, "EBS");
```

In this snippet, we see that we force the size of the browser windows, we configure a global implicit wait of 5 seconds (to wait for elements to be located by WebDriver), then we open the TORM URL, and then we use the parent method `startTestSupportService` to start the support service identified by the label `EBS`.

The next part is specific for the EBS. First, we determine the EBS Service Spark Docker Container Id:

```java
        // Get EBS Service Spark Docker Container Id
        String ebsInstances = driver.findElement(By.xpath("//div[contains(string(), 'Instance Id:')]")).getText();
        String[] lines = ebsInstances.split("\\r?\\n");
        Boolean tagJustFound = false;
        String containerId = "";
        String tag = "Instance Id:";
        for (String line : lines) {
                // First find a tag line containing the literal "Instance Id" used in the GUI
                if(line.contains(tag)) tagJustFound = true;
                // The next line after the tag line is the value of service Id
                if(!line.contains(tag) && tagJustFound) {
                        tagJustFound = false;
                        // Construct the docker container Id based on the service instance Id
                        containerId = line.replace("-", "")+"_spark_1";
                }
        }

```

Then we execute a command inside the EBS docker container. This command copies a file from the container local filesystem to HDFS through Alluxio.

```java
        // Start a process to execute the command
        String[] command = {"docker", "exec", "-i", containerId, "alluxio", "fs", "copyFromLocal", "/opt/spark/README.md", "/hdfs/"+fileName};
        ProcessBuilder pb = new ProcessBuilder(command);
        Process p = pb.start();
```

After that, we check is line of output for the expected successful result. 

```java
        while ((output = processOutput.readLine()) != null) {
                log.info("*** NORMAL OUTPUT : "+output);
                if (output.contains("Copied file:///opt/spark/README.md to /hdfs")) success = true;
        }

```

Finally, we log the result and assert that success should be true. 


[Selenium WebDriver]: http://www.seleniumhq.org/projects/webdriver/
[JUnit 5]: http://junit.org/junit5/docs/current/user-guide/
[selenium-jupiter]: https://bonigarcia.github.io/selenium-jupiter/
[EBSSupportServiceE2eTest.java]: https://github.com/elastest/elastest-bigdata-service/blob/master/e2e-test/src/test/java/io/elastest/EBS/test/e2e/EBSSupportServiceE2eTest.java
[EBSBaseTest.java]: https://github.com/elastest/elastest-bigdata-service/blob/master/e2e-test/src/test/java/io/elastest/EBS/test/base/EBSBaseTest.java
[Jenkins pipeline]: https://github.com/elastest/elastest-bigdata-service/blob/master/e2e-test/Jenkinsfile
[elastest/ci-docker-e2e]: https://hub.docker.com/r/elastest/ci-docker-e2e/
