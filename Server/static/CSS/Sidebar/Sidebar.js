// Obtém a referência da sidebar
const sidebar = document.getElementById('sidebar');

// Função para mostrar a sidebar
function showSidebar() {
    sidebar.classList.add('visible');
    sidebar.classList.remove('hidden');
}

// Função para esconder a sidebar
function hideSidebar() {
    sidebar.classList.add('hidden');
    sidebar.classList.remove('visible');
}

// Adiciona um listener de movimento do mouse
document.addEventListener('mousemove', function(event) {
    // Verifica se a posição X do mouse está dentro dos 20px da borda esquerda da tela
    if (event.clientX <= 20) {
        showSidebar();
    } 
    if (event.clientX >= 220) {
        hideSidebar();
    }
});

// Esconde a sidebar após 2 segundos sem interação do mouse
let hideTimeout;
document.addEventListener('mousemove', () => {
    clearTimeout(hideTimeout);
    hideTimeout = setTimeout(hideSidebar, 2000); // Esconde após 2 segundos
});
