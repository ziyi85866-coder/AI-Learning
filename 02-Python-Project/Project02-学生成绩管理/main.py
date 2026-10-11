# print("====== 学生成绩管理系统 ======")
# students = ["张三", "李四", "王五"]
# scores = [88, 45, 76]
# pass_count = 0
# for i in range(len(students)):
#     if scores[i] >= 60:
#         pass_count += 1
#         print(f"{students[i]}：{scores[i]}(及格)")
#     else:
#         print(f"{students[i]}：{scores[i]}(不及格)")
# print("及格人数：", pass_count)
# total = 0
# for score in scores:
#     total += score
# print("平均分：",total/len(scores))
# print("最高分：",max(scores))
# print("最低分：",min(scores))


def show_title():
    print("====== 学生成绩管理系统 ======")
def show_students(students, scores):
    for i in range(len(students)):
        if scores[i] >= 60:
            print(f"{students[i]}：{scores[i]}（及格）")
        else:
            print(f"{students[i]}：{scores[i]}（不及格）")

def show_average(scores):
    total = 0

    for score in scores:
        total += score

    print("平均分：", total / len(scores))

def show_statistics(scores):
    print("最高分：", max(scores))
    print("最低分：", min(scores))

def main():
    students = ["张三", "李四", "王五"]
    scores = [88, 45, 76]

    show_title()
    show_students(students, scores)
    show_average(scores)
    show_statistics(scores)

main()