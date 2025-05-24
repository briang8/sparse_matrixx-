class SparseMatrix:
    """
    Represents a sparse matrix using a dictionary to store non-zero values.
    The keys are (row, column) tuples, and the values are integers.
    """
    def __init__(self, rows=0, cols=0):
        self.rows = rows
        self.cols = cols
        self.data = {}  # {(row, col): value}

    @staticmethod
    def from_file(file_path):
        """
        Reads a sparse matrix from a file. 
        The file format must be:
        - First line: rows=<num_rows>
        - Second line: cols=<num_cols>
        - Subsequent lines: (row, col, value)
        Returns a SparseMatrix instance.
        """
        matrix = SparseMatrix()
        with open(file_path, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
            matrix.rows = int(lines[0].split('=')[1])
            matrix.cols = int(lines[1].split('=')[1])
            for line in lines[2:]:
                if not (line.startswith('(') and line.endswith(')')):
                    raise ValueError("Wrong format")
                parts = line[1:-1].split(',')
                r, c, v = int(parts[0]), int(parts[1]), int(parts[2])
                if v != 0:
                    matrix.data[(r, c)] = v
        return matrix

    def get(self, r, c):
        """Returns the value at (r, c) or 0 if it is not explicitly stored."""
        return self.data.get((r, c), 0)

    def set(self, r, c, v):
        """Sets the value at (r, c). Removes entry if value is 0 to keep it sparse."""
        if v != 0:
            self.data[(r, c)] = v
        elif (r, c) in self.data:
            del self.data[(r, c)]

    def add(self, other):
        """
        Adds two sparse matrices.
        Matrices must have the same dimensions.
        Returns a new SparseMatrix instance.
        """
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Size mismatch")
        result = SparseMatrix(self.rows, self.cols)
        for (r, c), v in self.data.items():
            result.set(r, c, v)
        for (r, c), v in other.data.items():
            result.set(r, c, result.get(r, c) + v)
        return result

    def subtract(self, other):
        """
        Subtracts the other sparse matrix from this one.
        Matrices must have the same dimensions.
        Returns a new SparseMatrix instance.
        """
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Size mismatch")
        result = SparseMatrix(self.rows, self.cols)
        for (r, c), v in self.data.items():
            result.set(r, c, v)
        for (r, c), v in other.data.items():
            result.set(r, c, result.get(r, c) - v)
        return result

    def multiply(self, other):
        """
        Multiplies this sparse matrix with another.
        Number of columns of the first matrix must equal the number of rows of the second.
        Returns a new SparseMatrix instance.
        """
        if self.cols != other.rows:
            raise ValueError("Size mismatch")
        result = SparseMatrix(self.rows, other.cols)
        for (i, k), v in self.data.items():
            for j in range(other.cols):
                val = v * other.get(k, j)
                if val != 0:
                    result.set(i, j, result.get(i, j) + val)
        return result

    def __str__(self):
        """
        Returns a string representation of the sparse matrix in the specified file format.
        """
        out = [f"rows={self.rows}", f"cols={self.cols}"]
        for (r, c), v in sorted(self.data.items()):
            out.append(f"({r}, {c}, {v})")
        return '\n'.join(out)

    def to_file(self, file_path):
        """Writes the sparse matrix to a file in the correct format."""
        with open(file_path, 'w') as f:
            f.write(str(self))


def main():
    """
    Main execution function:
    - Prompts user to load two matrix files
    - Asks for the operation (add, subtract, multiply)
    - Displays and saves the resulting matrix to a user-specified file
    """
    print("Sparse Matrix Operations")
    a_path = input("Matrix A file: ")
    b_path = input("Matrix B file: ")
    A = SparseMatrix.from_file(a_path)
    B = SparseMatrix.from_file(b_path)

    print("1: Add\n2: Subtract\n3: Multiply")
    choice = input("Choose operation: ")

    if choice == '1':
        result = A.add(B)
    elif choice == '2':
        result = A.subtract(B)
    elif choice == '3':
        result = A.multiply(B)
    else:
        print("Invalid option")
        return

    print("\nResult:")
    print(result)

    output_path = input("Enter output file path to save result (e.g., result.txt): ")
    result.to_file(output_path)
    print(f"Result saved to {output_path}")


if __name__ == "__main__":
    main()
