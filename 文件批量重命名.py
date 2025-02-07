import os
import tkinter as tk
from tkinter import filedialog, messagebox
import webbrowser

def create_main_window():
    # 创建主窗口
    root = tk.Tk()
    root.title("批量文件重命名工具")
    root.geometry("540x600")

    # 创建选择文件夹或文件的按钮
    btn_select_folder = tk.Button(root, text="选择文件夹", command=select_folder)
    btn_select_folder.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

    btn_select_files = tk.Button(root, text="选择文件", command=select_files)
    btn_select_files.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

    # 创建显示当前名称的文本框
    label_current_names = tk.Label(root, text="当前名称:")
    label_current_names.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

    global current_names_text
    current_names_text = tk.Text(root, height=30, width=35)
    current_names_text.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

    # 创建输入新名称的文本框
    label_new_names = tk.Label(root, text="新名称 (每行对应一个文件):")
    label_new_names.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)

    global new_names_text
    new_names_text = tk.Text(root, height=30, width=35)
    new_names_text.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)

    # 绑定粘贴事件
    new_names_text.bind("<Control-v>", add_sequence_numbers)

    # 添加显示或隐藏序号的复选框
    global show_sequence_var
    show_sequence_var = tk.BooleanVar(value=False)
    chk_show_sequence = tk.Checkbutton(root, text="添加序号(需重新选择)", variable=show_sequence_var, command=lambda: display_items(items, base_path_var))
    chk_show_sequence.grid(row=3, column=0, columnspan=2, pady=5, sticky=tk.W)

    # 添加修改后缀名的复选框
    global modify_extension_var
    modify_extension_var = tk.BooleanVar(value=False)
    chk_modify_extension = tk.Checkbutton(root, text="不修改后缀名(需重新选择)", variable=modify_extension_var, command=lambda: display_items(items, base_path_var))
    chk_modify_extension.grid(row=4, column=0, columnspan=2, pady=5, sticky=tk.W)

    # 添加带有链接的文字
    link_label = tk.Label(root, text="打开百度翻译", fg="blue", cursor="hand2")
    link_label.grid(row=5, column=0, columnspan=2, pady=5)
    link_label.bind("<Button-1>", lambda e: webbrowser.open("https://fanyi.baidu.com/mtpe-individual/multimodal?aldtype=16047&ext_channel=Aldtype#/auto/zh"))

    # 创建确认按钮
    btn_rename = tk.Button(root, text="确认重命名", command=rename_items)
    btn_rename.grid(row=6, column=0, columnspan=2, pady=10)

    # 添加底部居中的灰色小字
    footer_label = tk.Label(root, text="zhufengque", fg="gray")
    footer_label.grid(row=7, column=0, columnspan=2, pady=5, sticky=tk.S)

    return root

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        items = os.listdir(folder_path)
        display_items(items, folder_path)

def select_files():
    file_paths = filedialog.askopenfilenames()
    if file_paths:
        items = [os.path.basename(path) for path in file_paths]
        base_path = os.path.dirname(file_paths[0])  # 获取文件所在目录
        display_items(items, base_path)

def display_items(items, base_path):
    current_names_text.delete(1.0, tk.END)
    new_names_text.delete(1.0, tk.END)
    for index, item in enumerate(items, start=1):
        if modify_extension_var.get():
            item_name, item_ext = os.path.splitext(item)
            if show_sequence_var.get():
                current_names_text.insert(tk.END, f"{index}. {item_name}\n")
                new_names_text.insert(tk.END, f"{index}. \n")
            else:
                current_names_text.insert(tk.END, f"{item_name}\n")
                new_names_text.insert(tk.END, f"\n")
        else:
            if show_sequence_var.get():
                current_names_text.insert(tk.END, f"{index}. {item}\n")
                new_names_text.insert(tk.END, f"{index}. \n")
            else:
                current_names_text.insert(tk.END, f"{item}\n")
                new_names_text.insert(tk.END, f"\n")
    global base_path_var
    base_path_var = base_path

def add_sequence_numbers(event):
    # 获取粘贴的内容
    pasted_text = root.clipboard_get()
    lines = pasted_text.strip().split("\n")
    new_text = ""
    for index, line in enumerate(lines, start=1):
        if show_sequence_var.get():
            new_text += f"{index}. {line}\n"
        else:
            new_text += f"{line}\n"
    new_names_text.delete(1.0, tk.END)
    new_names_text.insert(tk.END, new_text)

def rename_items():
    current_names = current_names_text.get(1.0, tk.END).strip().split("\n")
    new_names = new_names_text.get(1.0, tk.END).strip().split("\n")

    if len(current_names) != len(new_names):
        messagebox.showerror("错误", "当前名称和新名称的数量不匹配")
        return

    success_count = 0
    error_messages = []

    for old_name, new_name in zip(current_names, new_names):
        if show_sequence_var.get():
            old_name = old_name.split(". ", 1)[1]  # 去掉序号
            new_name = new_name.split(". ", 1)[1]  # 去掉序号

        if modify_extension_var.get():
            old_name_with_ext, old_ext = os.path.splitext(old_name)
            new_name_with_ext = new_name + old_ext
            old_path = os.path.join(base_path_var, old_name_with_ext + old_ext)
            new_path = os.path.join(base_path_var, new_name_with_ext)
        else:
            old_path = os.path.join(base_path_var, old_name)
            new_path = os.path.join(base_path_var, new_name)

        # 确保路径是Unicode字符串
        old_path = os.path.normpath(old_path)
        new_path = os.path.normpath(new_path)

        # 检查路径是否存在
        if not os.path.exists(old_path):
            error_messages.append(f"路径 {old_path} 不存在")
            continue

        try:
            os.rename(old_path, new_path)
            success_count += 1
        except Exception as e:
            error_messages.append(f"重命名 {old_name} 到 {new_name} 失败: {e}")

    if success_count > 0:
        messagebox.showinfo("成功", f"成功重命名 {success_count} 个文件")
    if error_messages:
        error_message = "\n".join(error_messages)
        messagebox.showerror("错误", f"部分文件重命名失败:\n{error_message}")

if __name__ == "__main__":
    base_path_var = ""
    root = create_main_window()
    root.mainloop()