import json
import os

# ==== LỚP STUDENT ====
class Student:
    def __init__(self, name, mssv, class_name, phone, dob, address):
        self.name = name
        self.mssv = mssv
        self.class_name = class_name
        self.phone = phone
        self.dob = dob
        self.address = address

# ==== LỚP FAMILY ====
class Family:
    def __init__(self, student, family_address, father_name, mother_name):
        self.student = student
        self.family_address = family_address
        self.father_name = father_name
        self.mother_name = mother_name

    def to_dict(self, _id):
        return {
            "id": _id,
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

# ==== TRÌNH QUẢN LÝ SINH VIÊN ====
class StudentManager:
    def __init__(self, filename='students.json'):
        self.filename = filename
        self.students = self.load_students()

    def load_students(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        return []

    def save_students(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.students, f, ensure_ascii=False, indent=4)

    def add_student(self, family):
        new_id = 1 if not self.students else self.students[-1]['id'] + 1
        self.students.append(family.to_dict(new_id))
        self.save_students()

    def update_student(self, mssv, new_family):
        for idx, student in enumerate(self.students):
            if student["Thông tin sinh viên"]["MSSV"] == mssv:
                self.students[idx] = new_family.to_dict(student["id"])
                self.save_students()
                print("✅ Cập nhật thành công.")
                return
        print("❌ Không tìm thấy sinh viên.")

    def delete_student(self, mssv):
        original_len = len(self.students)
        self.students = [s for s in self.students if s["Thông tin sinh viên"]["MSSV"] != mssv]
        if len(self.students) < original_len:
            self.save_students()
            print("✅ Xóa thành công.")
        else:
            print("❌ Không tìm thấy sinh viên.")

    def list_students(self):
        for student in self.students:
            print(json.dumps(student, ensure_ascii=False, indent=4))

# ==== MENU CHẠY CHƯƠNG TRÌNH ====
def main():
    manager = StudentManager()

    while True:
        print("\n===== MENU QUẢN LÝ SINH VIÊN =====")
        print("1. Thêm sinh viên")
        print("2. Cập nhật sinh viên")
        print("3. Xóa sinh viên")
        print("4. Hiển thị danh sách")
        print("5. Thoát")
        choice = input("Chọn chức năng: ")

        if choice == "1":
            name = input("Họ tên: ")
            mssv = input("MSSV: ")
            class_name = input("Lớp: ")
            phone = input("SĐT: ")
            dob = input("Ngày sinh: ")
            address = input("Địa chỉ hiện tại: ")
            family_address = input("Địa chỉ gia đình: ")
            father = input("Tên bố: ")
            mother = input("Tên mẹ: ")

            student = Student(name, mssv, class_name, phone, dob, address)
            family = Family(student, family_address, father, mother)
            manager.add_student(family)
            print("✅ Thêm sinh viên thành công!")

        elif choice == "2":
            mssv = input("Nhập MSSV cần cập nhật: ")
            name = input("Họ tên mới: ")
            class_name = input("Lớp mới: ")
            phone = input("SĐT mới: ")
            dob = input("Ngày sinh mới: ")
            address = input("Địa chỉ hiện tại mới: ")
            family_address = input("Địa chỉ gia đình mới: ")
            father = input("Tên bố mới: ")
            mother = input("Tên mẹ mới: ")

            student = Student(name, mssv, class_name, phone, dob, address)
            family = Family(student, family_address, father, mother)
            manager.update_student(mssv, family)

        elif choice == "3":
            mssv = input("Nhập MSSV cần xóa: ")
            manager.delete_student(mssv)

        elif choice == "4":
            manager.list_students()

        elif choice == "5":
            break

        else:
            print("❌ Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    main()
