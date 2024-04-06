class GradeSystem:
    def __init__(self):
        self.studentList = []
        self.weightList = ['0.1','0.1','0.1','0.3','0.4']
        self.gradeDistribution = {'A+': 0, 'A': 0, 'A-': 0, 'B+': 0, 'B': 0, 'B-': 0, 
                                  'C+': 0, 'C': 0, 'C-': 0, 'D': 0, 'E': 0}
        try:
            # Open file and read data
            with open('input.txt', 'r', encoding='utf-8') as fh:
                
                for line in fh.readlines():
                    tmp = line.split()
                    # Create a new Student object and append to studentList
                    tmpStudent = Student(tmp[0], tmp[1], tmp[2], tmp[3], tmp[4], tmp[5], tmp[6], self.weightList)
                    self.studentList.append(tmpStudent)
                    self.gradeDistribution[tmpStudent.letterGrade] += 1
        except FileNotFoundError:
            print("Error: File 'studentList.txt' not found.")
        except Exception as e:
            print("Error occurred while reading file:", e)

    def recalculateDistribution(self):
        # Reset all grade distribution counts to 0
        for grade in self.gradeDistribution:
            self.gradeDistribution[grade] = 0
        
        # Recalculate grade distribution based on student letter grades
        for student in self.studentList:
            self.gradeDistribution[student.letterGrade] += 1
        
    def addStudent(self, info):
        newInfo = info.split()
        tmpStudent = Student(newInfo[0],newInfo[1],newInfo[2],newInfo[3],newInfo[4],newInfo[5],newInfo[6],self.weightList)
        self.studentList.append(tmpStudent)
        self.gradeDistribution[tmpStudent.letterGrade] += 1
    
    def updateScore(self, info):
        newInfo = info.split()
        print(newInfo)
        for student in self.studentList:
            if student.sID == newInfo[0]:
                for i, j in enumerate(newInfo[1::2], start=1):  # Increment by 2
                    if j == 'final':
                        student.scores[4] = newInfo[i * 2]
                    elif j == 'midterm':
                        student.scores[3] = newInfo[i * 2]
                    else:
                        student.scores[int(j[-1]) - 1] = newInfo[i * 2]
                   
                    student.recalculate(self.weightList)
                    self.recalculateDistribution()
                    
    def updateWeight(self, info):
        newInfo = info.split()
        for i, j in enumerate(newInfo[::2], start=0):  # Increment by 2
            if j == 'final':
                self.weightList[4] = newInfo[i * 2 + 1]
            elif j == 'midterm':
                self.weightList[3] = newInfo[i * 2 + 1]
            else:
                self.weightList[int(j[-1]) - 1] = newInfo[i * 2 + 1]
        
        for student in self.studentList:
            student.recalculate(self.weightList)
        self.recalculateDistribution()
        
    def showScore(self, sID):
        found = False
        for student in self.studentList:
            if student.sID == sID:
                print("\nLab Scores:", student.scores[:3])
                print("Midterm Score:", student.scores[3])
                print("Final Score:", student.scores[4],'\n')
                found = True
                break
        
        if not found:
            print(f"Student with ID {sID} not found.")
            
    def showLetterGrade(self, sID):
        found = False
        for student in self.studentList:
            if student.sID == sID:
                print("\nLetter Grade:", student.letterGrade,'\n')
                found = True
                break
        if not found:
            print(f"Student with ID {sID} not found.")
            
    def showAverage(self, sID):
        found = False
        for student in self.studentList:
            if student.sID == sID:
                print("\nAverage Score: {:.2f}\n".format(student.averageScore))
                found = True
                break
        if not found:
            print(f"Student with ID {sID} not found.")
    
    def showRank(self, sID):
        # Sort studentList based on average score in descending order
        sorted_students = sorted(self.studentList, key=lambda x: x.averageScore, reverse=True)
        # Find the position of the student with the given ID in the sorted list
        for i, student in enumerate(sorted_students, start=1):
            if student.sID == sID:
                print(f"\nRanking: {i}\n")
                break
        else:
            print(f"Student with ID {sID} not found.")
    
    def showGradeDistribution(self):
        print("Grade Distribution:")
        for grade, count in self.gradeDistribution.items():
            print(f"{grade}: {count}")

    def showFilter(self, Thres):
        sorted_students = sorted(self.studentList, key=lambda x: x.averageScore, reverse=True)
        print('\n')
        for i, student in enumerate(sorted_students, start=1):
            if student.averageScore > Thres:
                print(f"{i} {student.name} {student.sID} {student.letterGrade} {student.averageScore:.2f}")

class Student:
    def __init__(self, sID, name, lab1, lab2, lab3, mid, final, weightList):
        self.sID = sID
        self.name = name
        self.scores = [float(lab1), float(lab2), float(lab3), float(mid), float(final)]
        self.averageScore = self.average(weightList)
        self.letterGrade = self.countLetterGrade()

    def recalculate(self,weightList):
        self.averageScore = self.average(weightList)
        self.letterGrade = self.countLetterGrade()
        
    def average(self, weightList):
        total_score = sum(float(score) * float(weight) for score, weight in zip(self.scores, weightList))
        return total_score
    
    def countLetterGrade(self):
        if 90 <= self.averageScore <= 100:
            return 'A+'
        elif 85 <= self.averageScore < 90:
            return 'A'
        elif 80 <= self.averageScore < 85:
            return 'A-'
        elif 77 <= self.averageScore < 80:
            return 'B+'
        elif 73 <= self.averageScore < 77:
            return 'B'
        elif 70 <= self.averageScore < 73:
            return 'B-'
        elif 67 <= self.averageScore < 70:
            return 'C+'
        elif 63 <= self.averageScore < 67:
            return 'C'
        elif 60 <= self.averageScore < 63:
            return 'C-'
        elif 50 <= self.averageScore < 60:
            return 'D'
        else:
            return 'E'


if __name__ == "__main__":
    # Create GradeSystem object
    grade_system = GradeSystem()

    # Main loop
    while True:
        print("Welcome to Grade System.")
        print("Function menu:")
        print("1) Show grades")
        print("2) Show grade letters")
        print("3) Show average")
        print("4) Show rank")
        print("5) Show distribution")
        print("6) Filtering")
        print("7) Add Student")
        print('8) Update Score')
        print("9) Update weights")
        print("10) Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            sID = input("Enter student ID: ")
            grade_system.showScore(sID)
        elif choice == "2":
            sID = input("Enter student ID: ")
            grade_system.showLetterGrade(sID)
        elif choice == "3":
            sID = input("Enter student ID: ")
            grade_system.showAverage(sID)
        elif choice == "4":
            sID = input("Enter student ID: ")
            grade_system.showRank(sID)
        elif choice == "5":
            grade_system.showGradeDistribution()
        elif choice == "6":
            threshold = float(input("Enter threshold score: "))
            grade_system.showFilter(threshold)
        elif choice == "7":
            info = input("Enter student info (sID name lab1 lab2 lab3 mid final): ")
            grade_system.addStudent(info)
        elif choice == '8':
            info = input("Update grades, input format : StudentID score_name new_grades ... \nExample: 00001 lab1 50 lab3 40 midterm 100\n")
            grade_system.updateScore(info)
        elif choice == "9":
            info = input("Update weights, input format: weight_name new_weight \nExample: lab1 0.1 lab2 0.1 lab3 0.1 midterm 0.3 final 0.4\n")
            grade_system.updateWeight(info)
        elif choice == "10":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice")