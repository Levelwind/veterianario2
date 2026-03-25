// ============================
// VetCare - JavaScript principal
// ============================

document.addEventListener('DOMContentLoaded', function () {
  if (window.bootstrap) {
    var tooltipTriggerList = [].slice.call(
      document.querySelectorAll('[data-bs-toggle="tooltip"]')
    );
    tooltipTriggerList.map(function (tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl);
    });
  }

  document.querySelectorAll('form:not(.setup-form)').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      if (this.checkValidity()) {
        const btn = this.querySelector(
          'button[type="submit"].btn-primary, button[type="submit"].btn-success, button[type="submit"].btn-warning'
        );
        if (btn) {
          if (btn.dataset.submitted === 'true') {
            e.preventDefault();
            return;
          }
          btn.dataset.submitted = 'true';
          btn.innerHTML =
            '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Procesando...';
          btn.style.opacity = '0.8';
          btn.style.pointerEvents = 'none';
        }
      }
    });
  });

  if (typeof TomSelect !== 'undefined') {
    document.querySelectorAll('select.js-enhanced-select').forEach(function (el) {
      if (
        el.tomselect ||
        el.closest('.django-otp-challenge') ||
        el.multiple ||
        el.type === 'hidden'
      ) {
        return;
      }

      if (!el.classList.contains('form-select')) {
        el.classList.add('form-select');
      }

      new TomSelect(el, {
        create: false,
        maxOptions: null,
        allowEmptyOption: true,
      });
    });
  }

  if (typeof flatpickr !== 'undefined') {
    document.querySelectorAll('input.js-date-picker').forEach(function (el) {
      if (el._flatpickr) {
        return;
      }

      flatpickr(el, {
        locale: 'es',
        dateFormat: 'Y-m-d',
        altInput: true,
        altFormat: 'j F, Y',
        disableMobile: true,
      });
    });
  }

  const sidebar = document.getElementById('sidebar');
  const mainContent = document.getElementById('mainContent');
  const sidebarToggle = document.getElementById('sidebarToggle');

  if (sidebarToggle) {
    sidebarToggle.addEventListener('click', function () {
      if (window.innerWidth <= 768) {
        sidebar.classList.toggle('open');
      } else {
        sidebar.classList.toggle('collapsed');
        mainContent.classList.toggle('expanded');
      }
    });
  }

  document.addEventListener('click', function (e) {
    if (window.innerWidth <= 768 && sidebar && sidebar.classList.contains('open')) {
      if (!sidebar.contains(e.target) && e.target !== sidebarToggle) {
        sidebar.classList.remove('open');
      }
    }
  });

  const reloj = document.getElementById('reloj');
  if (reloj) {
    function actualizarReloj() {
      const ahora = new Date();
      reloj.textContent = ahora.toLocaleTimeString('es-CO', {
        hour: '2-digit',
        minute: '2-digit',
      });
    }
    actualizarReloj();
    setInterval(actualizarReloj, 1000);
  }

  setTimeout(function () {
    document.querySelectorAll('.alert-dismissible').forEach(function (alert) {
      if (window.bootstrap) {
        const bsAlert = bootstrap.Alert.getInstance(alert);
        if (bsAlert) {
          bsAlert.close();
          return;
        }
      }
      alert.style.display = 'none';
    });
  }, 5000);

  const vetCards = document.querySelectorAll('.vet-card[data-vet-id]');
  const vetInput = document.getElementById('id_veterinario');

  vetCards.forEach(function (card) {
    card.addEventListener('click', function () {
      vetCards.forEach(function (currentCard) {
        currentCard.classList.remove('selected');
      });
      card.classList.add('selected');
      if (vetInput) {
        vetInput.value = card.dataset.vetId;
      }
      cargarInfoVet(card);
    });
  });

  function cargarInfoVet(card) {
    const infoBox = document.getElementById('vet-info-box');
    if (!infoBox) {
      return;
    }
    infoBox.innerHTML =
      '<div class="d-flex align-items-center gap-3 p-3 bg-primary-subtle rounded-3">' +
      '<i class="bi bi-person-badge-fill text-primary fs-3"></i>' +
      '<div>' +
      `<div class="fw-semibold">${card.dataset.nombre}</div>` +
      `<div class="text-muted small">${card.dataset.especialidad} · ${card.dataset.duracion} min por cita</div>` +
      `<div class="text-muted small">Horario: ${card.dataset.horarioInicio} - ${card.dataset.horarioFin}</div>` +
      '</div>' +
      '</div>';
    infoBox.classList.remove('d-none');
  }

  if (vetInput && vetInput.value) {
    const selectedCard = document.querySelector(
      `.vet-card[data-vet-id="${vetInput.value}"]`
    );
    if (selectedCard) {
      selectedCard.classList.add('selected');
      cargarInfoVet(selectedCard);
    }
  }
});

function confirmar(mensaje) {
  return confirm(mensaje || '¿Estás seguro de esta acción?');
}
