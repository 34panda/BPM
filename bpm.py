import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


class BlenderProject(Base):
    __tablename__ = 'blender_projects'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String)
    is_finished = Column(Boolean, nullable=False, default=False)

    paths = relationship('Path', back_populates='project', cascade="all, delete-orphan")
    dates = relationship('Date', back_populates='project', cascade="all, delete-orphan")


class Path(Base):
    __tablename__ = 'paths'

    id = Column(Integer, primary_key=True, autoincrement=True)
    file_name = Column(String)
    path = Column(String)
    project_id = Column(Integer, ForeignKey('blender_projects.id'))

    project = relationship('BlenderProject', back_populates='paths')


class Date(Base):
    __tablename__ = 'dates'

    id = Column(Integer, primary_key=True, autoincrement=True)
    start_date = Column(String)
    finish_date = Column(String)
    project_id = Column(Integer, ForeignKey('blender_projects.id'))

    project = relationship('BlenderProject', back_populates='dates')


# Database setup
engine = create_engine('sqlite:///blender_projects.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Blender Projects Manager")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.project_frame = ttk.Frame(self.notebook)
        self.path_frame = ttk.Frame(self.notebook)
        self.date_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.project_frame, text="Projects")
        self.notebook.add(self.path_frame, text="Paths")
        self.notebook.add(self.date_frame, text="Dates")

        self.create_project_widgets()
        self.create_path_widgets()
        self.create_date_widgets()

    def create_project_widgets(self):
        self.project_tree = ttk.Treeview(self.project_frame, columns=("ID", "Name", "Description", "Is Finished"),
                                         show='headings')
        self.project_tree.heading("ID", text="ID")
        self.project_tree.heading("Name", text="Name")
        self.project_tree.heading("Description", text="Description")
        self.project_tree.heading("Is Finished", text="Is Finished")
        self.project_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.populate_project_tree()

        self.project_name_var = tk.StringVar()
        self.project_description_var = tk.StringVar()
        self.project_is_finished_var = tk.BooleanVar()

        self.project_label_name = ttk.Label(self.project_frame, text="Name:")
        self.project_label_name.pack(pady=5)
        self.project_entry_name = ttk.Entry(self.project_frame, textvariable=self.project_name_var)
        self.project_entry_name.pack(pady=5)

        self.project_label_description = ttk.Label(self.project_frame, text="Description:")
        self.project_label_description.pack(pady=5)
        self.project_entry_description = ttk.Entry(self.project_frame, textvariable=self.project_description_var)
        self.project_entry_description.pack(pady=5)

        self.project_check_is_finished = ttk.Checkbutton(self.project_frame, text="Is Finished",
                                                         variable=self.project_is_finished_var)
        self.project_check_is_finished.pack(pady=5)

        self.project_button_add = ttk.Button(self.project_frame, text="Add Project", command=self.add_project)
        self.project_button_add.pack(pady=5)
        self.project_button_update = ttk.Button(self.project_frame, text="Update Project", command=self.update_project)
        self.project_button_update.pack(pady=5)
        self.project_button_delete = ttk.Button(self.project_frame, text="Delete Project", command=self.delete_project)
        self.project_button_delete.pack(pady=5)

        self.project_tree.bind('<ButtonRelease-1>', self.select_project_item)

    def create_path_widgets(self):
        self.path_tree = ttk.Treeview(self.path_frame, columns=("ID", "File Name", "Path", "Project ID"),
                                      show='headings')
        self.path_tree.heading("ID", text="ID")
        self.path_tree.heading("File Name", text="File Name")
        self.path_tree.heading("Path", text="Path")
        self.path_tree.heading("Project ID", text="Project ID")
        self.path_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.populate_path_tree()

        self.path_file_name_var = tk.StringVar()
        self.path_path_var = tk.StringVar()
        self.path_project_id_var = tk.IntVar()

        self.path_label_file_name = ttk.Label(self.path_frame, text="File Name:")
        self.path_label_file_name.pack(pady=5)
        self.path_entry_file_name = ttk.Entry(self.path_frame, textvariable=self.path_file_name_var)
        self.path_entry_file_name.pack(pady=5)

        self.path_label_path = ttk.Label(self.path_frame, text="Path:")
        self.path_label_path.pack(pady=5)
        self.path_entry_path = ttk.Entry(self.path_frame, textvariable=self.path_path_var)
        self.path_entry_path.pack(pady=5)

        self.path_label_project_id = ttk.Label(self.path_frame, text="Project ID:")
        self.path_label_project_id.pack(pady=5)
        self.path_entry_project_id = ttk.Entry(self.path_frame, textvariable=self.path_project_id_var)
        self.path_entry_project_id.pack(pady=5)

        self.path_button_add = ttk.Button(self.path_frame, text="Add Path", command=self.add_path)
        self.path_button_add.pack(pady=5)
        self.path_button_update = ttk.Button(self.path_frame, text="Update Path", command=self.update_path)
        self.path_button_update.pack(pady=5)
        self.path_button_delete = ttk.Button(self.path_frame, text="Delete Path", command=self.delete_path)
        self.path_button_delete.pack(pady=5)

        self.path_tree.bind('<ButtonRelease-1>', self.select_path_item)

    def create_date_widgets(self):
        self.date_tree = ttk.Treeview(self.date_frame, columns=("ID", "Start Date", "Finish Date", "Project ID"),
                                      show='headings')
        self.date_tree.heading("ID", text="ID")
        self.date_tree.heading("Start Date", text="Start Date")
        self.date_tree.heading("Finish Date", text="Finish Date")
        self.date_tree.heading("Project ID", text="Project ID")
        self.date_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.populate_date_tree()

        self.date_start_date_var = tk.StringVar()
        self.date_finish_date_var = tk.StringVar()
        self.date_project_id_var = tk.IntVar()

        self.date_label_start_date = ttk.Label(self.date_frame, text="Start Date:")
        self.date_label_start_date.pack(pady=5)
        self.date_entry_start_date = ttk.Entry(self.date_frame, textvariable=self.date_start_date_var)
        self.date_entry_start_date.pack(pady=5)

        self.date_label_finish_date = ttk.Label(self.date_frame, text="Finish Date:")
        self.date_label_finish_date.pack(pady=5)
        self.date_entry_finish_date = ttk.Entry(self.date_frame, textvariable=self.date_finish_date_var)
        self.date_entry_finish_date.pack(pady=5)

        self.date_label_project_id = ttk.Label(self.date_frame, text="Project ID:")
        self.date_label_project_id.pack(pady=5)
        self.date_entry_project_id = ttk.Entry(self.date_frame, textvariable=self.date_project_id_var)
        self.date_entry_project_id.pack(pady=5)

        self.date_button_add = ttk.Button(self.date_frame, text="Add Date", command=self.add_date)
        self.date_button_add.pack(pady=5)
        self.date_button_update = ttk.Button(self.date_frame, text="Update Date", command=self.update_date)
        self.date_button_update.pack(pady=5)
        self.date_button_delete = ttk.Button(self.date_frame, text="Delete Date", command=self.delete_date)
        self.date_button_delete.pack(pady=5)

        self.date_tree.bind('<ButtonRelease-1>', self.select_date_item)

    def populate_project_tree(self):
        for i in self.project_tree.get_children():
            self.project_tree.delete(i)
        projects = session.query(BlenderProject).all()
        for project in projects:
            self.project_tree.insert('', 'end',
                                     values=(project.id, project.name, project.description, project.is_finished))

    def populate_path_tree(self):
        for i in self.path_tree.get_children():
            self.path_tree.delete(i)
        paths = session.query(Path).all()
        for path in paths:
            self.path_tree.insert('', 'end', values=(path.id, path.file_name, path.path, path.project_id))

    def populate_date_tree(self):
        for i in self.date_tree.get_children():
            self.date_tree.delete(i)
        dates = session.query(Date).all()
        for date in dates:
            self.date_tree.insert('', 'end', values=(date.id, date.start_date, date.finish_date, date.project_id))

    def add_project(self):
        name = self.project_name_var.get()
        description = self.project_description_var.get()
        is_finished = self.project_is_finished_var.get()
        if name:
            new_project = BlenderProject(name=name, description=description, is_finished=is_finished)
            session.add(new_project)
            session.commit()
            self.populate_project_tree()
        else:
            messagebox.showerror("Error", "Name cannot be empty")

    def update_project(self):
        selected_item = self.project_tree.selection()[0]
        item = self.project_tree.item(selected_item)
        project_id = item['values'][0]
        project = session.query(BlenderProject).filter_by(id=project_id).first()
        project.name = self.project_name_var.get()
        project.description = self.project_description_var.get()
        project.is_finished = self.project_is_finished_var.get()
        session.commit()
        self.populate_project_tree()

    def delete_project(self):
        selected_item = self.project_tree.selection()[0]
        item = self.project_tree.item(selected_item)
        project_id = item['values'][0]
        project = session.query(BlenderProject).filter_by(id=project_id).first()
        session.delete(project)
        session.commit()
        self.populate_project_tree()

    def select_project_item(self, event):
        selected_item = self.project_tree.selection()[0]
        item = self.project_tree.item(selected_item)
        self.project_name_var.set(item['values'][1])
        self.project_description_var.set(item['values'][2])
        self.project_is_finished_var.set(item['values'][3])

    def add_path(self):
        file_name = self.path_file_name_var.get()
        path = self.path_path_var.get()
        project_id = self.path_project_id_var.get()
        new_path = Path(file_name=file_name, path=path, project_id=project_id)
        session.add(new_path)
        session.commit()
        self.populate_path_tree()

    def update_path(self):
        selected_item = self.path_tree.selection()[0]
        item = self.path_tree.item(selected_item)
        path_id = item['values'][0]
        path = session.query(Path).filter_by(id=path_id).first()
        path.file_name = self.path_file_name_var.get()
        path.path = self.path_path_var.get()
        path.project_id = self.path_project_id_var.get()
        session.commit()
        self.populate_path_tree()

    def delete_path(self):
        selected_item = self.path_tree.selection()[0]
        item = self.path_tree.item(selected_item)
        path_id = item['values'][0]
        path = session.query(Path).filter_by(id=path_id).first()
        session.delete(path)
        session.commit()
        self.populate_path_tree()

    def select_path_item(self, event):
        selected_item = self.path_tree.selection()[0]
        item = self.path_tree.item(selected_item)
        self.path_file_name_var.set(item['values'][1])
        self.path_path_var.set(item['values'][2])
        self.path_project_id_var.set(item['values'][3])

    def add_date(self):
        start_date = self.date_start_date_var.get()
        finish_date = self.date_finish_date_var.get()
        project_id = self.date_project_id_var.get()
        new_date = Date(start_date=start_date, finish_date=finish_date, project_id=project_id)
        session.add(new_date)
        session.commit()
        self.populate_date_tree()

    def update_date(self):
        selected_item = self.date_tree.selection()[0]
        item = self.date_tree.item(selected_item)
        date_id = item['values'][0]
        date = session.query(Date).filter_by(id=date_id).first()
        date.start_date = self.date_start_date_var.get()
        date.finish_date = self.date_finish_date_var.get()
        date.project_id = self.date_project_id_var.get()
        session.commit()
        self.populate_date_tree()

    def delete_date(self):
        selected_item = self.date_tree.selection()[0]
        item = self.date_tree.item(selected_item)
        date_id = item['values'][0]
        date = session.query(Date).filter_by(id=date_id).first()
        session.delete(date)
        session.commit()
        self.populate_date_tree()

    def select_date_item(self, event):
        selected_item = self.date_tree.selection()[0]
        item = self.date_tree.item(selected_item)
        self.date_start_date_var.set(item['values'][1])
        self.date_finish_date_var.set(item['values'][2])
        self.date_project_id_var.set(item['values'][3])


if __name__ == "__main__":
    root = ThemedTk(theme="black")
    app = App(root)
    root.mainloop()
