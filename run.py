import json
import tkinter as tk
from tkinter import ttk

from support.attributerow import AttributeRow

class RelicApp:
    def __init__(self, root):
        self.widget = None
        self.deputy_attribute_vars = None
        self.main_attribute_vars = None
        self.copy_button = None
        self.item_button = None
        self.command_text = None
        self.part_mapping = None
        self.relic_sets = None
        self.level_combobox = None
        self.level_var = None
        self.part_combobox = None
        self.part_var = None
        self.set_combobox = None
        self.set_var = None
        self.category_combobox = None
        self.category_var = None
        self.entry_title_widgets = []
        self.entry_widgets = []
        self.attribute_widgets = []
        self.root = root
        self.root.title("快键指令生成")
        self.root.geometry("850x600")

        # 配置网格布局
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # 创建自定义菜单栏
        self.menubar = tk.Frame(root, bg="lightgray", height=30)
        self.menubar.grid(row=0, column=0, sticky="ew")

        # 创建界面框架
        self.relic_frame = self.create_frame("")

        # 添加菜单项
        self.create_menu_button("遗器", self.show_relic)

        # 读取 JSON 文件
        self.relics_data = self.load_json('data/relic/relics.json')
        self.ornaments_data = self.load_json('data/relic/ornaments.json')
        self.relics_entry_host_data = self.load_json('data/relic/entry/host/relics.json')
        self.ornaments_entry_host_data = self.load_json('data/relic/entry/host/ornaments.json')
        self.entry_deputy_data = self.load_json('data/relic/entry/deputy.json')

        # 初始化遗器界面
        self.init_relic_interface()

    def create_frame(self, text):
        frame = ttk.Frame(self.root)
        frame.grid(row=1, column=0, sticky="nsew")
        label = ttk.Label(frame, text=text, font=("Arial", 24))
        label.pack(pady=100)
        return frame

    def create_menu_button(self, text, command):
        button = tk.Button(
            self.menubar,
            text=text,
            font=("Arial", 12),
            width=10,
            bg="lightgray",
            fg="black",
            relief="flat",
            command=command,
        )
        button.pack(side="left", padx=5, pady=2)

    def show_relic(self):
        self.relic_frame.tkraise()

    @staticmethod
    def load_json(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def init_relic_interface(self):
        # 类别选择框
        self.category_var = tk.StringVar()
        self.category_combobox = ttk.Combobox(
            self.relic_frame,
            textvariable=self.category_var,
            values=["隧洞遗器", "位面饰品"],
            state="readonly",
            font=("Arial", 12),
            width=8,
        )
        self.category_combobox.place(x=50, y=20)
        self.category_combobox.bind("<<ComboboxSelected>>", self.update_set_combobox)

        # 套装选择框
        self.set_var = tk.StringVar()
        self.set_combobox = ttk.Combobox(
            self.relic_frame,
            textvariable=self.set_var,
            values=["请选择"],
            state="readonly",
            font=("Arial", 12),
            width=15,
        )
        self.set_combobox.place(x=200, y=20)
        self.set_combobox.bind("<<ComboboxSelected>>", self.update_part_combobox)

        # 部位选择框
        self.part_var = tk.StringVar()
        self.part_combobox = ttk.Combobox(
            self.relic_frame,
            textvariable=self.part_var,
            values=["请选择"],
            state="disabled",
            font=("Arial", 12),
            width=8,
        )
        self.part_combobox.place(x=420, y=20)
        self.part_combobox.bind("<<ComboboxSelected>>", self.create_attribute_widgets)

        # 等级选择框
        self.level_var = tk.StringVar()
        self.level_combobox = ttk.Combobox(
            self.relic_frame,
            textvariable=self.level_var,
            values=[str(i) for i in range(16)],
            state="readonly",
            font=("Arial", 12),
            width=4,
        )
        self.level_combobox.place(x=570, y=20)
        self.level_var.set('0')

        # 类别与套装的映射关系
        self.relic_sets = {
            "隧洞遗器": list(self.relics_data.keys()),
            "位面饰品": list(self.ornaments_data.keys()),
        }

        # 类别与部位的映射关系
        self.part_mapping = {
            "隧洞遗器": ["头部", "手部", "躯干", "脚部"],
            "位面饰品": ["位面球", "连结绳"],
        }

        # 创建 Text 组件用于显示命令
        self.command_text = tk.Text(self.relic_frame, height=1, width=30, font=("Arial", 12))
        self.command_text.place(x=40, y=480)

        # 创建获取物品 ID 按钮
        self.item_button = tk.Button(self.relic_frame, text="生成命令", command=self.get_command)
        self.item_button.place(x=440, y=520)

        # 创建复制按钮
        self.copy_button = tk.Button(self.relic_frame, text="复制命令", command=self.copy_to_clipboard)
        self.copy_button.place(x=570, y=520)

    def update_set_combobox(self, event):
        selected_category = self.category_var.get()
        if selected_category in self.relic_sets:
            self.set_combobox["values"] = ["请选择"] + self.relic_sets[selected_category]
            self.set_combobox.current(0)
            self.update_part_combobox()
        else:
            self.set_combobox["values"] = ["请选择"]
            self.update_part_combobox()

    def update_part_combobox(self, event=None):
        selected_set = self.set_var.get()
        selected_category = self.category_var.get()
        if selected_category in self.part_mapping and selected_set != "请选择":
            self.part_combobox["values"] = ["请选择"] + self.part_mapping[selected_category]
            self.part_combobox.current(0)
            self.part_combobox.config(state="readonly")
        else:
            self.part_combobox["values"] = ["请选择"]
            self.part_combobox.current(0)
            self.part_combobox.config(state="disabled")

    def create_attribute_widgets(self, event):
        for widget in self.entry_widgets:
            widget.destroy()
        self.entry_widgets.clear()

        for widget in self.entry_title_widgets:
            if widget is not None:  # 增加类型检查
                widget.destroy()
        self.entry_title_widgets.clear()

        category = self.category_var.get()
        selected_part = self.part_var.get()

        if category in ["隧洞遗器", "位面饰品"] and selected_part not in ["", "请选择"]:
            self.create_main_attribute_widgets(category, selected_part)
            self.create_deputy_attribute_widgets()

    def create_main_attribute_widgets(self, category, selected_part):
        attributes = self.relics_entry_host_data.get(selected_part, {}) if category == "隧洞遗器" else self.ornaments_entry_host_data.get(selected_part, {})
        self.entry_title_widgets.append(ttk.Label(self.relic_frame, text="主属性", font=("Arial", 20)).place(x=120, y=50))

        self.main_attribute_vars = []
        for index, (attribute, value) in enumerate(attributes.items()):
            var = tk.IntVar()
            self.main_attribute_vars.append(var)
            widget = AttributeRow(self.relic_frame, attribute, 60, 90 + index * 30, var, self.main_attribute_vars)
            self.entry_widgets.append(widget.label)
            self.entry_widgets.append(widget.checkbox)
            self.attribute_widgets.append(widget)

    def create_deputy_attribute_widgets(self):
        deputy_attributes = list(self.entry_deputy_data.keys())
        self.entry_title_widgets.append(ttk.Label(self.relic_frame, text="副属性", font=("Arial", 20)).place(x=420, y=50))

        self.deputy_attribute_vars = []
        for index, attribute in enumerate(deputy_attributes):
            var = tk.IntVar()
            self.deputy_attribute_vars.append(var)
            widget = AttributeRow(
                self.relic_frame, attribute, 360, 90 + index * 30, var, self.deputy_attribute_vars,
                is_main_attribute=True, limit=4
            )
            self.entry_widgets.append(widget.label)
            self.entry_widgets.append(widget.entry)
            self.entry_widgets.append(widget.add_button)
            self.entry_widgets.append(widget.subtract_button)
            self.entry_widgets.append(widget.checkbox)
            self.attribute_widgets.append(widget)

    def get_selected_attributes(self):
        selected_attributes = [widget.get_h() for widget in self.attribute_widgets if widget.var.get() == 1]
        print(selected_attributes)

    def get_command(self):
        category = self.category_var.get()
        selected_set = self.set_var.get()
        selected_part = self.part_var.get()
        selected_level = self.level_var.get()

        if category == "隧洞遗器":
            relic_data = self.relics_data
            relic_entry_data = self.relics_entry_host_data

        if category == "位面饰品":
            relic_data = self.ornaments_data
            relic_entry_data = self.ornaments_entry_host_data

        if selected_set in relic_data and selected_part in relic_data[selected_set]:
            item_id = relic_data[selected_set][selected_part]
            host_name_l = [widget.get_h() for widget in self.attribute_widgets if widget.var.get() == 1 and not widget.is_main_attribute]
            if len(host_name_l) == 0:
                command = f"/give {item_id}"
                self.command_text.delete(1.0, tk.END)
                self.command_text.insert(tk.END, command)
                return command
            else:
                entry_id = relic_entry_data[selected_part][host_name_l[0]]
                deputy_name_l = [widget.get_o() for widget in self.attribute_widgets if widget.var.get() == 1 and widget.is_main_attribute]
                if len(deputy_name_l) == 0:
                    command = f"/relic {item_id} l{selected_level} {entry_id}"
                    self.command_text.delete(1.0, tk.END)
                    self.command_text.insert(tk.END, command)
                    return command
                elif  0 < len(deputy_name_l) <= 4:
                    command = f"/relic {item_id} l{selected_level} {entry_id}"
                    for _ in range(1, len(deputy_name_l) + 1):
                        t, n = deputy_name_l[_-1]
                        command += f" {self.entry_deputy_data[t]}:{n}"
                    self.command_text.delete(1.0, tk.END)
                    self.command_text.insert(tk.END, command)
                    return command

    def copy_to_clipboard(self):
        command = self.command_text.get(1.0, tk.END).strip()
        if command:
            self.root.clipboard_clear()
            self.root.clipboard_append(command)
            print(f"命令已复制到剪贴板: {command}")

if __name__ == "__main__":
    r = tk.Tk()
    app = RelicApp(r)
    r.mainloop()