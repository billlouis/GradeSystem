import copy
class GradeSystem:
    """
    A class representing a grading system.

    This class manages student data and operations for
    displaying grades, updating scores, updating weights, and more.

    Attributes:
        studentList (list): A list of Student objects for students.
        weightList (list): A list of weights for each grade.
        gradeDistribution (dict): A dictionary of distribution of letter grades of all the students.

    """
    def __init__(self):
        """
        Initializes the GradeSystem object.

        Running Example:
            grade_system = GradeSystem()
        """
        self.studentList = []
        self.weightList = [0.1,0.1,0.1,0.3,0.4]
        self.gradeDistribution = {'A+': 0, 'A': 0, 'A-': 0, 'B+': 0, 'B': 0, 'B-': 0, 
                                  'C+': 0, 'C': 0, 'C-': 0, 'D': 0, 'E': 0}
        try:
            # Open file and read data
            with open('input.txt', 'r', encoding='utf-8') as fh:
                
                for line in fh.readlines():
                    tmp = line.split()
                    assert len(tmp) == 7, "Invalid data format in input file"
                    # Create a new Student object and append to studentList
                    tmpStudent = Student(tmp[0], tmp[1], tmp[2], tmp[3], tmp[4], tmp[5], tmp[6], self.weightList)
                    self.studentList.append(tmpStudent)
                    self.gradeDistribution[tmpStudent.letterGrade] += 1
        except FileNotFoundError:
            print("Error: File 'studentList.txt' not found.")
        except Exception as e:
            print("Error occurred while reading file:", e)

    def recalculateDistribution(self):
        """
        Recalculates the distribution of letter grades among students.

        Running Example:
            grade_system.recalculateDistribution()
        """
        # Reset all grade distribution counts to 0
        for grade in self.gradeDistribution:
            self.gradeDistribution[grade] = 0

        # Recalculate grade distribution based on student letter grades
        for student in self.studentList:
            self.gradeDistribution[student.letterGrade] += 1

    def addStudent(self, info):
        """
        Adding a new student to the list, as well as all his/her grades.

        :param info: A string containing information about the new student in the format (sID name lab1 lab2 lab3 mid final).
        :type info: str

        Running Example:
            grade_system.addStudent('123 John 90 85 75 85 90')
        """
        try:
            newInfo = info.split()
            for student in self.studentList:
                if student.sID == newInfo[0]:
                    raise AssertionError("Student with ID '{}' already exists.".format(student.sID))
            if len(newInfo) != 7:
                raise ValueError("Invalid data format: Expected 7 elements")

            tmpStudent = Student(newInfo[0], newInfo[1], newInfo[2], newInfo[3], newInfo[4], newInfo[5], newInfo[6],
                                     self.weightList)
            self.studentList.append(tmpStudent)
            self.gradeDistribution[tmpStudent.letterGrade] += 1
            print('Student added successfully.')
        except ValueError as ve:
            print("Error adding student:", ve)
        except Exception as e:
            print("Error adding student:", e)


    def updateScore(self, info):
        """
        Updating one or more score of a certain student.

        :param info: A string containing the updated scores and the score names for a student in the format 'sID score_name new_score ...'.
        :type info: str

        Running Example:
            grade_system.updateScore('123 lab1 88 lab3 89')
        """
        try:
            newInfo = info.split()
            tmpStudentCopy = None
            for student in self.studentList:
                if student.sID == newInfo[0]:
                    tmpStudentCopy = copy.deepcopy(student)
                    break

            for i, j in enumerate(newInfo[1::2], start=1):  # Increment by 2
                if j == 'final':
                    tmpStudentCopy.scores[4] = float(newInfo[i * 2])
                elif j == 'midterm':
                    tmpStudentCopy.scores[3] = float(newInfo[i * 2])
                elif j == 'lab1' or j == 'lab2' or j == 'lab3':
                    tmpStudentCopy.scores[int(j[-1]) - 1] = float(newInfo[i * 2])
                else:
                    raise AssertionError(f"Invalid score format: {j}")

            for student in self.studentList:
                if student.sID == tmpStudentCopy.sID:
                    student.scores = tmpStudentCopy.scores
                    student.recalculate(self.weightList)
                    break
            self.recalculateDistribution()
        except Exception as e:
            print("Error updating score:", e)

                    
    def updateWeight(self, info):
        """
        Updates the weights of lab assignments, midterm, and final exam.

        :param info: A string containing the new weights for lab assignments, midterm, and final exam in the format 'weight_name new_weight ...'.
        :type info: str

        Running Example:
            grade_system.updateWeight('lab1 0.2 lab2 0.2 lab3 0.2 midterm 0.3 final 0.4')
        """
        try:
            newInfo = info.split()
            tmpWeightList = copy.deepcopy(self.weightList)
            for i, j in enumerate(newInfo[::2], start=0):  # Increment by 2
                assert float(newInfo[i*2+1]), f"Invalid weight format: {newInfo[i*2+1]}"
                if j == 'final':
                    tmpWeightList[4] = float(newInfo[i * 2 + 1])
                elif j == 'midterm':
                    tmpWeightList[3] = float(newInfo[i * 2 + 1])
                elif j == 'lab1' or j == 'lab2' or j == 'lab3':
                    tmpWeightList[int(j[-1]) - 1] = float(newInfo[i * 2 + 1])
                else:
                    raise AssertionError(f"Invalid weight format: {j}")
            if sum(tmpWeightList)>1.0:
                raise AssertionError(f"Invalid weight sum: {sum(tmpWeightList):.2f}")
            else:
                self.weightList = tmpWeightList
            for student in self.studentList:
                student.recalculate(self.weightList)
            self.recalculateDistribution()
        except Exception as e:
            print("Error updating weight:", e)
        
    def showScore(self, sID):
        """
        Shows the score of a student, using his/her student id.

        :param sID: The ID of the student whose scores are to be displayed.
        :type sID: str

        Running Example:
            grade_system.showScore('123')
        """
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
        """
        shows a letter grade of a student by his/her student id.

        :param sID: The ID of the student whose letter grade is going to be displayed.
        :type sID: str

        Running Example:
            grade_system.showLetterGrade('123')
        """
        found = False
        for student in self.studentList:
            if student.sID == sID:
                print("\nLetter Grade:", student.letterGrade,'\n')
                found = True
                break
        if not found:
            print(f"Student with ID {sID} not found.")
            
    def showAverage(self, sID):
        """
        Shows the average score of a student by his/her student id.

        :param sID: The ID of the student whose average score is to be displayed.
        :type sID: str

        Running Example:
            grade_system.showAverage('123')
        """
        found = False
        for student in self.studentList:
            if student.sID == sID:
                print("\nAverage Score: {:.2f}\n".format(student.averageScore))
                found = True
                break
        if not found:
            print(f"Student with ID {sID} not found.")
    
    def showRank(self, sID):
        """
        Shows the rank of a student identified by his/her student id.

        :param sID: The ID of the student whose rank is to be displayed.
        :type sID: str

        Running Example:
            grade_system.showRank('123')
        """
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
        """
        Shows the distribution of letter grades from all students.

        Running Example:
            grade_system.showGradeDistribution()
        """
        print("Grade Distribution:")
        for grade, count in self.gradeDistribution.items():
            print(f"{grade}: {count}")

    def showFilter(self, Thres):
        """
        Show all the students which the score is above the threshold.

        :param Thres: The threshold score.
        :type Thres: float

        Running Example:
            grade_system.showFilter(85)
        """
        sorted_students = sorted(self.studentList, key=lambda x: x.averageScore, reverse=True)
        print('\n')
        for i, student in enumerate(sorted_students, start=1):
            if student.averageScore > Thres:
                print(f"{i} {student.name} {student.sID} {student.letterGrade} {student.averageScore:.2f}")

