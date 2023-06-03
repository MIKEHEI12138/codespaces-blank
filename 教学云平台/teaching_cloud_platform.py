import tkinter

import pymysql
from tkinter import *
from tkinter import messagebox
import contact
import reply
import course_management
import Optional_course
import assignment_management
connection = pymysql.connect(host='10.128.250.177', user='root', password='123456', db='teaching_cloud_platform',
                             charset='utf8mb4')


class Student:
    def __init__(self, student_id, student_name, gender, account, password):
        self.student_id = student_id
        self.student_name = student_name
        self.gender = gender
        self.account = account
        self.password = password

    def getStudent_id(self):
        return self.student_id

    def getStudent_name(self):
        return self.student_name

    def getGender(self):
        return self.gender

    def getAccount(self):
        return self.account

    def getPassword(self):
        return self.password


class Teacher:
    def __init__(self, teacher_id, teacher_name, gender, account, password):
        self.teacher_id = teacher_id
        self.teacher_name = teacher_name
        self.gender = gender
        self.account = account
        self.password = password

    def getTeacher_id(self):
        return self.teacher_id

    def getTeacher_name(self):
        return self.teacher_name

    def getGender(self):
        return self.gender

    def getAccount(self):
        return self.account

    def getPassword(self):
        return self.password


def get_conn():
    conn = pymysql.connect(host='10.128.250.177', port=3306, user='root', passwd='123456',
                           database='teaching_cloud_platform')  # 数据库名字改下
    return conn


def open_teacherside(cursor):  # 教师端登录界面
    global teacherside
    teacherside = Toplevel(root)
    teacherside.title("教师端登录")
    teacherside.geometry("500x180")

    entry01 = Entry(teacherside)
    entry01.insert(0, "账号")
    entry01.config(fg="gray")
    entry01.place(relx=0.6, rely=0.6, relheight=0.1, width=120)

    entry02 = Entry(teacherside)
    entry02.insert(0, "密码")
    entry02.config(fg="gray")
    entry02.place(relx=0.6, rely=0.7, relheight=0.1, width=120)

    def clear_placeholder1(event):
        if entry01.get() == "账号":
            entry01.delete(0, END)
            entry01.config(fg="black")

    def restore_placeholder1(event):
        if entry01.get() == "":
            entry01.insert(0, "账号")
            entry01.config(fg="gray")

    def clear_placeholder2(event):
        if entry02.get() == "密码":
            entry02.delete(0, END)
            entry02.config(fg="black",show="*")

    def restore_placeholder2(event):
        if entry02.get() == "":
            entry02.insert(0, "密码")
            entry02.config(fg="gray",show="")

    entry01.bind("<FocusIn>", clear_placeholder1)
    entry01.bind("<FocusOut>", restore_placeholder1)
    entry02.bind("<FocusIn>", clear_placeholder2)
    entry02.bind("<FocusOut>", restore_placeholder2)

    def toggle_password_visibility():
        if entry02.cget("show") == "*":
            entry02.config(show="")
            btn_show_password.config(text="隐藏密码")
        else:
            entry02.config(show="*")
            btn_show_password.config(text="显示密码")

    btn_show_password = Button(teacherside, text="显示密码", command=toggle_password_visibility)
    btn_show_password.place(x=420, rely=0.7, relheight=0.1, width=80)

    btn01_1 = Button(teacherside, command=lambda: login(entry01.get(), entry02.get(), cursor, "Teachers"))
    btn01_1["text"] = "登录"
    btn01_1.place(relx=0.6, rely=0.8, relheight=0.1, width=120)


