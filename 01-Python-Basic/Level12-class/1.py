class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def introduce(self):
        print(f"我是{self.name}，今年{self.age}岁" )


student1 = Student("小明", 20)
student2 = Student("小红", 21)

student1.introduce()
student2.introduce()