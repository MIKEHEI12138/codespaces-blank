#contact
import tkinter as tk
import pymysql
import tkinter.ttk as ttk
import threading


# 连接数据库
connection = pymysql.connect(host='localhost', user='root', password='123456', db='teaching_cloud_platform',
                             charset='utf8mb4')

def getName():
    return cs.getStudent_name()
#对于messagetype 教师端显示3代表消息由教师发出，4代表消息由学生发出
def send_message(sender, receiver, message, messagetype):
    try:
        # 开始事务
        with connection.cursor() as cursor:
            # 插入消息到数据库
            sql = "INSERT INTO messages (sender, receiver, message, messagetype) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (sender, receiver, message, messagetype))

        # 提交事务
        connection.commit()

    except pymysql.Error as e:
        # 发生错误时回滚事务
        connection.rollback()
        print(f"发生错误：{e}")



def get_contacts():
    with connection.cursor() as cursor:
        # 查询联系人列表
        sql = "SELECT DISTINCT TeacherName FROM Teachers"
        cursor.execute(sql)
        contacts = cursor.fetchall()
        return contacts


def get_messages(sender, receiver):
    with connection.cursor() as cursor:
        connection.commit()
        # 查询消息
        sql = "SELECT sender, receiver, message,messagetype FROM messages WHERE (sender = %s AND receiver = %s) OR (sender = %s AND receiver = %s)"
        cursor.execute(sql, (sender, receiver, receiver, sender))
        messages = cursor.fetchall()
        return messages

def send_button_clicked():
    sender =getName()
    receiver = contacts_list.get(tk.ACTIVE)  # 接收者为选定的联系人
    message = message_entry.get()

    if message:
        # 发送消息
        send_message(sender, receiver, message,1)
        message_entry.delete(0, tk.END)
        update_message_list(receiver)

def update_message_list(receiver):
    sender =getName()

    # 获取消息列表
    messages = get_messages(sender, receiver)

    # 清空消息列表框
    message_list.delete(0, tk.END)

    # 更新消息列表框
    for message in messages:
        sender, receiver, message_text,messagetype= message
        if messagetype=='1':
            message_list.insert(tk.END,f'{sender}:')
            message_list.insert(tk.END,f'{message_text}')

        elif messagetype=='2':
            message_list.insert(tk.END,f'{sender}:')
            message_list.insert(tk.END, f'{message_text}')


def contact_selected(event):
    selected_contact = contacts_list.get(contacts_list.curselection())
    update_message_list(selected_contact)


def update_messages():
    selected_contact = contacts_list.get(tk.ACTIVE)
    update_message_list(selected_contact)
    window.after(2000, update_messages)#5秒一次更新


def contact_button(currentStu):
    #用于保存登录学生的信息
    global cs
    cs=currentStu
    # 创建主窗口
    global window
    window = tk.Tk()
    window.title("Chat Application")

    # 创建联系人列表框
    global contacts_list
    contacts_list = tk.Listbox(window)
    contacts_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    contacts_list.bind('<<ListboxSelect>>', contact_selected)

    # 创建消息列表框
    global message_list
    message_list = tk.Listbox(window)
    message_list.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # 创建滚动条
    scrollbar = tk.Scrollbar(message_list)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    message_list.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=message_list.yview)

    # 创建对话框
    global dialog_frame
    dialog_frame = tk.Frame(window)
    dialog_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # 创建消息输入框
    global message_entry
    message_entry = tk.Entry(dialog_frame)
    message_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # 创建发送按钮
    global send_button
    send_button = tk.Button(dialog_frame, text="Send", command=send_button_clicked)
    send_button.pack(side=tk.LEFT)

    # 获取联系人列表
    global contacts
    contacts = get_contacts()

    # 更新联系人列表框
    for contact in contacts:
        contacts_list.insert(tk.END, contact[0])

    # 开始主循环
    window.mainloop()

    # 关闭数据库连接
    connection.close()