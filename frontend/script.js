const API_URL = "http://localhost:5000/api/tasks";

const form = document.getElementById("task-form");
const tasksList = document.getElementById("tasks-list");

async function loadTasks() {
  const res = await fetch(API_URL);
  const tasks = await res.json();
  tasksList.innerHTML = "";
  tasks.forEach((task) => {
    const div = document.createElement("div");
    div.className = "task-item" + (task.status === "done" ? " done" : "");
    div.innerHTML = `
      <span>${task.title} - ${task.description || ""}</span>
      <span class="task-actions">
        <button onclick="toggleTask(${task.id}, '${task.status}')">✔</button>
        <button onclick="deleteTask(${task.id})">🗑</button>
      </span>
    `;
    tasksList.appendChild(div);
  });
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const title = document.getElementById("title").value;
  const description = document.getElementById("description").value;

  await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, description }),
  });

  form.reset();
  loadTasks();
});

async function toggleTask(id, currentStatus) {
  const newStatus = currentStatus === "done" ? "todo" : "done";
  await fetch(`${API_URL}/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status: newStatus }),
  });
  loadTasks();
}

async function deleteTask(id) {
  await fetch(`${API_URL}/${id}`, { method: "DELETE" });
  loadTasks();
}

loadTasks();
