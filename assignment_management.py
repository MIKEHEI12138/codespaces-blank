import tkinter
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, filedialog
from tkinter import *
import matplotlib.pyplot as plt
import pymysql

from PIL.ImageTk import PhotoImage

# 连接数据库
connection = pymysql.connect(host='10.128.250.177', user='root', password='123456', db='teaching_cloud_platform',
                             charset='utf8mb4')


def get_conn():
    connection = pymysql.connect(host='10.128.250.177', user='root', password='123456', db='teaching_cloud_platform',
                                 charset='utf8mb4')
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
        tree.delete(*tree.get_children())

        # 更新作业列表
        assignments = get_assignments(course_id)
        for assignment in assignments:
            tree.insert("", tk.END, values=(assignment[3], assignment[0]))

        messagebox.showinfo("成功", "作业已成功群发给所有学生！")
    else:
        messagebox.showerror("错误", "请选择课程并填写作业内容！")


# 统计本次作业的提交情况起到辅助预测的作用
def Assisted_prediction(event):#
    # 检查是否存在旧窗口并关闭
    if 'new_window' in globals():
        new_window.destroy()

    with connection.cursor() as cursor:
        selected_item = tree.focus()
        if selected_item:  # 如果有选中的项
            result = tree.item(selected_item)["values"]
            id = result[1]
        teacher_id = ct.teacher_id
        # 查找对应课程
        sql = 'select CourseID from Assignment where id = %s '
        cursor.execute(sql, (id))
        course_id = cursor.fetchall()[0][0]
        # 统计需要提交的人数
        sql = 'select count(*) from CourseStudent where  CourseID = %s and teacherID = %s'
        cursor.execute(sql, (course_id, teacher_id))
        num = cursor.fetchall()[0][0]

        # 统计提交的人数
        sql = 'select count(*) from submithomework where CourseID = %s and teacherID = %s and ID = %s'
        cursor.execute(sql, (course_id, teacher_id, id))
        sub_num = cursor.fetchall()[0][0]

        # 未提交人数
        a = num - sub_num

        # 定义数据
        labels = ['The number of submissions', 'Number of non-submissions']
        sizes = [sub_num, a]

        # 创建饼状图
        plt.pie(sizes, labels=labels, autopct='%1.1f%%')

        # 设置图表标题
        plt.title('Assignment submission status')
        # 显示图表
        plt.show()

        # 辅助预测功能
        if a > sub_num:
            messagebox.showwarning("警告:", "半数以上同学未交作业，请教师加以督促")


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
        tree.delete(*tree.get_children())
        course_id = selected_course.split()[0][:5]

        assignments = get_assignments(course_id)

        # 显示作业列表
        for assignment in assignments:
            tree.insert("", tk.END, values=(assignment[3], assignment[0]))


def scatter_plot(x, y):
    plt.title('Assignment Statistics')
    plt.xlabel('Assignment Count')
    plt.ylabel('Number of Submissions')
    plt.plot(x, y, linestyle='--', marker='o', color='r')
    plt.show()


def bar_chart(x, y):
    plt.title('Assignment Statistics')
    plt.xlabel('Assignment Count')
    plt.ylabel('Number of Submissions')
    plt.bar(x, y)
    plt.show()


def assignment_statistics(selected_course):
    with connection.cursor() as cursor:
        global new_window
        new_window = tkinter.Toplevel(window)

        window_width = 50
        window_height = 80
        # 计算窗口在屏幕中的坐标位置
        x = (screen_width - window_width) // 2 - 150
        y = (screen_height - window_height) // 2 -100

        # 设置窗口的位置
        new_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x, y))

        new_window.resizable(False, False)

        # 获取选中的课程
        course_id = selected_course[:5]
        teacher_id = ct.teacher_id
        # 统计作业数
        sql = 'select count(id) from assignment where CourseID = %s and TeacherID = %s '
        cursor.execute(sql, (course_id, teacher_id))
        assignment_num = int(cursor.fetchall()[0][0])
        # 得到每次作业id
        sql = 'select id from assignment where CourseID = %s and TeacherID = %s '
        cursor.execute(sql, (course_id, teacher_id))
        assignment_id = cursor.fetchall()

        # 横坐标
        x = []
        # 纵坐标
        y = []
        for i in range(1, assignment_num + 1):
            x.append('homework' + str(i))
        for id in assignment_id:
            sql = 'select count(*) from submithomework where CourseID = %s and TeacherID = %s and id = %s'
            cursor.execute(sql, (course_id, teacher_id, id))
            num = int(cursor.fetchall()[0][0])

            y.append(num)
        Button1 = tk.Button(new_window, text='散点图', command=lambda: scatter_plot(x, y))
        Button1.pack()
        Button2 = tk.Button(new_window, text='柱状图', command=lambda: bar_chart(x, y))
        Button2.pack()


# 得到作业号对应的课程号
def getass_courseid(assignment_id):
    cursor.execute("SELECT CourseID FROM submithomework WHERE id = %s", (assignment_id))
    result = cursor.fetchone()
    CourseID = result[0] if result else 0
    return CourseID