def open_studentside(cursor):  # 学生端登录界面
    global studentside
    studentside = Toplevel(root)
    studentside.title("学生端登录")
    studentside.geometry("200x200")

    entry01 = Entry(studentside)
    entry01.insert(0, "账号")
    entry01.config(fg="gray")
    entry01.pack()

    entry02 = Entry(studentside)
    entry02.insert(0, "密码")
    entry02.config(fg="gray")
    entry02.pack()

    btn02_1 = Button(studentside, command=lambda: login(entry01.get(), entry02.get(), cursor, "Students"))
    btn02_1["text"] = "登录"
    btn02_1.pack()

    # 定义获取焦点时清除提示文字的函数
    def clear_placeholder1(event):
        if entry01.get() == "账号":
            entry01.delete(0, END)
            entry01.config(fg="black")

    # 定义失去焦点时恢复提示文字的函数
    def restore_placeholder1(event):
        if entry01.get() == "":
            entry01.insert(0, "账号")
            entry01.config(fg="gray")

        # 定义获取焦点时清除提示文字的函数

    def clear_placeholder2(event):
        if entry02.get() == "密码":
            entry02.delete(0, END)
            entry02.config(fg="black")

        # 定义失去焦点时恢复提示文字的函数

    def restore_placeholder2(event):
        if entry02.get() == "":
            entry02.insert(0, "密码")
            entry02.config(fg="gray")

    # 绑定获取焦点和失去焦点事件
    entry01.bind("<FocusIn>", clear_placeholder1)
    entry01.bind("<FocusOut>", restore_placeholder1)

    entry02.bind("<FocusIn>", clear_placeholder2)
    entry02.bind("<FocusOut>", restore_placeholder2)

    def toggle_password_visibility():
        if entry02.cget("show") == "*":
            entry02.config(show="")
            btn_show_password.config(text="隐藏密码")
        else:
            entry02.config(show="*")
            btn_show_password.config(text="显示密码")

    btn_show_password = Button(studentside, text="显示密码", command=toggle_password_visibility)
    btn_show_password.place(x=entry02.winfo_x() + entry02.winfo_width() + 20, y=entry02.winfo_y(), anchor=W)
    btn_show_password.pack()


def login(username, password, cursor, user_type):
    if user_type == "Teachers":
        query = f"SELECT Password FROM Teachers WHERE Account = '{username}'"
    elif user_type == "Students":
        query = f"SELECT Password FROM Students WHERE Account = '{username}'"
    cursor.execute(query)
    result = cursor.fetchone()
    if result and password == result[0]:
        if user_type == "Teachers":
            query = f"SELECT TeacherID,TeacherName,Gender,Account,Password FROM Teachers WHERE Account = '{username}'"
            cursor.execute(query)
            result = cursor.fetchone()
            TeacherID = result[0]
            TeacherName = result[1]
            Gender = result[2]
            Account = result[3]
            Password = result[4]
            global currentTch
            currentTch = Teacher(TeacherID, TeacherName, Gender, Account, Password)
            teacherside_alreadyopen()

        elif user_type == "Students":
            query = f"SELECT StudentID,StudentName,Gender,Account,Password FROM Students WHERE Account = '{username}'"
            cursor.execute(query)
            result = cursor.fetchone()
            StudentID = result[0]
            StudentName = result[1]
            Gender = result[2]
            Account = result[3]
            Password = result[4]
            global currentStu
            currentStu = Student(StudentID, StudentName, Gender, Account, Password)
            studentside_alreadyopen()

    else:
        messagebox.showerror("登录失败", "账号或密码错误！")


def getcurrentStu():
    print(currentStu.getStudent_name())
    return currentStu


def insert_teacher_class():
    with connection.cursor() as cursor:
        connection.commit()
        # 查询课程列表
        teacher_id = currentTch.teacher_id
        sql = "SELECT CourseID FROM CourseTeacher WHERE TeacherID = %s"
        cursor.execute(sql, (teacher_id))
        course_id = cursor.fetchall()
        for id in course_id:
            sql = "SELECT CourseName, optional FROM Course WHERE CourseID = %s"
            cursor.execute(sql, (id[0]))
            result = cursor.fetchall()
            course_name = result[0][0]
            optional = result[0][1]
            if optional == 1:
                course_list.insert(tkinter.END, f"{id[0]}{course_name}{'(公选课)'}")
            else:
                course_list.insert(tkinter.END, f"{id[0]}{course_name}")


# 实现课程刷新
def course_flash():
    course_list.delete(0, tkinter.END)
    insert_teacher_class()


