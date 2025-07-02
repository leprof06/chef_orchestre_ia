// ----------- Explorer dynamique de fichiers -----------

/**
 * Charge la liste des fichiers/folders du projet et affiche l'explorer
 */
async function loadExplorer() {
  const project = document.getElementById('project').value;
  const resp = await fetch(`/project_files?project=${encodeURIComponent(project)}`);
  const data = await resp.json();

  const explorer = document.getElementById('explorer');
  explorer.innerHTML = '';
  if (data.success && data.tree) {
    renderExplorer(data.tree, explorer, '');
  } else {
    explorer.innerHTML = "<div style='color:#f44336'>Impossible de charger l’explorer.</div>";
  }
}

/**
 * Affiche l'arborescence de fichiers dans l'explorer
 */
function renderExplorer(tree, parentElem, path) {
  tree.forEach(item => {
    if (item.type === 'folder') {
      const folderElem = document.createElement('div');
      folderElem.className = 'explorer-folder';
      folderElem.innerHTML = `<i class="fa fa-folder${item.open ? '-open' : ''}"></i> ${item.name}`;
      folderElem.onclick = function () {
        item.open = !item.open;
        parentElem.innerHTML = '';
        renderExplorer(tree, parentElem, path);
      };
      parentElem.appendChild(folderElem);
      if (item.open && item.children) {
        const childrenDiv = document.createElement('div');
        childrenDiv.style.marginLeft = '1.1rem';
        renderExplorer(item.children, childrenDiv, path + '/' + item.name);
        parentElem.appendChild(childrenDiv);
      }
    } else if (item.type === 'file') {
      const fileElem = document.createElement('div');
      fileElem.className = 'explorer-file';
      fileElem.innerHTML = `<i class="fa fa-file-code"></i> ${item.name}`;
      fileElem.onclick = function () {
        selectFile(path + '/' + item.name);
        document.querySelectorAll('.explorer-file').forEach(el => el.classList.remove('active'));
        fileElem.classList.add('active');
      };
      parentElem.appendChild(fileElem);
    }
  });
}

/**
 * Charge le contenu d’un fichier sélectionné dans la zone de code
 */
async function selectFile(filepath) {
  const project = document.getElementById('project').value;
  const resp = await fetch(`/load_file?project=${encodeURIComponent(project)}&filename=${encodeURIComponent(filepath)}`);
  const data = await resp.json();
  if (data.success) {
    document.getElementById('code-area').value = data.code;
    document.getElementById('filename').value = filepath.replace(/^\//, '');
    document.getElementById('current-filename').textContent = filepath.replace(/^\//, '');
    notify("Fichier chargé : " + filepath.replace(/^\//, ''), true);
  } else {
    notify(data.message || "Erreur de chargement du fichier", false);
  }
}

// ----------- Sauvegarde réelle -----------

async function saveCode() {
  const code = document.getElementById('code-area').value;
  const project = document.getElementById('project').value;
  const filename = document.getElementById('filename').value;
  const resp = await fetch('/save_code', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ code, project, filename })
  });
  const data = await resp.json();
  notify(data.message || (data.success ? "Code enregistré !" : "Erreur lors de l'enregistrement."), data.success);
}

// ----------- Notifications UX -----------

function notify(msg, success) {
  let notif = document.getElementById('notif');
  notif.textContent = msg;
  notif.style.background = success ? '#4caf50' : '#f44336';
  notif.style.display = 'block';
  notif.style.color = '#fff';
  notif.style.padding = '1rem 1.6rem';
  notif.style.borderRadius = '1rem';
  notif.style.position = 'fixed';
  notif.style.top = '20px';
  notif.style.right = '20px';
  notif.style.zIndex = 9999;
  notif.style.fontWeight = '600';
  notif.style.boxShadow = '0 2px 16px rgba(0,0,0,0.10)';
  setTimeout(() => notif.style.display = 'none', 2500);
}

// ----------- Chat IA FULL branché -----------

async function sendChat(e) {
  e.preventDefault();
  const input = document.getElementById('chat-input');
  const message = input.value.trim();
  if (!message) return;

  // Affiche le message utilisateur dans la zone chat
  addChatMessage('user', message);

  // Reset input
  input.value = '';
  input.disabled = true;

  // Charge contexte code/fichier
  const code = document.getElementById('code-area').value;
  const filename = document.getElementById('filename').value;

  // Affiche un loader IA
  addChatMessage('ai', "<i class='fa fa-spinner fa-spin'></i> L’IA réfléchit…");

  // Envoie au backend
  const resp = await fetch('/chat_ia', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, code, filename })
  });
  const data = await resp.json();

  // Supprime loader précédent
  removeLastAIMsg();

  // Affiche la réponse IA
  addChatMessage('ai', data.answer || "Erreur IA.");

  input.disabled = false;
  input.focus();
}

// Affiche un message dans le chat (user ou ai)
function addChatMessage(role, text) {
  const div = document.createElement('div');
  div.className = 'chat-msg ' + role;
  div.innerHTML = `
    <i class="fa ${role === 'user' ? 'fa-user' : 'fa-robot'}"></i>
    <div>${text}</div>
  `;
  document.getElementById('chat-messages').appendChild(div);
  document.getElementById('chat-messages').scrollTop = 99999;
}

// Supprime le dernier message IA (pour loader)
function removeLastAIMsg() {
  const msgs = document.querySelectorAll('.chat-msg.ai');
  if (msgs.length) msgs[msgs.length - 1].remove();
}

// ----------- Init au chargement -----------

window.addEventListener('DOMContentLoaded', () => {
  loadExplorer();
});
