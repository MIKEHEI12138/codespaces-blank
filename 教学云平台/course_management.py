import tkinter as tk
import pymysql
import tkinter.ttk as ttk
from tkinter import messagebox
# 连接数据库
connection = pymysql.connect(host='localhost', user='root', password='123456', db='teaching_cloud_platform', charset='utf8mb4')

# 获取课程信息并插入到左侧列表中
def insert_list():
    with connection.cursor() as cursor:
        connection.commit()
        # 查询课程列表
        sql = "SELECT CourseID, CourseName,optional FROM Course"
        cursor.execute(sql)
        course_info = cursor.fetchall()
        for info in course_info:
            if info[2]==1:
                continue
            else:
                course_list.insert(tk.END, f"{info[0]} {info[1]}")
#增加课程功能
def add_course():
    with connection.cursor() as cursor:
        course_id = entry.get()

        # 查询输入的课程id是否正确
        sql = "SELECT * FROM Course WHERE CourseID = %s"
        cursor.execute(sql, (course_id))
        result = cursor.fetchall()
        if not result:
            messagebox.showerror("Error", "课程号错误，请重新输入")
        else:
            # 查询该课程是否已经被添加
            teacher_id = ct.getTeacher_id()
            sql = "SELECT * FROM CourseTeacher WHERE CourseID = %s AND TeacherID = %s"
            cursor.execute(sql, (course_id, teacher_id))
            result = cursor.fetchall()
            if result:
                messagebox.showerror("Error", "课程已存在，请勿重复添加")
            else:
                # 进行课程添加的操作
                sql="INSERT INTO CourseTeacher (CourseID, TeacherID) VALUES (%s, %s)"
                cursor.execute(sql,(course_id,teacher_id))
                connection.commit()
                messagebox.showinfo("Success", "课程添加成功")


def delete_course():
    with connection.cursor() as cursor:
        course_id = entry.get()

        # 查询输入的课程id是否正确
        sql = "SELECT * FROM Course WHERE CourseID = %s"
        cursor.execute(sql, (course_id))
        result = cursor.fetchall()
        if not result:
            messagebox.showerror("Error", "课程号错误，请重新输入")
        else:
            # 查询该课程是否已经被添加
            teacher_id = ct.getTeacher_id()
            sql = "SELECT * FROM CourseTeacher WHERE CourseID = %s AND TeacherID = %s"
            cursor.execute(sql, (course_id, teacher_id))
            result = cursor.fetchall()
            if result:
                # 进行课程删除的操作
                sql = "DELETE FROM CourseTeacher WHERE CourseID = %s"
                cursor.execute(sql, (course_id))
                connection.commit()
                messagebox.showinfo("Success", "课程删除成功")

            else:
                messagebox.showerror("Error", "您本学期没有该课程")
# 初始化课程管理界面
def manage_button(currentTch):
    # 用于保存登录教师的信息
    global ct
    ct = currentTch
    # 创建主窗口
    window = tk.Tk()
    window.title("Course_management")
    # 创建联系人列表框
    global course_list
    course_list = tk.Listbox(window)
    course_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    insert_list()

    #创建一个输入框用以输入想添加或删除的课程
    global entry
    entry=tk.Entry(window)
    entry.pack()
    add_button=tk.Button(window,text="添加课程",command=add_course)
    add_button.pack()
    delete_button=tk.Button(window,text="删除课程",command=delete_course)
    delete_button.pack()
    window.mainloop()


