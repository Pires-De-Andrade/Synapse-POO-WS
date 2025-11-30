/**
 * Synapse - JavaScript Principal
 * Funções utilitárias e inicializações
 */

// Importar Bootstrap
const bootstrap = window.bootstrap

document.addEventListener("DOMContentLoaded", () => {
  // Inicializar tooltips Bootstrap
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  tooltipTriggerList.map((tooltipTriggerEl) => new bootstrap.Tooltip(tooltipTriggerEl))

  // Auto-hide alerts após 5 segundos
  setTimeout(() => {
    var alerts = document.querySelectorAll(".alert")
    alerts.forEach((alert) => {
      if (alert.classList.contains("alert-dismissible")) {
        var bsAlert = new bootstrap.Alert(alert)
        bsAlert.close()
      }
    })
  }, 5000)

  // Formatação automática de CPF
  document.querySelectorAll('input[id*="cpf"], input[name*="cpf"]').forEach((input) => {
    input.addEventListener("input", (e) => {
      let value = e.target.value.replace(/\D/g, "")
      value = value.replace(/(\d{3})(\d)/, "$1.$2")
      value = value.replace(/(\d{3})(\d)/, "$1.$2")
      value = value.replace(/(\d{3})(\d{1,2})$/, "$1-$2")
      e.target.value = value.substring(0, 14)
    })
  })

  // Formatação automática de telefone
  document.querySelectorAll('input[type="tel"], input[id*="phone"], input[name*="phone"]').forEach((input) => {
    input.addEventListener("input", (e) => {
      let value = e.target.value.replace(/\D/g, "")
      if (value.length <= 10) {
        value = value.replace(/(\d{2})(\d)/, "($1) $2")
        value = value.replace(/(\d{4})(\d)/, "$1-$2")
      } else {
        value = value.replace(/(\d{2})(\d)/, "($1) $2")
        value = value.replace(/(\d{5})(\d)/, "$1-$2")
      }
      e.target.value = value.substring(0, 15)
    })
  })

  // Smooth scroll para links internos
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      const target = document.querySelector(this.getAttribute("href"))
      if (target) {
        e.preventDefault()
        target.scrollIntoView({ behavior: "smooth", block: "start" })
      }
    })
  })
})

/**
 * Helper para requisições API
 */
async function apiRequest(url, options = {}) {
  const defaultOptions = {
    headers: {
      "Content-Type": "application/json",
    },
  }

  const config = { ...defaultOptions, ...options }

  try {
    const response = await fetch(url, config)
    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.error || data.message || "Erro na requisição")
    }

    return data
  } catch (error) {
    console.error("API Error:", error)
    showToast(error.message, "danger")
    throw error
  }
}

/**
 * Mostrar toast de notificação
 */
function showToast(message, type = "info") {
  const toast = document.createElement("div")
  toast.className = `alert alert-${type} alert-dismissible fade show position-fixed`
  toast.style.cssText = "top: 20px; right: 20px; z-index: 9999; min-width: 300px; max-width: 400px;"
  toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `
  document.body.appendChild(toast)

  setTimeout(() => {
    if (toast.parentNode) {
      toast.classList.remove("show")
      setTimeout(() => toast.remove(), 150)
    }
  }, 5000)
}

/**
 * Validar CPF
 */
function validateCPF(cpf) {
  cpf = cpf.replace(/[^\d]/g, "")

  if (cpf.length !== 11) return false
  if (/^(\d)\1{10}$/.test(cpf)) return false

  let sum = 0
  for (let i = 0; i < 9; i++) {
    sum += Number.parseInt(cpf.charAt(i)) * (10 - i)
  }
  let remainder = (sum * 10) % 11
  if (remainder === 10 || remainder === 11) remainder = 0
  if (remainder !== Number.parseInt(cpf.charAt(9))) return false

  sum = 0
  for (let i = 0; i < 10; i++) {
    sum += Number.parseInt(cpf.charAt(i)) * (11 - i)
  }
  remainder = (sum * 10) % 11
  if (remainder === 10 || remainder === 11) remainder = 0
  if (remainder !== Number.parseInt(cpf.charAt(10))) return false

  return true
}

/**
 * Formatar data para exibição (DD/MM/YYYY)
 */
function formatDate(dateStr) {
  if (!dateStr) return "-"
  const [year, month, day] = dateStr.split("-")
  return `${day}/${month}/${year}`
}

/**
 * Formatar hora para exibição (HH:MM)
 */
function formatTime(timeStr) {
  if (!timeStr) return "-"
  return timeStr.substring(0, 5)
}

// Exportar funções para uso global
window.Synapse = {
  apiRequest,
  showToast,
  validateCPF,
  formatDate,
  formatTime,
}
