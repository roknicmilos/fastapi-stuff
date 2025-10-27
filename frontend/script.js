const API_URL = 'http://localhost:8000';
const WS_URL = 'ws://localhost:8000/ws';

// Conversation participants (IDs) — as requested, show conversation for users 1 and 2
const USER_A = 1; // left
const USER_B = 2; // right

const messageList = document.getElementById('message-list');
let conversationId = null;
const seenMessageIds = new Set();

const formatTime = (dateString) => {
    try {
        const d = new Date(dateString);
        return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    } catch (e) {
        return '';
    }
};

const createMessageElement = (msg) => {
    const li = document.createElement('li');
    const side = Number(msg.user_id) === USER_B ? 'right' : 'left';
    li.className = `message ${side}`;

    const bubble = document.createElement('div');
    bubble.className = 'bubble';
    bubble.textContent = msg.text || '';

    const meta = document.createElement('div');
    meta.className = 'meta';
    meta.textContent = formatTime(msg.created_at || msg.createdAt || new Date());

    bubble.appendChild(meta);
    li.appendChild(bubble);
    return li;
};

const appendMessage = (msg) => {
    if (!msg || !msg.id) return;
    if (seenMessageIds.has(msg.id)) return;
    seenMessageIds.add(msg.id);
    const el = createMessageElement(msg);
    messageList.appendChild(el);
};

const scrollToBottom = () => {
    // small timeout to allow render
    requestAnimationFrame(() => {
        messageList.scrollTop = messageList.scrollHeight;
    });
};

const showEmptyState = (text) => {
    messageList.innerHTML = '';
    const li = document.createElement('li');
    li.style.textAlign = 'center';
    li.style.color = '#6b7280';
    li.textContent = text;
    messageList.appendChild(li);
};

const fetchConversation = async () => {
    try {
        const res = await fetch(
            `${API_URL}/conversations/by_users?user_a=${USER_A}&user_b=${USER_B}`
        );
        if (!res.ok) {
            showEmptyState('Conversation not found.');
            return;
        }
        const conv = await res.json();
        conversationId = conv.id;

        const messages = Array.isArray(conv.messages) ? conv.messages : [];
        // API returns newest->oldest; show oldest->newest
        const ordered = messages.slice().reverse();
        if (ordered.length === 0) {
            showEmptyState('No messages yet.');
            return;
        }

        messageList.innerHTML = '';
        ordered.forEach(appendMessage);
        scrollToBottom();
    } catch (err) {
        console.error('Failed to fetch conversation:', err);
        showEmptyState('Failed to load messages');
    }
};

// Setup WebSocket and handle incoming messages
const socket = new WebSocket(WS_URL);

socket.addEventListener('open', () => {
    console.log('WebSocket connected');
});

socket.addEventListener('message', (evt) => {
    try {
        const payload = JSON.parse(evt.data);
        // We expect message objects to have a conversation_id property.
        if (!payload || typeof payload !== 'object') return;
        if (!('conversation_id' in payload)) return; // ignore other broadcasts (e.g., todos)
        // If conversationId not yet loaded, try to fetch it (to sync state)
        if (conversationId === null) {
            // fetch conversation once to initialize
            fetchConversation();
            return;
        }
        if (Number(payload.conversation_id) === Number(conversationId)) {
            appendMessage(payload);
            scrollToBottom();
        }
    } catch (e) {
        console.error('Error handling websocket message', e);
    }
});

socket.addEventListener('error', (e) => {
    console.error('WebSocket error', e);
});

socket.addEventListener('close', () => {
    console.log('WebSocket closed');
});

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    fetchConversation();
});