# 添加删除界面
def addordelete(event, course_info):
    global awindow
    awindow = tkinter.Toplevel(manage_window)
    awindow.title("添加或删除")
    add_button = Button(awindow, text='添加', command=lambda: add_single(course_info))
    add_button.pack()
    delete_button = Button(awindow, text='删除', command=lambda: delete_single(course_info))
    delete_button.pack()


# 单个学生的添加或删除
def add_single(course_info):
    with connection.cursor() as cursor:
        stu_item = stu_list.get(stu_list.curselection())
        stu_info = stu_item[:4]
        sql = 'Select * from CourseStudent where CourseID = %s and StudentID = %s and TeacherID = %s'
        cursor.execute(sql, (course_info, stu_info, currentTch.teacher_id))
        result = cursor.fetchall()
        if result:
            messagebox.showerror("Error", "该学生在课程中")
        else:
            if add_nownum(course_info) == 1:
                sql = 'INSERT INTO CourseStudent(CourseID,StudentID,TeacherID) VALUES (%s,%s,%s)'
                cursor.execute(sql, (course_info, stu_info, currentTch.teacher_id))
                connection.commit()
                messagebox.showinfo("Success", "学生添加成功")
            elif add_nownum(course_info) == 0:
                messagebox.showerror("Error", "课程人数已达到上线")


def delete_single(course_info):
    with connection.cursor() as cursor:
        stu_item = stu_list.get(stu_list.curselection())
        stu_info = stu_item[:4]
        sql = 'Select * from CourseStudent where CourseID = %s and StudentID = %s and TeacherID = %s'
        cursor.execute(sql, (course_info, stu_info, currentTch.teacher_id))
        result = cursor.fetchall()
        if result:
            sql = 'DELETE FROM CourseStudent where CourseID = %s and StudentID = %s and TeacherID = %s'
            cursor.execute(sql, (course_info, stu_info, currentTch.teacher_id))
            connection.commit()
            delete_nownum(course_info)
            messagebox.showinfo("Success", "学生已从课程中移除")
        else:
            messagebox.showerror("Error", "该学生未在课程中")


# 学生列表信息显示
def insert_stu(course_info):
    with connection.cursor() as cursor:
        sql = "SELECT StudentID,StudentName FROM Students"
        cursor.execute(sql)
        stu_info = cursor.fetchall()
        for info in stu_info:   
            stu_list.insert(tkinter.END, f"{info[0]}{info[1]}")
        # 点击条目实现单个添加或删除
        stu_list.bind("<<ListboxSelect>>", lambda event: addordelete(event, course_info))


# 批量添加或删除
def add_alot(course_info):
    try:
        # 切换为手动提交模式
        connection.autocommit(False)

        with connection.cursor() as cursor:
            startid = int(startfrom.get())
            endid = int(endto.get())

            while startid <= endid:
                sql = 'SELECT * FROM CourseStudent WHERE CourseID = %s AND StudentID = %s and TeacherID = %s'
                cursor.execute(sql, (course_info, startid, currentTch.teacher_id))
                result = cursor.fetchall()
                if result:
                    connection.rollback()
                    messagebox.showerror("Error", "部分学生已在课程中")
                    flag = 0
                    break  # 在回滚事务后跳出循环
                else:
                    if add_nownum(course_info) == '1':
                        # 执行添加操作
                        sql = 'INSERT INTO CourseStudent (CourseID, StudentID,TeacherID) VALUES (%s, %s, %s)'
                        cursor.execute(sql, (course_info, str(startid), currentTch.teacher_id))
                        startid += 1
                        flag = 1
                    elif add_nownum(course_info) == '0':
                        connection.rollback()
                        flag = 0
                        messagebox.showerror("Error", "课程人数已达到上线")
                        break
            # 手动提交事务
            connection.commit()
            if flag:
                messagebox.showinfo("Success", "学生已批量添加成功")
    except pymysql.Error as e:
        # 发生错误时回滚事务
        connection.rollback()
        print(f"发生错误：{e}")
    finally:
        # 切换回自动提交模式
        connection.autocommit(True)


