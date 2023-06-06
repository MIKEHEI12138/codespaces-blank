import os
import sys
import tkinter
import pymysql
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import threading
connection = pymysql.connect(host='10.128.250.177', user='root', password='123456', db='teaching_cloud_platform',
                             charset='utf8mb4')

# 创建线程锁
lock = threading.Lock()

def join_course(course_id, course_name, teacher_id, teacher_name, remain_num, num):
    with connection.cursor() as cursor:
        try:
            # 加锁
            lock.acquire()

            sql = 'select * from CourseStudent where CourseID = %s and StudentID = %s and TeacherID = %s'
            cursor.execute(sql, (course_id, cs.getStudent_id(), teacher_id))
            result = cursor.fetchall()
            if result:
                messagebox.showerror("Error", "请勿重复选课")
            else:
                sql = 'select * from CourseTeacher where CourseID = %s and TeacherID = %s FOR UPDATE'
                cursor.execute(sql, (course_id, teacher_id))
                now_num = cursor.fetchall()[0][3]
                if now_num == num:
                    messagebox.showerror("Error", "课程已满了哟")
                else:
                    sql = 'INSERT INTO CourseStudent(CourseID, StudentID, TeacherID) VALUES(%s, %s, %s)'
                    cursor.execute(sql, (course_id, cs.getStudent_id(), teacher_id))
                    sql = 'UPDATE CourseTeacher SET now_num = %s WHERE CourseID = %s AND TeacherID = %s'
                    new_num = now_num + 1
                    cursor.execute(sql, (new_num, course_id, teacher_id))
                    messagebox.showinfo("Success", "选课成功")
                connection.commit()
        except pymysql.Error as e:
            # 处理数据库错误
            print(f"Database Error: {e}")
        finally:
            # 释放锁
            lock.release()
            window3.destroy()






#退课模块
def drop_course(course_id, course_name, teacher_id,teacher_name,remain_num,num):
    with connection.cursor() as cursor:
        try:
            lock.acquire()
            sql = 'SELECT * FROM CourseStudent WHERE CourseID = %s AND StudentID = %s AND TeacherID = %s'
            cursor.execute(sql, (course_id, cs.getStudent_id(), teacher_id))
            print(course_id, cs.getStudent_id(), teacher_id)
            result = cursor.fetchall()
            if not result:
                messagebox.showerror("Error", "未选修该课程，无法退课")
            else:
                sql = 'SELECT * FROM CourseTeacher WHERE CourseID = %s AND TeacherID = %s FOR UPDATE'
                cursor.execute(sql, (course_id, teacher_id))
                now_num = cursor.fetchone()[3]
                sql = 'DELETE FROM CourseStudent WHERE CourseID = %s AND StudentID = %s AND TeacherID = %s'
                cursor.execute(sql, (course_id, cs.getStudent_id(), teacher_id))
                sql = 'UPDATE CourseTeacher SET now_num = %s WHERE CourseID = %s AND TeacherID = %s'
                new_num = now_num - 1
                cursor.execute(sql, (new_num, course_id, teacher_id))
                messagebox.showinfo("Success", "退课成功")
                connection.commit()
        except pymysql.Error as e:
            # 处理数据库错误
            print(f"Database Error: {e}")
        finally:
            # 释放锁
            lock.release()
            window3.destroy()



def select_course(event):
    selection=tree.focus()
    values = tree.item(selection, "values")
    course_id=str(values[0])
    course_name=str(values[1])
    teacher_id=str(values[2])
    teacher_name=str(values[3])
    remain_num=int(values[4])
    num=int(values[5])
    global window3
    window3 = tkinter.Toplevel(root1)

    window_width = 60
    window_height = 70
    # 计算窗口在屏幕中的坐标位置
    x = (screen_width - window_width) // 2 - 200
    y = (screen_height - window_height) // 2 - 150

    # 设置窗口的位置
    window3.geometry("{}x{}+{}+{}".format(window_width, window_height, x, y))

    window3.resizable(False, False)
    join_button=Button(window3,text='选课',command=lambda :join_course(course_id,course_name,teacher_id,teacher_name,remain_num,num))
    join_button.pack()
    leave_button=Button(window3,text='退课',command=lambda :drop_course(course_id,course_name,teacher_id,teacher_name,remain_num,num))
    leave_button.pack()


def insert_tree():
    with connection.cursor() as cursor:
        try:
            tree.delete(*tree.get_children())
            tree.update()
            sql = "SELECT CourseID, CourseName FROM course WHERE optional = %s"
            cursor.execute(sql, ('1'))
            result = cursor.fetchall()
            print(result)
            for row in result:
                course_id = row[0]
                course_name = row[1]

                sql = "SELECT TeacherID FROM CourseTeacher WHERE CourseID = %s"
                cursor.execute(sql, (course_id))
                teacher_id = cursor.fetchall()[0][0]

                sql = "SELECT TeacherName FROM teachers WHERE TeacherID = %s"
                cursor.execute(sql, (teacher_id))
                teacher_name = cursor.fetchall()[0][0]

                sql = "SELECT num, now_num FROM CourseTeacher WHERE CourseID = %s AND TeacherID = %s"
                cursor.execute(sql, (course_id, teacher_id))
                result = cursor.fetchall()
                num = result[0][0]
                now_num = result[0][1]
                remain_num = num - now_num

                tree.insert("", tkinter.END, values=(course_id, course_name,teacher_id ,teacher_name, remain_num,num))

        except pymysql.Error as e:
            # 处理数据库错误
            print(f"Database Error: {e}")


def init_course(currentStu,root):
    global cs
    cs=currentStu
    global root1
    root1=Toplevel(root)
    root1.title("公选课选课平台")

    background_image26 = PhotoImage(file=get_resource_path("images/3333.png"))
    background_label26 = Label( root1, image=background_image26)
    background_label26.place(x=0, y=0, relwidth=1, relheight=1)


    label=tkinter.Label(root1,text="可供选择的公选课",bg='white')
    label.pack()

    global screen_width
    screen_width = root1.winfo_screenwidth()
    global screen_height
    screen_height = root1.winfo_screenheight()

    window_width = 500
    window_height = 300
    # 计算窗口在屏幕中的坐标位置
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # 设置窗口的位置
    root1.geometry("{}x{}+{}+{}".format(window_width, window_height, x, y))

    root1.resizable(False, False)

    global tree
    tree=ttk.Treeview(root1,columns=("1","2","3","4","5","6"),show="headings")
    # 设置列标题
    tree.column("1", width=80)
    tree.column("2", width=80)
    tree.column("3", width=80)
    tree.column("4", width=80)
    tree.column("5", width=80)
    tree.column("6", width=80)
    tree.heading("1", text="公选课ID")
    tree.heading("2", text="公选课")
    tree.heading("3",text="教师ID")
    tree.heading("4",text="教师名称")
    tree.heading("5", text="剩余人数")
    tree.heading("6",text="总人数")


    #显示
    tree.pack()
    insert_tree()
    tree.bind("<ButtonRelease-1>", select_course)
    flash_button=Button(root1,text="刷新",bg='white',command=insert_tree)
    flash_button.pack()
    root1.mainloop()
def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

