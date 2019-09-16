######################
# Author: Nick Gavalas
# 2/3/2019 fixed by Kimon Moschandreou
######################

import time
import sys
import os
import selenium
from selenium import webdriver

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
eusUrl=os.environ['ET_EUS_API']
print("EUS URL is: "+str(eusUrl))
print(capabilities)
driver = webdriver.Remote(desired_capabilities=capabilities, command_executor=url)
# driver.get(url)
# create new project
time.sleep(5)
element=driver.find_element_by_xpath("//button[contains(string(), 'New Project')]")
element.click()
time.sleep(5)
driver.find_element_by_name("project.name").send_keys(projectname)
driver.find_element_by_xpath("//button[contains(string(), 'SAVE')]").click()
time.sleep(5)

# create new tjob
driver.find_element_by_xpath("//button[contains(string(), 'New TJob')]").click()
time.sleep(5)
driver.find_element_by_name("tJobName").send_keys(tjobname)
# driver.find_element_by_xpath('//*[@id="mat-select-0"]/div/div[1]/span').click()
driver.find_element_by_class_name("mat-select-trigger").click() 
driver.find_element_by_xpath("//mat-option/span[contains(string(), 'None')]").click()
driver.find_element_by_name("tJobImageName").send_keys(tjobimage)
driver.find_element_by_name("commands").send_keys(commands)
driver.find_element_by_xpath("//mat-checkbox[@id='serviceEBS']/label").click()
driver.find_element_by_xpath("//button[contains(string(), 'SAVE')]").click()
time.sleep(1)

# run tjob
driver.find_element_by_xpath("//button[@title='Run TJob']").click()
time.sleep(10)

# default max wait 5 minutes
TSS_MAX_WAIT  = 300
# check for success.
while TSS_MAX_WAIT > 0:
	try:
		element = driver.find_element_by_id('resultMsgText')
		if (element.text=="Executing Test" or element.text=="Starting Test Support Service: EBS" or element.text=="Starting Dockbeat to get metrics..."):
			print("\t Waiting for tjob execution to complete")
			time.sleep(20)
			TSS_MAX_WAIT = TSS_MAX_WAIT - 20
			element = driver.find_element_by_id('resultMsgText')
			continue
		else:
			print("\t TJob Execution Result: "+element.text)
			break
	except:
		print("\t Something is wrong")
		break



driver.close()
