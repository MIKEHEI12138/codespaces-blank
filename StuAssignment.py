import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, filedialog
from tkinter import *
import pymysql

# 连接数据库
connection = pymysql.connect(host='10.128.250.177', user='root', password='123456', db='teaching_cloud_platform', charset='utf8mb4')

def get_conn():
    connection = pymysql.connect(host='10.128.250.177', user='root', password='123456', db='teaching_cloud_platform', charset='utf8mb4')
    return connection

cursor = connection.cursor()

def get_courses(currentStu):
    # 查询课程列表
    student_id = currentStu.student_id
    sql = "SELECT CourseID FROM CourseStudent WHERE StudentID = %s"
    cursor.execute(sql, (student_id,))
    course_id = cursor.fetchall()
    print(course_id)
    for id in course_id:
        sql = "SELECT CourseName From Course Where CourseID = %s "
        cursor.execute(sql, (id,))
        course_name = cursor.fetchall()
        for name in course_name:
            course_listbox.insert(tk.END, f"{id[0]} {name[0]}")

#获取学生当前所有作业
def getAssignment(course_id):
    cursor.execute("SELECT * FROM assignment WHERE CourseID = %s", (course_id,))
    assignments = cursor.fetchall()
    return assignments

def get_submitted_assignments(student_id, assignment_id):
    cursor.execute("SELECT * FROM submithomework WHERE StudentID = %s AND id = %s", (student_id, assignment_id))
    submitted_assignments = cursor.fetchall()
    return submitted_assignments

def get_teacher_id(assignment_id):
    # 查询教师ID
    sql = "SELECT TeacherID FROM assignment WHERE id = %s"
    cursor.execute(sql, (assignment_id,))
    teacher_id = cursor.fetchone()[0]
    return teacher_id

def submit_homework():
    selected_items = tree.selection()
    if selected_items:
        for selected_item in selected_items:
            # 获取选中的作业信息
            item = tree.item(selected_item)
            values = item['values']
            assignment_id = values[0]  # 作业号
            requirement = values[1]  # 作业内容

            # 弹出对话框让学生输入作业内容
            submit_window = tk.Toplevel(window2)
            submit_window.title("提交作业")

            # 创建作业内容文本框
            content_label = tk.Label(submit_window, text="作业内容")
            content_label.pack()
            content_textbox = tk.Text(submit_window, height=10, width=50)
            content_textbox.pack()

            # 创建提交按钮
            def submit_assignment():
                # 获取学生ID和课程ID
                student_id = cs.student_id
                course_id = course_listbox.get(course_listbox.curselection()).split()[0]

                # 获取作业内容
                content = content_textbox.get("1.0", tk.END).strip()
                teacher_id=get_teacher_id(assignment_id)
                # 将作业信息插入到数据库表中
                sql = "INSERT INTO submithomework (id, StudentID, CourseID, submitime, content, TeacherID) VALUES (%s, %s, %s, CURDATE(), %s, %s)"
                values = (assignment_id, student_id, course_id, content, teacher_id)
                cursor.execute(sql, values)
                connection.commit()

                messagebox.showinfo("提交成功", "作业已成功提交。")

                # 清除已提交的作业
                tree.delete(selected_item)

                submit_window.destroy()

            submit_button = tk.Button(submit_window, text="提交", command=submit_assignment)
            submit_button.pack(pady=10)

    else:
        messagebox.showwarning("未选中作业", "请先选中要提交的作业。")

def show_assignments(event):
    selected_item = course_listbox.get(course_listbox.curselection())
    course_id = selected_item.split()[0][:5]
    student_id = cs.student_id
    tree.delete(*tree.get_children())  # 清除之前的作业列表
    assignments = getAssignment(course_id)
    for assignment in assignments:
        assignment_id = assignment[0]
        requirement = assignment[3]
        '''添加是否提交'''
        # 检查学生是否已提交该作业
        submitted_assignments = get_submitted_assignments(student_id, assignment_id)
        if submitted_assignments:
            submitted = "已提交"
        else:
            submitted = "未提交"

        tree.insert("", tk.END, values=(assignment_id, requirement, submitted))


def view_submitted_homework():
    # 创建窗口
    submitted_window = tk.Toplevel(window2)
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
    submitted_tree.heading("3", text="教师ID")

    submitted_tree.pack()

    # 查询已提交作业
    student_id = cs.student_id
    sql = "SELECT id, content, TeacherID FROM submithomework WHERE StudentID = %s"
    cursor.execute(sql, (student_id,))
    submitted_assignments = cursor.fetchall()

    # 在作业列表中显示已提交作业
    for assignment in submitted_assignments:
        assignment_id = assignment[0]
        content = assignment[1]
        teacher_id = assignment[2]
        submitted_tree.insert("", tk.END, values=(assignment_id, content, teacher_id))

    # 创建下载按钮和相关函数
    def download_assignment():
        selected_item = submitted_tree.selection()
        if selected_item:
            item = submitted_tree.item(selected_item)
            values = item['values']
            assignment_id = values[0]
            content = values[1]

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



def submmit_button(currentStu,root):
    global cs
    cs = currentStu

    # 创建主窗口
    global window2
    window2 = Toplevel(root)
    window2.title("作业管理系统")
    global screen_width
    global screen_height
    screen_width = window2.winfo_screenwidth()
    screen_height = window2.winfo_screenheight()

    # 设置窗口的位置

    window_width = 500
    window_height = 400
    # 计算窗口在屏幕中的坐标位置
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # 设置窗口的位置
    window2.geometry("{}x{}+{}+{}".format(window_width, window_height, x, y))

    window2.resizable(False, False)

    background_image03 = PhotoImage(file="2222.png")  # 替换图片路径,像素大小500x375
    background_label03 = Label(window2, image=background_image03)
    background_label03.place(x=0, y=0, relwidth=1, relheight=1)

    # 创建课程列表框
    course_frame = tk.Frame(window2,bg='white')
    course_frame.place(relx=0.05,rely=0.1, relwidth=0.3, relheight=0.47)

    course_label = tk.Label(course_frame, text="课程列表",font=("华文新魏", 14),bg='white')
    course_label.place(relheight=0.1)

    global course_listbox
    course_listbox = tk.Listbox(course_frame, width=20)
    course_listbox.place(rely=0.1)
    get_courses(cs)
    course_listbox.bind("<<ListboxSelect>>", show_assignments)

    # 创建作业列表
    assignment_frame = tk.Frame(window2, bg='white')
    assignment_frame.place(relx=0.5, rely=0.1, relwidth=0.5, relheight=0.6)

    assignment_label = tk.Label(assignment_frame, text="作业列表",font=("华文新魏", 14),bg='white')
    assignment_label.place(relheight=0.1)

    global tree
    tree = ttk.Treeview(assignment_frame, columns=("1", "2", "3"), show="headings")
    # 设置列标题
    tree.column("1", width=30)
    tree.column("2", width=30)
    tree.column("3", width=30)

    tree.heading("1", text="作业号")
    tree.heading("2", text="作业内容")
    tree.heading("3", text="是否提交")

    tree.place(rely=0.1, relwidth=1, relheight=0.7)

    # 创建提交作业按钮
    submit_button = tk.Button(window2, text="提交作业", command=submit_homework)
    submit_button.place(relx=0.5,rely=0.6, relwidth=0.4, relheight=0.05)

    # 创建查看已提交作业按钮
    view_button = tk.Button(window2, text="查看已提交作业", command=view_submitted_homework)
    view_button.place(relx=0.8, rely=0.02, relheight=0.05)


    # 主事件循环
    window2.mainloop()

    # 关闭数据库连接
    connection.close()


