function submitForm() {
    var formData = {
      Email: $('#Email').val(),
      Senha: $('#Senha').val()
    };

    $.ajax({
      type: 'POST',
      url: 'http://localhost:8000/api/login',
      data: JSON.stringify(formData),
      contentType: 'application/json',
      success: function(response) {
        console.log(response);
        // Aqui você pode lidar com a resposta do servidor, por exemplo, redirecionar para outra página
      },
      error: function(error) {
        console.error('Erro:', error);
        // Aqui você pode lidar com o erro, por exemplo, exibir uma mensagem de erro ao usuário
      }
    });
  }