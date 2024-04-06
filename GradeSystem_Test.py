import pytest
from GradeSystem import GradeSystem

@pytest.fixture
def grade_system():
    return GradeSystem()

def test_add_student(grade_system):
    """
    Test Function: GradeSystem.addStudent(info)
    Test Description:
        -Step 1: Add student with missing scores/data to GradeSystem
            Expected result : Student won't be added
        -Step 2: Add student with invalid scores/data to GradeSystem
            Expected result : Student won't be added
        -Step 3: Add valid student to GradeSystem
            Expected result : Student will be created and the length of grade_system.studentList will increase
    """
    previous_len = len(grade_system.studentList)
    # Test adding an invalid student with missing data
    grade_system.addStudent("110006213 Bill 80 75 85 78")
    assert len(grade_system.studentList) == previous_len
    # Test adding an invalid student with invalid scores
    grade_system.addStudent("110006213 Bill 80 75 85 78 b1")
    assert len(grade_system.studentList) == previous_len
    # Test adding a valid student
    grade_system.addStudent("110006213 Bill 90 85 95 88 92")
    assert len(grade_system.studentList) == previous_len+1

def test_update_score(grade_system):
    """
    Test Function: GradeSystem.updateScore(info)
    Test Description:
        -Step 1: Add valid student to GradeSystem
            Expected result : Student will be added into grade_system.studentList
        -Step 2: Find the student from the grade_system.studentList
            Expected result : Student will be saved into student_added
        -Step 3: Updating with wrong format
            Expected result : student_added.scores will not be updated
        -Step 4: Updating with proper format
            Expected result : Student scores will be updated
    """
    # Add a student first
    grade_system.addStudent("110006213 Bill 90 85 95 88 92")
    student_added = "0"
    for student in grade_system.studentList:
        if(student.sID == "110006213"):
            student_added = student

    # Test updating scores for the student failed (wrong format)
    grade_system.updateScore("110006213 lab 95 lab5 88 lab3 90 midterm 85 final 94")
    assert student_added.scores == [90, 85, 95, 88, 92]
    # Test updating scores for the student
    grade_system.updateScore("110006213 lab1 95 lab2 88 lab3 90 midterm 85 final 94")
    assert student_added.scores == [95, 88, 90, 85, 94]

def test_update_weight(grade_system):
    """
    Test Function: GradeSystem.updateWeight(info)
    Test Description:
        -Step 1: Updating weight with wrong format
            Expected result : Weight will not be updated
        -Step 2: Updating weight with proper format
            Expected result : Weight will be updated
    """
    # Test updating weights failed (wrong format)
    grade_system.updateWeight("lab5 0.2 lab2 0.2 lab3 0.2 midterm 0.2 final 0.2")
    assert grade_system.weightList == [0.1, 0.1, 0.1, 0.3, 0.4]
    # Test updating weights
    grade_system.updateWeight("lab1 0.2 lab2 0.2 lab3 0.2 midterm 0.2 final 0.2")
    assert grade_system.weightList == [0.2, 0.2, 0.2, 0.2, 0.2]

def test_show_score(grade_system, capsys):
    """
    Test Function: GradeSystem.showScore(sID)
    Test Description:
        -Step 1: Adding student "110006213"
             Expected result : Student will be added
        -Step 2: Try showing score for student "110006221"
            Expected result : Student not found
        -Step 3: Try showing score for student "110006213"
            Expected result : Student found, match the Scores
    """
    # Add a student first
    grade_system.addStudent("110006213 Bill 90 85 95 88 92")
    # Test showing scores (student not found)
    grade_system.showScore("110006221")
    captured = capsys.readouterr()
    assert "Student with ID 110006221 not found."
    # Test showing scores for the student
    grade_system.showScore("110006213")
    captured = capsys.readouterr()
    assert "Lab Scores: [90.0, 85.0, 95.0]" in captured.out
    assert "Midterm Score: 88.0" in captured.out
    assert "Final Score: 92.0" in captured.out

def test_show_letterGrade(grade_system,capsys):
    """
    Test Function: GradeSystem.showLetterGrade(sID)
    Test Description:
        -Step 1: Adding student "110006213"
             Expected result : Student will be added
        -Step 2: Try showing letterGrade for student "110006221"
            Expected result : Student not found
        -Step 3: Try showing leterGrade for student "110006213"
            Expected result : Student found, match the letterGrade
    """
    # Add a student first
    grade_system.addStudent("110006213 Bill 99 95 95 98 92")
    # Test showing scores (student not found)
    grade_system.showLetterGrade("110006221")
    captured = capsys.readouterr()
    assert "Student with ID 110006221 not found."
    # Test showing scores for the student
    grade_system.showLetterGrade("110006213")
    captured = capsys.readouterr()
    assert 'Letter Grade: A+' in captured.out

