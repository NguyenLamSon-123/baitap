import json

class Student:
    def __init__(self, name, mssv, class_name, phone, dob, address):
        self.name = name
        self.mssv = mssv
        self.class_name = class_name
        self.phone = phone
        self.dob = dob
        self.address = address

class Family:
    def __init__(self, student, family_address, father_name, mother_name):
        self.student = student
        self.family_address = family_address
        self.father_name = father_name
        self.mother_name = mother_name

    def to_dict(self):
        return {
            "id": self.student.mssv,
            "Thông tin sinh viên": {
                "Họ tên": self.student.name,
                "MSSV": self.student.mssv,
                "Lớp": self.student.class_name,
                "SĐT": self.student.phone,
                "Ngày sinh": self.student.dob,
                "Địa chỉ hiện tại": self.student.address
            },
            "Thông tin gia đình": {
                "Địa chỉ gia đình": self.family_address,
                "Họ tên bố": self.father_name,
                "Họ tên mẹ": self.mother_name
            }
        }
class StudentManager:
    def __init__(self, filename='students.json'):
        self.filename = filename
        self.students = self.load_students()

    def load_students(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [Family(Student(**item['Thông tin sinh viên']), **item['Thông tin gia đình']) for item in data]
        except FileNotFoundError:
            return []

    def save_students(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump([student.to_dict() for student in self.students], f, ensure_ascii=False, indent=4)

    def add_student(self, student, family_address, father_name, mother_name):
        family = Family(student, family_address, father_name, mother_name)
        self.students.append(family)
        self.save_students()

    def update_student(self, mssv, updated_student, updated_family_address, updated_father_name, updated_mother_name):
        for family in self.students:
            if family.student.mssv == mssv:
                family.student = updated_student
                family.family_address = updated_family_address
                family.father_name = updated_father_name
                family.mother_name = updated_mother_name
                self.save_students()
                return
        print("Sinh viên không tồn tại.")

    def delete_student(self, mssv):
        self.students = [family for family in self.students if family.student.mssv != mssv]
        self.save_students()
# Khởi tạo quản lý sinh viên
manager = StudentManager()

# Thêm sinh viên mới
student = Student("Nguyễn Văn A", "123456789", "Lớp 10A1", "0123456789", "2005-01-01", "Hà Nội")
manager.add_student(student, "Hà Nội", "Nguyễn Văn B", "Trần Thị C")

# Cập nhật thông tin sinh viên
updated_student = Student("Nguyễn Văn A", "123456789", "Lớp 10A2", "0987654321", "2005-01-01", "Hà Nội")
manager.update_student("123456789", updated_student, "Hà Nội", "Nguyễn Văn B", "Trần Thị C")

# Xóa sinh viên
manager.delete_student("123456789")
