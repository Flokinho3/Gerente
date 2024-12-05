        let abaAtiva = "Home";  // Valor inicial (pode ser configurado de acordo com a página atual)

        // Função que envia a informação da aba ativa para o servidor
        function enviarAbaAtiva() {
            fetch('/atualizar_aba', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ aba: abaAtiva })
            })
            .then(response => response.json())
            .then(data => console.log("Informação enviada:", data))
            .catch(error => console.error("Erro ao enviar a informação:", error));
        }

        // Monitorar quando a aba ou página está visível
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                abaAtiva = "Outros";  // Quando a aba não está visível
            } else {
                abaAtiva = "Home";  // Ou qualquer outra página em que o usuário esteja
            }
            enviarAbaAtiva();  // Enviar para o servidor sempre que mudar a aba
        });

        // Enviar a informação a cada 5 segundos
        setInterval(enviarAbaAtiva, 5000);