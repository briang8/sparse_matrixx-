class SparseMatrix:
    def __init__(self, num_rows=0, num_cols=0):
        self.rows = num_rows
        self.cols = num_cols
        self.data = {}  # key: (row, col), value: int

    @staticmethod
    def from_file(file_path):
        matrix = SparseMatrix()
        try:
            with open(file_path, 'r') as file:
                lines = [line.strip() for line in file if line.strip()]
        except:
            raise ValueError("Unable to open file.")

        if not lines[0].startswith("rows=") or not lines[1].startswith("cols="):
            raise ValueError("Input file has wrong format")

        try:
            matrix.rows = int(lines[0].split("=")[1])
            matrix.cols = int(lines[1].split("=")[1])
        except:
            raise ValueError("Input file has wrong format")

        for line in lines[2:]:
            if not (line.startswith("(") and line.endswith(")")):
                raise ValueError("Input file has wrong format")
            content = line[1:-1]
            parts = content.split(",")
            if len(parts) != 3:
                raise ValueError("Input file has wrong format")
            try:
                row = int(parts[0].strip())
                col = int(parts[1].strip())
                val = int(parts[2].strip())
            except:
                raise ValueError("Input file has wrong format")

            if val != 0:
                matrix.set_element(row, col, val)

        return matrix

    def get_element(self, row, col):
        return self.data.get((row, col), 0)

    def set_element(self, row, col, value):
        if row < 0 or col < 0 or row >= self.rows or col >= self.cols:
            print(
                f"Invalid index: ({row}, {col}) for matrix size {self.rows}x{self.cols}")
            raise IndexError("Index out of range.")
        if value != 0:
            self.data[(row, col)] = value
        elif (row, col) in self.data:
            del self.data[(row, col)]

    def add(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions must match for addition")

        result = SparseMatrix(self.rows, self.cols)
        for (r, c), v in self.data.items():
            result.set_element(r, c, v)

        for (r, c), v in other.data.items():
            sum_val = result.get_element(r, c) + v
            result.set_element(r, c, sum_val)

        return result

    def subtract(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions must match for subtraction")

        result = SparseMatrix(self.rows, self.cols)
        for (r, c), v in self.data.items():
            result.set_element(r, c, v)

        for (r, c), v in other.data.items():
            diff_val = result.get_element(r, c) - v
            result.set_element(r, c, diff_val)

        return result

    def multiply(self, other):
        if self.cols != other.rows:
            raise ValueError(
                "Matrix dimensions incompatible for multiplication")

        result = SparseMatrix(self.rows, other.cols)
        for (i, k), a_val in self.data.items():
            for j in range(other.cols):
                b_val = other.get_element(k, j)
                if b_val != 0:
                    prev = result.get_element(i, j)
                    result.set_element(i, j, prev + a_val * b_val)
        return result

    def print_matrix(self):
        print(f"rows={self.rows}")
        print(f"cols={self.cols}")
        for (r, c), v in sorted(self.data.items()):
            print(f"({r}, {c}, {v})")


def main():
    try:
        file1 = input("Enter path for Matrix A: ").strip()
        file2 = input("Enter path for Matrix B: ").strip()

        A = SparseMatrix.from_file("../../sample_inputs/easy_sample_01_2.txt")
        B = SparseMatrix.from_file("../../sample_inputs/easy_sample_01_2.txt")

        print("\nSelect Operation:\n1. Addition\n2. Subtraction\n3. Multiplication")
        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == "1":
            result = A.add(B)
        elif choice == "2":
            result = A.subtract(B)
        elif choice == "3":
            result = A.multiply(B)
        else:
            print("Invalid choice.")
            return

        print("\nResult:")
        result.print_matrix()

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
