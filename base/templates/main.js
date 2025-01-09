document.addEventListener('DOMContentLoaded', () => {
    const taskInput = document.getElementById('taskInput');
    const addBtn = document.getElementById('addBtn');
    const taskList = document.getElementById('taskList');
    const filterSelect = document.getElementById('filter');
    const searchInput = document.getElementById('searchInput');
    const clearBtn = document.getElementById('clearBtn');

    let tasks = [];

    function createTaskElement(task) {
        const taskItem = document.createElement('div');
        taskItem.className = 'task-item';

        const checkbox = document.createElement('div');
        checkbox.className = `task-checkbox ${task.completed ? 'checked' : ''}`;
        checkbox.onclick = () => toggleTask(task.id);

        const taskText = document.createElement('div');
        taskText.className = `task-text ${task.completed ? 'completed' : ''}`;
        taskText.textContent = task.text;

        const actions = document.createElement('div');
        actions.className = 'task-actions';

        const editBtn = document.createElement('button');
        editBtn.className = 'edit-btn';
        editBtn.textContent = 'Edit';
        editBtn.onclick = () => editTask(task.id);

        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'delete-btn';
        deleteBtn.textContent = '🗑';
        deleteBtn.onclick = () => deleteTask(task.id);

        actions.appendChild(editBtn);
        actions.appendChild(deleteBtn);

        taskItem.appendChild(checkbox);
        taskItem.appendChild(taskText);
        taskItem.appendChild(actions);

        return taskItem;
    }

    function addTask() {
        const text = taskInput.value.trim();
        if (text) {
            const task = {
                id: Date.now(),
                text,
                completed: false
            };
            tasks.push(task);
            taskInput.value = '';
            renderTasks();
        }
    }

    function toggleTask(id) {
        const task = tasks.find(t => t.id === id);
        if (task) {
            task.completed = !task.completed;
            renderTasks();
        }
    }

    function editTask(id) {
        const task = tasks.find(t => t.id === id);
        if (task) {
            const newText = prompt('Edit task:', task.text);
            if (newText !== null) {
                task.text = newText.trim();
                renderTasks();
            }
        }
    }

    function deleteTask(id) {
        tasks = tasks.filter(t => t.id !== id);
        renderTasks();
    }

    function filterTasks() {
        const filterValue = filterSelect.value;
        const searchText = searchInput.value.toLowerCase();

        return tasks.filter(task => {
            const matchesFilter =
                filterValue === 'all' ||
                (filterValue === 'pending' && !task.completed) ||
                (filterValue === 'completed' && task.completed);

            const matchesSearch = task.text.toLowerCase().includes(searchText);

            return matchesFilter && matchesSearch;
        });
    }

    function renderTasks() {
        taskList.innerHTML = '';
        const filteredTasks = filterTasks();
        filteredTasks.forEach(task => {
            taskList.appendChild(createTaskElement(task));
        });
    }

    addBtn.onclick = addTask;
    taskInput.onkeypress = (e) => {
        if (e.key === 'Enter') addTask();
    };
    filterSelect.onchange = renderTasks;
    searchInput.oninput = renderTasks;
    clearBtn.onclick = () => {
        tasks = [];
        renderTasks();
    };

    renderTasks();
});




