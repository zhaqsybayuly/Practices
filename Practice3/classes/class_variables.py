# Class variables are shared, instance variables are unique

# Example 1: Shared vs Unique data
class Employee:
    # Every employee belongs to the same company
    company_name = "TechCorp"
    employee_count = 0  # count how many people we have

    def __init__(self, name, salary):
        # Each employee has their own name and pay
        self.name = name
        self.salary = salary
        # Count goes up every time we make a new employee
        Employee.employee_count += 1

    def show_info(self):
        print(f"Name: {self.name}, Salary: ${self.salary}, Company: {Employee.company_name}")


emp1 = Employee("Aibek", 50000)
emp2 = Employee("Dana", 60000)

emp1.show_info()
emp2.show_info()

# Check the total count from the class itself
print(f"\nTotal employees: {Employee.employee_count}")


# Example 2: Changing a class variable
class Cat:
    # All cats (usually) have 4 legs
    legs = 4

    def __init__(self, name):
        self.name = name

cat1 = Cat("Whiskers")
cat2 = Cat("Luna")

print(f"{cat1.name} has {cat1.legs} legs")
print(f"{cat2.name} has {cat2.legs} legs")