def delete_alot(course_info):
    try:
        # 切换为手动提交模式
        connection.autocommit(False)

        with connection.cursor() as cursor:
            startid = int(startfrom.get())
            endid = int(endto.get())

            while startid <= endid:
                sql = 'SELECT * FROM Cours eStudent WHERE CourseID = %s AND StudentID = %s and TeacherID = %s'
                cursor.execute(sql, (course_info, startid, currentTch.teacher_id))
                result = cursor.fetchall()
                if result:
                    # 执行删除操作
                    sql = 'DELETE FROM CourseStudent WHERE CourseID = %s AND StudentID = %s and TeacherID = %s'
                    cursor.execute(sql, (course_info, str(startid), currentTch.teacher_id))
                    startid += 1
                    flag = 1
                    delete_nownum(course_info)
                else:
                    connection.rollback()
                    messagebox.showerror("Error", "部分学生未在课程中")
                    flag = 0
                    break  # 在回滚事务后跳出循环

            # 手动提交事务
            connection.commit()
            if flag:
                messagebox.showinfo("Success", "学生已批量删除成功")
    except pymysql.Error as e:
        # 发生错误时回滚事务
        connection.rollback()
        print(f"发生错误：{e}")
    finally:
        # 切换回自动提交模式
        connection.autocommit(True)


# 更新now_num
def add_nownum(course_info):
    with connection.cursor() as cursor:
        # 查询人数限额
        sql = 'SELECT num FROM CourseTeacher WHERE CourseID = %s AND TeacherID = %s'
        cursor.execute(sql, (course_info, currentTch.teacher_id))
        num = int(cursor.fetchone()[0])
        # 查询旧的学生人数
        sql = 'SELECT now_num FROM CourseTeacher WHERE CourseID = %s AND TeacherID = %s'
        cursor.execute(sql, (course_info, currentTch.teacher_id))
        oldnum = int(cursor.fetchone()[0])
        if num == oldnum:
            return 0
        else:
            # 更新新的学生人数
            newnum = oldnum + 1
            sql = 'UPDATE CourseTeacher SET now_num = %s WHERE CourseID = %s AND TeacherID = %s'
            cursor.execute(sql, (newnum, course_info, currentTch.teacher_id))
            # 提交事务
            connection.commit()
            return 1


def delete_nownum(course_info):
    with connection.cursor() as cursor:
        # 查询旧的学生人数
        sql = 'SELECT now_num FROM CourseTeacher WHERE CourseID = %s AND TeacherID = %s'
        cursor.execute(sql, (course_info, currentTch.teacher_id))
        oldnum = int(cursor.fetchone()[0])
        newnum = oldnum - 1
        sql = 'UPDATE CourseTeacher SET now_num = %s WHERE CourseID = %s AND TeacherID = %s'
        cursor.execute(sql, (newnum, course_info, currentTch.teacher_id))
        # 提交事务
        connection.commit()


# 设置学生人数
def set_Stunum(course_info):
    with connection.cursor() as cursor:
        num = int(entry1.get())
        sql = 'UPDATE CourseTeacher SET num = %s WHERE CourseID =%s and  TeacherID = %s'
        cursor.execute(sql, (num, course_info, currentTch.teacher_id))
        connection.commit()
        messagebox.showinfo("Success","人数设置成功")


# 刷新学生人数
def update_Stunum(course_info):
    with connection.cursor() as cursor:
        sql = 'select count(*) from CourseStudent WHERE CourseID =%s and  TeacherID = %s'
        cursor.execute(sql, (course_info, currentTch.teacher_id))
        result = cursor.fetchone()[0]
        Label_stunum.config(text=str(result))


