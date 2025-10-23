const todoList = document.getElementById('todo-list');

const API_URL = 'http://localhost:8000';
const WS_URL = 'ws://localhost:8000/ws';

const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-GB');
};

const addTodoToList = (todo) => {
    const li = document.createElement('li');
    li.innerHTML = `
        <span>
            <strong>${todo.title}</strong> - <em>${formatDate(todo.due_date)}</em>
            ${todo.description ? `<br><small>${todo.description}</small>` : ''}
        </span>
    `;
    todoList.prepend(li);
};

const fetchTodos = async () => {
    try {
        const response = await fetch(`${API_URL}/todos`);
        const todos = await response.json();
        todos.forEach(addTodoToList);
    } catch (error) {
        console.error('Error fetching todos:', error);
    }
};

const socket = new WebSocket(WS_URL);

socket.onmessage = (event) => {
    const todo = JSON.parse(event.data);
    addTodoToList(todo);
};

socket.onopen = () => {
    console.log('WebSocket connection established');
};

socket.onerror = (error) => {
    console.error('WebSocket error:', error);
};

document.addEventListener('DOMContentLoaded', fetchTodos);
