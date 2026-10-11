def show_title():
    print("====== 学生成绩管理系统 ======")
def show_students(students, scores):
    for i in range(len(students)):
        if scores[i] >= 60:
            print(f"{students[i]}：{scores[i]}（及格）")
        else:
            print(f"{students[i]}：{scores[i]}（不及格）")
show_title()
students = ["张三", "李四", "王五"]
scores = [88, 45, 76]
show_students(students, scores)