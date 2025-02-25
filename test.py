import os
from openai import OpenAI
import json

with open("config/ark.json") as ark_config_file:
    ark = json.load(ark_config_file)


client = OpenAI(
    # 从环境变量中读取您的方舟API Key
    api_key=ark["Credentials"]["api_key"], 
    base_url=ark["Credentials"]["base_url"],
    )
completion = client.chat.completions.create(
    # 将推理接入点 <Model>替换为 Model ID
    model="deepseek-r1-250120",
    messages=[
        {
            "role": "user", 
            "content": 
            '''
            进行简要总结
            Overload
            Overload 是重载，一般是用于在一个类内实现若干重载的方法，这些
            方法的名称相同而参数形式不同。
            Yang Liu
            Student
            # sid: String
            # name: String
            # sex: String
            # sclass: String
            # major: String
            + register()
            + selectCourse(String course)
            + printStates()
            UndergraduateStudent
            + doCourseDesign(String course)
            GraduateStudent
            - supervisor: String
            - researchDirection: String
            + participateInProject(String project)
            + printStates()
            + setSupervisor(String sv)
            + setSupervisor(String sv1, String sv2)
            '''
        }
    ]
)
print(completion.choices[0].message)