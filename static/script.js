const API_URL = "http://127.0.0.1:8000/users";

document.addEventListener("DOMContentLoaded", () => {
  carregarPlanos();
  carregarUsuarios();
});
document.getElementById("user-form").addEventListener("submit", salvarUsuario);

async function carregarUsuarios() {
  try {
    const res = await fetch(API_URL);
    if (!res.ok) throw new Error("Erro ao buscar usuários");
    
    const usuarios = await res.json();
    const tbody = document.getElementById("tabela-usuarios");
    tbody.innerHTML = "";

    usuarios.forEach(user => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${user.id}</td>
        <td>${user.address}</td>
        <td>${user.email}</td>
        <td>${user.cpf}</td>
        <td>${user.type || user.plan_type || user.plan_id}</td>
        <td>
          <button class="btn btn-edit" onclick="prepararEdicao(${user.id}, '${user.address}', '${user.email}', '${user.cpf}', ${user.plan_id})">Editar</button>
          <button class="btn btn-delete" onclick="deletarUsuario(${user.id})">Excluir</button>
        </td>
      `;
      tbody.appendChild(tr);
    });
  } catch (err) {
    exibirMensagem(err.message, true);
  }
}

async function salvarUsuario(e) {
  e.preventDefault();
  
  const id = document.getElementById("user-id").value;
  const address = document.getElementById("address").value;
  const email = document.getElementById("email").value;
  const cpf = document.getElementById("cpf").value;
  const plan_id = parseInt(document.getElementById("plan_id").value);

  const payload = {};
  if (address) payload.address = address;
  if (email) payload.email = email;
  if (cpf) payload.cpf = cpf;
  if (plan_id) payload.plan_id = plan_id;

  const url = id ? `${API_URL}/${id}` : API_URL;
  const method = id ? "PATCH" : "POST";

  try {
    const res = await fetch(url, {
      method: method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      const errorData = await res.json();
      throw new Error(errorData.detail || "Erro ao salvar usuário");
    }

    exibirMensagem(id ? "Usuário atualizado com sucesso!" : "Usuário cadastrado com sucesso!");
    limparFormulario();
    carregarUsuarios();
  } catch (err) {
    exibirMensagem(err.message, true);
  }
}

function prepararEdicao(id, address, email, cpf, plan_id) {
  document.getElementById("user-id").value = id;
  document.getElementById("address").value = address;
  document.getElementById("email").value = email;
  document.getElementById("cpf").value = cpf;
  document.getElementById("plan_id").value = plan_id;

  document.getElementById("form-titulo").innerText = `Editar Aluno #${id}`;
  document.getElementById("btn-salvar").innerText = "Atualizar";
  document.getElementById("btn-cancelar").classList.remove("oculta");
}

async function carregarPlanos() {
  try {
    const res = await fetch("http://127.0.0.1:8000/users/plans");
    if (!res.ok) throw new Error("Erro ao buscar planos");

    const planos = await res.json();
    const select = document.getElementById("plan_id");
    select.innerHTML = '<option value="">Selecione um plano</option>';

    planos.forEach(plano => {
      const option = document.createElement("option");
      option.value = plano.id;
      option.textContent = `${plano.type} (ID: ${plano.id})`;
      select.appendChild(option);
    });
  } catch (err) {
    exibirMensagem("Não foi possível carregar os planos.", true);
  }
}

async function deletarUsuario(id) {
  if (!confirm(`Tem certeza que deseja excluir o aluno #${id}?`)) return;

  try {
    const res = await fetch(`${API_URL}/${id}`, { method: "DELETE" });
    if (!res.ok) throw new Error("Erro ao deletar usuário");

    exibirMensagem("Aluno removido com sucesso!");
    carregarUsuarios();
  } catch (err) {
    exibirMensagem(err.message, true);
  }
}

function limparFormulario() {
  document.getElementById("user-id").value = "";
  document.getElementById("user-form").reset();
  document.getElementById("form-titulo").innerText = "Cadastrar Novo Aluno";
  document.getElementById("btn-salvar").innerText = "Salvar Aluno";
  document.getElementById("btn-cancelar").classList.add("oculta");
}

function exibirMensagem(texto, ehErro = false) {
  const msgDiv = document.getElementById("mensagem");
  msgDiv.innerText = texto;
  msgDiv.className = `mensagem ${ehErro ? 'erro' : 'sucesso'}`;
  setTimeout(() => msgDiv.classList.add("oculta"), 4000);
}