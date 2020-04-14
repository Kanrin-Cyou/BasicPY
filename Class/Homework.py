# Demand:
# 角色:学校、学员、课程、讲师
# 要求:

# 1. 创建北京、上海 2 所学校

# 2. 创建linux , python , go 3个课程 ， linux\py 在北京开， go 在上海开
# 3. 通过学校创建课程,  课程包含，周期，价格
# 4. 通过学校创建班级， 班级关联课程、讲师

# 5. 创建学员时，选择学校，关联班级
# 5. 创建讲师角色时要关联学校

# 6. 提供两个角色接口
# 6.1 学员视图， 可以注册， 交学费， 选择班级，
# 6.2 讲师视图， 讲师可管理自己的班级， 上课时选择班级， 查看班级学员列表 ， 修改所管理的学员的成绩
# 6.3 管理视图，创建讲师， 创建班级，创建课程

# 7. 上面的操作产生的数据都通过pickle序列化保存到文件里

class school(object):
    
    def __init__(self,name,location):
        self.name = name
        self.location = location
        self.courses = []
        self.classes = []
        self.students = []
        self.staffs = []

    def creat_courses(self,course_obj):
        print('[{}]在[{}]开课了,[{}]学费[{}]'.format(course_obj.name,self.name,course_obj.period,course_obj.tuition))
        self.courses.append(course_obj)

    def creat_classes(self,classes_obj,teacher_obj):
        print('最新消息：[{}][{}][{}]班由[{}]老师授课，速来报名'.format(self.name,classes_obj.course,classes_obj.name,teacher_obj.name))
        self.classes.append(classes_obj)
        teacher_obj.teach_class(classes_obj)

    def staff_enroll(self,staff_obj):
        '''注册'''
        print("\033[32;1m[%s]加盟[%s],本校有[%s]名老师.\033[0m " %(staff_obj.name,self.name,len(self.staffs)+1))
        self.staffs.append(staff_obj)

    def student_enroll(self,student_obj):
        '''注册'''
        print("\033[32;1m[%s]:欢迎[%s]加入本校\033[0m " %(self.name,student_obj.name))
        self.students.append(student_obj)

    def student_course_enroll(self,student_obj,classes_obj):
        if student_obj in self.students:
            if classes_obj in self.classes:
                classes_obj.student_enroll(self,student_obj)
            else:
                print('[%s]，[%s] dont have [%s]'%(student_obj.name,self.name,classes_obj.name))
        else:
            print('[%s] is not registrated yet'%(student_obj.name))


    # def __del__(self):
    #     '''析构方法'''
    #     print("\033[31;1mmember [%s] is dead!\033[0m" %self.name)

class course(object):

    def __init__(self,name,period,tuition):
        self.name = name
        self.period = period
        self.tuition = tuition

class classes(course):
    
    def __init__(self,name,obj_course):
        self.name = name
        self.course = obj_course.name
        self.tuition = obj_course.tuition
        self.period = obj_course.period
        self.students = []

    def student_enroll(self,school_obj,student_obj):
        '''注册'''
        print("\033[32;1m[%s]:欢迎[%s]加入[%s][%s]班级\033[0m " %(school_obj.name,student_obj.name,self.course,self.name))
        self.students.append(student_obj)    

class school_member(object):
    
    def __init__(self,name,age,sex):
        self.name = name
        self.age = age
        self.sex = sex

class teacher(school_member):
# 6.2 讲师视图， 讲师可管理自己的班级， 上课时选择班级， 查看班级学员列表 ， 修改所管理的学员的成绩
    def __init__(self,name,age,sex,course,school_obj):
        super(teacher,self).__init__(name,age,sex)
        self.course = course
        self.school = school_obj.name
        school_obj.staff_enroll(self)

    def teach_class(self,classes_obj):
        self.classes=classes_obj
        #print('[{}]来教[{}]'.format(self.name,classes_obj.name))

    def student_list(self):
        for item in self.classes.students:
            print(item.name)


class student(school_member):
# 6.1 学员视图， 可以注册， 交学费， 选择班级，
    def __init__(self,name,age,sex):
        super(student,self).__init__(name,age,sex)
    
    def registration(self,school_obj):
        self.school = school_obj
        school_obj.student_enroll(self)

    def select_class(self,classes_obj):
        self.classes = classes_obj
        self.school.student_course_enroll(self,classes_obj)

    def pay_tuition(self):
        print('[{}] paid [{}] for class[{}]'.format(self.name,self.classes.tuition,self.classes.name))

beijing = school('北京老男孩学校','Beijing')
shanghai = school('上海老男孩学校','Shanghai')

linux = course('linux','1term','$10000')
py = course('python','2term','$20000')
go = course('go','0.5term','$5000')

beijing.creat_courses(linux)
beijing.creat_courses(py)
shanghai.creat_courses(go)

alex = teacher('alex',34,'M','Python',beijing)
ben = teacher('ben',20,'M','Go',shanghai)

Apple = classes('Python 14期',py)
Butter = classes('Go 14期',go)

beijing.creat_classes(Apple,alex)
shanghai.creat_classes(Butter,ben)

t1 = student("ChenRonghua",24,'M')
t2 = student("SanJiang", 26,'M')
t1.registration(beijing)
t1.select_class(Apple)
t1.pay_tuition()

alex.student_list()