# 点击列表条目
def manage_stu(event):
    course_item = course_list.get(course_list.curselection())
    course_info = course_item[:5]
    # 创建新窗口
    global manage_window
    manage_window = tkinter.Toplevel(new_window)
    manage_window.title("学生课程信息管理")
    # 创建学生列表框
    global stu_list
    stu_list = tkinter.Listbox(manage_window)
    stu_list.place(x=40, y=100, width=200, height=200)
    insert_stu(course_info)
    # 批量加入删除
    global startfrom
    startfrom = tkinter.Entry(manage_window)
    startfrom.pack()
    global endto
    endto = tkinter.Entry(manage_window)
    endto.pack()

    add_alotbutton = Button(manage_window, text='批量添加', command=lambda: add_alot(course_info))
    add_alotbutton.pack()
    delete_alotbutton = Button(manage_window, text='批量删除', command=lambda: delete_alot(course_info))
    delete_alotbutton.pack()

    # 设置课程人数
    Label1 = tkinter.Label(manage_window, text='学生人数')
    Label1.pack()
    global entry1
    entry1 = tkinter.Entry(manage_window)
    entry1.pack()
    set_stunum_button = Button(manage_window, text="设置学生人数", command=lambda: set_Stunum(course_info))
    set_stunum_button.pack()

    # 显示当前学生
    Label2 = tkinter.Label(manage_window, text='当前学生人数')
    Label2.pack()
    global Label_stunum
    Label_stunum = tkinter.Label(manage_window, text='0')
    Label_stunum.pack()
    update_Stunum(course_info)
    update_stunum_button = Button(manage_window, text='刷新学生人数', command=lambda: update_Stunum(course_info))
    update_stunum_button.pack()


def create_course_window():
    # 创建新窗口
    global create_window
    create_window = tkinter.Toplevel(new_window)
    create_window.title("公选课的开设")
    # 创设输入框
    label1 = tkinter.Label(create_window, text="课程ID")
    label1.pack()

    entry3 = tkinter.Entry(create_window)
    entry3.pack()
    label2 = tkinter.Label(create_window, text="课程名称")
    label2.pack()

    entry4 = tkinter.Entry(create_window)
    entry4.pack()
    label3 = tkinter.Label(create_window, text="课程人数")
    label3.pack()

    entry5 = tkinter.Entry(create_window)
    entry5.pack()

    # 创设按钮
    create_button = Button(create_window, text="开设课程", command=lambda: create_course(entry3, entry4, entry5))
    create_button.pack()


def create_course(entry3, entry4, entry5):
    with connection.cursor() as cursor:
        course_id = str(entry3.get())
        course_name = str(entry4.get())
        course_num = int(entry5.get())
        # 先检查是否有雷同课程
        sql = 'SELECT * FROM Course WHERE CourseID = %s AND CourseName = %s'
        cursor.execute(sql, (course_id, course_name))
        result = cursor.fetchall()
        if result:
            messagebox.showerror("Error", "同名课程已存在")
        else:
            # 写入课程表
            sql = 'INSERT INTO Course(CourseID, CourseName,optional) VALUES (%s, %s,%s)'
            cursor.execute(sql, (course_id, course_name, '1'))
            # 写入教师课程表
            sql = 'INSERT INTO CourseTeacher(CourseID, TeacherID, num,now_num) VALUES (%s, %s, %s,%s)'
            cursor.execute(sql, (course_id, currentTch.teacher_id, course_num,0))
            connection.commit()
            messagebox.showinfo("Success","开设成功")


def teacherside_alreadyopen():
    # 创建新窗口
    global new_window
    new_window = Toplevel(root)
    new_window.title("教学云平台——教师端")
    new_window.geometry("500x400")
    #删除旧窗口
    teacherside.destroy()
    reply_button = Button(new_window, text="沟通", command=lambda: reply.reply_button(currentTch))
    reply_button.pack()
    manage_button = Button(new_window, text="管理课程", command=lambda: course_management.manage_button(currentTch))
    manage_button.pack(side='bottom')
    # 创建课程列表框
    global course_list
    course_list = tkinter.Listbox(new_window)
    course_list.place(x=40, y=100, width=200, height=200)
    insert_teacher_class()
    # 课程刷新按钮
    flash_button = Button(new_window, text="刷新课程", command=course_flash)
    flash_button.pack()
    # 绑定列表框的点击事件
    course_list.bind("<<ListboxSelect>>", manage_stu)
    # 添加开设公选课
    create_course_button = Button(new_window, text="开设公选课", command=create_course_window)
    create_course_button.pack()
    #添加作业布置
    assignment_button=Button(new_window,text="作业布置",command=lambda :assignment_management.assignment_button(currentTch))
    assignment_button.pack()

