import tkinter
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import pymysql
import matplotlib.pyplot as plt
# 连接数据库
connection = pymysql.connect(host='10.128.250.177', user='root', password='123456', db='teaching_cloud_platform', charset='utf8mb4')

def get_conn():
    connection = pymysql.connect(host='10.128.250.177', user='root', password='123456', db='teaching_cloud_platform', charset='utf8mb4')
    return connection

cursor = connection.cursor()

# 群发作业给所有学生
def send_assignment():
    # 获取选中的课程和作业内容
    selected_course = course_listbox.get(course_listbox.curselection())
    selected_assignment = message_entry.get("1.0", tk.END).strip()

    if selected_course and selected_assignment:
        # 获取课程ID
        course_id = selected_course.split()[0][:5]

        # 向Assignment表添加作业记录
        sql = "INSERT INTO Assignment (CourseID, TeacherID, Requirement) VALUES (%s, %s, %s)"
        values = (course_id, ct.teacher_id, selected_assignment)
        cursor.execute(sql, values)
        connection.commit()

        # 清空作业列表
        assignment_listbox.delete(0, tk.END)

        # 更新作业列表
        assignments = get_assignments(course_id)
        for assignment in assignments:
            assignment_listbox.insert(tk.END, f"{assignment[3]}")

        messagebox.showinfo("成功", "作业已成功群发给所有学生！")
    else:
        messagebox.showerror("错误", "请选择课程并填写作业内容！")


# 获取指定课程的作业
def get_assignments(course_id):
    cursor.execute("SELECT * FROM assignment WHERE CourseID = %s", (course_id,))
    assignments = cursor.fetchall()
    return assignments


# 获取教师的课程
def get_courses(teacher_id):
    # 查询课程列表
    teacher_id = ct.teacher_id
    sql = "SELECT CourseID FROM CourseTeacher WHERE TeacherID = %s"
    cursor.execute(sql, (teacher_id))
    course_id = cursor.fetchall()
    for id in course_id:
        sql = "SELECT CourseName From Course Where CourseID = %s "
        cursor.execute(sql, (id))
        course_name = cursor.fetchall()
        for name in course_name:
            course_item = f"{id[0]}{name[0]}"
            course_listbox.insert(tk.END, course_item)

def select_course(event):

    # 获取选中的课程
    selected_course = course_listbox.get(course_listbox.curselection())
    assignment_statistics(selected_course)
    if selected_course:
        # 清空作业列表
        assignment_listbox.delete(0, tk.END)
        course_id = selected_course.split()[0][:5]

        assignments = get_assignments(course_id)

        # 显示作业列表
        for assignment in assignments:
            assignment_listbox.insert(tk.END, f"{assignment[3]}")

def scatter_plot(x,y):
    plt.title('Assignment Statistics')
    plt.xlabel('Assignment Count')
    plt.ylabel('Number of Submissions')
    plt.plot(x, y, linestyle='--', marker='o', color='r')
    plt.show()
def bar_chart(x,y):
    plt.title('Assignment Statistics')
    plt.xlabel('Assignment Count')
    plt.ylabel('Number of Submissions')
    plt.bar(x, y)
    plt.show()

def assignment_statistics(selected_course):
    with connection.cursor() as cursor:
        global new_window
        new_window=tkinter.Toplevel(window)

        #获取选中的课程
        course_id=selected_course[:5]
        teacher_id=ct.teacher_id
        #统计作业数
        sql='select count(id) from assignment where CourseID = %s and TeacherID = %s '
        cursor.execute(sql,(course_id,teacher_id))
        assignment_num=int(cursor.fetchall()[0][0])
        #得到每次作业id
        sql='select id from assignment where CourseID = %s and TeacherID = %s '
        cursor.execute(sql,(course_id,teacher_id))
        assignment_id =cursor.fetchall()

        #横坐标
        x=[]
        #纵坐标
        y=[]
        for i in range(1,assignment_num+1):
            x.append('homework'+str(i))
        for id in assignment_id:
            sql = 'select count(*) from submithomework where CourseID = %s and TeacherID = %s and id = %s'
            cursor.execute(sql, (course_id, teacher_id, id))
            num = int(cursor.fetchall()[0][0])

            y.append(num)
        Button1 =tk.Button(new_window, text='散点图',command=lambda :scatter_plot(x,y))
        Button1.pack()
        Button2 = tk.Button(new_window, text='柱状图',command=lambda:bar_chart(x,y))
        Button2.pack()

def assignment_button(currentTch):
    global ct
    ct=currentTch


    # 创建主窗口
    global window
    window = tk.Tk()
    window.title("作业管理系统")

    # 创建课程列表框
    course_frame = tk.Frame(window)
    course_frame.pack(side=tk.LEFT, padx=10, pady=10)

    course_label = tk.Label(course_frame, text="课程列表")
    course_label.pack()

    global course_listbox
    course_listbox = tk.Listbox(course_frame, width=20)
    course_listbox.pack()

    get_courses(ct.teacher_id)

    # 创建作业列表框
    assignment_frame = tk.Frame(window)
    assignment_frame.pack(side=tk.LEFT, padx=10, pady=10)

    assignment_label = tk.Label(assignment_frame, text="作业列表")
    assignment_label.pack()

    global assignment_listbox
    assignment_listbox = tk.Listbox(assignment_frame, width=30)
    assignment_listbox.pack()

    # 创建作业内容输入框和发送按钮
    message_frame = tk.Frame(window)
    message_frame.pack(side=tk.LEFT, padx=10, pady=10)

    message_label = tk.Label(message_frame, text="作业内容")
    message_label.pack()

    global message_entry
    message_entry = tk.Text(message_frame, width=30, height=10)
    message_entry.pack()

    send_button = tk.Button(message_frame, text="发送作业", command=send_assignment)
    send_button.pack()

    # 绑定选择课程事件
    course_listbox.bind("<<ListboxSelect>>", select_course)



    # 主事件循环
    window.mainloop()

    # 关闭数据库连接
    connection.close()




