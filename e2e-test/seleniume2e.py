######################
# Author: Nick Gavalas
# 2/3/2019 fixed by Kimon Moschandreou
######################

from selenium import webdriver
import time
import sys
import selenium

# TODO: Substitute timers with webdriverwaits.
url = sys.argv[1]
projectname = 'deleteme'
tjobname = 'deletethisproject'
tjobimage = 'elastest/ebs-spark'
commands = """
git clone https://github.com/elastest/demo-projects.git
cd demo-projects/ebs-test
mvn -q package
rm -f big.txt
wget -q https://norvig.com/big.txt
hadoop fs -rmr /out.txt 
hadoop fs -rm /big.txt
hadoop fs -copyFromLocal big.txt /big.txt
spark-submit --class org.sparkexample.WordCountTask --master spark://sparkmaster:7077 /demo-projects/ebs-test/target/hadoopWordCount-1.0-SNAPSHOT.jar /big.txt
hadoop fs -getmerge /out.txt ./out.txt
head -20 out.txt
"""

	#setup Chrome WebDriver
	options = webdriver.ChromeOptions()
	options.add_argument('headless')
	options.add_argument('--no-sandbox')
	capabilities = options.to_capabilities()
	try:
		eusUrl=os.environ['ET_EUS_API']
		print("EUS URL is: "+str(eusUrl))
		driver = webdriver.Remote(command_executor=eusUrl, desired_capabilities=capabilities)
	except:
		print("ERROR (Ignorable): EUS environment variable could not be read")
		#driver = webdriver.Chrome()
		driver = webdriver.Chrome(chrome_options=options)



# Navigate to projects
# this is normally not necessary, but this method was selected in order to
# avoid E2E test issues in case the 'New Project' button is removed from the
# main screen.
time.sleep(5)
elemProjects = driver.find_element_by_id('nav_projects')
if not elemProjects.is_displayed():
    elemMenu = driver.find_element_by_id("main_menu").click()
    time.sleep(1) # delay to allow menu animation to complete.
elemProjects.click()
time.sleep(1)

# create new project
driver.find_element_by_xpath("//button[contains(string(), 'New Project')]").click()
driver.find_element_by_name("project.name").send_keys(projectname)
driver.find_element_by_xpath("//button[contains(string(), 'SAVE')]").click()
time.sleep(1)

# create new tjob
driver.find_element_by_xpath("//button[contains(string(), 'New TJob')]").click()
time.sleep(5)
driver.find_element_by_name("tJobName").send_keys(tjobname)
driver.find_element_by_xpath("//mat-select/div/div/span[contains(string(), 'Select a SuT')]").click()
driver.find_element_by_xpath("//mat-option/span[contains(string(), 'None')]").click()
# driver.find_element_by_class_name("mat-select-trigger").click()                  # ugly way of navigating to SuT
# driver.find_element_by_xpath("//md-option[contains(string(), 'None')]").click()  # but it is mandatory.
driver.find_element_by_name("tJobImageName").send_keys(tjobimage)
driver.find_element_by_name("commands").send_keys(commands)
# driver.find_element_by_xpath("//mat-checkbox[@title='Select EBS']").click()
driver.find_element_by_xpath("//mat-checkbox[@id='serviceEBS']/label").click()
# xpath("//*[@id='mat-checkbox-1']/label")).click()
driver.find_element_by_xpath("//button[contains(string(), 'SAVE')]").click()
time.sleep(1)

# run tjob
driver.find_element_by_xpath("//button[@title='Run TJob']").click()
time.sleep(10)

# default wait 10 minutes
TSS_MAX_WAIT  = 300
# check for success.
while TSS_MAX_WAIT > 0:
    try:
        # res = driver.find_element_by_xpath("//etm-dashboard/div[1]/div/md-card/md-card-content/div/span[1]/span[1][ contains(string(), 'SUCCESS') or contains(string(), 'ERROR') or contains(string(), 'FAIL') ]")
        res = driver.find_element_by_xpath("//span/h4[contains(string(), 'SUCCESS') or contains(string(), 'ERROR') or contains(string(), 'FAIL') ]")
        print(res.text)
        break
    except selenium.common.exceptions.NoSuchElementException:
        print("waiting for job to finish")
        time.sleep(20)
        TSS_MAX_WAIT = TSS_MAX_WAIT - 20


if 'SUCCESS' in res.text:
    print('job succeeded')
    print(res.text)
    exit(0)
else:
    print('job failed')
    print(res.text)
    exit(1)

driver.close()
