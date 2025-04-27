from fastapi import APIRouter
from models import *
from fastapi import Request
from pydantic import BaseModel, field_validator
from typing import List, Union
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import HTTPException

student_api = APIRouter()

@student_api.get("/")
async def getAllStudent():
    # 从models中导入Student，通过异步方式await Student.all()映射成queryset的数据对象。
    # 查询所有all方法
    students = await Student.all()  # 是queryset的数据对象。
    print("students",  students)  # students [<Student: 1>, <Student: 2>, <Student: 3>]
    print(students[0].name)
    for stu in students:
        print(stu.name, stu.sno)

    # 过滤查询 filter方法，返回模型类型对象列表
    l_students = await Student.filter(name="rain")  # [<Student: 1>]
    # l_students = await Student.filter(clas_id=1)
    print(l_students)
    for stu in l_students:
        print(stu.name, stu.sno)

    # 过滤查询 get方法，返回模型类型对象，
    # 即如果只对一个字段进行过滤，可以使用get方法。
    # students = await Student.get(name="rain")  # <Student>
    # print(students)
    # print(students.sno)

    # # 模糊查询, 学号大于2001
    # l_stu = await Student.filter(sno__gt=2001)
    # print(l_stu)  # [<Student: 2>, <Student: 3>]
    #
    # # 模糊查询, 学号范围在2001,2002之间
    # l_stu = await Student.filter(sno__in=[2001, 2002])
    # print(l_stu)  # [<Student: 1>, <Student: 2>]

    # values查询，以字典方式组成列表对象
    # l_stu = await Student.all().values("name",'sno')
    # print(l_stu)  # [{'name': 'rain', 'sno': '2001'}, {'name': 'eric', 'sno': '2002'}, {'name': 'avlin', 'sno': '2003'}]

    # l_stu = await Student.filter(sno__range=[1, 10000])  # 无结果，应为sno是字符串，不是int
    # l_stu = await Student.filter(sno__gte="1", sno__lte="10000")
    # print(l_stu)
    # return {"操作": l_stu}

    # 一对多查询，多对多查询
    # 一对多，查询某个学生的信息
    stu = await Student.get(name="titi")
    # print(stu.name)
    # print(stu.clas_id)
    # print(await stu.clas.values("name"))

    # 一对多，查询所有学生的姓名和课程名
    # stu = await Student.all().values("name", "clas__name")

    # 多对多
    # 获取titi所有课程名和课程名对应的老师。
    # 学生titi对应student_course有两门课，这两门课对应的老师。
    # print(await stu.courses.all().values("name", "teacher__name"))

    # 查询所有学生的姓名、班级及课程名
    stu = await Student.all().values("name", "clas__name","courses__name")
    print(stu)


    return {"操作": stu}

@student_api.get("/index.html")
async def indexhtml(request: Request):
    template = Jinja2Templates(directory="templates")
    students = await Student.all()  # 是queryset的数据对象。

    return template.TemplateResponse(
            "index.html",
            {"request": request,
             "students": students}
        )


class StudentIn(BaseModel):
    name: str
    pwd: str
    sno: str
    clas_id: int
    courses: List[int] = []
    # 约束字段
    @field_validator("name")
    def name_must_alpha(cls, value):
        assert value.isalpha(),'name must be alpha'
        return value

@student_api.post("/")
async def addStudent(student_in: StudentIn):

    # 插入到数据库
    # 方式1：
    # 实现了类对象的构建，将类对象实例化映射一条sql语句
    # student = Student(name=student_in.name, pwd=student_in.pwd, sno=student_in.sno, clas_id=student_in.clas_id)
    # 数据库操作，采用await
    # await student.save() # 插入到数据库student表

    # 方式2：
    student = await Student.create(name=student_in.name, pwd=student_in.pwd, sno=student_in.sno, clas_id=student_in.clas_id)

    # 多不多的关系绑定
    # 过滤课程
    choose_courses = await Course.filter(id__in=student_in.courses)
    print("choose_courses:", choose_courses)  # choose_courses: [<Course: 1>, <Course: 2>]

    # await student.courses.clear()

    # 将课程绑定到学生，即student_course 学生生成2个课程绑定关系
    await student.courses.add(*choose_courses)
    print("Courses added to student:", await student.courses.all())  # 调试信息
    # print("Courses added to student:", student.courses)  # 调试信息

    return student



    # return {"操作":"添加一个学生"}

@student_api.get("/{student_id}")
async def getOneStudent(student_id: int):
    student = await Student.get(id = student_id)
    return student
    # return {"操作":f"查看id={student_id}一个学生"}

@student_api.put("/{student_id}")
async def updateStudent(student_id: int, student_in: StudentIn):
    data = student_in.dict()
    print("data",data) # data {'name': 'titihaha', 'pwd': '1212', 'sno': '3090', 'clas_id': 2, 'courses': [2]}
    # 注意：由于Student中没有courses字段，所以需要手动去除。
    courses = data.pop("courses")

    # 更新的值
    await Student.filter(id=student_id).update(**data)

    # 设置多对多的选修课，即更新课程
    edit_stu = await Student.get(id=student_id)
    choose_courses = await Course.filter(id__in=courses)
    await edit_stu.courses.clear()  # 清除之前的关联关系。
    await edit_stu.courses.add(*choose_courses)

    return edit_stu

    # return {"操作":f"更新id={student_id}一个学生"}


@student_api.delete("/{student_id}")
async def deleteStudent(student_id: int):

    deleteCount = await Student.filter(id=student_id).delete()
    if not deleteCount:
        raise HTTPException(status_code=404, detail="Student not found")

    return {}
    # return {"操作":f"删除id={student_id}一个学生"}
