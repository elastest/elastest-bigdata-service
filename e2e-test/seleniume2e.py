######################
# Author: Nick Gavalas
######################

from selenium import webdriver
import time
import sys

# TODO: Substitute timers with webdriverwaits.

url = sys.argv[1]
projectname = 'deleteme'
tjobname = 'deletethisproject'
tjobimage = 'elastest/ebs-spark'
commands = """
git clone https://github.com/elastest/demo-projects.git
cd demo-projects/ebs-test
mvn package
rm -f big.txt
wget https://norvig.com/big.txt
#clean the pre-existing file
hadoop fs  -rmr /out.txt
hadoop fs -rmr /big.txt
hadoop fs -copyFromLocal big.txt /big.txt
spark-submit --class org.sparkexample.WordCountTask --master spark://spark:7077 /demo-projects/ebs-test/target/hadoopWordCount-1.0-SNAPSHOT.jar /big.txt
hadoop fs -getmerge /out.txt ./out.txt
head -20 out.txt
"""
driver = webdriver.Chrome()
# driver.get("http://localhost:37000")
driver.get(url)


# assert "Dashboard" in driver.title

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
driver.find_element_by_name("tJobName").send_keys(tjobname)
driver.find_element_by_class_name("mat-select-trigger").click()                  # ugly way of navigating to SuT
driver.find_element_by_xpath("//md-option[contains(string(), 'None')]").click()  # but it is mandatory.
driver.find_element_by_name("tJobImageName").send_keys(tjobimage)
driver.find_element_by_name("commands").send_keys(commands)
driver.find_element_by_xpath("//md-checkbox[@title='Select EBS']").click()
driver.find_element_by_xpath("//button[contains(string(), 'SAVE')]").click()
time.sleep(1)

# run tjob
driver.find_element_by_xpath("//button[@title='Run TJob']").click()
time.sleep(10)

# check for success.


driver.close()