def insert_student_class():
    with connection.cursor() as cursor:
        connection.commit()
        # 查询课程列表
        student_id = currentStu.student_id
        sql = "SELECT CourseID FROM CourseStudent WHERE StudentID = %s"
        cursor.execute(sql, (student_id))
        course_id = cursor.fetchall()
        for id in course_id:
            sql = "SELECT CourseName From Course Where CourseID = %s "
            cursor.execute(sql, (id))
            course_name = cursor.fetchall()
            for name in course_name:
                stu_course_list.insert(tkinter.END, f"{id[0]}{name[0]}")


def insert_work(course_info):
    with connection.cursor() as cursor:
        print(course_info, currentStu.student_id)
        sql = 'SELECT TeacherID FROM CourseStudent WHERE CourseID = %s AND StudentID = %s'
        cursor.execute(sql, (course_info, currentStu.student_id))
        teacher_ids = cursor.fetchall()
        if teacher_ids:
            teacher_id = teacher_ids[0][0]
            print(teacher_id)
            sql = 'SELECT TeacherName FROM Teachers WHERE TeacherID = %s'
            cursor.execute(sql, (teacher_id,))
            teacher_names = cursor.fetchall()
            if teacher_names:
                teacher_name = teacher_names[0][0]
                print(teacher_name)
                sql = 'SELECT id FROM Assignment WHERE CourseID = %s AND StudentID = %s'
                cursor.execute(sql, (course_info, currentStu.student_id))
                course_ids = cursor.fetchall()
                print(course_ids)
                i = 1
                for id in course_ids:
                    work_list.insert(tkinter.END, f"作业{i} 来自于{teacher_name}")
                    i += 1


def manage_course(event):
    course_item = stu_course_list.get(stu_course_list.curselection())
    course_info = course_item[:5]
    # 创建新窗口
    global work_window
    work_window = tkinter.Toplevel(new1_window)
    work_window.title("学习资源管理")
    # 创建作业列表
    global work_list
    work_list = tkinter.Listbox(work_window)
    work_list.place(x=40, y=100, width=200, height=200)
    # 插入作业
    insert_work(course_info)


def studentside_alreadyopen():
    # 创建新窗口
    global new1_window
    new1_window = Toplevel(root)
    new1_window.title("教学云平台——学生端")
    new1_window.geometry("500x400")
    #删除窗口
    studentside.destroy()
    contact_button = Button(new1_window, text="咨询", command=lambda: contact.contact_button(currentStu))
    contact_button.pack()
    # 创建课程列表框
    global stu_course_list
    stu_course_list = tkinter.Listbox(new1_window)
    stu_course_list.place(x=40, y=100, width=200, height=200)
    insert_student_class()
    # 绑定列表框的点击事件
    stu_course_list.bind("<<ListboxSelect>>", manage_course)
    option_button=Button(new1_window,text="公选课选课",command=lambda :Optional_course.init_course(currentStu))
    option_button.pack()
def init_window(cursor):
    global root
    root = Tk()
    root.title("教学云平台")
    root.geometry("500x300+100+200")



    btn01 = Button(root, command=lambda :open_teacherside(cursor), text="教师端登录", font=("华文新魏", 14), relief=RAISED)
    btn01.place(relx=0.3, rely=0.7, relheight=0.1, width=200)
    btn02 = Button(root, command=lambda :open_studentside(cursor),text="学生端登录", font=("华文新魏", 14))
    btn02.place(relx=0.3, rely=0.8, relheight=0.1, width=200)

    root.mainloop()


if __name__ == '__main__':
    db = get_conn()
    cursor = db.cursor()
    init_window(cursor)
    cursor.close()
    db.close()