def test_show_Average(grade_system,capsys):
    """
    Test Function: GradeSystem.showAverage(sID)
    Test Description:
        -Step 1: Adding student "110006213"
             Expected result : Student will be added
        -Step 2: Try showing averageScore for student "110006221"
            Expected result : Student not found
        -Step 3: Try showing averageScore for student "110006213"
            Expected result : Student found, match the averageScore
    """
    # Add a student first
    grade_system.addStudent("110006213 Bill 99 95 95 98 92")
    # Test showing scores (student not found)
    grade_system.showAverage("110006221")
    captured = capsys.readouterr()
    assert "Student with ID 110006221 not found."
    # Test showing scores for the student
    grade_system.showAverage("110006213")
    captured = capsys.readouterr()
    assert 'Average Score: 95.10' in captured.out

def test_show_Rank(grade_system,capsys):
    """
    Test Function: GradeSystem.showRank(sID)
    Test Description:
        -Step 1: Adding student "110006213"
             Expected result : Student will be added
        -Step 2: Try showing ranking for student "110006221"
            Expected result : Student not found
        -Step 3: Try showing ranking for student "110006213"
            Expected result : Student found, match the ranking
    """
    # Add a student first
    grade_system.addStudent("110006213 Bill 99 95 95 98 92")
    # Test showing scores (student not found)
    grade_system.showRank("110006221")
    captured = capsys.readouterr()
    assert "Student with ID 110006221 not found."
    # Test showing scores for the student
    grade_system.showRank("110006213")
    captured = capsys.readouterr()
    assert 'Ranking: 2' in captured.out

def test_show_gradeDistribution(grade_system, capsys):
    """
    Test Function: GradeSystem.showGradeDistribution()
    Test Description:
        -Step 1: Getting the expected_distribution from default data
        -Step 2: Comparing the expected distribution with actual distribution
            Expected result : Distribution matches
    """
    expected_output = "Grade Distribution:\nA+: 27\nA: 33\nA-: 3\nB+: 0\nB: 0\nB-: 0\nC+: 0\nC: 0\nC-: 0\nD: 0\nE: 0\n"

    grade_system.showGradeDistribution()
    captured_output = capsys.readouterr()

    assert captured_output.out.strip() == expected_output.strip()

def test_show_filter(grade_system, capsys):
    """
    Test Function: GradeSystem.showFilter(Thres)
    Test Description:
        -Step 1: Getting the expected_output based on the Threshold from default data
        -Step 2: Comparing the expected_output with actual output
            Expected result : filter output matches
    """
    expected_output = """1 蔡宗衛 985002509 A+ 95.20
2 辜麟傑 985002515 A+ 95.00
3 楊宗穎 975002070 A+ 94.70
4 朱燕雲 985002004 A+ 93.90
5 許貴松 985002015 A+ 93.90
6 許佳華 985002503 A+ 93.90
7 陳柏彰 985002021 A+ 93.50
8 曾裕庭 985002039 A+ 93.50"""

    grade_system.showFilter(93)
    captured_output = capsys.readouterr()

    assert captured_output.out.strip() == expected_output.strip()

def test_recalculate_distribution(grade_system):
    """
    Test Function: GradeSystem.recalculateDistribution(Thres)
    Test Description:
        -Step 1: Adding student 110006213 with A+ worth of grades
        -Step 2: Saving the original number of A+ and E in grade_system.gradeDistribution
        -Step 3: Find the student from the grade_system.studentList
        -Step 4: Modifying the scores of added_student
        -Step 5: Recalculate the scores of added_student
            Expected result: Letter grade of added_student will be reduced to E
        -Step 6: Recalculate Distribution ***
        -Step 7: Compare the number of A+ and E in grade_system.gradeDistribution
            Expected result: the number of A+ will decrease and the number of E will increase
    """
    grade_system.addStudent("110006213 Bill 99 95 95 98 92")
    original_Aplus = grade_system.gradeDistribution['A+']
    original_E = grade_system.gradeDistribution['E']
    added_student = None
    for student in grade_system.studentList:
        if student.sID == "110006213":
            added_student = student
    added_student.scores = [0,0,0,50,50]
    added_student.recalculate(grade_system.weightList)
    grade_system.recalculateDistribution()
    assert grade_system.gradeDistribution['A+'] == original_Aplus-1
    assert grade_system.gradeDistribution['E'] == original_E+1