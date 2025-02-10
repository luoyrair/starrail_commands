import tkinter as tk
from tkinter import ttk

class AttributeRow:
    def __init__(self, parent, attribute, x, y, var, vars_list, is_main_attribute=False, limit=None):
        self.o = None
        self.h = None
        self.subtract_button = None
        self.add_button = None
        self.entry = None
        self.checkbox = None
        self.label = None
        self.parent = parent
        self.attribute = attribute
        self.x = x
        self.y = y
        self.var = var
        self.vars_list = vars_list
        self.limit = limit
        self.is_main_attribute = is_main_attribute

        self.create_widgets()

    def create_widgets(self):
        # 创建标签
        self.label = ttk.Label(self.parent, text=self.attribute)
        self.label.place(x=self.x, y=self.y)

        # 创建复选框
        self.checkbox = tk.Checkbutton(
            self.parent, variable=self.var,
            command=lambda: self.single_select() if self.limit is None else self.limit_selection()
        )
        self.checkbox.place(x=self.x - 30, y=self.y)

        # 如果是副属性，添加输入框和加减按钮
        if self.is_main_attribute:
            self.entry = ttk.Entry(self.parent, width=5)
            self.entry.place(x=self.x + 100, y=self.y)
            self.entry.insert(0, "1")
            self.entry.bind("<Return>", self.update_value)

            self.add_button = tk.Button(self.parent, text="+", command=self.increment_value)
            self.add_button.place(x=self.x + 150, y=self.y)

            self.subtract_button = tk.Button(self.parent, text="-", command=self.decrement_value)
            self.subtract_button.place(x=self.x + 180, y=self.y)

    def increment_value(self):
        current_value = self.entry.get()
        if current_value.isdigit():
            self.entry.delete(0, tk.END)
            self.entry.insert(0, str(int(current_value) + 1))
        if self.var.get() == 1:  # 检查复选框是否被选中
            value_tuple = self.get_value_tuple()
            self.o = value_tuple  # 保存

    def decrement_value(self):
        current_value = self.entry.get()
        if current_value.isdigit() and int(current_value) > 0:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, str(int(current_value) - 1))
        if self.var.get() == 1:  # 检查复选框是否被选中
            value_tuple = self.get_value_tuple()
            self.o = value_tuple  # 保存

    def update_value(self, event):
        current_value = self.entry.get()
        if current_value.isdigit():
            # 这里可以添加对值的限制，例如最大值等
            self.entry.delete(0, tk.END)
            self.entry.insert(0, str(int(current_value)))
        if self.var.get() == 1:  # 检查复选框是否被选中
            value_tuple = self.get_value_tuple()
            self.o = value_tuple  # 保存

    def single_select(self):
        for var in self.vars_list:
            if var != self.var:
                var.set(0)
        if self.var.get() == 1:  # 检查复选框是否被选中
            value_tuple = self.get_tuple()
            self.h = value_tuple  # 保存

    def limit_selection(self):
        if sum(var.get() for var in self.vars_list) > self.limit:
            self.var.set(0)
        if self.var.get() == 1:  # 检查复选框是否被选中
            value_tuple = self.get_value_tuple()
            self.o = value_tuple  # 保存

    def get_tuple(self):
        """获取当前标签文本"""
        label_text = self.label.cget("text")  # 获取标签的文本
        return label_text

    def get_value_tuple(self):
        """获取当前标签文本和输入框内容的元组"""
        label_text = self.label.cget("text")  # 获取标签的文本
        entry_value = self.entry.get()  # 获取输入框的内容
        return label_text, entry_value

    def get_h(self):
        return self.h

    def get_o(self):
        """获取当前的元组"""
        return self.o