class Student:
    """
    A class representing a student.

    This class stores information about a student including their ID, name, scores, average score, and letter grade.

    """
    def __init__(self, sID, name, lab1, lab2, lab3, mid, final, weightList):
        """
        Initializes a Student object.

        :param sID: The student's ID.
        :type sID: str
        :param name: The student's name.
        :type name: str
        :param lab1: The student's score for lab1.
        :type lab1: str
        :param lab2: The student's score for lab2.
        :type lab2: str
        :param lab3: The student's score for lab3.
        :type lab3: str
        :param mid: The student's score for the midterm exam.
        :type mid: str
        :param final: The student's score for the final exam.
        :type final: str
        :param weightList: A list of weights for lab assignments, midterm, and final exam.
        :type weightList: list

        Running Example:
            student = Student('123', 'John', '90', '85', '75', '85', '90', ['0.1', '0.1', '0.1', '0.3', '0.4'])
        """
        try:
            self.sID = sID
            self.name = name
            self.scores = [float(lab1), float(lab2), float(lab3), float(mid), float(final)]
            self.averageScore = self.average(weightList)
            self.letterGrade = self.countLetterGrade()
        except Exception as e:
            print("Error constructing student:", e, "student creation cancelled")
            raise
    def recalculate(self,weightList):
        """
        Recalculates the student's average score and letter grade based on the weight list.

        :param weightList: A list of weights for lab assignments, midterm, and final exam.
        :type weightList: list

        Running Example:
            student.recalculate(['0.2', '0.2', '0.2', '0.3', '0.4'])
        """
        self.averageScore = self.average(weightList)
        self.letterGrade = self.countLetterGrade()
        
    def average(self, weightList):
        """
        Calculates the student's average score using the weight.

        :param weightList: A list of weights for lab assignments, midterm, and final exam.
        :type weightList: list
        :return: The average score of the student.
        :rtype: float

        Running Example:
            average_score = student.average(['0.2', '0.2', '0.2', '0.3', '0.4'])
        """
        total_score = sum(float(score) * float(weight) for score, weight in zip(self.scores, weightList))
        return total_score
    
    def countLetterGrade(self):
        """
        Converts the letter grade of the student using average score.

        :return: The letter grade of the student.
        :rtype: str

        Running Example:
            letter_grade = student.countLetterGrade()
        """
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
    print("Welcome to Grade System.")
    # Main loop
    while True:
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

            info = input("Update grades, input format : StudentID score_name new_grades ... \n"
                         "Example: 00001 lab1 50 lab3 40 midterm 100\n")
            print(f"{info.split()[0]}'s previous grades are : ")
            grade_system.showScore(info.split()[0])
            print(f"and you're updating it to {info[len(info.split()[0]):]}")
            confirmation = input(f"Do you want to continue? [Y/N]")
            if confirmation == "Y" or confirmation == "y":
                grade_system.updateScore(info)
            else:
                print("Cancelled")
                continue
        elif choice == "9":
            info = input("Update weights, input format: weight_name new_weight \n"
                         "Example: lab1 0.1 lab2 0.1 lab3 0.1 midterm 0.3 final 0.4\n")
            print(f"The previous weights are : lab1={float(grade_system.weightList[0])*100}% "
                  f"lab2={float(grade_system.weightList[1])*100}% "
                  f"lab3={float(grade_system.weightList[2])*100}% "
                  f"midterm={float(grade_system.weightList[3])*100}% "
                  f"final={float(grade_system.weightList[4])*100}%")
            confirmation = input(f"The given weights {info} will be updated. Do you want to continue? [Y/N]")
            if confirmation == "Y":
                grade_system.updateWeight(info)
            else:
                continue
        elif choice == "10":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice")