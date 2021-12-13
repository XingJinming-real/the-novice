# serverComputer
import tkinter as tk
import tkinter.messagebox
import os
import re
import socket as sk
import threading

userName = 'David'
clientAddress = None
serverName = "localhost"
serverPort = 16888
clientName = 'Client2'
clientSocket = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)

FLAG = 0
flag = 0


def main():
    if not os.path.exists('password.txt'):
        f = open('password.txt', 'wt')
        f.write('admin,admin')
        f.close()
    window = tk.Tk()
    window.title('Log In')
    window.geometry('690x660')

    def view_it():
        tk.messagebox.showinfo(title='Be discreet', message=var_pw.get())
        pass

    def confirmServerName():
        global serverName
        tk.messagebox.showinfo(title='OK', message='confirmed!')
        serverName = t_serverName.get()

    tk.Label(window, bg='yellow', text='Welcome to the Chat-Program'.center(40)).pack()
    try:
        canvas = tk.Canvas(window, width=800, height=600)
        file_img = tk.PhotoImage(file='test.gif')
        canvas.create_image(0, 0, anchor='nw', image=file_img)
        canvas.pack()
    except:
        pass
    tk.Label(window, text='User name:').place(x=50, y=400)
    tk.Label(window, text='Password:').place(x=50, y=450)
    tk.Label(window, text='Host Ip:').place(x=50, y=500)
    tk.Button(window, text='View it', command=view_it).place(x=300, y=450)
    var_un = tk.StringVar()
    var_pw = tk.StringVar()
    var_un.set('Example@126.com')
    t_un = tk.Entry(window, textvariable=var_un)
    t_pw = tk.Entry(window, textvariable=var_pw, show='*')
    t_un.place(x=150, y=400)
    t_pw.place(x=150, y=450)
    var_serverName = tk.StringVar()
    var_serverName.set("请输入服务器的IP地址")
    t_serverName = tk.Entry(window, textvariable=var_serverName)
    t_serverName.place(x=150, y=500)
    serverNameButton = tk.Button(window, text='Confirm', command=confirmServerName)
    serverNameButton.place(x=300, y=500)

    def login():
        global clientName
        f = open('password.txt', 'rt')
        for i in f:
            info = i.split(',')
            user_name = info[0]
            keys[user_name] = info[1].strip('\n')
        if t_un.get() == '' or t_un.get() == 'Example@126.com':
            tk.messagebox.showwarning(title='Warning', message='Please input your account')
            f.close()
        elif t_un.get() not in keys.keys():
            k = tk.messagebox.askquestion(title='Warning', message='You have not signed up!\
     Sign up now?')
            if k == 'yes':
                sign_up()
                f.close()
            else:
                f.close()
                pass
        else:
            if not t_pw.get() == keys[t_un.get()]:
                tk.messagebox.showinfo(title='Warning', message='Password error')
                f.close()
            else:
                clientName = t_un.get()
                tk.messagebox.showinfo(title='Welcome', message='Logined')
                window.destroy()
                open_new()
                f.close()
        pass

    def open_new():
        window_new = tk.Tk()
        window_new.title('ChatRoom')
        window_new.geometry('400x600')
        varString = tk.StringVar()
        outPutTxt = tk.Text(window_new, width=54, height=400, bg='yellow')
        outPutTxt.place(x=0, y=0)
        inputTxt = tk.Text(window_new, width=400, height=200)
        inputTxt.place(x=0, y=400)
        menuBar = tk.Menu(window_new)

        def getInfo():
            while True:
                try:
                    message, serverAddress = clientSocket.recvfrom(9999)
                    outPutTxt.insert('end', message.decode())
                    outPutTxt.insert('end', '\n')
                except:
                    continue

        def sendInfo():
            global FLAG
            if FLAG == 0:
                message = clientName
                FLAG = 1
            else:
                varString.set(inputTxt.get(1.0, 'end'))
                inputTxt.delete(1.0, 'end')
                message = varString.get().strip('\n')
            clientSocket.sendto(message.encode(), (serverName, serverPort))

        def quitButton():
            tempKey = tk.messagebox.askyesno(title='Quit', message='Quit?')
            if tempKey:
                clientSocket.sendto((clientName + " has left").encode(), (serverName, serverPort))
                window_new.destroy()

        threadGet = threading.Thread(name='getInfo', target=getInfo)
        threadGet.start()
        global FLAG
        if not FLAG:
            sendInfo()
        scroll = tk.Scrollbar(window_new)
        scroll.config(command=outPutTxt.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        outPutTxt.config(yscrollcommand=scroll.set)
        menuBar.add_command(label='Quit', command=quitButton)
        sendButton = tk.Button(window_new, text='Send', command=sendInfo)
        sendButton.place(x=330, y=550)
        window_new.config(menu=menubar)
        window_new.mainloop()

    def sign_up():
        su_window = tk.Tk()
        su_window.title('Sign up')
        su_window.geometry('300x400')

        def direction():  # 待完善menubar
            tk.messagebox.showinfo(title='Help', message='Input randomly whatever you want !')
            pass

        def send_email():  # 待完善menubar
            tk.messagebox.showinfo(title='Send Email',
                                   message='Please send your problem to xjm0801@126.com for more help!')

        menubar = tk.Menu(su_window)
        help_menu = tk.Menu(menubar, tearoff=0)  # 待完善menubar
        menubar.add_cascade(label='Help', menu=help_menu)
        help_menu.add_command(label='Directions', command=direction)
        more_menu = tk.Menu(help_menu, tearoff=0)
        help_menu.add_cascade(label='More', menu=more_menu)
        more_menu.add_command(label='Send Email', command=send_email)
        help_menu.add_separator()
        help_menu.add_command(label='Exit', command=su_window.quit())
        su_window.config(menu=menubar)
        tk.Label(su_window, text='Your email address:').place(x=20, y=50)
        e_email = tk.Entry(su_window)
        e_email.place(x=140, y=50)
        tk.Label(su_window, text='Your password:').place(x=20, y=110)
        ps = tk.Entry(su_window)
        ps.place(x=140, y=110)
        tk.Label(su_window, text='Confirm password:').place(x=20, y=170)
        ps_confirm = tk.Entry(su_window)
        ps_confirm.place(x=140, y=170)
        flag = 0

        def sign_up_check():
            global userName, clientName
            if e_email.get() in keys.keys():
                tk.messagebox.showwarning(title='Warning', message='This account has already existed')
            if not re.match(r'\w+@\w{1,8}\.com', e_email.get()):
                tk.messagebox.showerror(title='Error', message='Please rectify the pattern of your email address!')
                su_window.destroy()
                sign_up()
            else:
                pass

            if not ps_confirm.get() == ps.get():
                tk.messagebox.showerror(title='Error', message='Please make sure your password is same!')
                su_window.destroy()
                sign_up()
            else:
                clientName = e_email.get()
                keys[e_email.get()] = ps_confirm.get()
                tk.messagebox.showinfo(title='Welcome', message='Welcome ' + e_email.get() + ' !')

                f = open('password.txt', 'at')
                f.write('\n')
                f.write(e_email.get() + ',' + ps.get())
                f.close()
                userName = e_email.get()
                open_new()
                su_window.destroy()
                window.destroy()

        def sign_over():
            global flag
            tk.messagebox.showinfo(title='ok', message='OK')
            with open('password.txt', 'at') as f:
                f.write('\n')
                f.write(e_email.get())
                f.write(',')
                f.write(ps.get())
                flag = 1
            su_window.quit()

        tk.Button(su_window, text="Confirm", command=sign_over).place(x=215, y=210)
        su_window.mainloop()
        if flag:
            sign_up_check()
            su_window.destroy()
            sign_up_check()
        else:
            tk.messagebox.showinfo(title='info', message='please click the sign up button to login')

        check_b = tk.Button(su_window, text='Sign up', bg='yellow', command=sign_up_check)
        check_b.place(x=220, y=350)
        pass

    keys = {}
    b_login = tk.Button(window, text='Log in', command=login)
    b_sign_up = tk.Button(window, text='Sign up', command=sign_up)
    b_login.place(x=560, y=520)
    b_sign_up.place(x=560, y=560)
    menubar = tk.Menu(window)

    def readMe():
        tk.messagebox.showwarning(title='Administrator', message='初次使用请输入服务器IP，默认为localhost\n请确保服务器已在运行\n'
                                                                 '管理员账户密码为\nadmin\nadmin')

    menubar.add_command(label='ReadMe', command=readMe)
    back_menu = tk.Menu(menubar, tearoff=0)  # 待完善menubar
    menubar.add_cascade(label='Back', menu=back_menu)

    def back_step():
        k = tk.messagebox.askquestion(title='Warning', message='Are you sure to quit out?')
        if k == 'yes':
            window.destroy()

    back_menu.add_command(label='Back to the previous step', command=back_step)
    window.config(menu=menubar)
    tk.messagebox.showinfo(title='Read Me', message="初次使用请先阅读左上角ReadMe")
    window.mainloop()


if __name__ == "__main__":
    main()
