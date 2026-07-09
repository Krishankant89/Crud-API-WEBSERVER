async function loadStudents() {
    try {
        const response = await fetch('/api/v1/students');
        const students = await response.json();

        let html = "";

        if (students.length === 0) {
            html = "<p>No students found.</p>";
        } else {
            students.forEach(student => {
                html += `
                    <div>
                        <h3>${student.name}</h3>
                        <p>Email: ${student.email}</p>
                        <p>Age: ${student.age}</p>

                        <button onclick="deleteStudent(${student.id})">
                            Delete
                        </button>
                    </div>
                    <hr>
                `;
            });
        }

        document.getElementById("students").innerHTML = html;

    } catch (error) {
        console.error("Error loading students:", error);
    }
}

const studentForm = document.getElementById("studentForm");
if (studentForm) {
    studentForm.addEventListener("submit", async (e) => {

        e.preventDefault();

        const formData = new FormData(studentForm);
        const data = {
            name: String(formData.get("name") || "").trim(),
            email: String(formData.get("email") || "").trim(),
            age: Number(formData.get("age"))
        };

        try {
            const response = await fetch('/api/v1/students', {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (!response.ok) {
                alert(result.error || "Failed to create student");
                return;
            }

            document.getElementById("name").value = "";
            document.getElementById("email").value = "";
            document.getElementById("age").value = "";

            loadStudents();

        } catch (error) {
            console.error("Error creating student:", error);
        }
    });
}

async function deleteStudent(id) {
    try {
        const response = await fetch(`/api/v1/students/${id}`, {
            method: "DELETE"
        });

        if (!response.ok) {
            alert("Failed to delete student");
            return;
        }

        loadStudents();

    } catch (error) {
        console.error("Error deleting student:", error);
    }
}

// Load students when page opens
loadStudents();