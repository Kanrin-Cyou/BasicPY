class School(object):

    def __init__(self,name,addr):
        self.name = name
        self.addr = addr
        self.students = []
        self.staffs = []

    def enroll(self,stu_obj):
        print('为学生[{}]办理注册手续'.format(stu_obj.name))
        self.students.append(stu_obj)

    def hire(self,staff_obj):
        print('雇佣老师[{}]'.format(staff_obj.name))
        self.staffs.append(staff_obj)

class SchoolMember(object):

    members = 0 #初始学校人数为0
    
    def __init__(self,name,age,sex):
        self.name = name
        self.age = age
        self.sex = sex
 
    def tell(self): #打印自己的变量信息
        pass
 
    def enroll(self):
        '''注册'''
        SchoolMember.members +=1
        print("\033[32;1mnew member [%s] is enrolled,now there are [%s] members.\033[0m " %(self.name,SchoolMember.members))
     
    def __del__(self):
        '''析构方法'''
        print("\033[31;1mmember [%s] is dead!\033[0m" %self.name)


class Teacher(SchoolMember):

    def __init__(self,name,age,sex,course,salary):
        super(Teacher,self).__init__(name,age,sex)
        self.course = course
        self.salary = salary
        self.enroll()
 
    def teach(self):
        '''讲课方法'''
        print("Teacher [%s] is teaching [%s] for class [%s]" %(self.name,self.course,'s12'))
 
    def tell(self):
        '''自我介绍方法'''
        msg = '''Hi, my name is [%s], works for [%s] as a [%s] teacher !''' %(self.name,'Oldboy', self.course)
        print(msg)


class Student(SchoolMember):
    def __init__(self,name,age,sex,stu_id,grade):
        super(Student,self).__init__(name,age,sex)
        self.grade = grade
        self.stu_id = stu_id
        self.enroll()
 
    def tell(self):
        '''自我介绍方法'''
        msg = '''Hi, my name is [%s], I'm studying [%s] in [%s]!''' %(self.name, self.grade,'Oldboy')
        print(msg)

    def pay_tuition(self,amount):
        print('%s has paid tuition for $%s'%(self.name,amount))

oldboy = School('老男孩IT','沙河')
t1 = Teacher("Alex",22,'M','PythoTn',20000)
t2 = Teacher("TengLan",29,'M','Linux',3000)

s1 = Student("ChenRonghua",24,'M',1001,'S14')
s2 = Student("SanJiang", 26,'M',1002,'S14')

oldboy.enroll(s1)
oldboy.enroll(s2)
oldboy.hire(t1)
oldboy.hire(t2)

oldboy.students
oldboy.staffs
 
oldboy.staffs[0].teach()
# for stu in school.students:

for stu in oldboy.students:
    stu.pay_tuition(5000)