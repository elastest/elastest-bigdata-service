import json
import requests
import time
import sys

# create a dummy project


url = sys.argv[0]
res = requests.get(url)
data = json.dumps({"id": 666, "name": "EBSE2E"})
headers = {'content-type': 'application/json'}
res = requests.post(url+'/api/project', data=data, headers=headers)
print res.text
print json.loads(res.text)


# create a tjob in the project
COMMANDS = """
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
head -10 out.txt"""

tjob=json.dumps({ "id": 0,
  "name": "demotjob",
  "imageName": "elastest/ebs-spark:latest",
  #"sut": '',
  "project": json.loads(res.text),
  "tjobExecs": [],
  "parameters": [],
  # "commands": "git clone https://github.com/elastest/demo-projects.git\r\ncd demo-projects/ebs-test\r\nmvn package\r\nrm -f big.txt\r\nwget https://norvig.com/big.txt\r\n#clean the pre-existing file\r\nhadoop fs  -rmr /out.txt\r\nhadoop fs -rmr /big.txt\r\nhadoop fs -copyFromLocal big.txt /big.txt\r\nspark-submit --class org.sparkexample.WordCountTask --master spark://spark:7077 /demo-projects/ebs-test/target/hadoopWordCount-1.0-SNAPSHOT.jar /big.txt\r\nhadoop fs -getmerge /out.txt ./out.txt\r\nhead -10 out.txt",
  "commands": COMMANDS,
  "esmServicesString": "[{\"id\":\"a1920b13-7d11-4ebc-a732-f86a108ea49c\",\"name\":\"EBS\",\"selected\":true},{\"id\":\"fe5e0531-b470-441f-9c69-721c2b4875f2\",\"name\":\"EDS\",\"selected\":false},{\"id\":\"af7947d9-258b-4dd1-b1ca-17450db25ef7\",\"name\":\"ESS\",\"selected\":false},{\"id\":\"29216b91-497c-43b7-a5c4-6613f13fa0e9\",\"name\":\"EUS\",\"selected\":false},{\"id\":\"bab3ae67-8c1d-46ec-a940-94183a443825\",\"name\":\"EMS\",\"selected\":false}]",
  "esmServices": [
      {
          "id": "a1920b13-7d11-4ebc-a732-f86a108ea49c",
          "name": "EBS",
          "selected": True
      },
      {
          "id": "fe5e0531-b470-441f-9c69-721c2b4875f2",
          "name": "EDS",
          "selected": False
      },
      {
          "id": "af7947d9-258b-4dd1-b1ca-17450db25ef7",
          "name": "ESS",
          "selected": False
      },
      {
          "id": "29216b91-497c-43b7-a5c4-6613f13fa0e9",
          "name": "EUS",
          "selected": False
      },
      {
          "id": "bab3ae67-8c1d-46ec-a940-94183a443825",
          "name": "EMS",
          "selected": False
      }
  ],
  })
res = requests.post(url+'/api/tjob', headers=headers, data=tjob)
resjson = res.json()
tjobid = resjson['id']
print resjson['id']


# run the tjob
data = {"tJobParams": []}
res = requests.post(url + '/api/tjob/' + str(tjobid) + '/exec', headers=headers, json=data)
print res.text


# probe for results
# s = requests.Session()
# exec_resp = s.get(url + "/api/tjob/" + str(tjobid) + "/exec/" + str(json.loads(res.text)["id"]))
exec_resp = requests.get(url + "/api/tjob/" + str(tjobid) + "/exec/" + str(json.loads(res.text)["id"]))

while ("FAIL" != str(json.loads(exec_resp.text)["result"]).strip()) and ("SUCCESS" != str(json.loads(exec_resp.text)["result"]).strip()):
    print("TJob execution status is: "+str(json.loads(exec_resp.text)["result"]))
    exec_resp = requests.get(url + "/api/tjob/" + str(tjobid) + "/exec/" + str(json.loads(res.text)["id"]))
    time.sleep(5)


# exit successfully
if "SUCCESS" in str(json.loads(exec_resp.text)["result"]):
    # print exec_resp.text
    print("TJob execution successful")
    exit(0)
# or exit with failure
elif "FAIL" in str(json.loads(exec_resp.text)["result"]):
    # print exec_resp.text
    print("TJob execution failed")
    exit(1)