def view_submitted_homework():
    # 创建窗口
    submitted_window = tk.Toplevel(window)
    submitted_window.title("已提交作业")

    window_width = 400
    window_height = 300
    # 计算窗口在屏幕中的坐标位置
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # 设置窗口的位置
    submitted_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x, y))


    background_image27 = PhotoImage(file="2222.png")
    background_label27 = Label(submitted_window, image=background_image27)
    background_label27.place(x=0, y=0, relwidth=1, relheight=1)

    submitted_window.image = background_image27

    submitted_window.resizable(False, False)
    # 创建作业列表
    submitted_tree = ttk.Treeview(submitted_window, columns=("1", "2", "3"), show="headings")
    # 设置列标题
    submitted_tree.column("1",width=100)
    submitted_tree.column("2", width=100)
    submitted_tree.column("3", width=100)
    submitted_tree.heading("1", text="作业号")
    submitted_tree.heading("2", text="作业内容")
    submitted_tree.heading("3", text="学生id")

    submitted_tree.pack()

    selected_items = tree.selection()
    if selected_items:
        # 获取选中的作业信息
        item = tree.item(selected_items)
        values = item['values']
        assignment_id = values[1]  # 作业号
        requirement = values[0]  # 作业内容

        # 查询已提交作业
        course_id = getass_courseid(assignment_id)
        sql = "SELECT id, content, StudentID FROM submithomework WHERE id = %s"
        cursor.execute(sql, (assignment_id,))
        submitted_assignments = cursor.fetchall()

        # 在作业列表中显示已提交作业
        for assignment in submitted_assignments:
            assignment_id = assignment[0]
            content = assignment[1]
            student_id = assignment[2]
            submitted_tree.insert("", tk.END, values=(assignment_id, content, student_id))

    # 创建下载按钮和相关函数
    def download_assignment():
        selected_item = submitted_tree.selection()
        if selected_item:
            item = submitted_tree.item(selected_item)
            values = item['values']
            assignment_id = values[0]
            content = values[1]
            student_id = values[2]

            # 创建保存文件对话框
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[('Text Files', '*.txt')])
            if file_path:
                # 将作业内容保存到文件
                with open(file_path, 'w') as f:
                    f.write(content)

                messagebox.showinfo("下载成功", "作业已成功下载。")
        else:
            messagebox.showwarning("未选中作业", "请先选中要下载的作业。")

    download_button = tk.Button(submitted_window, text="下载作业", command=download_assignment)
    download_button.pack(pady=10)


def assignment_button(currentTch,root):
    global ct
    ct = currentTch

    # 创建主窗口
    global window
    window = tk.Toplevel(root)
    window.title("作业管理系统")
    global screen_width
    global screen_height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # 设置窗口的位置

    window_width = 500
    window_height = 400
    # 计算窗口在屏幕中的坐标位置
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # 设置窗口的位置
    window.geometry("{}x{}+{}+{}".format(window_width, window_height, x, y))

    window.resizable(False, False)


    background_image26 = PhotoImage(file="2222.png")
    background_label26 = Label(window, image=background_image26)
    background_label26.place(x=0, y=0, relwidth=1, relheight=1)

    window.image = background_image26


    course_frame = tk.Frame(window, bg='white')  # 创建课程列表框
    course_frame.place(relx=0.05, rely=0.1, relwidth=0.3, relheight=0.47)

    course_label = tk.Label(course_frame, text="课程列表", font=("华文新魏", 14), bg='white')
    course_label.place(relheight=0.1)

    global course_listbox
    course_listbox = tk.Listbox(course_frame, width=20)
    course_listbox.place(rely=0.1)

    get_courses(ct.teacher_id)

    # 创建作业列表框
    assignment_frame = tk.Frame(window, bg='white')
    assignment_frame.place(relx=0.5, rely=0.1, relwidth=0.5, relheight=0.6)

    assignment_label = tk.Label(assignment_frame, text="作业列表", font=("华文新魏", 14), bg='white')
    assignment_label.place(relheight=0.1)
    global tree
    tree = ttk.Treeview(assignment_frame, columns=("1", "2"), show="headings")
    # 设置标题
    tree.column("1", width=50)
    tree.column("2", width=50)
    tree.heading("1", text='作业内容')
    tree.heading("2", text='作业ID')
    tree.place(rely=0.1, relwidth=0.8, relheight=0.7)

    tree.bind("<<TreeviewSelect>>", lambda event: Assisted_prediction(event))

    # 创建作业内容输入框和发送按钮
    message_frame = tk.Frame(window, bg='white')
    message_frame.place(relx=0.5, rely=0.6, relwidth=0.4, relheight=0.6)

    message_label = tk.Label(message_frame, text="作业内容", font=("华文新魏", 14), bg='white')
    message_label.place(relx=0, rely=0, relheight=0.1)
    global message_entry
    message_entry = tk.Text(message_frame)
    message_entry.place(rely=0.1, relwidth=1, relheight=0.4)

    send_button = tk.Button(message_frame, text="发送作业", command=send_assignment)
    send_button.place(rely=0.5, relwidth=1, relheight=0.1)

    # 绑定选择课程事件
    course_listbox.bind("<<ListboxSelect>>", select_course)

    # 创建查看已提交作业按钮
    view_button = tk.Button(window, text="查看已提交作业", command=view_submitted_homework)
    view_button.place(relx=0.8, rely=0.02, relheight=0.05)

    # 主事件循环
    window.mainloop()

    # 关闭数据库连接
    connection.close()
