from tortoise.models import Model
from tortoise import fields

#  四个模型，五张表

class Student(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=10, decription="姓名")
    pwd = fields.CharField(max_length=10, decription="密码")
    sno = fields.CharField(max_length=100, decription="学号")

    # 一对多关系（一个班级有多个学生）,生成字段clas_id
    # 从学生对象访问班级：可以通过student.clas访问该学生所属的班级。
    # 从班级对象访问学生：由于设置了related_name="students"，可以通过clas.students访问该班级下的所有学生。
    clas = fields.ForeignKeyField("models.Clas", related_name="students")

    # 多对多关系（多个学生可以选择多个课程，多个课程也可以被多个学生选择）
    # 创建连接表，建立学生-课程表（student_course）,这个中间表会包含两个外键，分别引用Student表和Course表的主键。
    # 从学生对象访问课程：可以通过student.courses访问该学生选择的所有课程。
    # 从课程对象访问学生：由于设置了related_name="students"，可以通过course.students访问选择该课程的所有学生。
    courses = fields.ManyToManyField("models.Course", related_name="students")

class Course(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=10, decription="课程名")
    teacher = fields.ForeignKeyField("models.Teacher", related_name="courses")
    addr = fields.CharField(max_length=100, decription="教室",default="")

class Teacher(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100, decription="姓名")
    pwd = fields.CharField(max_length=10, decription="密码")
    tno = fields.CharField(max_length=100, decription="老师编号")

    # 一对多关系（一个班级有多个老师）,生成字段clas_id
    clas = fields.ForeignKeyField("models.Clas", related_name="teachers")

class Clas(Model):
    name = fields.CharField(max_length=100, decription="班级")